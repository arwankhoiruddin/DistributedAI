# API Server

FastAPI-based API server for coordinating tasks between WordPress plugin and runners.

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will be available at `http://localhost:8000`

## API Endpoints

- `GET /` - API information
- `POST /register` - Register a new runner
- `POST /task` - Create a new task (from WordPress plugin)
- `GET /tasks?runner_id={id}` - Get available tasks for a runner
- `POST /result` - Submit task result
- `GET /result/{task_id}` - Get result for a specific task
- `GET /tasks/all` - Get all tasks (for WordPress dashboard)

## Storage

This MVP version uses in-memory storage. All data will be lost when the server restarts.
