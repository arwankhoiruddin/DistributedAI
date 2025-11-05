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
- `--retry-interval`: Retry interval for registration in seconds (default: 10)
- `--max-retries`: Maximum number of registration retry attempts (default: unlimited)

### Examples

```bash
# Run with default settings (unlimited retries)
python runner.py --server http://localhost:8000

# Run with custom retry interval
python runner.py --server http://localhost:8000 --retry-interval 15

# Run with maximum retry limit
python runner.py --server http://localhost:8000 --max-retries 5
```

## How it Works

1. **Registers with the API server** to get a runner_id
   - If registration fails, automatically retries with exponential backoff
   - Will keep retrying indefinitely unless `--max-retries` is specified
   - This ensures the runner stays in standby mode even when the API server is temporarily unavailable

2. **Polls the API server** for available tasks
   - Continuously polls at the specified interval
   - If consecutive errors occur (5 in a row), automatically attempts to re-register

3. **Executes tasks** based on operation code:
   - Code 100: Returns "raw data"
   - Code 200: Returns "filtered data"

4. **Submits results** back to the API server

5. **Repeats the polling loop** indefinitely until stopped with Ctrl+C

## Fault Tolerance

The runner is designed to stay in standby mode and handle temporary network issues:

- **Registration failures**: Retries with exponential backoff (starting at 10s, up to 60s max)
- **Polling errors**: Tracks consecutive errors and re-registers after 5 failures
- **Connection issues**: Continues operating and automatically recovers when the API server becomes available
