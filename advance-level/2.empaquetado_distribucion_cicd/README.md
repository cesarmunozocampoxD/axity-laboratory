# empaquetado-distribucion-cicd

A simple FastAPI lab covering Python packaging (wheel), Docker multi-stage builds, and a full GitHub Actions CI/CD pipeline.

---

## Project structure

```
.
├── src/
│   └── empaquetado_distribucion_cicd/
│       ├── __init__.py      # exposes __version__
│       └── main.py          # FastAPI application
├── tests/
│   ├── __init__.py
│   └── test_main.py         # pytest tests (100 % coverage)
├── Dockerfile               # multi-stage build
├── .dockerignore
├── pyproject.toml           # project metadata, deps, tool config
├── .github/
│   └── workflows/
│       └── ci.yml           # CI/CD pipeline
└── README.md
```

---

## Requirements

- Python 3.12+
- [Poetry](https://python-poetry.org/) (dependency manager)
- Docker (optional — for container build)

---

## Installation

```bash
# Clone the repo and enter the project folder
git clone <repo-url>
cd empaquetado-distribucion-cicd

# Install all dependencies (runtime + dev)
poetry install
```

---

## Running the API locally

```bash
poetry run uvicorn empaquetado_distribucion_cicd.main:app --reload
```

The API will be available at `http://localhost:8000`.

### Available endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health-check — returns a welcome message |
| GET | `/items/{item_id}` | Returns `item_id` and optional `name` query param |

**Example:**

```bash
curl http://localhost:8000/
# {"message":"Hello from empaquetado-distribucion-cicd!"}

curl "http://localhost:8000/items/42?name=widget"
# {"item_id":42,"name":"widget"}
```

Interactive docs are auto-generated at `http://localhost:8000/docs`.

---

## Development

### Lint

```bash
poetry run ruff check src/ tests/
```

### Type-check

```bash
poetry run mypy src/
```

### Tests with coverage

```bash
poetry run pytest tests/ --cov=empaquetado_distribucion_cicd --cov-report=term-missing
```

---

## Building the wheel

```bash
poetry run pip install build
poetry run python -m build --wheel --outdir dist/
```

The `.whl` file will appear in `dist/`. Install it anywhere with:

```bash
pip install dist/empaquetado_distribucion_cicd-0.1.0-py3-none-any.whl
```

---

## Docker

### Build the image (multi-stage)

```bash
docker build -t empaquetado-distribucion-cicd:latest .
```

**Stage 1 — builder:** installs the `build` frontend, copies source, and produces the wheel.  
**Stage 2 — runtime:** copies only the `.whl`, installs it, and runs as a non-root user.

### Run the container

```bash
docker run -p 8000:8000 empaquetado-distribucion-cicd:latest
```

---

## CI/CD — GitHub Actions

The workflow at [.github/workflows/ci.yml](.github/workflows/ci.yml) is triggered on every push and pull request to `main`.

```
push / PR to main
    ├── lint        →  ruff check src/ tests/
    ├── type-check  →  mypy src/
    └── test        →  pytest --cov (skips if no test files are present)
```

---

## Dependencies

| Package | Role |
|---------|------|
| `fastapi` | Web framework |
| `uvicorn[standard]` | ASGI server |
| `ruff` *(dev)* | Linter |
| `mypy` *(dev)* | Static type-checker |
| `pytest` + `pytest-cov` *(dev)* | Tests and coverage |
| `httpx` *(dev)* | HTTP client for `TestClient` |
