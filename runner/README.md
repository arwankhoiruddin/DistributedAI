# Runner

Python application that executes data analysis tasks.

## Installation

```bash
pip install -r requirements.txt
```

## Running the Runner

```bash
python runner.py --server http://localhost:8000 --interval 5
```

### Arguments

- `--server`: API server URL (default: http://localhost:8000)
- `--interval`: Polling interval in seconds (default: 5)

## How it Works

1. Registers with the API server to get a runner_id
2. Polls the API server for available tasks
3. Executes tasks based on operation code:
   - Code 100: Returns "raw data"
   - Code 200: Returns "filtered data"
4. Submits results back to the API server
5. Repeats the polling loop
