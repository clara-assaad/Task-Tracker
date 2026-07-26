# AI Prompt Log

AI tools used:
- Claude AI for user stories and architecture planning.
- GitHub Copilot in VS Code for backend implementation, frontend implementation, testing, and UI refinement.

---

# Feature 1: Due Date + Overdue Filter

## Prompt 1 — Backend Implementation

**Tool:** GitHub Copilot

**Prompt:**

> Read the existing Task Tracker backend before making changes.
>
> I want to implement only the backend part of Feature 1: Due Date + Overdue Filter.
>
> Requirements:
>
> Add an optional date-only due_date field to the existing task models.  
> Existing tasks and requests without due_date must continue to work.  
> due_date should default to None when absent.  
> Create and update operations must accept due_date.  
> A task is overdue only when:  
> due_date < today's server date AND status is not Done.  
> A task due today is NOT overdue.  
> Tasks with no due date are NOT overdue.  
> Do not store an is_overdue boolean.  
> Add the smallest backend change needed to support filtering overdue tasks while preserving the existing status and priority filters.  
> Overdue filtering must combine with existing filters using AND logic.  
> Do not add timezone handling.  
> Do not modify the frontend yet.  
> Do not change existing status-transition rules.  
> Do not add a database, authentication, notifications, or unrelated features.  
> Preserve all existing API behavior and existing tests.  
> First inspect the relevant existing backend files and then make only the minimal changes required for this feature.

**What AI did:**  
Copilot updated the task models, storage logic, list endpoint, and focused backend tests to support due dates and overdue filtering.

**My decision:**  
I reviewed and accepted the changes after running pytest and confirming the existing behavior was preserved.

---

## Prompt 2 — Frontend Implementation

**Tool:** GitHub Copilot

**Prompt:**

> Read the existing frontend before making changes.
>
> Implement only the frontend part of Feature 1: Due Date + Overdue Filter.
>
> Backend support already exists:
>
> Task objects may contain due_date as a date string in YYYY-MM-DD format or null.  
> GET /tasks supports the query parameter overdue=true.  
> A task is overdue when due_date < today and status is not Done.
>
> Requirements:
>
> Task form:
>
> Add an optional date input for due_date to the existing create/edit task modal.  
> Creating a task without a due date must continue to work.  
> When editing a task, pre-fill its existing due date.  
> Allow the user to clear an existing due date.  
> Send due_date to the existing create/update API requests without changing unrelated fields.
>
> Task card:
>
> Display the due date when present.  
> Do not show an empty due-date label when due_date is null.  
> Keep the current card design simple and consistent.
>
> Overdue filter:
>
> Add an Overdue filter/control alongside the existing filters.  
> When enabled, request/filter overdue tasks using the backend overdue=true support.  
> It must continue to work together with the existing status and priority filters.  
> When not enabled, preserve the current task-list behavior.
>
> Constraints:
>
> Do not modify backend files.  
> Do not redesign the application.  
> Preserve create, edit, delete, drag-and-drop, status filtering, priority filtering, and existing UI behavior.  
> Do not add timezone handling, reminders, notifications, or unrelated features.  
> Make only the smallest focused frontend changes required.  
> After making the changes, summarize exactly which frontend file(s) were changed and what was added.

**What AI did:**  
Copilot added the due-date field, edit/clear behavior, due-date display, and overdue filtering to the frontend.

**My decision:**  
I accepted the feature logic after manually testing it in the browser. The functionality worked correctly.

---

**Weak prompt:**

> Please refine the CSS.

This prompt is too vague because it does not explain what is wrong, what should be preserved, or what the AI is allowed to change.

**Improved prompt:**  
## Prompt 3 — UI/CSS Refinement

**Tool:** GitHub Copilot

**Prompt:**

> Make only two small frontend UI/CSS refinements in frontend/index.html. Do not change backend code or existing application logic.
>
> Fix the create/edit task modal sizing:  
> The modal became too tall after adding the Due Date field.  
> Make the modal compact enough to fit comfortably within a normal desktop viewport without requiring internal scrolling.  
> Keep all fields visible: Title, Description, Status, Priority, Assignee, Due Date, and the Cancel/Save buttons.  
> Reduce unnecessary vertical spacing, field heights, and modal padding where needed.  
> Preserve the current overall visual style.  
> Do not remove any fields or functionality.
>
> Improve overdue due-date styling:  
> If a task has a due_date earlier than today AND its status is not Done, display its due-date pill with a red/error style.  
> Future dates and dates due today should keep the normal due-date style.  
> Done tasks should not receive the overdue red style even if their due date is in the past.
>
> Important:
>
> Make the smallest possible changes.  
> Do not modify backend files.  
> Do not change filtering, drag-and-drop, create/edit logic, API requests, or validation.  
> Do not redesign the board.

**What AI did:**  
Copilot refined the modal and added overdue styling. However, some CSS changes made the form layout less organized than intended.

**My decision:**  
I kept the useful overdue styling but manually adjusted the CSS and modal layout until the form was compact and visually correct.

---

# Feature 2: Tags / Labels

## Prompt 1 — User Stories and Planning for Both Features

**Tool:** Claude AI

**Prompt:**

> You are helping me plan two small end-to-end feature extensions for an existing Task Tracker built with FastAPI backend and a simple Kanban frontend.
>
> Existing Task Tracker features:
> - Create, view, update, and delete tasks
> - Status: ToDo, InProgress, Done
> - Priority: Low, Medium, High
> - Optional description
> - Optional assignee
> - Filter by status and priority
> - Drag and drop between Kanban columns
> - No authentication
> - No database
> - In-memory storage only
>
> Selected new features:
>
> Feature 1: Due Date + Overdue Filter
> - Each task may optionally have a due date.
> - The frontend should allow entering and editing the due date.
> - The task card should display the due date when present.
> - An overdue filter should show tasks whose due date has passed and that are not Done.
>
> Feature 2: Tags / Labels
> - Each task may optionally have one or more simple text tags.
> - The frontend should allow adding/editing tags.
> - Tags should be visible on task cards.
> - Keep the implementation simple and in scope.
>
> Task:
>
> Write 3 to 5 user stories for EACH feature.
>
> For every user story:
> - Use the format: As a user, I want..., so that...
> - Include specific, testable acceptance criteria.
> - Include at least one meaningful edge case across each feature.
>
> Also:
> - List any assumptions you made.
> - For each feature, include at least one AI assumption that I could review and potentially correct.
> - Do not add authentication, database persistence, notifications, reminders, or other features outside this scope.
> - Keep the stories small enough for a short mid-course project.

**What AI did:**  
Claude generated user stories, acceptance criteria, edge cases, and assumptions for both selected features.

**My decision:**  
I reviewed and refined the output. Some assumptions and extra complexity were removed to keep both features within the project scope.

---

## Prompt 2 — Backend Implementation and Tests

**Tool:** GitHub Copilot

**Prompt:**

> Read the existing backend and tests first.
>
> Implement only the backend and pytest tests for Feature 2: Tags / Labels.
>
> Requirements:
>
> Add tags to the existing task models.  
> tags is optional and defaults to an empty list.  
> Create and update operations must accept a list of strings.  
> Existing requests without tags must continue to work.
>
> Normalize tags before storage:
> - trim leading/trailing whitespace
> - remove empty tags
> - remove duplicates case-insensitively
> - preserve the casing and order of the first occurrence
>
> Example:  
> [" Urgent ", "urgent", "", "Bug"] -> ["Urgent", "Bug"]
>
> Allow updating a task to an empty tags list.  
> Return normalized tags in API responses.
>
> Tests:
>
> Add at least 2 focused pytest tests:
>
> Creating a task with messy/duplicate tags returns the normalized list.  
> Updating/clearing tags works correctly.
>
> Constraints:
>
> Do not modify frontend files yet.  
> Do not add tag filtering, search, colors, predefined tags, limits, or advanced validation.  
> Do not change due-date behavior, status-transition rules, or unrelated API behavior.  
> Preserve all existing tests.  
> Make the smallest focused changes possible.  
> Run the full pytest suite after the changes and summarize exactly what files changed and the test result.

**What AI did:**  
Copilot added tags to the backend models, implemented tag normalization, updated storage behavior, and added two focused pytest tests.

**My decision:**  
I accepted the implementation after reviewing the diff and running the full test suite. The final suite reached 21 passing tests.

---

## Prompt 3 — Frontend Implementation

**Tool:** GitHub Copilot

**Prompt:**

> Read the existing frontend and make only the smallest changes needed for Feature 2: Tags / Labels.
>
> Backend support already exists:
>
> Task objects contain tags as a list of strings.  
> tags defaults to an empty list.  
> Backend normalizes whitespace, empty tags, and case-insensitive duplicates.
>
> Requirements:
>
> Task form:
>
> Add one optional Tags field to the existing create/edit modal.  
> Use a simple comma-separated text input.  
> Example placeholder: University, AI, Project  
> When creating a task, split the entered text by commas and send tags as a list of strings.  
> When editing a task, pre-fill the field using the existing tags joined with commas.  
> Allow clearing all tags.  
> Do not duplicate backend normalization logic unnecessarily.
>
> Task card:
>
> Display tags as small simple labels/chips when tags exist.  
> Show no empty tag area when the task has no tags.  
> Keep the current card design compact and consistent.
>
> Constraints:
>
> Do not modify backend files or tests.  
> Do not add tag filtering, search, colors, predefined tags, limits, or advanced validation.  
> Preserve due-date behavior, overdue styling/filtering, create/edit/delete, drag-and-drop, status/priority filters, and existing modal layout.  
> Make only focused frontend changes in frontend/index.html.  
> After changes, summarize what was added.

**What AI did:**  
Copilot added the optional tags input, converted comma-separated input to a list, pre-filled tags during editing, allowed tags to be cleared, and displayed them on task cards.

**My decision:**  
I accepted the feature functionality after manual browser testing. The CSS/layout needed some manual refinement, but the tags behavior itself worked correctly.

---

