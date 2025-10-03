# GitHub Copilot Instructions - Distributed Data Analysis Platform

## Project Overview

This is a **Distributed Data Analysis Platform** consisting of three main components:

1. **WordPress Plugin** – Dashboard UI for task management
2. **API Server** – Coordinator for communication between plugin and runners
3. **Runner (Python App)** – Python application that performs data analysis on local machines

## Repository Structure

```
/wordpress-plugin/   → WordPress Plugin (dashboard UI)
/api-server/         → API Server (FastAPI/Flask)
/runner/             → Python runner for analysis execution
```

## Architecture

### WordPress Plugin
- Users log in to WordPress dashboard
- Create analysis tasks from admin menu
- Tasks are sent to API server
- Technology: PHP (WordPress Settings API, Admin Menu, REST API Client)

### API Server
- Stores tasks from WordPress
- Manages task distribution to runners
- Provides endpoints for analysis results
- Authentication via API key
- Technology: Python (FastAPI/Flask), Database: PostgreSQL/MySQL

### Runner
- Registers with API server using ID/token
- Polls for available tasks
- Executes tasks (fetch data, filter, analyze)
- Sends results back to API server
- Technology: Python (Requests, Pandas/NumPy/scikit-learn)

## Workflow

1. **Runner Registration**
   - Runner sends `POST /register` to API server to get ID/token
   - Runner sends heartbeat (`/ping`) periodically

2. **User Creates Task**
   - User logs in to WordPress dashboard → **Data Analysis** menu
   - Plugin sends task to API server (`POST /task`)

3. **Runner Handles Task**
   - Runner polls `GET /tasks?runner_id=xxx`
   - Executes task according to `operation_code`
   - Sends result back to API server (`POST /result`)

4. **Plugin Displays Results**
   - Plugin reads results with `GET /result/{task_id}`
   - Dashboard displays results to user

## Operation Codes

When working with task operations, use these codes:

| Code | Description              |
|------|-------------------------|
| 100  | Fetch raw data          |
| 200  | Filter data             |
| 300  | ML model analysis       |
| 400  | Export report           |

## Running the Components

### API Server
```bash
cd api-server
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Runner
```bash
cd runner
pip install -r requirements.txt
python runner.py --server http://localhost:8000 --token <runner_token>
```

### WordPress Plugin
- Copy `wordpress-plugin` folder to `wp-content/plugins/`
- Activate plugin through **WordPress Admin > Plugins**
- Configure API server URL & API key in **Settings > Data Analysis**

## Development Guidelines

- Use FastAPI/Flask for API server endpoints
- Follow WordPress coding standards for plugin development
- Use Python type hints in runner and API server code
- Implement proper error handling for network communications
- Use environment variables for configuration (API keys, server URLs)
- Follow RESTful API design principles for endpoints

## Current Roadmap

- [ ] Basic API server (register, task, result)
- [ ] Runner polling & simple task execution
- [ ] Plugin admin page to send tasks
- [ ] Task status table in dashboard
- [ ] Result visualization (tables/charts)
- [ ] Task completion notifications
- [ ] Role-based access control in WordPress

## License

MIT License
