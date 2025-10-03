# API Examples

This document shows example API calls and responses.

## 1. Runner Registration

Register a new runner with the API server.

**Request:**
```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Python Runner"}'
```

**Response:**
```json
{
  "runner_id": "779c0e28-15b8-473b-a06e-1fa816d4156e",
  "message": "Runner registered successfully"
}
```

## 2. Create Task

Create a new task (typically called from WordPress plugin).

**Request:**
```bash
curl -X POST http://localhost:8000/task \
  -H "Content-Type: application/json" \
  -d '{
    "operation_code": 100,
    "params": {"dataset": "sales", "year": 2024},
    "api_key": "optional-key"
  }'
```

**Response:**
```json
{
  "task_id": "42e6ec9c-96ec-4a76-93e8-c36c717ce066",
  "message": "Task created successfully"
}
```

## 3. Poll for Tasks

Runner polls for available tasks.

**Request:**
```bash
curl "http://localhost:8000/tasks?runner_id=779c0e28-15b8-473b-a06e-1fa816d4156e"
```

**Response (when task available):**
```json
{
  "task_id": "42e6ec9c-96ec-4a76-93e8-c36c717ce066",
  "operation_code": 100,
  "params": {
    "dataset": "sales",
    "year": 2024
  }
}
```

**Response (when no tasks):**
```json
{
  "message": "No tasks available"
}
```

## 4. Submit Result

Runner submits task result.

**Request:**
```bash
curl -X POST http://localhost:8000/result \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "42e6ec9c-96ec-4a76-93e8-c36c717ce066",
    "runner_id": "779c0e28-15b8-473b-a06e-1fa816d4156e",
    "result_data": "raw data",
    "status": "completed"
  }'
```

**Response:**
```json
{
  "message": "Result submitted successfully"
}
```

## 5. Get Task Result

Retrieve result for a specific task (typically called from WordPress).

**Request:**
```bash
curl "http://localhost:8000/result/42e6ec9c-96ec-4a76-93e8-c36c717ce066"
```

**Response:**
```json
{
  "task_id": "42e6ec9c-96ec-4a76-93e8-c36c717ce066",
  "runner_id": "779c0e28-15b8-473b-a06e-1fa816d4156e",
  "result_data": "raw data",
  "status": "completed",
  "submitted_at": "2025-10-03T02:35:36.870567"
}
```

**Response (when task not completed):**
```json
{
  "task_id": "42e6ec9c-96ec-4a76-93e8-c36c717ce066",
  "status": "assigned",
  "message": "Task result not available yet"
}
```

## 6. Get All Tasks

List all tasks in the system (for WordPress dashboard).

**Request:**
```bash
curl "http://localhost:8000/tasks/all"
```

**Response:**
```json
{
  "tasks": [
    {
      "task_id": "42e6ec9c-96ec-4a76-93e8-c36c717ce066",
      "operation_code": 100,
      "status": "completed",
      "created_at": "2025-10-03T02:35:35.146363",
      "assigned_to": "779c0e28-15b8-473b-a06e-1fa816d4156e",
      "completed_at": "2025-10-03T02:35:36.870559"
    },
    {
      "task_id": "052f6aa6-0875-41b5-afdb-e21db96e313e",
      "operation_code": 200,
      "status": "pending",
      "created_at": "2025-10-03T02:35:56.283171",
      "assigned_to": null,
      "completed_at": null
    }
  ]
}
```

## 7. API Root

Get API information.

**Request:**
```bash
curl "http://localhost:8000/"
```

**Response:**
```json
{
  "message": "Distributed Data Analysis API",
  "version": "1.0.0",
  "endpoints": [
    "/register",
    "/task",
    "/tasks",
    "/result",
    "/result/{task_id}"
  ]
}
```

## Task Lifecycle Example

Complete flow from task creation to result retrieval:

```bash
# 1. Runner registers
RUNNER_ID=$(curl -s -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Runner 1"}' | jq -r '.runner_id')

echo "Runner registered: $RUNNER_ID"

# 2. Create task (from WordPress)
TASK_ID=$(curl -s -X POST http://localhost:8000/task \
  -H "Content-Type: application/json" \
  -d '{"operation_code": 100, "params": {}}' | jq -r '.task_id')

echo "Task created: $TASK_ID"

# 3. Runner polls for task
TASK=$(curl -s "http://localhost:8000/tasks?runner_id=$RUNNER_ID")
echo "Task received: $TASK"

# 4. Runner submits result
curl -s -X POST http://localhost:8000/result \
  -H "Content-Type: application/json" \
  -d "{
    \"task_id\": \"$TASK_ID\",
    \"runner_id\": \"$RUNNER_ID\",
    \"result_data\": \"raw data\",
    \"status\": \"completed\"
  }"

# 5. Get result (from WordPress)
curl -s "http://localhost:8000/result/$TASK_ID" | jq
```

## Error Responses

### Runner Not Found
```json
{
  "detail": "Runner not found"
}
```
Status: 404

### Task Not Found
```json
{
  "detail": "Task not found"
}
```
Status: 404

## WordPress Plugin Integration

The WordPress plugin uses `wp_remote_post()` and `wp_remote_get()`:

```php
// Create task
$response = wp_remote_post($api_url . '/task', array(
    'headers' => array('Content-Type' => 'application/json'),
    'body' => json_encode(array(
        'operation_code' => 100,
        'params' => array('key' => 'value')
    ))
));

// Get all tasks
$response = wp_remote_get($api_url . '/tasks/all');

// Get result
$response = wp_remote_get($api_url . '/result/' . $task_id);
```

## Testing with Python

```python
import requests

# Register runner
response = requests.post('http://localhost:8000/register', 
                        json={'name': 'Test Runner'})
runner_id = response.json()['runner_id']

# Create task
response = requests.post('http://localhost:8000/task',
                        json={'operation_code': 100, 'params': {}})
task_id = response.json()['task_id']

# Get task
response = requests.get('http://localhost:8000/tasks',
                       params={'runner_id': runner_id})
task = response.json()

# Submit result
requests.post('http://localhost:8000/result',
             json={
                 'task_id': task_id,
                 'runner_id': runner_id,
                 'result_data': 'raw data',
                 'status': 'completed'
             })

# Get result
response = requests.get(f'http://localhost:8000/result/{task_id}')
result = response.json()
print(result['result_data'])  # "raw data"
```
