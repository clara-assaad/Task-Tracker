# Task Tracker Architecture

## 1. What the app does

The Task Tracker is a FastAPI REST service that creates, retrieves, lists, partially updates, and deletes tasks. Listing supports status, priority, and overdue filters. Data is held in process memory.

## 2. Data model

The central entity is `Task`. A stored task contains a string `id`, title, description, status (`ToDo`, `InProgress`, or `Done`), priority (`Low`, `Medium`, or `High`), optional assignee, optional due date, tags, and UTC creation/update timestamps.

`TaskCreate` supplies creation fields and defaults. `TaskUpdate` makes every field optional for partial updates. `TaskResponse` represents the complete stored and returned entity.

## 3. Request flow

When a client sends `POST /tasks`, FastAPI parses the body as `TaskCreate`. Pydantic rejects unknown fields and validates the title, enums, dates, and tags. The endpoint passes the validated model to `storage.add_task()`, which generates an ID from the current dictionary size, creates UTC timestamps, constructs a `TaskResponse`, stores it in the module-level dictionary, and returns it with HTTP 201.

## 4. Key files

- `app/main.py` — Creates the FastAPI app, configures CORS, registers routes, and delegates task persistence to storage.
- `app/models.py` — Defines task request/response models, status and priority enums, and field normalization.
- `app/storage.py` — Implements in-memory CRUD operations, filtering, ordering, and overdue detection.
- `app/business_rules.py` — Referenced by `app/main.py` for status-transition validation; details are **not visible from the files I read**.
- `app/core/config.py` — Referenced for the environment value returned by the root endpoint; details are **not visible from the files I read**.
- `app/api/routes/health.py` — Supplies a health router included by the API; its routes are **not visible from the files I read**.
- Frontend files — Their names and implementation are **not visible from the files I read**.

## 5. Conventions

- **Validation:** Request models forbid unknown fields. Titles are trimmed, must be strings, cannot be blank, and are limited to 200 characters. Tags must be a list of strings; whitespace and empty entries are removed, and duplicates are removed case-insensitively while preserving the first spelling and order.
- **Storage:** Tasks live in a module-level dictionary and therefore are not durable across process restarts. IDs are decimal strings based on dictionary size. Lists are sorted by creation timestamp. A task is overdue when its due date precedes the current local date and it is not done.
- **Error handling:** Missing task IDs produce HTTP 404 in the API layer. Invalid update status transitions are delegated to a business-rule function whose implementation is **not visible from the files I read**. Other request-validation responses are **not visible from the files I read**.
- **Frontend/backend interaction:** CORS permits origins on local ports 5500 and 5173, plus the `"null"` origin. The actual frontend request behavior is **not visible from the files I read**.

## 6. Not visible or assumptions

Authentication, authorization, database integration, deployment topology, frontend implementation, health-route behavior, configuration loading, permitted status transitions, test coverage, and concurrency guarantees are **not visible from the files I read**. No assumptions about them are made here.
