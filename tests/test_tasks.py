import pytest

from app.models import TaskPriority, TaskStatus


def test_create_task_valid_returns_201_with_full_body(client):
    payload = {
        "title": "Task 1",
        "description": "A real task",
        "status": TaskStatus.TODO.value,
        "priority": TaskPriority.HIGH.value,
        "assignee": "Alice",
    }

    response = client.post("/tasks", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert data["id"] == "1"
    assert data["title"] == "Task 1"
    assert data["description"] == "A real task"
    assert data["status"] == TaskStatus.TODO.value
    assert data["priority"] == TaskPriority.HIGH.value
    assert data["assignee"] == "Alice"
    assert data["created_at"] == data["updated_at"]


def test_create_task_missing_title_returns_422(client):
    response = client.post("/tasks", json={})

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any(error["loc"] == ["body", "title"] for error in detail)


def test_create_task_blank_title_returns_422(client):
    response = client.post("/tasks", json={"title": "   "})

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any(error["loc"] == ["body", "title"] for error in detail)


def test_create_task_invalid_priority_returns_422(client):
    response = client.post("/tasks", json={"title": "Task 1", "priority": "Urgent"})

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any(error["loc"] == ["body", "priority"] for error in detail)


def test_create_task_unknown_field_returns_422(client):
    response = client.post("/tasks", json={"title": "Task 1", "unexpected": True})

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any(error["loc"] == ["body", "unexpected"] for error in detail)


def test_list_tasks_empty_returns_200_and_empty_list(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(client):
    response = client.get("/tasks", params={"status": TaskStatus.DONE.value})

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(client):
    client.post("/tasks", json={"title": "High task", "priority": TaskPriority.HIGH.value})
    client.post("/tasks", json={"title": "Low task", "priority": TaskPriority.LOW.value})
    client.post("/tasks", json={"title": "Another high task", "priority": TaskPriority.HIGH.value})

    response = client.get("/tasks", params={"priority": TaskPriority.HIGH.value})

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(task["priority"] == TaskPriority.HIGH.value for task in data)
    assert [task["title"] for task in data] == ["High task", "Another high task"]


def test_get_task_by_id_returns_task(created_task, client):
    response = client.get(f"/tasks/{created_task['id']}")

    assert response.status_code == 200
    data = response.json()
    assert data == created_task


def test_get_task_by_id_not_found_returns_404_with_detail(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task with id 999 not found"}


def test_patch_partial_update_keeps_other_fields(created_task, client):
    response = client.patch(f"/tasks/{created_task['id']}", json={"title": "updated title"})

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_task["id"]
    assert data["title"] == "updated title"
    assert data["description"] == created_task["description"]
    assert data["status"] == created_task["status"]
    assert data["priority"] == created_task["priority"]
    assert data["assignee"] == created_task["assignee"]
    assert data["created_at"] == created_task["created_at"]
    assert data["updated_at"] != created_task["updated_at"]


def test_patch_not_found_returns_404(client):
    response = client.patch("/tasks/999", json={"title": "updated title"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Task with id 999 not found"}


def test_patch_valid_transition_todo_to_inprogress_returns_200(created_task, client):
    response = client.patch(f"/tasks/{created_task['id']}", json={"status": TaskStatus.IN_PROGRESS.value})

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == TaskStatus.IN_PROGRESS.value


def test_patch_invalid_transition_todo_to_done_returns_422(created_task, client):
    response = client.patch(f"/tasks/{created_task['id']}", json={"status": TaskStatus.DONE.value})

    assert response.status_code == 422
    assert "Invalid status transition" in response.json()["detail"]


def test_patch_same_status_returns_422(created_task, client):
    response = client.patch(f"/tasks/{created_task['id']}", json={"status": TaskStatus.TODO.value})

    assert response.status_code == 422
    assert "Invalid status transition" in response.json()["detail"]


def test_delete_existing_returns_204_no_body(created_task, client):
    response = client.delete(f"/tasks/{created_task['id']}")

    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_returns_404(client):
    response = client.delete("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task with id 999 not found"}
