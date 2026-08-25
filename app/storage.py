from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Optional

from app.models import TaskCreate, TaskResponse, TaskStatus, TaskUpdate

_tasks: dict[str, TaskResponse] = {}


def add_task(payload: TaskCreate) -> TaskResponse:
    """Adds a new task to the in-memory storage.

    Args:
        payload (TaskCreate): The task creation data.

    Returns:
        TaskResponse: The created task response object.
    """
    task_id = str(len(_tasks) + 1)
    now = datetime.now(timezone.utc)
    task = TaskResponse(
        id=task_id,
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        due_date=payload.due_date,
        tags=payload.tags,
        created_at=now,
        updated_at=now,
    )
    _tasks[task_id] = task
    return task


def _is_overdue(task: TaskResponse) -> bool:
    if task.due_date is None:
        return False
    return task.due_date < date.today() and task.status != TaskStatus.DONE


def get_all_tasks(status=None, priority=None, overdue=None) -> list[TaskResponse]:
    """Retrieves all tasks with optional filtering, sorted by creation time.

    Args:
        status (TaskStatus | None): Filter tasks by status.
        priority (TaskPriority | None): Filter tasks by priority.
        overdue (bool | None): Filter tasks by overdue status.

    Returns:
        list[TaskResponse]: A sorted list of task response objects.
    """
    tasks = list(_tasks.values())
    if status is not None:
        tasks = [task for task in tasks if task.status == status]
    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]
    if overdue is not None:
        tasks = [task for task in tasks if _is_overdue(task) is overdue]
    return sorted(tasks, key=lambda task: task.created_at)


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    """Retrieves a task by its ID.

    Args:
        task_id (str): The unique identifier of the task.

    Returns:
        Optional[TaskResponse]: The task if found, otherwise None.
    """
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    """Updates an existing task in memory.

    Args:
        task_id (str): The unique identifier of the task.
        payload (TaskUpdate): The data to update.

    Returns:
        Optional[TaskResponse]: The updated task object if found, otherwise None.
    """
    existing_task = _tasks.get(task_id)
    if existing_task is None:
        return None

    update_data = payload.model_dump(exclude_unset=True)
    if not update_data:
        return existing_task

    updated_task = existing_task.model_copy(deep=True)
    for field, value in update_data.items():
        setattr(updated_task, field, value)

    updated_task.updated_at = datetime.now(timezone.utc)
    _tasks[task_id] = updated_task
    return updated_task


def delete_task(task_id: str) -> bool:
    """Deletes a task from in-memory storage.

    Args:
        task_id (str): The unique identifier of the task.

    Returns:
        bool: True if the task was found and deleted, otherwise False.
    """
    return _tasks.pop(task_id, None) is not None


def _reset() -> None:
    _tasks.clear()
