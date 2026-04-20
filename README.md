# Axity Laboratory — Python Course

A hands-on Python course that guides you from environment setup and language fundamentals through intermediate patterns and professional-grade advanced topics.  Each module is a self-contained lab with its own `pyproject.toml`, source code, and test suite managed with [Poetry](https://python-poetry.org/).

---

## Course Structure

```
axity-laboratory/
├── fundamental-level/      # Modules 1–6  — Python basics
├── intermediate-level/     # Modules 1–8  — Intermediate patterns
└── advance-level/          # Modules 1–4  — Advanced architecture & tooling
```

---

## Fundamental Level

### 1. entorno-herramientas — Dev Environment & Tools

Sets up a professional Python project with Poetry, virtual environments, code-quality tools (`black`, `isort`, `ruff`) and pre-commit hooks.

| Key concepts |
|---|
| Poetry project lifecycle (`install`, `build`, `shell`) |
| Pre-commit hooks for automated code quality checks |
| Running tests with `pytest` |

```bash
cd fundamental-level/1.entorno-herramientas
poetry install
poetry run pytest
```

---

### 2. fundamentos-lenguaje — Language Fundamentals

Interactive CLI application that manages a rock-band catalogue stored in a JSON file.  Covers core Python built-ins, collections, file I/O, and basic control flow.

| Key concepts |
|---|
| Built-in types and collections |
| File I/O with `json` |
| Functions, loops, and basic error handling |

```bash
cd fundamental-level/2.fundamentos-lenguaje
poetry install
poetry run python -m fundamentos_lenguaje.main
```

---

### 3. funciones-programacion-pythonic — Functions & Pythonic Programming

Practical exercises on higher-order functions, decorators, generators, and context managers.

| Key concepts |
|---|
| Retry decorator with exponential backoff (`functools.wraps`) |
| `batch_generator` — lazy iteration over large sequences |
| `timer` — context manager using `contextlib.contextmanager` |

```bash
cd fundamental-level/3.funciones-programacion-pythonic
poetry install
poetry run python -m funciones_programacion_pythonic.main
```

---

### 4. objetos_modelos_datos — Objects & Data Models

Domain entities for rock-band merchandise orders using Python's three main data-modelling libraries.

| Key concepts |
|---|
| `@dataclass` — derived fields, `__post_init__`, custom ordering |
| Pydantic v2 — validation, serialization, schemas |
| attrs — immutable value objects |

```bash
cd fundamental-level/4.objetos_modelos_datos
poetry install
poetry run pytest
```

---

### 5. estandar_ES — Standard Library & Ecosystem

Pipeline that reads a rock-bands CSV, computes metrics, and exports results to JSON; demonstrates structured logging at every stage.

| Key concepts |
|---|
| CSV ingestion with `csv.DictReader` + `pathlib` |
| Aggregations with `collections.defaultdict` |
| Logging levels: DEBUG, INFO, WARNING, ERROR |
| JSON export with `json.dump` |

```bash
cd fundamental-level/5.estandar_ES
poetry install
poetry run python -m estandar_es.rock_bands_lab
```

---

### 6. http_apis — HTTP & APIs

Robust `httpx`-based client for the PokéAPI featuring fine-grained timeouts, automatic retry with exponential backoff, and streaming file downloads.

| Key concepts |
|---|
| `httpx.Client` — timeouts, headers, redirects |
| Retry + exponential backoff for transient errors |
| Streaming downloads (`httpx.stream`, chunked writes) |

```bash
cd fundamental-level/6.http_apis
poetry install
poetry run python -m http_apis
```

---

## Intermediate Level

### 1. acceso_datos_ORM — Data Access & ORM

SQLAlchemy ORM lab with `User`, `Order`, and `OrderItem` models, Alembic migration workflow, and a full pytest suite on SQLite.

| Key concepts |
|---|
| SQLAlchemy declarative models and relationships |
| Alembic migrations (`upgrade`, `downgrade`, `autogenerate`) |
| CRUD functions and session management |

```bash
cd intermediate-level/1.acceso_datos_ORM
poetry install
poetry run alembic upgrade head
poetry run pytest tests/ -v
```

---

### 2. apis_fastapi — APIs with FastAPI

FastAPI application with JWT-based authentication using `pydantic-settings` for configuration.

| Key concepts |
|---|
| FastAPI routers, request/response schemas |
| JWT creation and validation (`python-jose`) |
| Password hashing (`passlib`) |
| Environment-based configuration with `pydantic-settings` |

```bash
cd intermediate-level/2.-apis_fastapi
poetry install
# copy and fill in .env values
poetry run uvicorn app.main:app --reload
```

Interactive docs: `http://127.0.0.1:8000/docs`

---

### 3. pruebas_tdd — Testing & TDD

Demonstrates the full TDD cycle and property-based testing on a password validator, with branch-coverage enforcement.

| Key concepts |
|---|
| Red → Green → Refactor cycle |
| `pytest` fixtures and markers |
| Property-based tests with `hypothesis` |
| Coverage reporting and thresholds (`pytest-cov`) |

```bash
cd intermediate-level/3.pruebas_tdd
poetry install --with dev
poetry run pytest          # runs all tests + coverage report
```

---

### 4. concurrencia_rendimiento — Concurrency & Performance

Benchmarks I/O-bound URL fetching (sync vs. `asyncio` + semaphore) and CPU-bound prime counting (sequential vs. `multiprocessing`).

| Key concepts |
|---|
| Python GIL and its effect on threads |
| `asyncio` + `httpx.AsyncClient` with semaphore |
| `multiprocessing.Pool` for CPU-bound tasks |
| Speedup measurement |

```bash
cd intermediate-level/4.concurrencia_rendimiento
poetry install --with dev
poetry run python -m concurrencia_rendimiento.fetcher_lab   # demo
poetry run pytest tests/ -v
```

---

### 5. solid — SOLID Principles

Illustrates all five SOLID principles through a `UserService` / `UserRepository` design, with in-memory and SQLAlchemy adapters.

| Key concepts |
|---|
| Single Responsibility, Open/Closed, Liskov Substitution |
| Interface Segregation, Dependency Inversion |
| Python `Protocol` for structural typing |

```bash
cd intermediate-level/5.solid
poetry install
poetry run pytest tests/ -v
```

---

### 6. patrones — Design Patterns

Three classic GoF patterns applied to a pricing domain, all sharing a common `get_price()` interface so they compose freely.

| Pattern | Module | What it does |
|---|---|---|
| Strategy | `pricing.py` | Swap pricing rules at runtime (`Regular`, `Member`, `Sale`) |
| Decorator | `cache.py` | Wrap any calculator to memoize results |
| Adapter | `provider.py` | Expose a legacy `fetch_price()` service as `get_price()` |

```bash
cd intermediate-level/6.patrones
poetry install
poetry run pytest tests/ -v
```

---

### 7. ciencia_datos — Data Science

End-to-end ML pipeline: load and clean an Iris-like CSV with pandas, train a `DecisionTreeClassifier`, persist it with joblib, and run inference.

| Key concepts |
|---|
| Data cleaning with `pandas` (`dropna`, `reset_index`) |
| Model training with `scikit-learn` |
| Model persistence with `joblib` |
| Prediction pipeline |

```bash
cd intermediate-level/7.ciencia_datos
poetry install
poetry run python -m ciencia_datos.clasificador
poetry run pytest tests/ -v
```

---

### 8. arquitectura_hexagonal — Hexagonal Architecture

Full Ports & Adapters implementation of a `CreateOrder` use case with in-memory and SQLAlchemy repository adapters, an HTTP notification adapter, and contract tests.

| Key concepts |
|---|
| Domain entities with business invariants |
| Ports as `Protocol` classes |
| Adapter swap without touching domain or application code |
| Contract tests: one base class, multiple adapter implementations |

```bash
cd intermediate-level/8.arquitectura_hexagonal
poetry install --with dev
poetry run pytest -v          # 24 tests
```

---

## Advanced Level

### 1. arquitectura-limpia — Clean Architecture

Implements the `CreateOrder` use case following Clean Architecture layers (Domain → Application → Infrastructure) with a Unit of Work pattern and domain events.

| Key concepts |
|---|
| Domain entity records its own `OrderCreated` event |
| Unit of Work: transaction scope, commit, rollback |
| Events dispatched **only after** a successful commit |
| Presenter shapes output independently of the use case |

```bash
cd advance-level/1.arquitectura-limpia
poetry install
poetry run pytest tests/ -v
poetry run uvicorn arquitectura_limpia.infrastructure.http.main:app --reload
```

---

### 2. empaquetado_distribucion_cicd — Packaging, Distribution & CI/CD

FastAPI service demonstrating the complete Python packaging and delivery lifecycle: wheel build, multi-stage Docker image, and a GitHub Actions pipeline.

| Key concepts |
|---|
| Building a Python wheel with `python -m build` |
| Multi-stage `Dockerfile` (builder → runtime) |
| GitHub Actions: lint → type-check → test → build wheel → push to GHCR |

```bash
cd advance-level/2.empaquetado_distribucion_cicd
poetry install
poetry run pytest tests/ --cov=empaquetado_distribucion_cicd
docker build -t empaquetado-distribucion-cicd:latest .
docker run -p 8000:8000 empaquetado-distribucion-cicd:latest
```

---

### 3. cli_automatizacion — CLI & Automation

Command-line orders manager built with **Typer** that consumes a REST API, reads configuration from environment variables, and renders output with **Rich** tables.

| Key concepts |
|---|
| Typer CLI: commands, options, arguments |
| Environment-based configuration with `os.getenv` |
| `requests` HTTP client layer |
| Rich tables for terminal output |

```bash
cd advance-level/3.cli_automatizacion
poetry install
poetry run orders --help
poetry run orders list
poetry run orders create --user-id 1 --product-id 5 --quantity 2
poetry run orders delete <ORDER_ID>
```

---

### 4. seguridad_mantenimiento — Security & Maintenance

Covers secure secrets management, dependency vulnerability scanning, version pinning, and Docker container hardening.

| Key concepts |
|---|
| `pydantic-settings` + `SecretStr` — secrets never leak in logs |
| `pip-audit` and `safety` for dependency auditing |
| PEP 440 version constraints for predictable resolution |
| Multi-stage Dockerfile with a dedicated non-root user |

```bash
cd advance-level/4.seguridad_mantenimiento
poetry install
cp .env.example .env          # fill in real values
poetry run python -m pytest tests/ -v
make audit                    # pip-audit + safety
make docker-build
```

---

## Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/docs/#installation) (dependency and environment manager)
- Docker (optional — required for modules 2 and 4 of the advanced level)

## Quick Start

Each lab is independent. Navigate into its directory, install dependencies, and run the tests:

```bash
cd <level>/<module>
poetry install
poetry run pytest
```

Refer to the `README.md` inside each module for detailed usage instructions.
