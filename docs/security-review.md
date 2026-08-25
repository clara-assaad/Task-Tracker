# Security Review

## AI Findings

| ID | Severity | File / Location | Finding | Suggested Fix | Evidence | Grade | Reason |
|---|---|---|---|---|---|---|---|
| SEC-01 | High | `app/main.py:31-148`; `README.md:103-109` | Task CRUD endpoints have no authentication or authorization. Anyone who can reach the API can list, read, create, update, or delete tasks. This is an intentional course-scope limitation, not production-ready behavior. | Keep the API limited to a trusted local environment for course use. Before shared or public deployment, add authentication and server-side authorization to every task operation. | The task route handlers declare no authentication dependency or ownership/role check. `README.md:109` documents “No Persistence/Auth” as a current limitation. | Valid | Confirmed from the route handlers. Authentication is intentionally outside the current course/project scope, so this is mainly a risk if the API is exposed beyond the intended local/course environment. |
| SEC-02 | High | `app/models.py:82-113`; `app/storage.py:91-100`; `app/models.py:116-128` | Explicit `null` values in PATCH requests can create invalid stored task state and potentially cause response-validation failures. | Reject explicit null values for fields that must remain non-null, or validate the fully merged `TaskResponse` before storing it. Add PATCH-null regression tests for every field. | `TaskUpdate` permits `None` for `title`, `description`, `status`, `priority`, and `tags`. `model_dump(exclude_unset=True)` retains explicitly supplied nulls, and `setattr()` stores them without reconstructing or revalidating the full response model. `TaskResponse` requires non-null values for these fields. | Valid | Confirmed from `TaskUpdate` allowing `None` and `storage.update_task()` applying explicitly supplied values using `model_dump(exclude_unset=True)` and `setattr()` without reconstructing or revalidating the complete `TaskResponse`. |
| SEC-03 | Medium | `app/storage.py:8,20,34,104-113` | ID generation can reuse an existing ID after deletion and overwrite a surviving task. | Use a monotonic counter or UUID. Add a create/create/delete/create regression test that verifies both the surviving task and new task remain present. | IDs are generated with `str(len(_tasks) + 1)`. For example, after creating IDs 1 and 2 and deleting ID 1, the next generated ID is 2, and assignment to `_tasks["2"]` replaces the surviving task. | Valid | Confirmed directly in `app/storage.py`. The `len(_tasks) + 1` calculation can generate an ID that is still in use after another task has been deleted. |
| SEC-04 | Medium | `app/models.py:10-33,48-57,82-91`; `AGENTS.md:152-160` | Several user-controlled fields are unbounded, allowing excessive memory, processing, response-size, and frontend DOM growth. | Define reasonable limits for description and assignee length, tag count, and individual tag length. Enforce an overall request-body limit at the deployment boundary and add boundary tests. | Only `title` has a 200-character limit. `description`, `assignee`, individual tags, and total tag count have no explicit bounds. Tag normalization iterates over and stores the entire submitted list. | Valid | Confirmed in `app/models.py`. The title has a 200-character limit, but description, assignee, tag length, and tag count do not have explicit bounds. |
| SEC-05 | Medium | `app/main.py:16-26` | CORS includes the opaque `"null"` origin, unnecessarily broadening browser access. The risk is more relevant because the API has no authentication. | Remove `"null"` unless file or sandbox origin support is explicitly required. Make the development origin allowlist environment-specific and narrow the allowed methods and headers. | `allow_origins` includes `"null"`, while `allow_methods` and `allow_headers` both use `"*"`. Credentials are not enabled, which limits but does not remove the risk for this unauthenticated API. | Valid | Confirmed in `app/main.py`. The `"null"` origin unnecessarily broadens the allowed browser origins, especially for an API without authentication. |
| SEC-06 | Medium | `.github/workflows/ci.yml:12-23`; `requirements.txt:1-4` | CI runs tests but has no dependency or security scanning, and `pytest` and `httpx` are installed without pinned versions. This is a CI/security-hardening concern rather than a functional defect. | Pin test dependencies in a development requirements or lock file. Add an appropriate dependency audit and consider lightweight static and secret scanning if the project will be deployed beyond coursework. | The workflow installs application requirements plus unpinned `pytest` and `httpx`, then runs only `pytest -v`. No dependency audit, static-security scan, secret scan, or image scan is visible. | Valid | Confirmed from `.github/workflows/ci.yml` and `requirements.txt`. This is CI/security hardening rather than a functional defect. |
| SEC-07 | Low | `.github/workflows/ci.yml:12-14`; `Dockerfile:2,14-15,19` | Some build inputs are mutable, reducing build reproducibility and supply-chain assurance. | For higher-assurance builds, pin GitHub Actions by commit SHA, pin the base image by digest, use a hash-locked dependency set, and avoid unconstrained tool upgrades during builds. | CI uses major-version GitHub Action tags, Docker uses the mutable `python:3.11-slim` tag, transitive dependencies have no hashes, and the builder upgrades pip without a version constraint. Direct application dependencies are version-pinned. | Valid | Confirmed from the Dockerfile and CI workflow. Treat this as low-severity supply-chain and build hardening. |
| SEC-08 | Low | `frontend/index.html:880`; `README.md:40-56`; `Dockerfile:37-39`; `app/main.py:18-23` | Frontend and backend port assumptions are inconsistent. This is a configuration and maintenance issue rather than a major security vulnerability. | Use a configurable API base URL or same-origin deployment. Align the development documentation, Docker exposure, frontend configuration, and CORS settings. | The frontend calls `http://localhost:8001`, while the documented local and Docker commands use port 8000. The mismatch originated from a local development workaround but remains hard-coded. | Valid | The frontend uses port 8001 while backend Docker/runtime configuration and documentation use port 8000. The hard-coded mismatch remains a configuration and maintenance issue. |

## My Manual Findings

| Severity | File / Location | Finding | Suggested Fix | Reason |
|---|---|---|---|---|
| Low | `app/core/config.py:13-14` | `PORT` is converted directly with `int(os.getenv("PORT", "8000"))`. A non-numeric environment value can make settings initialization fail and prevent application startup. | Validate the environment value and provide a clear configuration error, or use structured settings validation. | Identified during the manual scan of configuration and environment handling. This is primarily a configuration robustness and availability issue, not a major security vulnerability. |

## Reconciliation

### Agreement

Manual verification against the relevant repository files confirmed the underlying evidence for all eight AI findings. This verification does not mean that all eight were independently discovered before reviewing the AI audit.

### AI-only

The following findings were originally surfaced by the AI security audit and then manually verified:

- SEC-01: no authentication or authorization on task CRUD endpoints.
- SEC-02: explicit PATCH null values can create invalid stored state.
- SEC-03: task IDs can be reused after deletion.
- SEC-04: several user-controlled task fields are unbounded.
- SEC-05: CORS permits the `"null"` origin.
- SEC-06: CI lacks dependency/security scanning and uses unpinned test tools.
- SEC-07: mutable build inputs reduce reproducibility.
- SEC-08: frontend and backend port assumptions are inconsistent.

These are AI-surfaced findings, not independently discovered manual findings.

### You-only

The manual review identified one additional Low-severity issue in `app/core/config.py:13-14`: direct integer conversion of the `PORT` environment variable can prevent startup when the value is non-numeric. This is mainly an availability and configuration-robustness concern.

## Top 3 Unfixed Backlog

| Rank | Finding | Severity | Owner | Next Step |
|---|---|---|---|---|
| 1 | PATCH null handling / invalid stored state | High | Backend | Reject explicit null values for fields that must remain non-null or validate the fully merged `TaskResponse` before storing it, and add regression tests. |
| 2 | Task ID reuse after deletion | Medium | Backend | Replace `len(_tasks) + 1` ID generation with a monotonic counter or UUID and add a create/delete/create regression test. |
| 3 | Unbounded user-controlled task fields | Medium | Backend | Define reasonable limits for description length, assignee length, tag count, and tag length, then add boundary tests. |

These items remain unfixed security and engineering backlog work for this exercise.