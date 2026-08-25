# Release Evidence

## Baseline

- Branch: final-project
- Date: 2026-08-25
- Local app run command: `uvicorn app.main:app --reload --port 8001`
- /health result: HTTP 200 — `{"status":"ok","timestamp":"2026-08-25T09:11:48.472633+00:00"}`
- Frontend check: Loaded successfully. Manual testing confirmed task creation/display, a valid drag-and-drop status transition, and rejection of an invalid transition with an error shown.
- Test command: `pytest -v`
- Test result: Python 3.12.9 — 21 tests collected, 21 passed.

## CI evidence

- Workflow file: `.github/workflows/ci.yml`
- Latest run link or note: GitHub Actions CI run #5 on `final-project`, commit `901763a` — Success (17s); the test job succeeded.
- Python version used by CI: 3.12.14
- Test command used by CI: `pytest -v`
- Test result: 21 tests collected, 21 passed in 0.16s.
- Shortcut check: no continue-on-error / no || true / pytest is not skipped.

## Docker evidence

- Build command: `docker build -t task-tracker:dev .` — Successful. Docker reported `Building 305.5s (15/15) FINISHED` and created image `task-tracker:dev`.
- Run command: `docker run --rm -d -p 8001:8000 --name tt-dev task-tracker:dev` — Successful. Container `tt-dev` started with host port `8001` mapped to container port `8000`.
- /health check: `curl.exe -i http://127.0.0.1:8001/health` — HTTP 200. Response: `{"status":"ok","timestamp":"2026-08-25T10:12:44.464999+00:00"}`
- Non-root check, if implemented: The `Dockerfile` configures the runtime user with `USER app`; the image built and the container ran successfully with this configuration. No additional runtime user verification was performed.
- No-baked-secrets check: Configuration/static check only — `.dockerignore` excludes `.env`, and the runtime image copies only `app/`. No image-content inspection was performed.

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
| ------------- | ------------- | ------ | ------------------- |
| Task data is stored in memory and is lost when the backend restarts. | `README.md`; module-level `_tasks` dictionary in `app/storage.py` | Confirmed by implementation. | None |
| The permitted transitions are `ToDo` → `InProgress`, `InProgress` → `Done`, and `Done` → `InProgress`. | `README.md`; `VALID_TRANSITIONS` in `app/business_rules.py`; transition tests in `tests/test_tasks.py` | Confirmed by code and tests. | None |
| Tags are trimmed and de-duplicated case-insensitively. | `README.md`; `normalize_tags` in `app/models.py`; tag normalization test in `tests/test_tasks.py` | Confirmed by code and tests. | None |
| The Docker image uses a multi-stage build, copies only `app/`, and runs as a non-root user. | `README.md`; `Dockerfile` builder/runtime stages, `COPY --chown=app:app app/ ./app/`, and `USER app`; verified Docker build, container run, and `/health` check | Confirmed as configuration. The image built successfully, the container ran successfully, and `/health` returned HTTP 200. | None |
| CI installs dependencies and runs `pytest -v`. | `README.md`; `.github/workflows/ci.yml`; GitHub Actions CI run #5 on `final-project`, commit `901763a` | Confirmed. CI succeeded in 17s using Python 3.12.14, and `pytest -v` collected 21 tests and passed all 21 in 0.16s. No `continue-on-error`, `|| true`, or skipped pytest shortcut was found. | None |
