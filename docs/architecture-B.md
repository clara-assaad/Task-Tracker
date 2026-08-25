# Task Tracker Architecture

## 1. What the app does

Task Tracker is a learning-focused application for creating, viewing, filtering, partially updating, and deleting tasks. It uses a FastAPI REST backend and a vanilla HTML/CSS/JavaScript task-board frontend. Task data is stored in memory and is lost when the backend restarts.

## 2. Data model

The main entity is a **Task**, represented by Pydantic create, update, and response models.

| Field | Purpose |
|---|---|
| `id` | Generated decimal-string identifier |
| `title` | Required, trimmed, nonblank string; maximum 200 characters |
| `description` | Optional; defaults to an empty string |
| `status` | `ToDo`, `InProgress`, or `Done`; defaults to `ToDo` |
| `priority` | `Low`, `Medium`, or `High`; defaults to `Medium` |
| `assignee` | Optional string; defaults to `null` |
| `due_date` | Optional date |
| `tags` | List of normalized strings; defaults to an empty list |
| `created_at`, `updated_at` | Backend-generated UTC timestamps |

A task is overdue when its due date is earlier than the current local date and its status is not `Done`.

## 3. Request flow

When a user submits the new-task form, the frontend trims and checks the title, parses the tags, creates a JSON payload, and sends `POST /tasks`. FastAPI parses the payload as `TaskCreate`. Pydantic validates its fields, rejects unknown fields, applies defaults, and normalizes the title and tags. The endpoint passes the validated model to the storage layer, which generates an ID and timestamps, constructs the response model, and inserts the task into the in-memory dictionary. The API returns the created task with HTTP 201, after which the frontend requests the task list again and redraws the board. Validation failures return HTTP 422 and are displayed by the frontend.

## 4. Key files

- `app/main.py` — Configures FastAPI and CORS and exposes the task CRUD and root endpoints.
- `app/models.py` — Defines task models, enums, field defaults, title validation, and tag normalization.
- `app/storage.py` — Implements in-memory CRUD, ID generation, filtering, sorting, and overdue checks.
- `app/business_rules.py` — Defines and validates permitted task-status transitions.
- `app/core/config.py` — Loads the application environment and port settings.
- `app/api/routes/health.py` — Provides the `/health` endpoint.
- `frontend/index.html` — Contains the task-board UI, forms, filters, drag-and-drop behavior, and API calls.
- `tests/test_tasks.py` — Covers task operations, validation, filters, transitions, tags, and error responses.
- `tests/conftest.py` — Provides the test client and resets storage between tests.
- `docs/decisions/in-memory-task-storage.md` — Records the storage choice and its persistence trade-offs.

## 5. Conventions

- **Validation:** Request models reject unknown fields. Titles are trimmed and constrained to 200 characters. Tags are trimmed, empty entries are removed, and duplicates are removed case-insensitively while preserving the first occurrence.
- **Business rules:** Valid transitions are `ToDo → InProgress`, `InProgress → Done`, and `Done → InProgress`. Other transitions, including assigning the current status, return HTTP 422.
- **Storage:** Tasks live in a process-local Python dictionary. IDs are based on the dictionary size plus one, and list results are ordered by creation time.
- **Updates and errors:** `PATCH` preserves omitted fields. Missing task IDs return HTTP 404. Successful deletion returns HTTP 204 with no body.
- **Frontend/backend interaction:** The frontend communicates with the backend using JSON and `fetch`. FastAPI CORS configuration permits supported local frontend origins.

## 6. Not visible or assumptions

No database, ORM, authentication, authorization, frontend framework, JavaScript package manager, or production deployment architecture is confirmed. Behavior across multiple backend processes and long-term persistence is also not confirmed. The intended canonical local backend port is unclear: the supplied setup instructions use port `8000`, while the inspected frontend currently targets port `8001`.
