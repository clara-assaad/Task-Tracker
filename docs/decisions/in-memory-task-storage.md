# Technical Decision: In-Memory Task Storage

## 1. Context

The Task Tracker API needs a simple way to store tasks while the application is running. Since this project is mainly for learning and practicing API development, we do not need a full database at this stage.

The main goal is to keep the project simple so we can focus on FastAPI, task management, validation, testing, and the other features of the application.

## 2. Decision

We decided to use an in-memory Python dictionary to store the tasks.

The `_tasks` dictionary is defined in `app/storage.py`, and the storage functions use it to create, retrieve, update, and delete tasks.

This means the application can manage tasks without requiring a database or any additional storage configuration.

## 3. Alternatives Considered

### SQLite

SQLite could provide persistent storage while still being relatively simple. However, it would require database tables and additional database logic that are not necessary for the current project.

### External Database

A database such as PostgreSQL could also be used. It would be more appropriate for a larger application that needs persistent data and more advanced database features, but it would add unnecessary complexity to this project.

## 4. Trade-offs

The main advantage of using an in-memory dictionary is simplicity. It is easy to understand, requires no database setup, and allows us to focus on developing and testing the API.

The main disadvantage is that the data is temporary. If the backend server stops or restarts, all stored tasks are lost.

Another limitation is that this approach is designed for a simple prototype and would not be suitable if the application later needed permanent storage or multiple application instances.

## 5. Consequences

Using in-memory storage keeps the current project small and easy to run locally.

It also makes testing easier because we do not need to create or configure a database before running the tests.

However, the application cannot keep task data after the server restarts. If the project becomes a larger or real-world application, the storage approach would need to be changed.

I would do this differently by using SQLite or another database if the application needed to keep task data permanently.

## 6. Open Questions

- At what point would the project need to move from in-memory storage to a database?
- If persistent storage becomes necessary, would SQLite be enough, or would a larger database be more appropriate?
- How would changing the storage layer affect the existing API and tests?
