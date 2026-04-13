# seguridad-mantenimiento

Practical lab covering secure configuration, dependency auditing, and container hardening in Python.

---

## Topics covered

| Topic | Tool / concept |
|---|---|
| Secrets and configuration management | `pydantic-settings`, `SecretStr`, `.env` |
| Dependency vulnerability scanning | `pip-audit`, `safety` |
| Version constraints | PEP 440, `requires-python` upper bound |
| Container hardening | Multi-stage Dockerfile, non-root user |

---

## Project structure

```
.
├── src/
│   └── seguridad_mantenimiento/
│       ├── __init__.py
│       ├── config.py        # pydantic-settings: loads env vars / .env
│       └── app.py           # entry point, uses Settings, never leaks secrets
├── tests/
│   └── test_config.py       # 6 tests: defaults, env override, SecretStr masking
├── Dockerfile               # multi-stage, non-root (appuser UID 1001)
├── .dockerignore
├── .env.example             # safe template — copy to .env, never commit .env
├── .gitignore
├── Makefile                 # convenience targets
└── pyproject.toml
```

---

## .gitignore

The `.gitignore` protects against accidentally committing secrets, build artifacts, and local tooling.

```gitignore
# Secrets and local environment — never commit these
.env
*.env

# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
*.egg-info/
dist/
build/
.eggs/
*.whl

# Virtual environments
.venv/
venv/
env/

# pytest
.pytest_cache/
.coverage
htmlcov/

# mypy / pyright
.mypy_cache/
.dmypy.json

# IDE
.vscode/
.idea/
*.swp
*.swo
```

> The most important entry is `.env` — it prevents real secrets from ever reaching the repository.

---

## Setup

```bash
# Install all dependencies (including dev tools)
poetry install
```

---

## Configuration

Settings are loaded via `pydantic-settings` in this priority order:

1. Real environment variables
2. `.env` file (if present)
3. Default values in `config.py`

Copy the example file and fill in real values:

```bash
cp .env.example .env
```

`.env.example`:

```ini
APP_NAME=seguridad-mantenimiento
DEBUG=false
PORT=8000
DATABASE_URL=sqlite:///./app.db
API_KEY=replace-with-a-strong-random-key
```

> **Important:** `.env` is listed in `.gitignore`. Never commit it.

`API_KEY` is stored as `SecretStr` — its value is **never printed** in logs or tracebacks.  
Access it explicitly only where needed:

```python
cfg.api_key.get_secret_value()
```

---

## Running the app

```bash
poetry run python -m seguridad_mantenimiento.app
```

---

## Tests

```bash
poetry run python -m pytest tests/ -v
```

Expected output:

```
tests/test_config.py::test_default_values_are_applied PASSED
tests/test_config.py::test_settings_overridden_by_environment_variables PASSED
tests/test_config.py::test_api_key_secret_not_exposed_in_repr PASSED
tests/test_config.py::test_api_key_is_accessible_explicitly PASSED
tests/test_config.py::test_get_app_info_returns_expected_keys PASSED
tests/test_config.py::test_get_app_info_does_not_contain_api_key PASSED
6 passed
```

---

## Dependency auditing

### pip-audit (no account required)

```bash
poetry run pip-audit
# or
make audit-pip
```

Scans all installed packages against the PyPI vulnerability database.  
Output: `No known vulnerabilities found` when the environment is clean.

### safety (free account required)

```bash
# First-time setup — register once
poetry run safety auth register

# Then scan
poetry run safety scan
# or
make audit-safety
```

Run both audits at once:

```bash
make audit
```

---

## Container hardening

The `Dockerfile` follows these hardening practices:

- **Multi-stage build** — the build stage compiles the wheel; the runtime stage only installs it. Build tools never ship to production.
- **Minimal base image** — `python:3.12-slim` in both stages.
- **Non-root user** — `appuser` (UID 1001, GID 1001) with `--no-create-home` and `/usr/sbin/nologin`.
- **No secrets baked in** — sensitive values must be injected at deploy time via `-e` or an orchestrator secret manager.
- **`.dockerignore`** — excludes `.env`, tests, docs, and build artifacts from the image context.

### Build

```bash
docker build -t seguridad-mantenimiento:latest .
# or
make docker-build
```

### Run

Pass secrets at runtime, never bake them into the image:

```bash
docker run --rm \
  -e API_KEY=your-real-key \
  -e DATABASE_URL=sqlite:////app/app.db \
  seguridad-mantenimiento:latest
```

### Verify non-root

```bash
make docker-whoami
# docker run --rm --entrypoint id seguridad-mantenimiento:latest
# uid=1001(appuser) gid=1001(appgroup)
```

---

## Makefile targets

| Target | Description |
|---|---|
| `make install` | `poetry install` |
| `make test` | Run pytest |
| `make audit-pip` | Scan with pip-audit |
| `make audit-safety` | Scan with safety |
| `make audit` | Run both audits |
| `make docker-build` | Build the container image |
| `make docker-run` | Run the container locally |
| `make docker-whoami` | Confirm the container runs as non-root |

---

## Key takeaways

1. Keep secrets out of code — use `pydantic-settings` + `SecretStr` + `.env`.
2. Run `pip-audit` (and optionally `safety`) in CI to catch vulnerable dependencies early.
3. Use PEP 440 version bounds (`>=3.12,<4.0`) to keep dependency resolution predictable.
4. Harden containers: multi-stage builds, minimal base images, and a dedicated non-root user.
