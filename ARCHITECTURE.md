# Architecture and Workflow

## System Architecture

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│   WordPress     │         │   API Server    │         │     Runner      │
│     Plugin      │         │   (FastAPI)     │         │   (Python App)  │
│                 │         │                 │         │                 │
│  - Settings UI  │◄───────►│  - Task Queue   │◄───────►│  - Polling      │
│  - Task Creator │  HTTP   │  - In-Memory DB │  HTTP   │  - Execution    │
│  - Result View  │         │  - REST API     │         │  - Result Send  │
└─────────────────┘         └─────────────────┘         └─────────────────┘
```

## Workflow Diagram

### 1. Runner Registration

```
Runner                          API Server
  |                                |
  |------- POST /register -------->|
  |       {name: "Runner"}         |
  |                                |
  |<------ Response --------------|
  |     {runner_id: "uuid"}        |
  |                                |
```

### 2. Task Creation (from WordPress)

```
WordPress Plugin               API Server
  |                                |
  |------- POST /task ------------>|
  |  {operation_code: 100,         |
  |   params: {...}}               |
  |                                |
  |<------ Response --------------|
  |     {task_id: "uuid"}          |
  |                                |
```

### 3. Task Processing

```
Runner                          API Server
  |                                |
  |--- GET /tasks?runner_id=xxx -->|
  |                                |
  |<------ Task Data --------------|
  |  {task_id, operation_code}     |
  |                                |
  | [Execute Task Locally]         |
  | - Code 100 → "raw data"        |
  | - Code 200 → "filtered data"   |
  |                                |
  |--- POST /result -------------->|
  |  {task_id, result_data}        |
  |                                |
  |<------ Confirmation -----------|
  |     {message: "success"}       |
  |                                |
```

### 4. Result Retrieval (from WordPress)

```
WordPress Plugin               API Server
  |                                |
  |--- GET /result/{task_id} ----->|
  |                                |
  |<------ Result Data ------------|
  |  {task_id, result_data,        |
  |   status, runner_id}           |
  |                                |
  | [Display in UI]                |
  |                                |
```

## Component Details

### API Server Endpoints

| Method | Endpoint | Purpose | Request Body | Response |
|--------|----------|---------|--------------|----------|
| GET | `/` | API info | - | API metadata |
| POST | `/register` | Register runner | `{name}` | `{runner_id, message}` |
| POST | `/task` | Create task | `{operation_code, params, api_key}` | `{task_id, message}` |
| GET | `/tasks` | Get task for runner | Query: `runner_id` | Task data or empty |
| POST | `/result` | Submit result | `{task_id, runner_id, result_data, status}` | `{message}` |
| GET | `/result/{task_id}` | Get task result | - | Result data |
| GET | `/tasks/all` | List all tasks | - | Array of tasks |

### Data Flow

1. **WordPress Plugin** → Creates tasks via API
2. **API Server** → Stores tasks in memory queue
3. **Runner** → Polls for tasks every N seconds
4. **Runner** → Executes task based on operation code
5. **Runner** → Submits result back to API
6. **API Server** → Stores result in memory
7. **WordPress Plugin** → Retrieves and displays result

### Storage (In-Memory)

The MVP uses Python dictionaries for storage:

```python
runners = {}      # {runner_id: runner_info}
tasks = {}        # {task_id: task_info}
results = {}      # {task_id: result_info}
task_queue = []   # List of pending task_ids
```

**Note**: All data is lost when the API server restarts.

## Operation Codes

Current implementation:

```python
def execute_task(task):
    code = task['operation_code']
    
    if code == 100:
        return "raw data"
    elif code == 200:
        return "filtered data"
    else:
        return f"unknown operation code: {code}"
```

Future operation codes (300, 400) can be implemented by adding more conditions.

## WordPress Plugin Structure

```
wordpress-plugin/
├── distributed-data-analysis.php  # Main plugin file
├── css/
│   └── admin.css                 # Admin styling
├── js/
│   └── admin.js                  # Admin JavaScript
└── README.md                     # Plugin documentation
```

### Key Features

- **Settings Page**: Configure API server URL and API key
- **Tasks Page**: Create new tasks and view task list
- **Auto-refresh**: Tasks table updates every 10 seconds
- **Result Modal**: View task results in popup dialog
- **WordPress Integration**: Uses WordPress Settings API

## Security Considerations (For Future)

Current MVP has minimal security:
- No authentication between components
- API key field exists but not validated
- No HTTPS requirement
- No input validation/sanitization

For production, implement:
- JWT tokens for runner authentication
- API key validation
- HTTPS/TLS encryption
- Input validation and sanitization
- Rate limiting
- CORS configuration
