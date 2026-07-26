## Feature 1: Due Date + Overdue Filter

### Story 1.1 — Manage Due Date
**User Story:** As a user, I want to add, edit, or remove an optional due date so that I can track task deadlines.

**Acceptance Criteria:**
- Due date is optional and can be added, changed, or cleared.
- A valid date is stored and returned by the API.
- Invalid dates are rejected.

**Edge Case:** Clearing an overdue task's due date removes it from overdue results.

### Story 1.2 — Display Due Date
**User Story:** As a user, I want to see the due date on the task card so that I can quickly check deadlines.

**Acceptance Criteria:**
- Display the due date when present.
- Show nothing when no due date exists.
- Overdue dates are visually distinguished.

**Edge Case:** A task due today is not considered overdue.

### Story 1.3 — Filter Overdue Tasks
**User Story:** As a user, I want an overdue filter so that I can focus on late tasks.

**Acceptance Criteria:**
- Overdue means `due_date < today` and status is not `Done`.
- Tasks with no due date or status `Done` are excluded.
- The filter works with existing status and priority filters.

**Edge Case:** An overdue task disappears from the overdue results when marked Done.

**AI Assumption Corrected:**  
The AI initially considered timezone handling. We removed this unnecessary complexity and used simple date-only comparison for this project.


---

## Feature 2: Tags / Labels

### Story 2.1 — Manage Tags
**User Story:** As a user, I want to add, edit, or remove optional tags so that I can label my tasks.

**Acceptance Criteria:**
- Tasks can have zero or multiple tags.
- Tags can be added, edited, or removed.
- Removing all tags produces an empty list.

**Edge Case:** A task without tags loads normally with an empty list.

### Story 2.2 — Display Tags
**User Story:** As a user, I want tags displayed on task cards so that I can identify labels at a glance.

**Acceptance Criteria:**
- Display tags as simple labels.
- Show no tag area when the task has no tags.
- Preserve their stored order.

**Edge Case:** A one-character tag still displays correctly.

### Story 2.3 — Normalize Tags
**User Story:** As a user, I want tag input cleaned automatically so that tags stay consistent.

**Acceptance Criteria:**
- Trim whitespace and remove empty tags.
- Remove duplicates case-insensitively.
- Preserve the first occurrence's casing and order.

**Edge Case:** `[" Urgent ", "urgent", "", "Bug"]` becomes `["Urgent", "Bug"]`.

**AI Assumption Corrected:**  
The AI initially suggested extra tag limits, character restrictions, and filtering. We removed these as out of scope and kept tags as simple optional labels.