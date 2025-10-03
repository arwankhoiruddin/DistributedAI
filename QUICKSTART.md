# Quick Start Guide

This guide will help you get the Distributed Data Analysis Platform up and running.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- WordPress installation (for the plugin)

## Step 1: Start the API Server

```bash
cd api-server
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API server will be available at `http://localhost:8000`

## Step 2: Start the Runner

Open a new terminal and run:

```bash
cd runner
pip install -r requirements.txt
python runner.py --server http://localhost:8000 --interval 5
```

The runner will:
1. Register with the API server
2. Start polling for tasks every 5 seconds
3. Execute tasks and return results

## Step 3: Install WordPress Plugin

1. Copy the `wordpress-plugin` folder to your WordPress installation:
   ```bash
   cp -r wordpress-plugin /path/to/wordpress/wp-content/plugins/distributed-data-analysis
   ```

2. Log in to WordPress Admin
3. Go to **Plugins** menu
4. Find "Distributed Data Analysis" and click **Activate**

## Step 4: Configure the Plugin

1. Go to **Data Analysis > Settings** in WordPress Admin
2. Configure:
   - **API Server URL**: `http://localhost:8000`
   - **API Key**: (leave empty for now)
3. Click **Save Settings**

## Step 5: Create and Run Tasks

1. Go to **Data Analysis > Tasks**
2. Fill in the form:
   - **Operation Code**: Select an operation (e.g., "100 - Fetch Raw Data")
   - **Parameters**: Enter `{}` or custom JSON parameters
3. Click **Create Task**

The task will:
1. Be sent to the API server
2. Be picked up by the runner
3. Be executed (returns dummy data based on operation code)
4. Have its result stored in the API server

## Step 6: View Results

1. The tasks table will show all tasks with their status
2. When a task is completed, click **View Result** to see the output
3. The table auto-refreshes every 10 seconds

## Testing Without WordPress

You can test the system without WordPress using curl:

```bash
# Create a task
curl -X POST http://localhost:8000/task \
  -H "Content-Type: application/json" \
  -d '{"operation_code": 100, "params": {}}'

# Get all tasks
curl http://localhost:8000/tasks/all

# Get result for a specific task
curl http://localhost:8000/result/{task_id}
```

Or use the provided test script:

```bash
chmod +x test-e2e.sh
./test-e2e.sh
```

## Operation Codes

The current MVP supports these operation codes:

| Code | Description | Dummy Result |
|------|-------------|--------------|
| 100 | Fetch Raw Data | "raw data" |
| 200 | Filter Data | "filtered data" |
| 300 | ML Model Analysis | "unknown operation code: 300" |
| 400 | Export Report | "unknown operation code: 400" |

## Troubleshooting

### API Server won't start
- Check if port 8000 is already in use
- Run with different port: `uvicorn main:app --port 8001`

### Runner can't connect to API
- Verify API server is running
- Check the server URL is correct
- Use `--server http://localhost:8000` explicitly

### WordPress plugin can't connect
- Verify API server URL in plugin settings
- Check WordPress can access the API server URL
- Look for errors in WordPress debug log

### Tasks not being processed
- Check runner is running and polling
- Verify runner registered successfully
- Check API server logs for errors

## Next Steps

This is the MVP version with in-memory storage. For production use, you should:

1. Add database persistence to the API server
2. Implement proper authentication and API key validation
3. Add more sophisticated task execution logic in the runner
4. Implement real data analysis capabilities
5. Add task queuing and priority management
6. Implement multi-runner support with load balancing
