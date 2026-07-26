# Mini ADR — Mid-Course Feature Extension

**Status:** Approved  
**Date:** July 26, 2026

## Context

The Task Tracker uses a FastAPI/Pydantic backend with in-memory storage and a vanilla HTML/CSS/JavaScript frontend.

Two features were selected for the mid-course extension:
1. Due Date + Overdue Filter
2. Tags / Labels

The goal was to add both features without introducing a database, authentication, or unnecessary architectural complexity.

## Decision

### Due Date + Overdue Filter
- Add an optional `due_date` field to the existing task model.
- Compute overdue dynamically using: `due_date < today` and status is not `Done`.
- Do not store a separate `is_overdue` value.
- Extend the existing frontend form, task cards, and filters.

### Tags / Labels
- Add a `tags` list to the existing task model.
- Normalize tags before saving by trimming whitespace, removing empty values, and removing duplicates case-insensitively.
- Display tags on task cards.
- Keep tag filtering, colors, and predefined tag lists out of scope.

## Alternatives Rejected

- Storing `is_overdue` — rejected because it could become outdated.
- Timezone-aware due dates — unnecessary for this project.
- Separate Tag models/entities — too complex for simple labels.
- Tag filtering and advanced validation — outside the selected scope.

## Trade-offs

This approach keeps the implementation simple and compatible with the existing architecture. Overdue values remain accurate because they are calculated dynamically, but the project still uses in-memory storage, so due dates and tags are lost when the server restarts.