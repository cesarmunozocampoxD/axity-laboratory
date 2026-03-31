# Wiki practice

## Poetry

Poetry is a tool for managing dependencies and projects in Python.

📖 **For installation and project build instructions, see [README.md](README.md)**

It allows you to centralize everything in a single workflow:

- Create projects
- Install libraries
- Manage a virtual environment
- Package your project
- Publish packages

## Important Files

### `pyproject.toml`

This is where the project configuration and dependencies go.

### `poetry.lock`

Saves the exact versions installed so the project is reproducible.

## Useful Commands

### Create a new project

```bash
poetry new project_name
```

### Initialize Poetry in an existing folder

```bash
poetry init
```

### Install dependencies

```bash
poetry install
```

### Add a library

```bash
poetry add library_name
```

### Add development dependencies

```bash
poetry add --group dev library_name
```

### Remove a dependency

```bash
poetry remove library_name
```

### Activate or enter the virtual environment

```bash
poetry shell
```

### Run it

```bash
    poetry run python src/entorno_herramientas/main.py
```

## Python Code Standards

### PEP 8 - Style Guide

PEP 8 is the official Python style guide. It defines conventions for writing clean and readable code:

- **Indentation**: 4 spaces per level
- **Line length**: maximum 79 characters (88 for black)
- **Names**: `snake_case` for functions and variables, `PascalCase` for classes
- **Whitespace**: around operators and after commas
- **Imports**: one per line, organized by category (standard library, third-party, local)

[Official PEP 8](https://peps.python.org/pep-0008/)

### PEP 20 - The Zen of Python

PEP 20 (The Zen of Python) is a collection of principles for writing Python code:

```
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Readability counts.
```

View all: `python -c "import this"`

[Official PEP 20](https://peps.python.org/pep-0020/)

### Formatting and Analysis Tools

#### Black - Code Formatter

Black ensures consistent formatting automatically:
- Applies PEP 8 in an opinionated way
- Maximum line length of 88 characters
- Deterministic formatting (always the same result)

```bash
poetry run black src/
```

#### isort - Import Organizer

isort automatically organizes imports:
- Groups by standard library, third-party, and local
- Sorts alphabetically within each group
- Removes duplicate imports

```bash
poetry run isort src/
```

#### Ruff - Fast Linter

Ruff detects errors and style issues:
- Finds common bugs
- Verifies code conventions
- Much faster compared to other linters

```bash
poetry run ruff check src/
poetry run ruff check --fix src/  # Automatically fixes issues
```

### Pre-commit Hooks

The `.pre-commit-config.yaml` file automatically runs these tools before each commit:

```bash
pre-commit install
```

This ensures all committed code complies with the defined standards.