from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
import uuid
from datetime import datetime

app = FastAPI(title="Distributed Data Analysis API")

# In-memory storage
runners: Dict[str, dict] = {}
tasks: Dict[str, dict] = {}
results: Dict[str, dict] = {}
task_queue: List[str] = []  # Queue of task IDs waiting to be processed


class RunnerRegister(BaseModel):
    name: Optional[str] = "Runner"


class RunnerResponse(BaseModel):
    runner_id: str
    message: str


class Task(BaseModel):
    operation_code: int
    params: Optional[Dict] = {}
    api_key: Optional[str] = None


class TaskResponse(BaseModel):
    task_id: str
    message: str


class Result(BaseModel):
    task_id: str
    runner_id: str
    result_data: str
    status: str = "completed"


class ResultResponse(BaseModel):
    message: str


@app.get("/")
def read_root():
    return {
        "message": "Distributed Data Analysis API",
        "version": "1.0.0",
        "endpoints": ["/register", "/task", "/tasks", "/result", "/result/{task_id}"]
    }


@app.post("/register", response_model=RunnerResponse)
def register_runner(runner: RunnerRegister):
    """Register a new runner and get runner_id"""
    runner_id = str(uuid.uuid4())
    runners[runner_id] = {
        "id": runner_id,
        "name": runner.name,
        "registered_at": datetime.now().isoformat(),
        "status": "active"
    }
    return RunnerResponse(
        runner_id=runner_id,
        message="Runner registered successfully"
    )


@app.post("/task", response_model=TaskResponse)
def create_task(task: Task):
    """Create a new task from WordPress plugin"""
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "id": task_id,
        "operation_code": task.operation_code,
        "params": task.params,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "assigned_to": None
    }
    task_queue.append(task_id)
    return TaskResponse(
        task_id=task_id,
        message="Task created successfully"
    )


@app.get("/tasks")
def get_tasks(runner_id: str):
    """Get available tasks for a runner"""
    # Verify runner exists
    if runner_id not in runners:
        raise HTTPException(status_code=404, detail="Runner not found")
    
    # Get next available task from queue
    if task_queue:
        task_id = task_queue.pop(0)
        task = tasks[task_id]
        task["status"] = "assigned"
        task["assigned_to"] = runner_id
        return {
            "task_id": task_id,
            "operation_code": task["operation_code"],
            "params": task["params"]
        }
    
    return {"message": "No tasks available"}


@app.post("/result", response_model=ResultResponse)
def submit_result(result: Result):
    """Submit task result from runner"""
    # Verify task exists
    if result.task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update task status
    tasks[result.task_id]["status"] = result.status
    tasks[result.task_id]["completed_at"] = datetime.now().isoformat()
    
    # Store result
    results[result.task_id] = {
        "task_id": result.task_id,
        "runner_id": result.runner_id,
        "result_data": result.result_data,
        "status": result.status,
        "submitted_at": datetime.now().isoformat()
    }
    
    return ResultResponse(message="Result submitted successfully")


@app.get("/result/{task_id}")
def get_result(task_id: str):
    """Get result for a specific task"""
    if task_id not in results:
        # Check if task exists but no result yet
        if task_id in tasks:
            task = tasks[task_id]
            return {
                "task_id": task_id,
                "status": task["status"],
                "message": "Task result not available yet"
            }
        raise HTTPException(status_code=404, detail="Task not found")
    
    return results[task_id]


@app.get("/tasks/all")
def get_all_tasks():
    """Get all tasks (for WordPress dashboard)"""
    return {
        "tasks": [
            {
                "task_id": task_id,
                "operation_code": task["operation_code"],
                "status": task["status"],
                "created_at": task["created_at"],
                "assigned_to": task.get("assigned_to"),
                "completed_at": task.get("completed_at")
            }
            for task_id, task in tasks.items()
        ]
    }
