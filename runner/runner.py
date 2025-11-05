#!/usr/bin/env python3
"""
Runner application for Distributed Data Analysis Platform
Polls API server for tasks and executes them
"""

import requests
import time
import argparse
import sys
import json


class Runner:
    # Class constants for default behavior
    DEFAULT_REQUEST_TIMEOUT = 10  # seconds
    DEFAULT_MAX_RETRY_DELAY = 60  # seconds
    DEFAULT_MAX_SUBMIT_RETRIES = 3
    DEFAULT_SUBMIT_RETRY_DELAY = 2
    DEFAULT_MAX_CONSECUTIVE_ERRORS = 5
    
    def __init__(self, server_url, poll_interval=5, retry_interval=10, max_retries=None,
                 max_submit_retries=None, max_consecutive_errors=None):
        self.server_url = server_url.rstrip('/')
        self.poll_interval = poll_interval
        self.retry_interval = retry_interval
        self.max_retries = max_retries
        self.max_submit_retries = max_submit_retries or self.DEFAULT_MAX_SUBMIT_RETRIES
        self.max_consecutive_errors = max_consecutive_errors or self.DEFAULT_MAX_CONSECUTIVE_ERRORS
        self.runner_id = None
        
    def register(self):
        """Register with the API server with retry logic"""
        retry_count = 0
        retry_delay = self.retry_interval
        
        while True:
            try:
                response = requests.post(
                    f"{self.server_url}/register",
                    json={"name": "Python Runner"},
                    timeout=self.DEFAULT_REQUEST_TIMEOUT
                )
                response.raise_for_status()
                data = response.json()
                self.runner_id = data['runner_id']
                print(f"✓ Registered successfully with runner_id: {self.runner_id}")
                return True
            except Exception as e:
                retry_count += 1
                if self.max_retries and retry_count >= self.max_retries:
                    print(f"✗ Failed to register after {retry_count} attempts: {e}")
                    return False
                
                print(f"✗ Failed to register (attempt {retry_count}): {e}")
                print(f"  Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                
                # Exponential backoff with max delay
                retry_delay = min(retry_delay * 1.5, self.DEFAULT_MAX_RETRY_DELAY)
    
    def execute_task(self, task):
        """Execute a task based on operation code"""
        operation_code = task['operation_code']
        params = task.get('params', {})
        
        print(f"  Executing task with operation code: {operation_code}")
        
        # Dummy task execution based on operation code
        if operation_code == 100:
            result = "raw data"
            print(f"  → Returning: {result}")
        elif operation_code == 200:
            result = "filtered data"
            print(f"  → Returning: {result}")
        else:
            result = f"unknown operation code: {operation_code}"
            print(f"  → Returning: {result}")
        
        return result
    
    def submit_result(self, task_id, result_data):
        """Submit task result to API server with retry logic"""
        retry_delay = self.DEFAULT_SUBMIT_RETRY_DELAY
        
        for attempt in range(self.max_submit_retries):
            try:
                response = requests.post(
                    f"{self.server_url}/result",
                    json={
                        "task_id": task_id,
                        "runner_id": self.runner_id,
                        "result_data": result_data,
                        "status": "completed"
                    },
                    timeout=self.DEFAULT_REQUEST_TIMEOUT
                )
                response.raise_for_status()
                print(f"  ✓ Result submitted successfully")
                return True
            except Exception as e:
                if attempt < self.max_submit_retries - 1:
                    print(f"  ✗ Failed to submit result (attempt {attempt + 1}/{self.max_submit_retries}): {e}")
                    print(f"    Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    print(f"  ✗ Failed to submit result after {self.max_submit_retries} attempts: {e}")
                    print(f"    WARNING: Result for task {task_id} may be lost!")
                    return False
    
    def poll_tasks(self):
        """Poll for available tasks
        Returns:
            - dict with task data if task available
            - False if no task available (but connection successful)
            - None if there was an error
        """
        try:
            response = requests.get(
                f"{self.server_url}/tasks",
                params={"runner_id": self.runner_id},
                timeout=self.DEFAULT_REQUEST_TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
            
            # Check if there's a task available
            if 'task_id' in data:
                return data
            return False  # No task available, but connection successful
        except Exception as e:
            print(f"\n✗ Error polling tasks: {e}")
            return None  # Error occurred
    
    def run(self):
        """Main runner loop"""
        print(f"Starting runner...")
        print(f"API Server: {self.server_url}")
        print(f"Poll interval: {self.poll_interval}s")
        print(f"Retry interval: {self.retry_interval}s\n")
        
        # Register with API server (with retry logic)
        print("Registering with API server...")
        if not self.register():
            print("Failed to register after all retries. Exiting.")
            return
        
        print(f"\nStarting task polling loop...")
        print(f"Press Ctrl+C to stop\n")
        
        try:
            consecutive_errors = 0
            
            while True:
                # Poll for tasks
                task = self.poll_tasks()
                
                if task:  # Task available
                    consecutive_errors = 0  # Reset error counter on success
                    task_id = task['task_id']
                    print(f"\n✓ Received task: {task_id}")
                    
                    # Execute the task
                    result = self.execute_task(task)
                    
                    # Submit the result
                    self.submit_result(task_id, result)
                elif task is None:  # Error occurred
                    consecutive_errors += 1
                    print(f"  (Error count: {consecutive_errors}/{self.max_consecutive_errors})")
                    if consecutive_errors >= self.max_consecutive_errors:
                        print(f"\n✗ Too many consecutive errors. Attempting to re-register...")
                        if not self.register():
                            print("Failed to re-register. Exiting.")
                            return
                        consecutive_errors = 0
                else:  # task is False - no task available but connection successful
                    consecutive_errors = 0  # Reset on successful poll
                    print(".", end="", flush=True)
                
                # Wait before next poll
                time.sleep(self.poll_interval)
                
        except KeyboardInterrupt:
            print("\n\nStopping runner...")
            print("Goodbye!")


def main():
    parser = argparse.ArgumentParser(
        description='Runner for Distributed Data Analysis Platform'
    )
    parser.add_argument(
        '--server',
        type=str,
        default='http://localhost:8000',
        help='API server URL (default: http://localhost:8000)'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=5,
        help='Polling interval in seconds (default: 5)'
    )
    parser.add_argument(
        '--retry-interval',
        type=int,
        default=10,
        help='Retry interval for registration in seconds (default: 10)'
    )
    parser.add_argument(
        '--max-retries',
        type=int,
        default=None,
        help='Maximum number of registration retry attempts (default: unlimited)'
    )
    parser.add_argument(
        '--max-submit-retries',
        type=int,
        default=None,
        help='Maximum number of result submission retry attempts (default: 3)'
    )
    parser.add_argument(
        '--max-consecutive-errors',
        type=int,
        default=None,
        help='Maximum consecutive polling errors before re-registration (default: 5)'
    )
    
    args = parser.parse_args()
    
    runner = Runner(
        args.server,
        args.interval,
        args.retry_interval,
        args.max_retries,
        args.max_submit_retries,
        args.max_consecutive_errors
    )
    runner.run()


if __name__ == '__main__':
    main()
