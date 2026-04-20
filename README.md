# Career Opportunity Management Web Application

This project is a submission-ready software testing assignment built with Python and Flask. It includes:

- A web interface for posting and applying to career opportunities
- A REST API for core operations
- A layered architecture that supports isolated testing
- A complete `unittest` suite covering unit, integration, system, and API testing

## Important

Do not open files from `career_app/templates` directly in the browser.
Those are Jinja template files, not standalone web pages.

Use one of these instead:

- Run `python run.py`, then open `http://127.0.0.1:5000`
- On Windows, double-click `start_app.bat`

If you open the template files directly with a `file:///...` path, browser buttons and links will fail with messages like "Your file couldn't be accessed".

## Features

- Create career opportunities through HTML and JSON workflows
- View opportunities and submitted applications
- Apply to a role through the web interface or REST API
- Validation and error handling for invalid input
- A notification dependency that is intentionally easy to mock during tests

## Project Structure

```text
career_app/
  __init__.py
  errors.py
  notification.py
  repository.py
  services.py
  validators.py
  templates/
tests/
  helpers.py
  test_api.py
  test_integration_repository.py
  test_system_web.py
  test_unit_services.py
  test_unit_validators.py
run.py
start_app.bat
README.md
REPORT.md
requirements.txt
```

## How to Run

1. Create a virtual environment if desired.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the web application:

```bash
python run.py
```

Or on Windows, double-click `start_app.bat`.

4. Open `http://127.0.0.1:5000`

## How to Run Tests

```bash
python -m unittest discover -s tests -v
```

## Publishing to GitHub

1. Initialize a Git repository if one does not already exist:

```bash
git init
```

2. Add the current project files:

```bash
git add .
```

3. Commit the first version:

```bash
git commit -m "Initial career opportunity web app and test suite"
```

4. Create a GitHub repository and push the code.
   - Option A: Use GitHub CLI:

```bash
gh repo create <username>/<repository-name> --public --source=. --remote=origin --push
```

   - Option B: Use the GitHub website, then run:

```bash
git remote add origin https://github.com/<username>/<repository-name>.git
git branch -M main
git push -u origin main
```

5. Confirm the repository contains:
   - `career_app/`
   - `tests/`
   - `run.py`, `README.md`, `REPORT.md`
   - `requirements.txt`

Once pushed, the repository URL becomes the hosted source for both the web application and test suite.

## REST API Overview

- `GET /api/health`
- `GET /api/opportunities`
- `POST /api/opportunities`
- `GET /api/opportunities/<id>`
- `POST /api/opportunities/<id>/apply`
- `GET /api/opportunities/<id>/applications`

## Testing Strategy Snapshot

- Unit tests isolate validators and service logic
- Integration tests verify repository behavior with SQLite
- System tests exercise the HTML workflow using Flask's test client
- REST API tests validate JSON endpoints, status codes, and error handling
- `unittest.mock` patches time-dependent and external notification behavior
