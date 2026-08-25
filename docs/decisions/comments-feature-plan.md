# Comments on Tasks — Feature Plan

This is a planning document based on the repository’s current FastAPI, Pydantic, in-memory storage, pytest, and single-file vanilla frontend conventions. Comments are not currently implemented.

## 1. Data Model

Add `CommentCreate` and `CommentResponse` to `app/models.py`, alongside the existing task schemas.

`CommentCreate` should contain only client-supplied fields:

- `author`: required string, 1–100 characters.
- `body`: required string, 1–2000 characters.

It should use `ConfigDict(extra="forbid")`, matching `TaskCreate` and `TaskUpdate`. This prevents clients from supplying server-managed fields such as `id`, `task_id`, and `created_at`.

`CommentResponse` should contain:

- `id`: UUID represented as a string.
- `task_id`: string matching the existing task ID type.
- `author`: validated author.
- `body`: validated comment body.
- `created_at`: server-generated, timezone-aware UTC datetime.

The initial design should not add comments to `TaskResponse`. Loading comments through separate nested routes preserves existing task response shapes and avoids embedding a growing collection in each task.

Whether `author` and `body` are trimmed before validation remains an assumption to verify. Trimming would follow the existing task-title convention, but comment-specific whitespace behavior is not defined.

## 2. API Routes

The initial routes can remain in `app/main.py`, where the current task endpoints are defined.

### Create a comment

- Method: `POST`
- Path: `/tasks/{task_id}/comments`
- Request body: `author` and `body`
- Success response: `201 Created` with a full `CommentResponse`
- OpenAPI tag: `comments`

The route should confirm that the task exists, generate the UUID and UTC timestamp on the server, copy `task_id` from the path, and store the comment.

Error cases:

- `404 Not Found` when the task does not exist, following the existing `Task with id {task_id} not found` convention.
- `422 Unprocessable Entity` for missing, invalid, blank under the selected whitespace policy, or oversized fields.
- `422 Unprocessable Entity` for unknown or server-managed request fields.

### List comments for a task

- Method: `GET`
- Path: `/tasks/{task_id}/comments`
- Request body: none
- Success response: `200 OK` with a list of `CommentResponse` objects
- OpenAPI tag: `comments`

For an existing task with no comments, return an empty list. For a missing task, return `404`. Comments should initially be ordered by `created_at` ascending, matching the oldest-first convention used by `storage.get_all_tasks`.

Individual retrieval, editing, and deletion routes are not included unless the team decides that comments must support those operations. Any future nested comment route must verify that the comment belongs to the task identified in the path.

## 3. Tests

Add function-style API tests in `tests/test_comments.py`, following the `TestClient`, fixture, status-code, and JSON assertion patterns in `tests/test_tasks.py`. The autouse reset fixture in `tests/conftest.py` must clear comment storage as well as task storage.

### Happy path

- `test_create_comment_valid_returns_201_with_full_body`
- `test_create_multiple_comments_generates_unique_uuid_ids`
- `test_list_comments_for_task_returns_200_in_creation_order`
- `test_list_comments_for_existing_task_with_none_returns_empty_list`
- `test_list_comments_returns_only_comments_for_requested_task`
- `test_create_comment_trims_author_and_body`, if trimming is selected

The tests should parse generated IDs as UUIDs rather than compare them with fixed values. They should also verify that `task_id` matches the parent task and that `created_at` is a UTC-aware datetime.

### Validation

- `test_create_comment_missing_author_returns_422`
- `test_create_comment_missing_body_returns_422`
- `test_create_comment_blank_author_returns_422`
- `test_create_comment_blank_body_returns_422`
- `test_create_comment_author_over_100_characters_returns_422`
- `test_create_comment_body_over_2000_characters_returns_422`
- `test_create_comment_non_string_author_returns_422`
- `test_create_comment_non_string_body_returns_422`
- `test_create_comment_unknown_field_returns_422`
- `test_create_comment_client_supplied_id_returns_422`
- `test_create_comment_client_supplied_task_id_returns_422`
- `test_create_comment_client_supplied_created_at_returns_422`

Boundary tests should confirm acceptance of 1- and 100-character authors and 1- and 2,000-character bodies. Validation assertions should inspect FastAPI’s `detail` locations, matching existing test style.

### Edge cases

- `test_create_comment_for_missing_task_returns_404_with_detail`
- `test_list_comments_for_missing_task_returns_404_with_detail`
- `test_deleting_task_removes_its_comments`, if cascade deletion is selected
- `test_reset_storage_clears_comments`
- `test_comment_created_at_is_server_generated_utc_datetime`
- `test_comment_id_is_not_derived_from_collection_size`
- `test_comment_body_preserves_internal_line_breaks`, if multiline preservation is selected
- `test_comments_disappear_after_storage_reset`

The current suite was not run for this planning task. The documented expectation of 21 passing tests must not be treated as a current result or retained as the final expected count after implementation.

## 4. Frontend Changes

The frontend is contained in `frontend/index.html`, including its markup, CSS, and JavaScript. The current UI renders task cards in status columns and uses a shared create/edit task modal; it has no task-detail page or comments panel.

Recommended changes to `frontend/index.html`:

- Add a Comments action beside Edit on each task card.
- Open a dedicated comments modal for the selected task.
- Display the task title, loading state, empty state, comment list, and request errors.
- Show each comment’s author, safely rendered body, and formatted creation time.
- Add required author and multiline body controls with 100- and 2,000-character limits.
- Fetch `GET /tasks/{task_id}/comments` when the modal opens.
- Submit new comments to `POST /tasks/{task_id}/comments`.
- Preserve entered values on failure and clear the body after success.
- Follow the existing modal’s keyboard, focus, close-button, backdrop, and Escape-key behavior.
- Render user-controlled values as text rather than HTML.

No frontend test framework is visible. Automated frontend-test conventions are therefore not confirmed; a short manual verification checklist will be needed unless frontend test tooling is introduced separately.

`frontend/index.html` currently uses `http://localhost:8001` as `BASE_URL`, while `README.md` documents port 8000. This pre-existing discrepancy should be resolved or documented before comments UI verification, but it is not caused by this feature.

## 5. Migration Notes

No database migration is required under the current architecture. `docs/decisions/in-memory-task-storage.md` confirms that task data is held in memory and is lost when the process restarts.

Recommended changes to the future storage design:

- Keep the existing `_tasks` dictionary shape unchanged.
- Add a separate in-memory comment collection in `app/storage.py`.
- Generate comment IDs as UUIDs rather than using the task storage’s decimal ID convention.
- Filter comments by `task_id` and return them in ascending creation order.
- Extend `storage._reset()` to clear both tasks and comments.
- If cascade deletion is selected, remove a task’s comments inside the task deletion storage operation.

Existing task records require no backfill because the plan does not add comments to `TaskResponse`.

If the project later adopts relational persistence, comments would require a separate table, a foreign key to tasks, and an explicit deletion rule. The repository does not confirm an ORM, database, or migration framework.

## 6. Open Questions

1. Should `author` and `body` be trimmed, and are whitespace-only values invalid?
2. Should deleting a task cascade-delete its comments, block deletion, or preserve them?
3. Are comments immutable, or must individual retrieval, editing, or deletion be supported?
4. Is `author` permanently free-form or expected to become an authenticated identity?
5. Should internal line breaks in comment bodies be preserved?
6. Should comments be returned oldest-first or newest-first?
7. Is pagination required, now or at a documented threshold?
8. Should task responses expose a comment count without embedding comments?
9. Which UUID version should be required?

## Plan Evaluation

| Section | Label | Evidence | Minimal Correction |
|---|---|---|---|
| Data Model | Right | Placing request and response schemas in `app/models.py` and using `ConfigDict(extra="forbid")` follows `TaskCreate`, `TaskUpdate`, and `TaskResponse`. Keeping comments out of `TaskResponse` preserves the existing API shape. | Keep the design, then confirm trimming and UUID version before implementation. |
| API Routes | Needs-Resequencing | The nested create/list routes fit the task-centric API in `app/main.py`, but the plan finalizes the route set before deciding whether comments are editable or deletable. | Resolve comment mutability and required operations first, then approve the final route contract. |
| Tests | Right | The proposed function-style names, shared fixtures, `TestClient` calls, 422 detail checks, and storage reset behavior match `tests/conftest.py` and `tests/test_tasks.py`. | Keep the test plan and include only conditional tests whose related product decisions are approved. |
| Frontend Changes | Missing | The plan correctly targets the single-file UI in `frontend/index.html`, but no automated frontend-test convention exists and the plan does not provide a concrete manual acceptance checklist. | Add brief manual checks for opening, empty/loading states, validation, successful submission, failure preservation, safe rendering, and keyboard closure. |
| Migration Notes | Right | Separate in-memory comment storage, reset integration, UUID generation, and no task backfill align with `app/storage.py` and `docs/decisions/in-memory-task-storage.md`. | Keep the design and record the chosen task-deletion policy before storage work begins. |
| Open Questions | Needs-Resequencing | The questions are real unresolved decisions, but trimming, route scope, ordering, and deletion behavior affect the preceding model, API, storage, and test contracts. | Move these decisions into a short design-approval gate before implementation planning is considered final. |

## Generic vs Repo-Grounded Comparison

- **Biggest difference:** The generic plan identifies common feature concerns, while the repo-grounded plan maps them to `app/models.py`, `app/main.py`, `app/storage.py`, `tests/conftest.py`, `tests/test_tasks.py`, and the single-file `frontend/index.html`, including the actual in-memory reset and response-shape implications.
- **Plan I would hand to a teammate and why:** I would hand over the repo-grounded plan because it identifies concrete integration points, existing validation and testing conventions, storage lifecycle behavior, and repository-specific risks without claiming the feature already exists.
- **A task shape where generic chat is enough:** A technology-neutral product workshop deciding what fields a comment should contain and whether comments should be editable does not require repository access.

## Files Read

- `AGENTS.md`
- `README.md`
- `app/models.py`
- `app/main.py`
- `app/storage.py`
- `app/business_rules.py`
- `tests/conftest.py`
- `tests/test_tasks.py`
- `tests/verify_a.py`
- `frontend/index.html`
- `docs/decisions/in-memory-task-storage.md`
- `docs/midcourse/mini-adr.md`

## Assumptions to Verify

- **Assumption:** The initial feature includes only creating and listing comments.
- **Assumption:** Comment IDs use UUIDv4 represented as strings.
- **Assumption:** `author` and `body` are trimmed before length and blank-value validation.
- **Assumption:** Internal body whitespace and line breaks are preserved.
- **Assumption:** Existing task responses do not embed comments or comment counts.
- **Assumption:** Comments use a separate in-memory collection in `app/storage.py`.
- **Assumption:** Deleting a task deletes its comments.
- **Assumption:** An existing task with no comments returns `200` and an empty list.
- **Assumption:** A missing parent task returns `404` for both create and list operations.
- **Assumption:** Comments are returned oldest-first.
- **Assumption:** The frontend uses a dedicated comments modal in `frontend/index.html`.
- **Assumption:** No authentication, persistence layer, frontend testing framework, or migration framework exists beyond what was visible in the inspected files.
