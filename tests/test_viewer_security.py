import os
import unittest
from unittest.mock import patch

import app as manager


class ViewerSecurityTests(unittest.TestCase):
    def setUp(self):
        origins = patch.dict(os.environ, {"ISARD_VIEWER_ORIGINS": ""})
        origins.start()
        self.addCleanup(origins.stop)
        manager.app.config.update(TESTING=True, SECRET_KEY="test-only-secret")
        self.client = manager.app.test_client()
        with self.client.session_transaction() as session:
            session["api_key"] = "synthetic-api-key"
        self.origin = "https://cloud.uni.eus"

    def viewer_response(self, value, suffix=""):
        with patch.object(manager, "get_viewer_url", return_value=value):
            return self.client.get("/viewer/test-vm/browser-vnc" + suffix)

    def test_rejects_active_external_and_ambiguous_destinations(self):
        values = [
            "javascript:alert(1)", "data:text/html,<script>alert(1)</script>",
            "//evil.example/viewer", "https://evil.example/viewer",
            "https://cloud.uni.eus.evil.example/", "https://cloud.uni.eus@evil.example/",
            "https://user@cloud.uni.eus/", "https://cloud.uni.eus:444/viewer",
            "https://cloud.uni.eus:0/viewer",
            "https://cloud.uni.eus\\@evil.example/", "https://cloud.uni.eus\n@evil.example/",
            " https://cloud.uni.eus/viewer", "https://cloud.uni.eus:invalid/",
            "https://[invalid/", "https://cloud.uni.eus/\x00", "ftp://cloud.uni.eus/",
        ]
        for value in values:
            for payload in (value, {"type": "url", "url": value}):
                for suffix in ("", "?json=1"):
                    with self.subTest(value=value, payload=payload, suffix=suffix):
                        response = self.viewer_response(payload, suffix)
                        self.assertEqual(response.status_code, 502)
                        self.assertNotIn("Location", response.headers)

    def test_preserves_same_origin_urls_and_relative_viewer_paths(self):
        for value in (self.origin + "/viewer?token=synthetic#desktop", self.origin + ":443/viewer", "/viewer?token=synthetic"):
            for payload in (value, {"type": "url", "url": value}):
                with self.subTest(value=value, payload=payload):
                    response = self.viewer_response(payload)
                    self.assertEqual(response.status_code, 302)
                    self.assertEqual(response.headers["Location"], self.origin + value if value.startswith("/") else value)
                    self.assertNotIn(b"<script>", response.data)

    def test_url_is_never_interpolated_into_a_script_or_custom_html(self):
        value = self.origin + '/viewer?token="</script><script>window.pwned=1</script>'
        response = self.viewer_response({"type": "url", "url": value})
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(b"<script>", response.data)
        self.assertNotIn(b"window.location", response.data)

    def test_honors_custom_api_origin_and_explicit_viewer_origin(self):
        with patch.object(manager, "API_BASE_URL", "http://localhost:8080/api/v3"):
            self.assertEqual(manager.validated_viewer_url("/viewer"), "http://localhost:8080/viewer")
            self.assertIsNone(manager.validated_viewer_url(self.origin + "/viewer"))
            with patch.dict(os.environ, {"ISARD_VIEWER_ORIGINS": "https://broken.example:invalid,https://viewer.example:8443"}):
                value = "https://viewer.example:8443/viewer"
                self.assertEqual(manager.validated_viewer_url(value), value)
                self.assertIsNone(manager.validated_viewer_url("https://viewer.example/viewer"))

    def test_preserves_json_and_downloads(self):
        value = self.origin + "/viewer"
        response = self.viewer_response({"type": "url", "url": value}, "?json=1")
        self.assertEqual(response.json["data"]["url"], value)
        for kind, mime, name in (("rdp_file", "application/x-rdp", "desktop.rdp"),
                                 ("spice_file", "application/x-virt-viewer", "desktop.vv")):
            response = self.viewer_response({"type": kind, "content": "synthetic file", "filename": name, "mime": mime})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b"synthetic file")
            self.assertIn(name, response.headers["Content-Disposition"])
        response = self.viewer_response("data:application/x-rdp,synthetic%20file")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"synthetic file")

    def test_invalid_data_uri_is_not_redirected(self):
        response = self.viewer_response("data:application/x-rdp")
        self.assertEqual(response.status_code, 502)
        self.assertNotIn("Location", response.headers)

    def test_debug_error_does_not_disclose_exception_details(self):
        with patch.object(manager.requests, "get", side_effect=RuntimeError("synthetic-private-token")):
            response = self.client.get("/debug/viewer/test-vm")
        self.assertEqual(response.status_code, 502)
        self.assertNotIn(b"synthetic-private-token", response.data)
        self.assertNotIn("url_called", response.json)

    def test_browser_redirect_does_not_fetch_a_second_cookie_response(self):
        with patch.object(manager, "get_viewer_url", return_value={"type": "url", "url": self.origin + "/viewer"}):
            with patch.object(manager.requests, "get") as upstream:
                response = self.client.get("/viewer/test-vm/browser-vnc")
        self.assertEqual(response.status_code, 302)
        upstream.assert_not_called()


if __name__ == "__main__":
    unittest.main()
