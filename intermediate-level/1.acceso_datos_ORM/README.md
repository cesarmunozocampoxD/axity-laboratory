# acceso_datos_ORM

SQLAlchemy ORM lab with `User`, `Order`, and `OrderItem` models, Alembic migrations, and pytest tests on SQLite.

## Requirements

- Python 3.12+
- [Poetry](https://python-poetry.org/)

## Setup

```bash
poetry install
```

## Apply migrations

Creates `app.db` with the `users`, `orders`, and `order_items` tables.

```bash
poetry run alembic upgrade head
```

## Run tests

Tests run against an in-memory SQLite database — no `app.db` required.

```bash
poetry run pytest tests/ -v
```

## Project structure

```
src/acceso_datos_orm/
    models.py    # ORM models: User, Order, OrderItem
    database.py  # Engine and SessionLocal factory
    crud.py      # CRUD functions for all three models
alembic/
    env.py       # Alembic environment (points to Base.metadata)
    versions/    # Migration scripts
tests/
    test_crud.py # 31 tests using sqlite:///:memory:
```

## Useful Alembic commands

```bash
# Check current revision applied to app.db
poetry run alembic current

# View migration history
poetry run alembic history

# Roll back one migration
poetry run alembic downgrade -1

# Generate a new migration after changing models
poetry run alembic revision --autogenerate -m "describe change"
```
