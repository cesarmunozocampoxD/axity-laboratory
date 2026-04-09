# APIs FastAPI

A FastAPI project with JWT authentication.

## Requirements

- Python >= 3.12
- [Poetry](https://python-poetry.org/)

## Installation

```bash
poetry install
```

## Environment Variables

The app reads configuration from a `.env` file in the project root. Create one before running:

```env
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

| Variable                    | Default                    | Description                              |
|-----------------------------|----------------------------|------------------------------------------|
| `SECRET_KEY`                | `132456yhgbfvf324546uyjnb` | Secret used to sign JWT tokens           |
| `ALGORITHM`                 | `HS256`                    | JWT signing algorithm                    |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30`                     | Token lifetime in minutes                |

> **Warning:** Always override `SECRET_KEY` with a strong random value in production.
> Generate one with: `openssl rand -hex 32`

## Running the App

```bash
poetry run uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.  
Interactive docs: `http://127.0.0.1:8000/docs`

## Authentication

The project includes a dummy login endpoint for testing JWT:

```
POST /auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "secret"
}
```

Returns:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

**Dummy users (for development only):**

| Username | Password   |
|----------|------------|
| `admin`  | `secret`   |
| `user`   | `password` |

## Running Tests

```bash
poetry run pytest
```

## Project Structure

```
src/
  apis_fastapi/
    app/
      main.py          # FastAPI application entry point
      core/
        config.py      # Settings (pydantic-settings)
        security.py    # Password hashing & JWT utilities
      routers/
        hello.py       # Example router
        auth.py        # Login endpoint
      schemas/
        token.py       # Token response models
        user.py        # Login request model
tests/
```
