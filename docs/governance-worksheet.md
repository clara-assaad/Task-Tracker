# Governance Retrospective — AI-Assisted Coding

## What I Shared With AI

| Item                                     | Module | Risk Level | Reason                                                                                                    |
| ---------------------------------------- | ------ | ---------- | --------------------------------------------------------------------------------------------------------- |
| Task Tracker code                        | 2-5    | Low        | This is course project code, and no sensitive data, secrets, or credentials were included.                |
| Test output and stack traces             | 2-4    | Medium     | Stack traces can expose internal implementation details, file paths, and error context.                   |
| Frontend code                            | 3      | Low        | The frontend is course project code and does not contain secrets or private data.                         |
| Dockerfile and CI YAML                   | 4      | Medium     | CI and Docker configuration can reveal application architecture, build steps, and deployment assumptions. |
| Any real external data I used by mistake | N/A    | N/A        | No real external, personal, or confidential data was used or shared with AI.                              |

## What I Received From AI

| Generated Thing                        | Module | Do I Understand It Line by Line? | Action                                                                                                                                                           |
| -------------------------------------- | ------ | -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Backend models and validators          | 2      | Yes                              | Reviewed the models, fields, enums, validators, defaults, and validation rules against the project requirements.                                                 |
| Frontend board and drag-and-drop logic | 3      | Mostly                           | Reviewed the generated frontend behavior and verified that it works with the Task Tracker API; complex UI logic should still be rechecked before future changes. |
| CI workflow                            | 4      | Yes                              | Reviewed the workflow steps and verified that it installs the required dependencies and runs the test suite.                                                     |
| Dockerfile                             | 4      | Yes                              | Reviewed the build and runtime stages, dependency installation, non-root user, exposed port, and Uvicorn startup command                                         |
