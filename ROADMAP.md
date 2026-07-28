# Roadmap — IsardVDI Manager (unofficial)

> Personal, unofficial companion UI for the IsardVDI API. Not affiliated with the IsardVDI project. See the disclaimer in `README.md`.

## Purpose and users

- **Purpose:** give non-technical users a simple, safe way to see their IsardVDI desktops, start/stop them and open console viewers, with light folder organization.
- **Users:** students and staff of institutions running IsardVDI who find the official UI too dense for day-to-day desktop use.

## Current state (observed)

- Single-file Flask app (`app.py`, routes + inline templates), Python 3.9, Docker support.
- Session-based API-key login; key validated against the API on login; no on-disk credential storage.
- Configuration via environment variables (`.env.example` provided).
- Known limitations: Flask default session cookie is signed but not encrypted; no automated tests; no roles; destructive actions (stop VM) have no confirmation step; Spanish-only UI strings; API surface discovered by trial and error, so upstream API changes may break it.

## Now

- [x] Remove committed credential material from current state; ignore runtime files (`.env`, `config.json`, `folders.json`).
- [x] Environment-based configuration with documented `.env.example`.
- [x] Remove base64 "remember me" API-key persistence (`config.json`).
- [x] README: unofficial-project disclaimer, real supported operations, error states, security notes.

## Next

- Simple roles (user / teacher / limited admin) — only if a real multi-user deployment appears; otherwise skip.
- Confirmation dialogs for destructive actions (stop desktop, delete folder).
- Server-side session storage (or shorter session lifetime) so the API key is not recoverable from the client cookie.
- Basic accessibility pass (labels, contrast, keyboard navigation).
- Basic i18n (current UI strings are Spanish; extract messages).
- Tests against a mocked IsardVDI API (login flow, desktop listing, start/stop, folder CRUD).

## Later (optional)

- Classroom/teacher view (multiple users' desktops, read-only).
- Desktop templates shortcuts.
- Kiosk mode for shared lab screens.

## Out of scope

- Reimplementing IsardVDI administration (desktop creation, templates, quotas, user management) — that belongs to the official UI.
- Replacing the official IsardVDI web interface.
- Permanent credential storage without a proper security design (encryption at rest, threat model, user consent).
- Rewriting git history to purge the old committed token (human decision; token rotation is the actual mitigation).

## Archive / abandonment condition

This project tracks a third-party API with no stable contract. If the upstream API changes incompatibly and no active user depends on this app, or if the official IsardVDI UI covers the non-technical use case, the repository should be archived with a final README note rather than left silently unmaintained.
