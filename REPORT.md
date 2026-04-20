# Software Testing Project Report

## 1. Project Overview

This project implements a Python web application for managing career opportunities and job applications. The application was designed specifically to support strong software testing practices. It provides both a browser-based user interface and a REST API, allowing the same business processes to be exercised through multiple testing layers.

The application supports two primary user roles in a simplified way:

- Recruiters can publish career opportunities.
- Applicants can browse openings and submit applications.

## 2. Functional Scope

The implemented functionality includes:

- Creating a new career opportunity
- Listing all published opportunities
- Viewing a single opportunity and its applicants
- Submitting an application for a selected opportunity
- Exposing REST API endpoints for the same core operations
- Validating input and returning helpful errors

## 3. Application Architecture

The project follows a small layered design:

- `validators.py`: Input validation and normalization rules
- `services.py`: Business logic and orchestration
- `repository.py`: SQLite persistence and data access
- `notification.py`: External dependency abstraction for notifications
- Flask routes: HTML and REST API endpoints

This structure improves testability because each layer can be tested independently or combined depending on the test objective.

## 4. Testing Plan

### 4.1 Unit Testing

Purpose:
- Verify isolated logic in validators and services
- Confirm invalid data is rejected correctly
- Confirm business logic calls dependencies with the expected arguments

Implementation:
- `tests/test_unit_validators.py`
- `tests/test_unit_services.py`

Techniques used:
- `unittest.mock.MagicMock` to replace the repository and notification service
- `unittest.mock.patch` to replace the timestamp generator

Examples:
- Checking that opportunity data is trimmed and validated
- Checking that service logic adds timestamps before saving
- Checking that notifications are sent after a successful application
- Checking that missing opportunities raise the correct error

### 4.2 Integration Testing

Purpose:
- Ensure the repository works correctly with the SQLite database
- Validate schema behavior and data flow between stored opportunities and applications

Implementation:
- `tests/test_integration_repository.py`

Examples:
- Saving an opportunity and application, then loading them together
- Verifying ordering of opportunities by creation timestamp

### 4.3 System Testing

Purpose:
- Validate complete end-user workflows through the web interface
- Ensure HTML routes, forms, validation, redirects, and rendered content work together

Implementation:
- `tests/test_system_web.py`

Examples:
- Creating an opportunity through the HTML form
- Applying to the opportunity through the browser workflow
- Confirming validation messages appear for invalid user input

### 4.4 REST API Testing

Purpose:
- Verify endpoint correctness, response codes, JSON structure, and error handling

Implementation:
- `tests/test_api.py`

Examples:
- Health check endpoint
- Create and fetch opportunity endpoints
- Submit application endpoint
- Validation error responses
- Not found responses

## 5. Testing Tools and Frameworks

The following tools were selected:

- Flask:
  Used to build the web application and REST API with minimal overhead.

- `unittest`:
  Python's built-in test framework was chosen because it is reliable, structured, and requires no additional installation in constrained environments.

- `unittest.mock`:
  Used for mocks and patches to isolate dependencies such as the repository, notification service, and timestamp generation.

- SQLite:
  Used for lightweight persistence and fast integration tests.

Justification:
- The selected stack keeps the project simple and stable.
- It allows all required test categories to be implemented clearly.
- It reduces setup complexity while still demonstrating strong testing discipline.

## 6. Mocks and Patches

Mocks and patches were central to the assignment requirements.

Implemented examples:

- Mocked repository in service unit tests so business rules could be tested without touching the database
- Mocked notification service to verify side effects without calling an external provider
- Patched `utcnow_iso()` to make timestamp-dependent tests deterministic and repeatable

Benefits:
- Better isolation
- Faster execution
- Deterministic assertions
- Improved fault localization

## 7. Challenges and Solutions

### Challenge 1: Testing different layers without duplicate responsibility

Solution:
- The application was split into validators, services, repository, and routes so each testing level had a clear purpose.

### Challenge 2: Simulating external dependencies

Solution:
- A dedicated notification abstraction was created and mocked in tests.

### Challenge 3: Keeping tests stable and repeatable

Solution:
- Temporary SQLite databases were used per test case
- Time generation was patched for predictable timestamps

## 8. Test Results Summary

The test suite covers:

- Unit tests for validation and service behavior
- Integration tests for persistence logic
- System tests for browser-style workflows
- REST API tests for endpoint behavior and error cases

Expected outcome:
- All automated tests pass successfully when executed with:

```bash
python -m unittest discover -s tests -v
```

## 9. Conclusion

The project satisfies the assignment goals by delivering:

- A functioning Python web application for career opportunity management
- A REST API for essential operations
- A structured and comprehensive automated test suite
- Practical use of mocks and patches
- Documentation describing the strategy, implementation, and testing outcomes

The final solution demonstrates how thoughtful architecture directly supports reliable software testing across multiple layers of an application.

## 10. Source Code and GitHub Hosting

The complete source code for the web application and test suite is included in this repository. Key project folders and files are:

- `career_app/` — application package with routes, services, validation, persistence, and notifications
- `tests/` — unit, integration, system, and REST API tests
- `run.py` — application entry point
- `README.md` — usage and running instructions
- `requirements.txt` — dependency list
- `REPORT.md` — testing strategy, process, and outcomes documentation

To publish the project on GitHub:

1. Initialize Git (if required):

```bash
git init
```

2. Stage and commit the repository:

```bash
git add .
git commit -m "Initial career opportunity application and tests"
```

3. Create a GitHub repository and push the files. Example using GitHub CLI:

```bash
gh repo create <username>/<repo-name> --public --source=. --remote=origin --push
```

4. Alternatively, create the repository on GitHub.com and push manually:

```bash
git remote add origin https://github.com/<username>/<repo-name>.git
git branch -M main
git push -u origin main
```

Once the code is pushed, the GitHub repository serves as the hosted source for both the application and the test suite.

