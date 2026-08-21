# Financial Flask API

A Flask REST API built with Clean Architecture (Domain, Application, Presentation, Infrastructure layers) and dependency injection via [`dependency-injector`](https://python-dependency-injector.ets-labs.org/).

## Project layout

```
app/
  domain/            # Entities & repository interfaces (no framework dependencies)
    entities/
    repositories/
  application/        # Use cases orchestrating domain logic
    use_cases/
  infrastructure/      # Concrete repository implementations & DI container
    repositories/
    containers.py
  presentation/        # Flask blueprints/controllers (HTTP layer)
    controllers/
config.py
run.py
```

## Endpoints

| Method | Path                              | Description                  |
|--------|------------------------------------|-------------------------------|
| GET    | `/v1/financial/financialSummary/`  | Returns a financial summary   |
| GET    | `/v1/company/list`                 | Returns the list of companies |
| GET    | `/v1/user/me`                      | Returns current user          |
| GET    | `/v1/user/<int:user_id>`           | Returns a user by id          |

> Note: the user endpoint uses `/v1/user/<id>` (e.g. `/v1/user/1`) since an id must be supplied to identify which user to fetch.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Run

```bash
python run.py
```

The API will be available at `http://localhost:5000`.

## Swagger docs (public)

- UI: `http://localhost:5000/v1/docs/`
- OpenAPI JSON: `http://localhost:5000/v1/docs/openapi.json`

The documentation routes are public and are not protected by JWT. Business endpoints still require a bearer token.

## Tests

Use Docker to run tests in a consistent environment.

Start the database service:

```bash
docker compose up -d db
```

Run only endpoint tests (`/company/list`, `/financial/financialSummary/`, `/user/me`):

```bash
docker compose run --rm api sh -lc "pip install --no-cache-dir -r requirements-dev.txt >/tmp/pip-tests.log && pytest -q tests/presentation/controllers/test_protected_endpoints.py"
```

Run endpoint tests with coverage:

```bash
docker compose run --rm api sh -lc "pip install --no-cache-dir -r requirements-dev.txt >/tmp/pip-tests.log && pytest -q --cov=app --cov-report=term-missing tests/presentation/controllers/test_protected_endpoints.py"
```

Run the full test suite with coverage:

```bash
docker compose run --rm api sh -lc "pip install --no-cache-dir -r requirements-dev.txt >/tmp/pip-tests.log && pytest -q --cov=app --cov-report=term-missing"
```

## Example requests

```bash
curl http://localhost:5000/v1/financial/financialSummary/
curl http://localhost:5000/v1/company/list
curl http://localhost:5000/v1/user/1
```
