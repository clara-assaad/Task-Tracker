# Task Tracker Architecture

## What the app does

Task Tracker is a learning-focused web application for creating, viewing, filtering, editing, moving, and deleting tasks. A vanilla HTML/CSS/JavaScript board communicates with a FastAPI REST API; task data exists only for the lifetime of the backend process.

## Data model

The primary entity is `Task`, with a generated decimal-string `id`, required `title`, optional `description`, `assignee`, and `due_date`, plus `status` (`ToDo`, `InProgress`, or `Done`), `priority` (`Low`, `Medium`, or `High`), a list of `tags`, and UTC `created_at`/`updated_at` timestamps. `TaskCreate`, `TaskUpdate`, and `TaskResponse` define create, partial-update, and response shapes. Overdue is computed rather than stored: the due date must be before the current local date and the task must not be `Done`.

## Request flow

When a user submits the new-task form, frontend JavaScript validates the title, builds JSON, and sends `POST /tasks`. FastAPI parses the body as `TaskCreate`; Pydantic applies defaults, rejects unknown or invalid fields, trims the title, and normalizes tags. The route delegates to `storage.add_task`, which generates an ID and UTC timestamps, constructs a `TaskResponse`, and inserts it into the in-memory dictionary. FastAPI serializes the task with HTTP 201, after which the frontend reloads the task list and renders the board.

## Key files

- `app/main.py` — Configures FastAPI, CORS, health routing, and task CRUD endpoints.
- `app/models.py` — Defines task schemas, enums, defaults, and field normalization.
- `app/storage.py` — Implements in-memory CRUD, filtering, ordering, IDs, and overdue calculation.
- `app/business_rules.py` — Enforces the permitted task-status transitions.
- `app/core/config.py` — Loads environment name and port settings.
- `app/api/routes/health.py` — Provides the API health-check endpoint.
- `frontend/index.html` — Contains the complete board UI, styles, validation, rendering, and API calls.
- `tests/test_tasks.py` — Specifies tested API behavior for CRUD, validation, filtering, tags, and transitions.
- `docs/decisions/in-memory-task-storage.md` — Records the storage decision and persistence trade-offs.

## Conventions

- **Validation:** Pydantic rejects unknown fields and invalid enum values. Titles are trimmed, required on create, nonblank, and limited to 200 characters. Tags are trimmed, empty values removed, and duplicates removed case-insensitively.
- **Storage:** Tasks are held in a module-level Python dictionary and disappear on restart. List results are ordered by creation time.
- **Errors:** Missing tasks return HTTP 404; request and business-rule violations return HTTP 422; successful deletion returns HTTP 204 without a body.
- **Frontend/backend interaction:** The frontend uses `fetch` with JSON over REST (`POST`, `GET`, `PATCH`, and `DELETE`). CORS permits configured local development origins. Status and priority filtering occurs in the browser, while the overdue filter is sent to the API.

## Not visible or assumptions

No database, authentication, authorization, ORM, deployment architecture, production persistence, or multi-instance coordination is visible. The frontend hard-codes `http://localhost:8001`, while backend configuration and repository instructions default to port 8000; the intended integrated port is therefore not confirmed. Test results were not rerun for this document.
