# Final AI Review and Ownership Evidence

## AGENTS.md guardrails

- Repo-specific stack and commands included: yes
- Docs-first/read-first guardrail included: yes
- Unexpected app/frontend edits rule included: yes

The application-code protection is explicit for `app/`. Frontend and other repository files are covered by the broader read-only-by-default rule, which requires an explicit request before repository files are edited.

## AI code review mini-log

| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
|---|---|---|---|
| Using `len(_tasks) + 1` for task IDs can reuse an ID that is still occupied after another task is deleted. | Useful | This identifies a verified limitation of the current in-memory ID-generation approach. In a create/create/delete/create sequence, the new task can overwrite a surviving task. | Verified against `app/storage.py`. The implementation was kept unchanged because the Final Project focuses on reviewing and hardening the existing application rather than adding or redesigning product features. |
| Explicit `null` values in PATCH requests can create invalid stored task state and potentially cause response-validation failures. | Useful | `TaskUpdate` permits `None` for fields that are non-null in `TaskResponse`. Explicitly supplied nulls remain present after `model_dump(exclude_unset=True)` and are assigned without reconstructing or revalidating the complete response model. | Verified against `app/models.py`, `app/main.py`, `app/storage.py`, and the existing tests. No focused PATCH-null regression test was identified. No application-code change was made because the Final Project review did not authorize or require that product-code change. |
| The difference between host port `8001` and the container’s internal port `8000` was treated as a security or application defect. | Noise | Docker can intentionally map host port `8001` to container port `8000`. That mapping does not by itself indicate a security vulnerability or application defect. A hard-coded frontend port can still be a configuration-maintenance concern. | `docs/release-evidence.md` records successful local and Docker verification on host port `8001`, including HTTP 200 responses from `/health`. `README.md` was aligned with that verified host-port setup. |

## AI security mini-review

| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
|---|---|---|---|---|
| Task CRUD endpoints have no authentication or authorization. | `app/main.py`; `README.md` | Valid | The task route handlers do not enforce authentication, ownership, or role checks. This is acceptable for the current learning-focused scope but would matter if the API were shared or publicly deployed. | Keep the current course scope. Add authentication and server-side authorization before any real shared or public deployment. |
| Task ID generation can reuse an occupied ID after deletion. | `app/storage.py` | Valid | IDs are generated using the current dictionary size plus one. After a lower-numbered task is deleted, the next generated ID can collide with a surviving task and overwrite it. | Consider a monotonic counter, UUID, or persistent database-generated identifier in a future version. Do not change it solely for this Final Project unless a separate approved task requires the change. |
| The host-port `8001` to container-port `8000` mapping was treated as a security issue. | `frontend/index.html`; `README.md`; `Dockerfile`; `docs/release-evidence.md` | Noise | The current frontend and README use host port `8001`, while Docker intentionally maps it to the application’s internal port `8000`. That mapping is normal and is not a security vulnerability by itself. | No security fix is required solely because different host and container ports are used. A future version could make the frontend API base URL configurable to reduce maintenance risk. |

## Manual security check

I manually reviewed `.gitignore`, `.dockerignore`, `.env.example`, the Docker configuration, and the relevant project files for obvious accidental exposure of sensitive configuration. I confirmed that `.env` is excluded by both `.gitignore` and `.dockerignore`, while `.env.example` contains only non-sensitive example configuration. I did not identify passwords, tokens, credentials, or real personal or customer data in the files reviewed. This was a targeted configuration and static review, not a comprehensive secret scan, Git-history scan, or Docker image-content inspection. This matters because secrets should not be committed to the repository or copied into the Docker build context.

## One AI output I rejected or corrected

AI initially treated the port difference as a broader security or application issue. I corrected and refined that conclusion after reviewing the configuration and recorded verification evidence. The application was successfully verified locally and with Docker on host port `8001`, including successful `/health` responses with HTTP 200. Docker intentionally maps host port `8001` to container port `8000`, which is not an application defect or security vulnerability by itself. Instead of changing application behavior unnecessarily, I aligned `README.md` with the verified host-port setup while retaining configurable frontend routing as a possible future improvement.

## Three AI usage rules

1. Never paste: Passwords, credentials, private IDs, personal information, or other sensitive or confidential data into an AI tool.
2. Always verify: Review AI-generated work and test or validate it using evidence appropriate to the task before accepting it.
3. Record AI contributions by: Documenting important areas where AI assisted, what was reviewed or changed, and what I personally verified before accepting the result.

## Ownership statement

I am comfortable submitting this repository as my work because I understand the application, its main architecture, and the changes made throughout the course. AI helped me with planning, reviewing, debugging, and documentation, but I did not accept its output automatically. I reviewed proposed changes, ran the application and tests, verified the frontend, API health endpoint, and Docker workflow, and corrected or refined AI conclusions when the evidence did not support them. I remain responsible for the final decisions and for the repository I submit.
