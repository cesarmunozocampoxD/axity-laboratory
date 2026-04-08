# entorno-herramientas

A Python project providing tools and environment setup utilities.

📖 **For detailed information about Poetry commands and code standards, see [WIKI.md](WIKI.md)**

## Prerequisites

- Python 3.12 or higher
- Poetry (for dependency management and building)

### Install Poetry

If you don't have Poetry installed, follow the [official installation guide](https://python-poetry.org/docs/#installation).

## Installation

Clone the repository and navigate to the project directory:

```bash
cd entorno-herramientas
```

Install dependencies using Poetry:

```bash
poetry install
```

This will:
- Create a virtual environment
- Install all project dependencies
- Install development tools (black, isort, ruff, pre-commit)

## Building the Project

### Build the Package

To build the distribution packages (wheel and source distribution):

```bash
poetry build
```

Output files will be created in the `dist/` directory.

### Install in Development Mode

To install the package in editable mode for development:

```bash
poetry install
```

Then activate the virtual environment:

```bash
poetry shell
```

## Running the Project

To run the main module:

```bash
poetry run python -m entorno_herramientas.main
```

Or, within the Poetry shell:

```bash
python -m entorno_herramientas.main
```

## Development

### Pre-commit Hooks

Before committing code, install pre-commit hooks to automatically run code quality checks:

```bash
pre-commit install
```

Now, code quality checks will run automatically before each commit. You can also run manually:

```bash
pre-commit run --all-files
```

### Running Tests

```bash
poetry run pytest
```

Or within the Poetry shell:

```bash
pytest
```
