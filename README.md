# Task Tracker API

A simple Task Tracker application with a FastAPI backend and a vanilla HTML/CSS/JavaScript frontend.
It supports creating, viewing, filtering, updating, and deleting tasks with statuses, priorities, assignees, due dates, and tags. Task data is stored in memory and is lost when the backend restarts.

## Tech Stack

- **Backend:** Python 3.11+, FastAPI, Pydantic
- **Frontend:** Vanilla HTML5, CSS3, JavaScript (ES6+)
- **Testing:** Pytest, HTTPX
- **Containerization:** Docker

## Prerequisites

- Python 3.11 or 3.12
- Docker (optional)

## Local Setup

1. **Create and activate a virtual environment:**

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   *(For macOS/Linux, use `source venv/bin/activate`)*

2. **Install dependencies:**

   ```powershell
   pip install -r requirements.txt
   pip install pytest httpx
   ```

3. **Create the optional local environment file:**

   ```powershell
   Copy-Item .env.example .env
   ```

## Run the App Locally

### Backend

Run the FastAPI server from the repository root on port `8001`. The frontend currently connects to this port:

```powershell
uvicorn app.main:app --reload --port 8001
```

The API is available at `http://127.0.0.1:8001`.

- Health check: `http://127.0.0.1:8001/health`
- Interactive API documentation: `http://127.0.0.1:8001/docs`

### Frontend

In a second terminal, serve the frontend:

```powershell
cd frontend
python -m http.server 5500
```

Open `http://localhost:5500`.

## Run Tests

From the repository root:

```powershell
pytest -v
```

Current verified result on Python 3.12.9: `21` tests collected and `21 passed`.

## Run with Docker

The Docker image runs the backend API only. Serve `frontend/` separately as described above if you want to use the browser interface.

Build the image:

```powershell
docker build -t task-tracker:dev .
```

Run the container, mapping the frontend's expected host port `8001` to the container's port `8000`:

```powershell
docker run --rm -d -p 8001:8000 --name tt-dev task-tracker:dev
```

Verify the health endpoint:

```powershell
Invoke-RestMethod http://127.0.0.1:8001/health
```

Stop the container:

```powershell
docker stop tt-dev
```

The Dockerfile installs pinned application dependencies in a multi-stage build, copies only `app/` into the runtime image, and runs the API as a non-root user.

## CI Workflow Summary

The GitHub Actions workflow in [`.github/workflows/ci.yml`](.github/workflows/ci.yml):

- Runs on pushes to any branch.
- Runs on pull requests targeting `main`.
- Uses Python 3.12.
- Installs the application and test dependencies.
- Runs `pytest -v`.

The workflow is configured, but the final-project CI result will be verified after the branch is pushed.

## Final Project

**Branch reviewed:** `final-project`

### What this submission demonstrates

- Existing Task Tracker app still runs inside the intended course scope.
- CI is configured to run `pytest -v` on push; the actual final-project GitHub Actions execution is pending until the branch is pushed.
- The Docker image built successfully, and the container ran successfully with `/health` returning HTTP 200.
- AI review, security, release verification, and ownership evidence are documented in `docs/`.

### How to run locally

From the repository root, create and activate the virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the application and test dependencies:

```powershell
pip install -r requirements.txt
pip install pytest httpx
```

Optionally create the local environment file:

```powershell
Copy-Item .env.example .env
```

Run the backend on host port `8001`:

```powershell
uvicorn app.main:app --reload --port 8001
```

In a second terminal, serve the frontend on port `5500`:

```powershell
cd frontend
python -m http.server 5500
```

Open `http://localhost:5500`.

### How to run tests

```powershell
pytest -v
```

Verified local result: Python 3.12.9 — `21` tests collected, `21 passed`.

### How to run with Docker

```powershell
docker build -t task-tracker:dev .
docker run --rm -d -p 8001:8000 --name tt-dev task-tracker:dev
curl.exe -i http://127.0.0.1:8001/health
```

### Evidence files

- [Release evidence](docs/release-evidence.md)
- [Final AI review and ownership evidence](docs/final-ai-review.md)
- [Personal AI coding playbook](docs/ai-playbook.md)

### AI assistance summary

AI helped draft or review CI, Docker, documentation, security findings, debugging, and release preparation.

I verified the work by:

- Reviewing proposed diffs.
- Running `pytest -v`.
- Manually testing the frontend.
- Verifying the local `/health` endpoint.
- Building and running the Docker image.
- Verifying Docker `/health`.

One AI suggestion I rejected or corrected: AI initially treated the `8000` versus `8001` port difference as a broader application or security issue. I verified the actual configuration and runtime behavior and refined that conclusion: host port `8001` is valid, and Docker intentionally maps host port `8001` to container port `8000`.

## Project Structure

```text
├── .github/workflows/
│   └── ci.yml                 # GitHub Actions test workflow
├── app/
│   ├── api/routes/health.py   # Health endpoint
│   ├── core/config.py         # Environment settings
│   ├── model_package/         # Health response model
│   ├── business_rules.py      # Permitted status transitions
│   ├── main.py                # FastAPI app and task endpoints
│   ├── models.py              # Pydantic task models
│   └── storage.py             # In-memory task storage
├── docs/
│   ├── decisions/             # Technical decisions and plans
│   ├── midcourse/             # Mid-course evidence
│   ├── ai-playbook.md
│   ├── ai-usage.md
│   ├── architecture.md
│   ├── final-ai-review.md
│   ├── governance-worksheet.md
│   ├── release-evidence.md
│   └── security-review.md
├── frontend/
│   └── index.html             # Static Kanban interface
├── tests/                     # Pytest API and model tests
├── .dockerignore
├── AGENTS.md                  # Repository-specific AI guardrails
├── Dockerfile
├── README.md
└── requirements.txt
```

## Project Conventions and Current Limitations

- **In-Memory Storage:** Data is lost whenever the backend server restarts.
- **Status Transitions:** Enforces a controlled workflow: `ToDo -> InProgress`, `InProgress -> Done`, and `Done -> InProgress`.
- **Due Dates:** A task is overdue when its due date is earlier than the current local date and its status is not `Done`.
- **Tag Normalization:** Tags are automatically trimmed and de-duplicated (case-insensitive) via Pydantic validators.
- **No Persistence or Authentication:** This learning-focused prototype does not include a database, authentication, or authorization.

## AI Assistance

AI assisted with repository-grounded architecture, security, governance, planning, and documentation reviews. Suggestions were checked against the implementation, tests, configuration, and manual application behavior before being accepted or rejected. Repository-specific working rules are recorded in [`AGENTS.md`](AGENTS.md).

## Documentation

### Final-project and Module 5 documentation

- [Release evidence](docs/release-evidence.md)
- [Final AI review and ownership evidence](docs/final-ai-review.md)
- [Consolidated architecture review](docs/architecture.md)
- [Minimal-context architecture draft](docs/architecture-A.md)
- [Structured-context architecture draft](docs/architecture-B.md)
- [Targeted-context architecture draft](docs/architecture-C.md)
- [Security review](docs/security-review.md)
- [Governance worksheet](docs/governance-worksheet.md)
- [Personal AI usage rules](docs/ai-usage.md)
- [Personal AI coding playbook](docs/ai-playbook.md)

### Decisions and mid-course evidence

- [In-Memory Task Storage](docs/decisions/in-memory-task-storage.md)
- [Comments Feature Plan](docs/decisions/comments-feature-plan.md)
- [Mini ADR — Feature Extensions](docs/midcourse/mini-adr.md)
- [User Stories & Acceptance Criteria](docs/midcourse/user-stories.md)
- [Verification Report](docs/midcourse/verification.md)
