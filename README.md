# 🖥️ IsardVDI Manager

[![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-lightgrey?logo=flask)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Unofficial web interface to manage and organize IsardVDI virtual machines, aimed at non-technical users.

> **⚠️ Disclaimer:** This is a **personal, unofficial project**. It is **not affiliated with, endorsed by, or supported by the IsardVDI project** ([isardvdi.com](https://isardvdi.com/) / [GitLab](https://gitlab.com/isard/isardvdi)) nor by UPV/EHU. It simply consumes the public IsardVDI API with your own API key. Use it at your own risk.

## 📋 Project Description

A small web application written in **Python** with the **Flask** framework. Its purpose is to give non-technical users a simple view of their IsardVDI desktops (start/stop, open console viewers) with folder-based organization. Maintained by [tears-mysthrala](https://github.com/tears-mysthrala).

### Supported operations

Everything the app does goes through the IsardVDI API (`/api/v3`) using the API key you enter at login:

- **Login / logout** with your personal IsardVDI API key. The key is validated against the API on login and kept in the Flask session — it is never written to disk by the application.
- **List your desktops** with name, status and IP addresses (in-memory cache, no database).
- **Start and stop desktops** (one click per machine).
- **Open console viewers**: browser viewers (noVNC / SPICE web client / browser RDP) and downloadable connection files (`.vv` for virt-viewer, `.rdp` for RDP gateway/VPN), depending on what the API offers for each desktop.
- **Folder organization**: create, rename and delete folders, and assign/unassign desktops to them. Folders are stored in a local `folders.json` file (git-ignored).
- **JSON endpoints**: `/api/vms` (desktop/folder state for AJAX refresh) and `/api/viewers/<vm_id>` (which viewer types are available for a desktop).

Anything not listed above (creating desktops, managing templates, users, quotas, etc.) is **not** supported — use the official IsardVDI web UI for that.

### Error handling

- **Invalid or expired API key** (API returns 401): the session key is discarded and you are redirected to the login page with an explanatory message.
- **API unreachable or unexpected errors**: the dashboard shows an error banner instead of machine data; JSON endpoints return an error payload.
- **Viewer not available for a desktop**: the app detects it and hides or disables that viewer option.
- Folder file errors are logged to the console and the app starts with an empty folder set.

### Technologies Used

- **Language**: Python 3.9
- **Web Framework**: Flask 3.1.2
- **Libraries**: `requests` 2.32.5 (HTTP calls to the API)
- **Containerization**: Docker and Docker Compose for deployment
- **Storage**: in-memory VM cache + `folders.json` for folder assignments

### Project Structure

```text
├── app.py                 # Main Flask application (routes + inline templates)
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker image build configuration
├── docker-compose.yml     # Container execution configuration
├── .env.example           # Example environment configuration (copy to .env)
└── folders.json           # Runtime-generated folder data (git-ignored)
```

## ⚙️ Configuration

Configuration is read from environment variables. Copy `.env.example` to `.env` and adjust:

| Variable | Default | Purpose |
|----------|---------|---------|
| `ISARD_API_BASE_URL` | `https://cloud.uni.eus/api/v3` | IsardVDI API base URL |
| `SECRET_KEY` | random per start | Flask session signing key; set a fixed random value for stable sessions |
| `PORT` | `5000` | Listening port |
| `FLASK_DEBUG` | `false` | Flask debug mode — **never enable outside local development** |

Docker Compose loads `.env` automatically (`env_file`). For local runs, export the variables yourself or load them with your shell (the app does not read `.env` files directly).

Your **IsardVDI API key is not part of this configuration**: you enter it in the login form and it lives only in your session. Get it from your user profile on your IsardVDI instance.

## 🚀 Quick Start with Docker

### Option 1: Docker Compose (recommended)

```bash
cp .env.example .env   # then edit .env
docker-compose up -d --build
```

### Option 2: Plain Docker

```bash
docker build -t isard-webapp .
docker run -d -p 5000:5000 --env-file .env --name isard-app isard-webapp
```

The application will be available at `http://localhost:5000`

> Note: a historical prebuilt image (`sasukeuni/isard-app`) exists on Docker Hub, but it is not published or verified from this repository — prefer building from source as shown above.

## 📦 Local Installation

### Prerequisites
- Python 3.9+
- pip

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/tears-mysthrala/isard-webapp.git
cd isard-webapp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) configure environment:
```bash
cp .env.example .env
# export the variables, e.g.: set -a; . ./.env; set +a
```

4. Run the application:
```bash
python app.py
```

## 🛠️ Development Process

This application was built iteratively against the live IsardVDI API, in the absence of complete official API documentation:

1. **Initial API exploration**: probing endpoints of `https://cloud.uni.eus/api/v3` with `curl` and small Python scripts to map available functionality.
2. **Version research**: trial and error across `/v1`, `/v2` and `/v3` until finding the active version, handling 404/401 responses along the way.
3. **Reading the source**: the public IsardVDI GitLab repository was the main reference for response structures (`interfaces`, `guest_properties`, `ips`, viewer payloads).
4. **Iteration**: authentication format (`Bearer {API_KEY}`), IP parsing from network interfaces, and error handling for unexpected API responses were all refined through repeated testing.
5. **Refinement**: in-memory caching, folder organization and the web UI were added on top of the working API calls.

This hands-on approach produced a functional application, but it also means behavior may break if the upstream API changes — there is no official contract to rely on.

## 🔒 Security notes

- The IsardVDI API key is stored **only in the Flask session**. There is no "remember me" persistence: earlier versions stored a base64-encoded key in `config.json`; that was removed because base64 is encoding, not protection.
- Note that Flask's default session is a **signed but not encrypted** client-side cookie: the API key is recoverable from the cookie value, so protect the cookie (and any logs or proxies that might capture it) like the key itself. Server-side session storage is on the roadmap.
- Viewer responses may contain short-lived connection tokens; the app does not log them.
- Do not expose this app directly to the internet: it has no user accounts of its own beyond the API-key session, and anyone who reaches it can drive the API with whatever key they enter.
- If you previously cloned this repository, note that its history once contained a real API token. History has not been rewritten; treat that token as compromised (rotate/revoke it on the IsardVDI side if you haven't). Never commit `.env`, `config.json` or `folders.json`.

## 🤝 Contributing

Contributions are welcome! If you find any bugs or have suggestions, please open an issue.

## 👤 Author

**[tears-mysthrala](https://github.com/tears-mysthrala)** — Founder / OT Cybersecurity Consultant

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## 🔗 Links

- [IsardVDI](https://isardvdi.com/)
- [IsardVDI GitLab](https://gitlab.com/isard/isardvdi)

---

⭐ If you find this project useful, consider giving it a star on GitHub!
