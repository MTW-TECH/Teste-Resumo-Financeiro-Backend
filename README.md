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
| GET    | `/financial/FinancialSummary/`     | Returns a financial summary   |
| GET    | `/company/list`                    | Returns the list of companies |
| GET    | `/user/<int:user_id>`              | Returns a user by id          |

> Note: the user endpoint uses `/user/<id>` (e.g. `/user/1`) since an id must be supplied to identify which user to fetch.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python run.py
```

The API will be available at `http://localhost:5000`.

## Example requests

```bash
curl http://localhost:5000/financial/FinancialSummary/
curl http://localhost:5000/company/list
curl http://localhost:5000/user/1
```
