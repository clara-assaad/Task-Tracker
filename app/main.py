from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app import storage
from app.api.routes.health import router as health_router
from app.business_rules import validate_status_transition
from app.core.config import settings
from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate

app = FastAPI(
    title="Task Tracker API",
    description="Module 1 Task Tracker - REST API skeleton",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5173",
        "null",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    """Creates a new task.

    Args:
        payload (TaskCreate): The data required to create a new task.

    Returns:
        TaskResponse: The created task object.

    Examples:
        >>> # Request to create a new task
        >>> client.post("/tasks", json={"title": "New Task", "status": "ToDo"})
        201 Created
    """
    return storage.add_task(payload)


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    """Retrieves a task by its ID.

    Args:
        task_id (str): The unique identifier of the task.

    Returns:
        TaskResponse: The requested task object.

    Raises:
        HTTPException: If no task with the given ID exists (404).

    Examples:
        >>> # Request to get a specific task
        >>> client.get("/tasks/1")
        200 OK
    """
    task = storage.get_task_by_id(task_id)
    if task is not None:
        return task
    raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    overdue: bool | None = None,
) -> list[TaskResponse]:
    """Lists all tasks with optional filtering, sorted by creation time.

    Args:
        status (TaskStatus | None): Filter tasks by status.
        priority (TaskPriority | None): Filter tasks by priority.
        overdue (bool | None): Filter tasks by overdue status.

    Returns:
        list[TaskResponse]: A sorted list of task response objects.

    Examples:
        >>> # Request to list tasks
        >>> client.get("/tasks?status=InProgress")
        200 OK
    """
    return storage.get_all_tasks(status=status, priority=priority, overdue=overdue)


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    """Updates an existing task.

    Args:
        task_id (str): The unique identifier of the task.
        payload (TaskUpdate): The partial data to update the task.

    Returns:
        TaskResponse: The updated task object.

    Raises:
        HTTPException: If the task is not found (404) or the status transition is invalid (422).

    Examples:
        >>> # Request to update a task status
        >>> client.patch("/tasks/1", json={"status": "InProgress"})
        200 OK
    """
    if payload.status is not None:
        existing_task = storage.get_task_by_id(task_id)
        if existing_task is None:
            raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
        validate_status_transition(existing_task.status, payload.status)

    updated_task = storage.update_task(task_id, payload)
    if updated_task is not None:
        return updated_task
    raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: str) -> None:
    """Deletes a task by its ID.

    Args:
        task_id (str): The unique identifier of the task.

    Returns:
        None: Returns None / no response body on successful deletion.

    Raises:
        HTTPException: If the task to delete is not found (404).

    Examples:
        >>> # Request to delete a task
        >>> client.delete("/tasks/1")
        204 No Content
    """
    if storage.delete_task(task_id):
        return None
    raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")


@app.get("/")
def read_root() -> dict:
    """Returns API information.

    Returns:
        dict: A dictionary containing 'message' (str) and 'environment' (str).

    Examples:
        >>> # Request to root
        >>> client.get("/")
        200 OK
    """
    return {
        "message": "Task Tracker API is running",
        "environment": settings.APP_ENV,
    }
