# CLI Automatización — Orders Manager

A command-line tool built with **Typer** to manage orders by consuming a REST API. Covers CLI design, environment-based configuration, and maintenance scripts using modern Python.

---

## Requirements

- Python 3.12+
- [Poetry](https://python-poetry.org/)

---

## Installation

```bash
git clone <repo-url>
cd 3.cli_automatizacion
poetry install
```

---

## Configuration

The API base URL is read from an environment variable. No code change is needed to point to a different backend.

| Variable | Default | Description |
|---|---|---|
| `ORDERS_API_URL` | `https://dummyjson.com/carts` | Base URL of the Orders API |

Set it before running any command:

```bash
# Windows PowerShell
$env:ORDERS_API_URL = "https://your-api.com/orders"

# Linux / macOS
export ORDERS_API_URL=https://your-api.com/orders
```

---

## Usage

After installation, the `orders` script is available inside the Poetry environment.

```bash
poetry run orders --help
```

### List all orders

```bash
poetry run orders list
```

### Create an order

```bash
poetry run orders create --user-id 1 --product-id 5 --quantity 2
```

| Option | Short | Required | Description |
|---|---|---|---|
| `--user-id` | `-u` | yes | ID of the user placing the order |
| `--product-id` | `-p` | yes | ID of the product to order |
| `--quantity` | `-q` | no (default 1) | Quantity of the product |

### Delete an order

```bash
poetry run orders delete <ORDER_ID>
```

### Run as a Python module

```bash
poetry run python -m cli_automatizacion --help
```

---

## Project Structure

```
3.cli_automatizacion/
├── pyproject.toml               # Project metadata, dependencies, entry point
├── README.md
├── WIKI.md                      # Conceptual notes: argparse / Click / Typer
├── src/
│   └── cli_automatizacion/
│       ├── __init__.py          # Exposes main() — registered as `orders` script
│       ├── __main__.py          # Enables python -m cli_automatizacion
│       ├── app.py               # Typer app: list / create / delete commands
│       ├── client.py            # HTTP layer (requests): wraps API calls
│       └── config.py            # Reads ORDERS_API_URL from environment
└── tests/
    └── __init__.py
```

---

## Key Concepts

| Concept | Implementation |
|---|---|
| CLI framework | Typer (type-hint-driven, built on Click) |
| Environment config | `os.getenv` in `config.py` |
| HTTP client | `requests` in `client.py` |
| Rich output | `rich.table.Table` for list command |
| Entry point | `[project.scripts]` in `pyproject.toml` |

---

## Dependencies

| Package | Purpose |
|---|---|
| `typer` | CLI commands, options, arguments |
| `requests` | HTTP calls to the Orders API |
| `rich` | Colored output and tables |
