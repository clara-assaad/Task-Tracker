# Verification

## Baseline

Before implementing the new features, the existing test suite was run:

```text
17 passed
```

The existing Task Tracker behavior was also checked: create, edit, delete, status/priority filters, and drag-and-drop were working.

## New Feature Tests

Four new pytest tests were added:

- Create a task with a due date.
- Verify overdue filtering with status and priority filters.
- Normalize messy/duplicate tags.
- Clear tags during task update.

After implementing both features:

```text
21 passed
```

All 17 original tests continued to pass.

## Manual Browser Checks

### Due Date + Overdue Filter
Verified:
- Create tasks with or without a due date.
- Edit and clear due dates.
- Display due dates on task cards.
- Overdue-only filtering works.
- Tasks due today are not overdue.
- Done tasks are excluded from overdue results.
- Status and priority filters still work.

### Tags / Labels
Verified:
- Create tasks with or without tags.
- Edit and clear tags.
- Tags display on task cards.
- Empty and duplicate tags are cleaned correctly.

Existing create, edit, delete, filtering, and drag-and-drop behavior remained working.

## Break Test 1 — Overdue Logic

The correct rule:

```python
task.due_date < date.today()
```

was temporarily changed to:

```python
task.due_date <= date.today()
```

This incorrectly treated a task due today as overdue.

Result:

```text
1 failed
```

The correct `<` comparison was restored and the same test was run again:

```text
1 passed
```

This confirmed that the overdue test detects incorrect behavior.

## Break Test 2 — Tag Normalization

The correct duplicate check:

```python
tag_key = trimmed_tag.lower()
```

was temporarily changed to:

```python
tag_key = trimmed_tag
```

This caused `"Urgent"` and `"urgent"` to be stored as separate tags.

Result:

```text
1 failed
```

After restoring `.lower()`, the same test passed:

```text
1 passed
```

This confirmed that the tag-normalization test detects broken duplicate handling.

## Behavior Contract After Changes

After both features were implemented:

- Existing Task Tracker behavior still worked.
- Due dates and overdue filtering worked correctly.
- Tags could be added, edited, cleared, normalized, and displayed.
- Existing status-transition rules were unchanged.

Final full test result:

```text
21 passed
```