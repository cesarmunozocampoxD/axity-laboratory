# pruebas_tdd

Lab project that demonstrates **TDD**, **property-based testing**, and **coverage reporting** using `pytest`, `hypothesis`, and `pytest-cov`.

---

## Project structure

```
3.pruebas_tdd/
├── src/
│   └── pruebas_tdd/
│       └── password_validator.py   # Production code
├── tests/
│   ├── conftest.py                 # Shared fixtures
│   ├── test_password_validator.py  # TDD example-based tests
│   └── test_password_properties.py # Hypothesis property-based tests
├── pytest.ini                      # pytest + coverage config
├── .coveragerc                     # Coverage thresholds & options
└── pyproject.toml
```

---

## Requirements

- Python 3.12+
- [Poetry](https://python-poetry.org/)

---

## Setup

```bash
poetry install --with dev
```

---

## Run all tests

```bash
poetry run pytest
```

Runs all tests and prints a branch-coverage report. The build fails if coverage drops below **80 %**.

---

## Run only a subset

```bash
# Unit / example-based tests
poetry run pytest -m unit

# Property-based tests (Hypothesis)
poetry run pytest -m property
```

---

## Generate an HTML coverage report

```bash
poetry run pytest --cov-report=html
```

Open `htmlcov/index.html` in a browser to inspect line-by-line coverage.

---

## What is tested

### `password_validator.py`

| Rule | Minimum |
|---|---|
| Length | ≥ 8 characters |
| Uppercase letter | ≥ 1 |
| Digit | ≥ 1 |

Public API:

- `validate_password(password) -> list[str]` — returns a list of error messages (empty if valid).
- `is_valid(password) -> bool` — returns `True` when there are no errors.

---

## TDD cycle followed

1. **Red** — write a failing test that describes the new behaviour.
2. **Green** — write the minimum code to make the test pass.
3. **Refactor** — clean up without breaking any test.

---
