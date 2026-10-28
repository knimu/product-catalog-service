# Product Catalogue Microservice

A small Flask REST API for managing products, with SQLAlchemy persistence, pytest tests, and Behave BDD scenarios.

## Requirements

- Python 3.10+
- SQLite (default)
- Flask, Flask-SQLAlchemy, Flask-RESTX, factory-boy, Faker, pytest, coverage, behave, selenium

## Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the service

```bash
export FLASK_APP=service
flask run
```

On Windows PowerShell:
```powershell
$env:FLASK_APP="service"
flask run
```

## Run tests

```bash
pytest
```

BDD tests may require a running app and a browser/driver configured in `features/environment.py`.

## API endpoints

- `GET /products`
- `GET /products/<id>`
- `PUT /products/<id>`
- `DELETE /products/<id>`
- `GET /products?name=...`
- `GET /products?category=...`
- `GET /products?available=true`
- `POST /products` (used for setup/testing)
