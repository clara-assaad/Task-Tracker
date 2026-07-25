from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from app.models import TaskCreate, TaskResponse, TaskUpdate

_tasks: dict[str, TaskResponse] = {}


def add_task(payload: TaskCreate) -> TaskResponse:
    task_id = str(len(_tasks) + 1)
    now = datetime.now(timezone.utc)
    task = TaskResponse(
        id=task_id,
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        created_at=now,
        updated_at=now,
    )
    _tasks[task_id] = task
    return task


def get_all_tasks(status=None, priority=None) -> list[TaskResponse]:
    tasks = list(_tasks.values())
    if status is not None:
        tasks = [task for task in tasks if task.status == status]
    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]
    return sorted(tasks, key=lambda task: task.created_at)


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
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
    return _tasks.pop(task_id, None) is not None


def _reset() -> None:
    _tasks.clear()
