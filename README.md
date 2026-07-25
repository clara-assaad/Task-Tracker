# Task Tracker API (Module 1)

A minimal learning-project REST API built with FastAPI. This is the initial
skeleton stage: it sets up the project structure, dependencies, and a
`/health` endpoint. CRUD functionality for tasks will be added in a later step.

## Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn

## Project Structure
task-tracker-api/
│
├── app/
│ ├── init.py
│ ├── main.py
│ ├── api/
│ │ ├── init.py
│ │ └── routes/
│ │ ├── init.py
│ │ └── health.py
│ ├── core/
│ │ ├── init.py
│ │ └── config.py
│ ├── models/
│ │ ├── init.py
│ │ └── health.py
│ └── storage/
│ └── .gitkeep
│
├── tests/
│ └── init.py
│
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt

## Setup Instructions

1. Create and activate a virtual environment:

   **Linux/macOS:**
```bash
   python3 -m venv venv
   source venv/bin/activate
```

   **Windows (PowerShell):**
```powershell
   python -m venv venv
   venv\Scripts\Activate.ps1
```

2. Install dependencies:
```bash
   pip install -r requirements.txt
```

3. Environment variables are already set in `.env` (copied from `.env.example`).
   Adjust `PORT` or `APP_ENV` there if needed.

## Running the Server

From the project root, with the virtual environment activated:

```bash
uvicorn app.main:app --reload --port 8000
```

The server will start at `http://127.0.0.1:8000`.

## Testing the Health Endpoint

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "timestamp": "2026-07-16T12:34:56.789012+00:00"
}
```

## API Documentation (Swagger)

Once the server is running, open your browser to:
http://127.0.0.1:8000/docs

This provides interactive Swagger UI documentation for all available endpoints.

## Status

This is a skeleton stage only. No CRUD endpoints, authentication, database,
Docker, or frontend are included yet.