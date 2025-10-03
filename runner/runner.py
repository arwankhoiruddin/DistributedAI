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
    def __init__(self, server_url, poll_interval=5):
        self.server_url = server_url.rstrip('/')
        self.poll_interval = poll_interval
        self.runner_id = None
        
    def register(self):
        """Register with the API server"""
        try:
            response = requests.post(
                f"{self.server_url}/register",
                json={"name": "Python Runner"}
            )
            response.raise_for_status()
            data = response.json()
            self.runner_id = data['runner_id']
            print(f"✓ Registered successfully with runner_id: {self.runner_id}")
            return True
        except Exception as e:
            print(f"✗ Failed to register: {e}")
            return False
    
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
        """Submit task result to API server"""
        try:
            response = requests.post(
                f"{self.server_url}/result",
                json={
                    "task_id": task_id,
                    "runner_id": self.runner_id,
                    "result_data": result_data,
                    "status": "completed"
                }
            )
            response.raise_for_status()
            print(f"  ✓ Result submitted successfully")
            return True
        except Exception as e:
            print(f"  ✗ Failed to submit result: {e}")
            return False
    
    def poll_tasks(self):
        """Poll for available tasks"""
        try:
            response = requests.get(
                f"{self.server_url}/tasks",
                params={"runner_id": self.runner_id}
            )
            response.raise_for_status()
            data = response.json()
            
            # Check if there's a task available
            if 'task_id' in data:
                return data
            return None
        except Exception as e:
            print(f"✗ Error polling tasks: {e}")
            return None
    
    def run(self):
        """Main runner loop"""
        print(f"Starting runner...")
        print(f"API Server: {self.server_url}")
        print(f"Poll interval: {self.poll_interval}s\n")
        
        # Register with API server
        if not self.register():
            print("Failed to register. Exiting.")
            return
        
        print(f"\nStarting task polling loop...")
        print(f"Press Ctrl+C to stop\n")
        
        try:
            while True:
                # Poll for tasks
                task = self.poll_tasks()
                
                if task:
                    task_id = task['task_id']
                    print(f"\n✓ Received task: {task_id}")
                    
                    # Execute the task
                    result = self.execute_task(task)
                    
                    # Submit the result
                    self.submit_result(task_id, result)
                else:
                    # No task available
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
    
    args = parser.parse_args()
    
    runner = Runner(args.server, args.interval)
    runner.run()


if __name__ == '__main__':
    main()
