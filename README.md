# Task Tracker

A simple Task Tracker application with a FastAPI backend and a vanilla HTML/CSS/JavaScript frontend.

## Tech Stack

- Python
- FastAPI
- Pydantic
- HTML/CSS/JavaScript
- Pytest

## Setup

From the project root, activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies if needed:

```powershell
pip install -r requirements.txt
```

## Run the Backend

```powershell
uvicorn app.main:app --reload --port 8000
```

The backend runs at:

`http://127.0.0.1:8000`

## Open the Frontend

Open `frontend/index.html` using **Live Server** in VS Code.

Alternatively:

```powershell
cd frontend
python -m http.server 5500
```

Then open:

`http://localhost:5500`

## Run Tests

From the project root:

```powershell
pytest -q
```

Expected result:

```text
21 passed
```