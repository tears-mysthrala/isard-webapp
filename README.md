# 🖥️ IsardVDI Manager

[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-sasukeuni%2Fisard--app-blue?logo=docker)](https://hub.docker.com/r/sasukeuni/isard-app)
[![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-lightgrey?logo=flask)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Web application to manage and organize IsardVDI virtual machines with folder organization and Docker support.

## 📋 Project Description

This project is a web application developed in **Python** using the **Flask** framework. Its main purpose is to manage and organize IsardVDI virtual machines (VMs), a cloud-based virtualization system. Created by cybersecurity student Unai Urzainqui, known on GitHub as [tears-mysthrala](https://github.com/tears-mysthrala).

### Key Features

- **VM Management**: The application connects to the IsardVDI API (`https://cloud.uni.eus/api/v3`) to retrieve the user's desktop list.
- **Folder Organization**: Allows grouping VMs into custom folders, stored in a JSON file (`folders.json`).
- **Web Interface**: Provides a web interface to visualize, organize, and manage virtual machines.
- **VM Caching**: Maintains an in-memory cache of machines to optimize queries.

### Technologies Used

- **Language**: Python 3.9
- **Web Framework**: Flask 2.3.3
- **Libraries**:
  - `requests` 2.31.0: For making HTTP requests to the API
  - `urllib.parse`: For URL decoding
  - `json`: For handling JSON files
  - `os`: For accessing environment variables
- **Containerization**: Docker and Docker Compose for deployment
- **Storage**: JSON file (`folders.json`) to persist folders and machine assignments

### Project Structure

```bash
/home/kalista/isard/
├── app.py                 # Main Flask application file
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker image build configuration
├── docker-compose.yml     # Container execution configuration
├── folders.json          # JSON file with folders and assigned machines
└── __pycache__/          # Compiled Python files (auto-generated)
```

## 🚀 Quick Start with Docker

### Option 1: Docker Hub (Recommended)

```bash
docker pull sasukeuni/isard-app:latest
docker run -d -p 5000:5000 --name isard-app sasukeuni/isard-app:latest
```

### Option 2: Docker Compose

Create a `docker-compose.yml` file:

```yaml
services:
  isard-app:
    image: sasukeuni/isard-app:latest
    ports:
      - "5000:5000"
    restart: unless-stopped
```

Then run:

```bash
docker-compose up -d
```

The application will be available at `http://localhost:5000`

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

3. Run the application:
```bash
python app.py
```

### Configuration

- **Port**: The application exposes port 5000
- **API Key**: The application will prompt you for your IsardVDI API key on first access
- **Data**: The `config.json` and `folders.json` files are automatically created to store your configuration

## 🛠️ Development Process

The development of this application was an iterative trial-and-error process, marked by the lack of official documentation and the need to directly explore the capabilities of the IsardVDI API. Here's how we reached the current state:

1. **Initial API Exploration**: We started by making basic queries to the API (`https://cloud.uni.eus/api/v3`) to understand what endpoints were available. Using tools like `curl` or simple Python scripts with `requests`, we tested different routes and HTTP methods to map the exposed functionalities.

2. **Version Research**: There was no clear documentation about which API version was being used. Through trial and error, we discovered that v3 was the active version, testing different paths like `/v1`, `/v2`, and `/v3` until finding valid responses. This involved handling 404 and 401 errors to identify correct credentials and functional endpoints.

3. **Deciphering Non-existent Documentation**: Official documentation was practically non-existent or very limited. To understand the structure of JSON responses and required parameters, we had to directly analyze the API responses. This included inspecting fields like `interfaces`, `guest_properties`, and `ips` to extract relevant information about virtual machines.

4. **GitLab Research**: When facing persistent failures (like authentication errors or incomplete data), we turned to the public IsardVDI repository on GitLab. We explored the source code to understand how the API worked internally, what fields were returned, and how requests were structured. This allowed us to adjust our queries to obtain complete data and handle edge cases.

5. **Trial and Error Iterations**: Each new functionality was implemented by testing different combinations of headers, parameters, and methods. For example:
   - We tested different authentication formats until finding that `Bearer {API_KEY}` worked.
   - We experimented with different ways to parse IPs from network interfaces.
   - We adjusted error handling for cases where the API returned unexpected data.

6. **Optimization and Refinement**: Once basic queries worked, we added logic to cache data, organize into folders, and build the web interface. Each step involved more testing to ensure stability.

This hands-on development approach resulted in a functional application, but highlights the importance of better documentation in open-source projects to facilitate integration development.

## 🤝 Contributing

Contributions are welcome! If you find any bugs or have suggestions, please open an issue.

## 👤 Author

**Unai Urzainqui** ([@tears-mysthrala](https://github.com/tears-mysthrala))
- Cybersecurity Student
- University of the Basque Country / Euskal Herriko Unibertsitatea

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## 🔗 Links

- [Docker Hub](https://hub.docker.com/r/sasukeuni/isard-app)
- [IsardVDI](https://isardvdi.com/)
- [IsardVDI GitLab](https://gitlab.com/isard/isardvdi)

---

⭐ If you find this project useful, consider giving it a star on GitHub!
