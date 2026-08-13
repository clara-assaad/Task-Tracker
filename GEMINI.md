# Task Tracker API

A simple Task Tracker application with a FastAPI backend and a vanilla HTML/CSS/JavaScript frontend.

## Tech Stack

- **Backend:** Python, FastAPI, Pydantic, Uvicorn
- **Frontend:** HTML, CSS, JavaScript
- **Testing:** Pytest, HTTPX

## Project Structure

```text
├── app/
│   ├── api/routes/       # API endpoints
│   ├── core/             # Configuration
│   ├── model_package/    # Models
│   ├── business_rules.py # Validation logic
│   ├── main.py           # Application entry point
│   ├── models.py         # Data models
│   └── storage.py        # In-memory storage
├── docs/midcourse/       # Documentation
├── frontend/             # Frontend static files
├── tests/                # Test suite
└── venv/                 # Virtual environment
```

## Running the Application

### Backend
Activate the virtual environment, then run:
```powershell
uvicorn app.main:app --reload --port 8000
```

### Frontend
Serve `frontend/index.html` (e.g., using Live Server or `python -m http.server 5500`).

## Running Tests
```powershell
.\venv\Scripts\pytest -q
```

## Current Features and Constraints

- Task CRUD: create, read, update, delete
- Status values: ToDo, InProgress, Done
- Priority values: Low, Medium, High
- Description and Assignee fields
- Status and priority filtering
- Kanban drag-and-drop
- Due Date + Overdue Filter
- Tags / Labels
- In-memory storage
- Current verified baseline: 21 passing pytest tests

