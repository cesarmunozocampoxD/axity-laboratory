# FastAPI APIs: Project Structure, Routers, and Dependencies

## 1. Goal

This guide explains how to organize a **FastAPI** project for APIs, with emphasis on:

- project structure
- routers
- dependencies
- clean separation of responsibilities
- scalability for medium and large projects

---

## 2. Recommended project structure

A clean structure helps when your API grows.

```text
my_fastapi_app/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── api/
│   │   ├── deps.py
│   │   ├── routers/
│   │   │   ├── users.py
│   │   │   ├── items.py
│   │   │   └── auth.py
│   ├── models/
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── item.py
│   │   └── token.py
│   ├── services/
│   │   ├── user_service.py
│   │   └── item_service.py
│   ├── db/
│   │   ├── session.py
│   │   └── base.py
│   └── repositories/
│       ├── user_repository.py
│       └── item_repository.py
├── tests/
│   ├── test_users.py
│   └── test_items.py
├── requirements.txt
└── README.md
```

---

## 3. Responsibility of each folder

### `app/main.py`
Application entry point.  
This is where you create the FastAPI instance and include routers.

### `app/api/routers/`
Contains endpoint groups.  
Each file usually represents one domain or resource:

- `users.py`
- `items.py`
- `auth.py`

### `app/api/deps.py`
Reusable dependencies for the API layer, for example:

- database session
- current authenticated user
- pagination params
- role validation

### `app/schemas/`
Pydantic models for request and response validation.

### `app/models/`
Database models, usually SQLAlchemy models.

### `app/services/`
Business logic.  
This avoids putting too much logic inside route functions.

### `app/repositories/`
Data access layer.  
Used to isolate queries and persistence logic.

### `app/core/`
Shared configuration such as:

- environment variables
- JWT settings
- password hashing
- app constants

### `app/db/`
Database connection, session management, and base metadata.

---

## 4. Minimal example of `main.py`

```python
from fastapi import FastAPI
from app.api.routers import users, items, auth

app = FastAPI(title="My FastAPI API", version="1.0.0")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(items.router, prefix="/items", tags=["Items"])


@app.get("/")
def root():
    return {"message": "API is running"}
```

### Why this is useful
- keeps the entry point small
- makes modules independent
- helps split the API by domain

---

## 5. Routers in FastAPI

FastAPI uses `APIRouter` to modularize endpoints.

### Example: `app/api/routers/users.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user, get_user_by_id
from app.api.deps import get_current_user

router = APIRouter()


@router.post("/", response_model=UserResponse)
def create_user_endpoint(payload: UserCreate):
    return create_user(payload)


@router.get("/{user_id}", response_model=UserResponse)
def get_user_endpoint(user_id: int, current_user=Depends(get_current_user)):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Key idea
A router should mainly handle:

- request input
- response output
- validation flow
- calling the business layer

A router should **not** contain heavy business logic or large SQL queries.

---

## 6. Dependencies in FastAPI

Dependencies are one of FastAPI’s strongest features.

They let you reuse logic such as:

- authentication
- DB session injection
- permission checks
- common query params
- headers
- validation helpers

FastAPI uses `Depends()` for this.

---

## 7. Basic dependency example

### `app/api/deps.py`

```python
from fastapi import Depends, HTTPException, status


def get_current_user():
    # Example only. Normally this would validate a JWT token.
    user = {"id": 1, "username": "janette", "role": "admin"}

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    return user
```

### Using it in a router

```python
from fastapi import APIRouter, Depends

from app.api.deps import get_current_user

router = APIRouter()


@router.get("/me")
def read_me(current_user=Depends(get_current_user)):
    return current_user
```

### Benefit
Instead of repeating auth validation in every route, you centralize it.

---

## 8. Database dependency example

A very common dependency is the database session.

### `app/db/session.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

### `app/api/deps.py`

```python
from app.db.session import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Using it in routes

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db

router = APIRouter()


@router.get("/")
def list_users(db: Session = Depends(get_db)):
    return {"message": "Use db session here"}
```

### Why `yield` is used
Because it allows setup and cleanup:

- open session before request
- close session after request

---

## 9. Layered architecture example

A good API usually separates responsibilities into layers.

### Router layer
Handles HTTP.

```python
@router.post("/")
def create_user_endpoint(payload: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, payload)
```

### Service layer
Handles business rules.

```python
def create_user(db, payload):
    existing = user_repository.get_by_email(db, payload.email)
    if existing:
        raise ValueError("Email already exists")

    return user_repository.create(db, payload)
```

### Repository layer
Handles database access.

```python
def get_by_email(db, email: str):
    return db.query(User).filter(User.email == email).first()
```

### Result
Your code becomes easier to:

- test
- maintain
- reuse
- refactor

---

## 10. Organizing routers by domain

For real APIs, routers should be grouped by business area.

Example:

```text
api/
├── routers/
│   ├── auth.py
│   ├── users.py
│   ├── items.py
│   ├── orders.py
│   └── payments.py
```

This is better than putting all routes into one file.

### Good practice
Use one router file per resource or domain.

Examples:
- `users.py`
- `products.py`
- `orders.py`
- `invoices.py`

---

## 11. Router prefixes and tags

When including routers, you can define prefixes and tags.

```python
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(items.router, prefix="/items", tags=["Items"])
```

### Benefits
- cleaner URL organization
- better Swagger/OpenAPI documentation
- simpler maintenance

Example generated routes:
- `GET /users/`
- `POST /users/`
- `GET /items/`
- `POST /items/`

---

## 12. Router-level dependencies

You can apply dependencies to the whole router.

```python
from fastapi import APIRouter, Depends
from app.api.deps import get_current_user

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/")
def list_users():
    return [{"id": 1, "name": "Janette"}]


@router.get("/{user_id}")
def get_user(user_id: int):
    return {"id": user_id}
```

### Benefit
Every route in that router requires authentication automatically.

This is useful for protected modules like:
- admin routes
- billing routes
- account settings

---

## 13. App-level dependencies

You can also define dependencies globally for the entire application.

```python
from fastapi import FastAPI, Depends

def verify_api_key():
    return True

app = FastAPI(dependencies=[Depends(verify_api_key)])
```

### Use with caution
Global dependencies are powerful, but they can become hard to manage if overused.

Usually:
- route-level dependencies are more explicit
- router-level dependencies are a good middle ground
- app-level dependencies are best for universal checks

---

## 14. Dependency with parameters

Sometimes you need dynamic authorization rules.

### Example

```python
from fastapi import Depends, HTTPException


def require_role(role: str):
    def role_checker(current_user=Depends(get_current_user)):
        if current_user["role"] != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return current_user

    return role_checker
```

### Usage

```python
@router.get("/admin")
def admin_panel(current_user=Depends(require_role("admin"))):
    return {"message": "Welcome, admin"}
```

### Why this is useful
This lets you build reusable permission patterns.

---

## 15. Schemas for request and response

Using Pydantic schemas keeps your API clear and safe.

### `app/schemas/user.py`

```python
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True
```

### Why separate schemas from models
Because database models and API contracts should not always be the same.

Common pattern:
- **models** = persistence
- **schemas** = API validation and serialization

---

## 16. Example of a more complete route

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.user import UserCreate, UserResponse
from app.services import user_service

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return user_service.create_user(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
```

### This route combines
- body validation
- DB injection
- auth dependency
- service delegation
- HTTP error handling

---

## 17. Best practices for FastAPI project structure

### 1. Keep `main.py` small
It should mostly:
- create the app
- include routers
- maybe register middleware or startup events

### 2. Do not put business logic in routes
Routes should stay thin.

### 3. Centralize dependencies
Put reusable dependencies in:
- `api/deps.py`
- `core/security.py`
- `db/session.py`

### 4. Separate schemas from database models
Avoid exposing raw ORM objects directly without proper response schemas.

### 5. Group routes by domain
This scales better than one huge routes file.

### 6. Use services for business rules
This makes your app easier to test.

### 7. Use repositories for complex persistence
Especially useful when queries become large or repeated.

### 8. Keep naming predictable
Examples:
- `user_service.py`
- `user_repository.py`
- `users.py`
- `user.py`

Consistency matters.

---

## 18. Example of scalable folder evolution

### Small project
```text
app/
├── main.py
├── deps.py
├── models.py
└── routes.py
```

### Medium project
```text
app/
├── main.py
├── api/
│   ├── deps.py
│   └── routers/
├── schemas/
├── models/
└── services/
```

### Large project
```text
app/
├── main.py
├── api/
│   ├── deps.py
│   └── routers/
├── core/
├── db/
├── models/
├── schemas/
├── services/
├── repositories/
└── utils/
```

Start simple, but structure early enough to avoid chaos.

---

## 19. Testing impact of good structure

A good structure helps testing a lot.

### Example
You can test:
- routers independently
- services independently
- repositories independently
- dependencies with overrides

FastAPI supports dependency overrides during testing.

```python
app.dependency_overrides[get_db] = override_get_db
```

This is very useful for:
- mock databases
- fake authenticated users
- isolated unit tests

---

## 20. Common mistakes

### 1. Putting everything in `main.py`
This becomes unmaintainable quickly.

### 2. Writing SQL directly in route functions
This mixes HTTP handling with persistence logic.

### 3. Repeating auth logic in every endpoint
Use dependencies instead.

### 4. Returning inconsistent responses
Use response schemas.

### 5. Mixing config, DB logic, and routes in one place
Separate concerns.

### 6. Creating giant utility files
Avoid dumping unrelated helpers into one file.

---

## 21. Suggested starter template

```text
app/
├── main.py
├── api/
│   ├── deps.py
│   └── routers/
│       ├── auth.py
│       ├── users.py
│       └── items.py
├── core/
│   ├── config.py
│   └── security.py
├── db/
│   └── session.py
├── models/
│   ├── user.py
│   └── item.py
├── schemas/
│   ├── user.py
│   └── item.py
└── services/
    ├── user_service.py
    └── item_service.py
```

This structure is a strong starting point for most FastAPI APIs.

---

## 22. Final recommendation

For FastAPI APIs, a practical mental model is:

- **routers** handle HTTP
- **dependencies** inject reusable request logic
- **services** contain business rules
- **repositories** handle persistence
- **schemas** define API contracts
- **models** define database structure

That separation gives you a codebase that is easier to scale, debug, and test.

---

## 23. Quick summary

If you only remember the essentials, keep these:

1. Use `APIRouter` to split endpoints by domain.
2. Use `Depends()` for authentication, DB sessions, and reusable validations.
3. Keep routes thin and move business logic into services.
4. Separate schemas, models, and persistence logic.
5. Make the project structure predictable from the beginning.

---
# FastAPI: Pydantic Schemas, Validation, and OpenAPI

## 1. Goal

This guide explains three core concepts in **FastAPI**:

- **Pydantic schemas**
- **data validation**
- **OpenAPI documentation**

These three work together and are one of the main reasons FastAPI is so productive for API development.

---

## 2. What are Pydantic schemas?

In FastAPI, **Pydantic schemas** are Python classes used to define:

- request body structure
- response body structure
- validation rules
- data serialization and transformation

FastAPI uses Pydantic to make sure incoming and outgoing data matches the structure you expect.

---

## 3. Why schemas matter

Schemas help you:

- validate data automatically
- reject invalid requests early
- document your API clearly
- avoid inconsistent payloads
- improve editor support and type safety

Without schemas, your API becomes harder to maintain and easier to break.

---

## 4. Basic schema example

```python
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
```

### What this does
This schema says that the request must contain:

- `username` as a string
- `email` as a valid email
- `password` as a string

If the client sends invalid data, FastAPI returns a validation error automatically.

---

## 5. Using schemas in FastAPI routes

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


@app.post("/users")
def create_user(payload: UserCreate):
    return {"message": "User created", "data": payload}
```

### What happens here
- FastAPI reads the request body
- converts JSON into a `UserCreate` object
- validates it
- if valid, passes it to the route
- if invalid, returns a `422 Unprocessable Entity`

---

## 6. Example of validation failure

If the client sends this:

```json
{
  "username": "janette",
  "email": "not-an-email",
  "password": "123456"
}
```

FastAPI will reject it because `email` is not valid.

Typical response:

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

This happens automatically, without writing custom validation code for the route.

---

## 7. Common field types in Pydantic

Pydantic supports many useful field types.

```python
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int
    active: bool
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    seller_email: EmailStr
```

### Notes
- `Optional[str] = None` means the field is not required
- `EmailStr` validates emails
- `datetime` parses ISO datetime strings automatically

---

## 8. Field constraints with `Field`

You can define validation rules more precisely with `Field`.

```python
from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
```

### Meaning
- `...` means the field is required
- `min_length=3` means at least 3 characters
- `max_length=100` means at most 100 characters
- `gt=0` means greater than 0
- `ge=0` means greater than or equal to 0

---

## 9. Example with metadata for docs

`Field` is also useful for OpenAPI documentation.

```python
from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=3, example="Mechanical Keyboard")
    price: float = Field(..., gt=0, example=1499.99)
    stock: int = Field(..., ge=0, example=10)
```

### Benefit
These examples appear in the generated Swagger UI docs.

---

## 10. Response schemas

Schemas are not only for incoming data.  
They should also be used for outgoing data.

```python
from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
```

### Why this matters
Response schemas:
- keep API responses consistent
- hide internal fields
- improve docs
- make refactoring safer

---

## 11. Request schema vs response schema

A common pattern is to separate input and output schemas.

```python
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
```

### Why separate them?
Because the API should accept a password during creation, but should not return it in the response.

This is a very important design principle.

---

## 12. Using `response_model` in FastAPI

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    return {
        "id": user_id,
        "username": "janette",
        "email": "janette@example.com",
        "password": "hidden"
    }
```

### What FastAPI does
Even if the route returns extra fields like `password`, FastAPI filters the response to match `UserResponse`.

The client only receives:

```json
{
  "id": 1,
  "username": "janette",
  "email": "janette@example.com"
}
```

---

## 13. Nested schemas

Schemas can contain other schemas.

```python
from pydantic import BaseModel, EmailStr


class Address(BaseModel):
    street: str
    city: str
    zip_code: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    address: Address
```

### Example request

```json
{
  "username": "janette",
  "email": "janette@example.com",
  "address": {
    "street": "Main St",
    "city": "CDMX",
    "zip_code": "01000"
  }
}
```

FastAPI validates the nested object too.

---

## 14. Lists and collections

```python
from pydantic import BaseModel
from typing import List


class TagList(BaseModel):
    tags: List[str]
```

### Example request

```json
{
  "tags": ["python", "fastapi", "backend"]
}
```

You can also combine nested models and lists.

```python
from typing import List
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float


class Order(BaseModel):
    items: List[Item]
```

---

## 15. Optional fields

```python
from typing import Optional
from pydantic import BaseModel


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
```

### Why useful
This is common for `PATCH` or partial update endpoints, where not every field must be sent.

---

## 16. Custom validation

Pydantic allows custom validation logic.

## Pydantic v2 style example

```python
from pydantic import BaseModel, field_validator


class UserCreate(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def username_must_not_have_spaces(cls, value: str) -> str:
        if " " in value:
            raise ValueError("Username must not contain spaces")
        return value
```

### What this does
If `username` contains spaces, validation fails before the route logic runs.

---

## 17. Another custom validation example

```python
from pydantic import BaseModel, field_validator


class ProductCreate(BaseModel):
    name: str
    price: float

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty")
        return value
```

### Important
Validation can also be used to normalize data, not only reject it.

---

## 18. Model configuration

In many projects, response schemas are built from ORM objects.

### Pydantic v2 example

```python
from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    model_config = {
        "from_attributes": True
    }
```

### Why this matters
This allows Pydantic to read attributes from ORM objects like SQLAlchemy models.

---

## 19. Schema inheritance

You can reuse base fields through inheritance.

```python
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
```

### Benefit
This avoids repeating shared fields across multiple schemas.

---

## 20. Validation of query parameters

FastAPI also validates query parameters.

```python
from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/search")
def search_items(
    q: str = Query(..., min_length=2, max_length=50),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    return {"q": q, "page": page, "limit": limit}
```

### What this does
- `q` is required
- `q` must be between 2 and 50 characters
- `page` must be at least 1
- `limit` must be between 1 and 100

---

## 21. Validation of path parameters

```python
from fastapi import FastAPI, Path

app = FastAPI()


@app.get("/users/{user_id}")
def get_user(user_id: int = Path(..., ge=1)):
    return {"user_id": user_id}
```

### Meaning
The path parameter must be an integer and at least 1.

---

## 22. Validation of headers

```python
from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/secure")
def secure_endpoint(x_token: str = Header(...)):
    return {"token_received": x_token}
```

You can validate headers the same way FastAPI validates other input sources.

---

## 23. Validation error behavior in FastAPI

When validation fails, FastAPI automatically returns:

- HTTP status `422`
- structured error details
- exact field location
- reason for the failure

This makes debugging much easier for both backend and frontend developers.

---

## 24. What is OpenAPI?

**OpenAPI** is a standard format for describing REST APIs.

It defines things like:

- endpoints
- methods
- parameters
- request bodies
- response models
- authentication schemes
- examples

FastAPI generates this automatically from your code.

---

## 25. Why OpenAPI is important

OpenAPI gives you:

- interactive documentation
- machine-readable API spec
- better frontend/backend collaboration
- easier testing
- potential client SDK generation

FastAPI automatically exposes this documentation.

---

## 26. Swagger UI and ReDoc in FastAPI

By default, FastAPI provides:

- **Swagger UI** at `/docs`
- **ReDoc** at `/redoc`
- raw OpenAPI schema at `/openapi.json`

These are generated automatically from:
- routes
- parameters
- Pydantic schemas
- type hints
- metadata

---

## 27. How Pydantic and OpenAPI connect

Pydantic schemas are a key source for OpenAPI generation.

For example:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float


@app.post("/items", response_model=Item)
def create_item(item: Item):
    return item
```

FastAPI uses this to document:
- the request body shape
- the response body shape
- field types
- validation rules

---

## 28. Improving docs with metadata

You can customize the app metadata.

```python
from fastapi import FastAPI

app = FastAPI(
    title="Store API",
    description="API for managing products, orders, and users",
    version="1.0.0"
)
```

This appears in `/docs` and `/redoc`.

---

## 29. Documenting route metadata

You can also add metadata to routes.

```python
@app.post(
    "/users",
    summary="Create a new user",
    description="Creates a new user account in the system",
    response_description="The created user"
)
def create_user(payload: UserCreate):
    return payload
```

### Benefit
This makes the generated documentation much more readable.

---

## 30. Tags for grouping endpoints

```python
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])
```

### Why useful
In Swagger UI, endpoints are grouped by tags, which makes the docs easier to navigate.

---

## 31. Examples in schemas and docs

You can define examples for better documentation.

```python
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(..., example="janette")
    email: str = Field(..., example="janette@example.com")
    password: str = Field(..., example="supersecret123")
```

These examples help consumers understand the expected payload quickly.

---

## 32. Multiple response documentation

FastAPI can also document different possible responses.

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get(
    "/users/{user_id}",
    responses={
        404: {"description": "User not found"},
        200: {"description": "Successful response"}
    }
)
def get_user(user_id: int):
    if user_id != 1:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": 1, "username": "janette"}
```

This improves the generated OpenAPI schema.

---

## 33. Schema-driven API design

A strong FastAPI pattern is:

1. define schemas first
2. define route signatures with type hints
3. let FastAPI generate validation and docs automatically

This leads to a very expressive API design style.

---

## 34. Common schema categories in real projects

A typical project may use schemas like:

- `UserCreate`
- `UserUpdate`
- `UserResponse`
- `LoginRequest`
- `TokenResponse`
- `ItemCreate`
- `ItemUpdate`
- `ItemResponse`

### Why this naming works
It clearly communicates the purpose of each schema.

---

## 35. Good practices

### 1. Separate request and response schemas
Do not reuse one schema for everything.

### 2. Use precise types
Prefer `EmailStr`, `datetime`, `int`, `float`, `bool`, etc.

### 3. Add field constraints
Use `Field()` and validation rules when appropriate.

### 4. Keep route functions thin
Let schemas validate input before business logic runs.

### 5. Use examples and metadata
This improves OpenAPI docs a lot.

### 6. Reuse base schemas
Use inheritance for repeated fields.

### 7. Avoid exposing internal DB models directly
Use response schemas as the API contract.

---

## 36. Common mistakes

### 1. Returning passwords or internal fields
Always use response schemas to control output.

### 2. Using one schema for create, update, and response
These usually have different requirements.

### 3. Skipping validation rules
This makes bugs reach deeper layers of the app.

### 4. Ignoring OpenAPI docs
FastAPI gives excellent docs almost for free. Use them.

### 5. Writing too much manual validation in routes
Prefer schema-level or parameter-level validation.

---

## 37. Practical mental model

A useful mental model is:

- **Pydantic schemas** define data contracts
- **validation** protects the API boundary
- **OpenAPI** documents those contracts automatically

So in FastAPI:

- the schema is not just validation
- it is also documentation
- and also part of your API design

---

## 38. Final recommendation

When building FastAPI APIs:

- define clean schemas first
- keep request and response models separate
- use built-in validation as much as possible
- enrich schemas with examples and constraints
- rely on generated OpenAPI docs to make the API easier to use

This is one of the main strengths of FastAPI and one of the best habits to build early.

---

## 39. Quick summary

If you only keep the essentials:

1. Pydantic schemas define the shape of input and output.
2. FastAPI validates requests automatically using those schemas.
3. Invalid data returns `422` with detailed errors.
4. FastAPI generates OpenAPI docs from routes, type hints, and schemas.
5. Good schemas make your API safer, cleaner, and easier to consume.

---

# FastAPI: JWT Authentication, Middleware, and CORS

## 1. Goal

This guide explains three important concepts for building real APIs with **FastAPI**:

- **JWT authentication**
- **middlewares**
- **CORS**

These are common in production APIs because they affect security, request processing, and frontend integration.

---

## 2. JWT Authentication

## What is JWT?

**JWT** stands for **JSON Web Token**.

It is a compact token format commonly used for authentication between a client and an API.

A JWT usually contains:

- a **header**
- a **payload**
- a **signature**

Example shape:

```text
xxxxx.yyyyy.zzzzz
```

### Why JWT is used
After a user logs in, the API can generate a token and return it to the client.  
Then the client sends that token on future requests, usually in the `Authorization` header.

Example:

```http
Authorization: Bearer <token>
```

This lets the API identify the user without storing session state on the server in the traditional way.

---

## 3. Common JWT flow

A common flow looks like this:

1. the user sends email/username and password
2. the API verifies the credentials
3. the API creates a JWT token
4. the client stores the token
5. the client sends the token in protected requests
6. the API validates the token and allows or denies access

---

## 4. JWT payload concepts

The payload often contains claims such as:

- `sub` → subject, usually the user identifier
- `exp` → expiration time
- `iat` → issued at
- `role` → user role, if needed

Example payload:

```json
{
  "sub": "123",
  "role": "admin",
  "exp": 1760000000
}
```

### Important
Do not put sensitive raw information inside the token unless you fully understand the risk.  
JWT payloads are encoded, not encrypted by default.

---

## 5. JWT in FastAPI

A common FastAPI setup uses:

- `python-jose` or another JWT library
- `passlib` for password hashing
- `OAuth2PasswordBearer` for bearer token extraction
- dependencies with `Depends()` for protected routes

---

### Why separate them
- `Token` defines what the login endpoint returns
- `TokenData` defines what you expect after decoding the JWT

---

## 8. Password hashing

Passwords must never be stored in plain text.

A typical helper module in `core/security.py`:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
```

### Why hashing matters
If your database is exposed, hashed passwords are far safer than plain-text passwords.

---

## 9. Creating JWT tokens

Example with `python-jose`:

```python
from datetime import datetime, timedelta, timezone
from jose import jwt

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

### Key idea
The token is signed with:
- a secret key
- an algorithm
- an expiration time

---

## 10. Decoding and validating JWT

```python
from jose import JWTError, jwt

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"


def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
```

### Important
Decoding alone is not enough.  
You should also verify:
- expiration
- subject existence
- user existence in database
- token status, if your design supports revocation

---

## 11. Extracting bearer tokens

FastAPI provides `OAuth2PasswordBearer` for bearer token extraction.

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
```

### What this does
It tells FastAPI:
- the app expects bearer tokens
- the token comes from the `Authorization` header
- the login endpoint is `/auth/login`

---

## 12. Creating a current-user dependency

A common dependency in `api/deps.py`:

```python
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Example only. Usually here you query the database.
    user = {"id": user_id, "username": "janette"}
    if user is None:
        raise credentials_exception

    return user
```

### Benefit
This dependency can be reused in any protected endpoint.

---

## 13. Protecting routes

```python
from fastapi import APIRouter, Depends
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/me")
def read_me(current_user=Depends(get_current_user)):
    return current_user
```

### Result
Only requests with a valid bearer token can access this route.

---

## 14. Login endpoint example

```python
from fastapi import APIRouter, HTTPException, status
from app.core.security import verify_password, create_access_token
from app.schemas.token import Token

router = APIRouter()


@router.post("/login", response_model=Token)
def login(username: str, password: str):
    # Example only. Normally validate against database.
    fake_user = {
        "id": 1,
        "username": "janette",
        "hashed_password": "$2b$12$example"
    }

    if username != fake_user["username"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    # Replace with actual verification logic
    access_token = create_access_token(data={"sub": str(fake_user["id"])})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
```

### Note
In real projects, login usually uses:
- a DB lookup
- hash verification
- proper form or JSON schema input

---

## 15. Role-based authorization

JWT can also support role-based access.

Example:

```python
from fastapi import Depends, HTTPException

def require_role(role: str):
    def checker(current_user=Depends(get_current_user)):
        if current_user.get("role") != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return current_user

    return checker
```

Usage:

```python
@router.get("/admin")
def admin_only(current_user=Depends(require_role("admin"))):
    return {"message": "Admin access granted"}
```

### Important distinction
- **authentication** = who are you?
- **authorization** = what are you allowed to do?

---

## 16. JWT good practices

### 1. Use a strong secret key
Never use weak or predictable secrets.

### 2. Keep secrets outside the code
Use environment variables or configuration management.

### 3. Set token expiration
Never create non-expiring access tokens.

### 4. Hash passwords properly
Use secure password hashing algorithms such as bcrypt.

### 5. Return proper 401 responses
Use `WWW-Authenticate: Bearer` when appropriate.

### 6. Keep payload minimal
Do not store unnecessary or sensitive data inside the token.

### 7. Consider refresh tokens
For real systems, refresh token flows are often needed.

---

## 17. Middleware in FastAPI

## What is middleware?

A **middleware** is code that runs **before and/or after** a request reaches your route handler.

It sits in the request-response pipeline.

Common middleware use cases:

- logging
- timing requests
- adding headers
- request tracing
- security checks
- centralized processing

---

## 18. How middleware works conceptually

Flow:

1. request arrives
2. middleware intercepts it
3. middleware may inspect or modify the request
4. route handler executes
5. middleware may inspect or modify the response
6. response is returned

This makes middleware ideal for cross-cutting concerns.

---

## 19. Basic custom middleware example

```python
from fastapi import FastAPI, Request
import time

app = FastAPI()


@app.middleware("http")
async def log_process_time(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    return response
```

### What this does
- measures how long the request took
- adds the result to the response headers

---

## 20. Why middleware is useful

Middleware is ideal when the same behavior should apply to many endpoints.

Examples:
- logging every request
- attaching correlation IDs
- adding security headers
- auditing traffic
- measuring latency

Without middleware, you would repeat the same logic in many routes.

---

## 21. Middleware vs dependencies

They are related, but they are not the same.

### Middleware
- runs globally in the request pipeline
- can act before and after route execution
- is good for request/response-level concerns

### Dependencies
- are more route-oriented
- inject values or validations into endpoints
- are good for auth, DB sessions, and reusable route logic

### Rule of thumb
- use **middleware** for cross-cutting HTTP concerns
- use **dependencies** for route-level business and access logic

---

## 22. Example use cases for middleware

### Logging middleware
Track method, URL, status code, duration.

### Correlation ID middleware
Attach a request ID for tracing logs across systems.

### Security headers middleware
Add headers like:
- `X-Content-Type-Options`
- `X-Frame-Options`
- `Strict-Transport-Security`

### Localization middleware
Read headers and determine locale preferences.

---

## 23. Middleware ordering

If you use multiple middlewares, order matters.

Why?
Because request and response flow passes through them in sequence.

That means:
- the order of registration affects behavior
- one middleware may depend on headers or changes made by another

Be deliberate about the order.

---

## 24. Example of adding headers in middleware

```python
from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def add_custom_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-App-Name"] = "My FastAPI API"
    return response
```

---

## 25. Middleware file organization

A clean project may store middleware in a dedicated module.

Example:

```text
app/
├── core/
│   └── middleware.py
└── main.py
```

Example helper:

```python
from fastapi import Request


async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response
```

Then in `main.py`:

```python
from fastapi import FastAPI
from app.core.middleware import add_security_headers

app = FastAPI()
app.middleware("http")(add_security_headers)
```

---

## 26. CORS

## What is CORS?

**CORS** stands for **Cross-Origin Resource Sharing**.

It is a browser security mechanism that controls whether a frontend from one origin can access resources from another origin.

An **origin** is defined by:
- scheme
- host
- port

Examples:
- `http://localhost:3000`
- `http://localhost:8000`

These are different origins because the ports are different.

---

## 27. Why CORS matters in APIs

A very common scenario:

- frontend runs on `http://localhost:3000`
- backend API runs on `http://localhost:8000`

From the browser’s perspective, that is cross-origin.  
Without proper CORS configuration, the browser blocks the frontend request.

Important: this is enforced by browsers, not by your backend language itself.

---

## 28. FastAPI CORS middleware

FastAPI commonly uses `CORSMiddleware`.

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://myfrontend.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### What this does
It allows the listed frontend origins to call the API.

---

## 29. Meaning of CORS options

### `allow_origins`
Which origins are allowed.

### `allow_credentials`
Whether cookies, authorization headers, or TLS client certs are allowed.

### `allow_methods`
Which HTTP methods are allowed, such as:
- `GET`
- `POST`
- `PUT`
- `DELETE`

### `allow_headers`
Which request headers are allowed.

---

## 30. CORS example for local development

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Why both may be needed
`localhost` and `127.0.0.1` are not always treated as the same origin.

---

## 31. CORS and JWT together

If your frontend sends JWT tokens in the `Authorization` header, CORS configuration becomes especially important.

Why?
Because the browser may block requests unless the backend allows the origin and relevant headers.

A common setup:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

This often works for SPA frontends that call protected FastAPI endpoints.

---

## 32. Preflight requests

For some cross-origin requests, browsers send a **preflight request** first using `OPTIONS`.

This happens especially when:
- custom headers are used
- methods like `PUT`, `PATCH`, or `DELETE` are used
- credentials are involved

The backend must respond correctly for the actual request to proceed.

`CORSMiddleware` handles this automatically in common FastAPI setups.

---

## 33. CORS good practices

### 1. Avoid `allow_origins=["*"]` in production
It is too permissive for many real systems.

### 2. Explicitly list trusted frontend origins
This is safer and clearer.

### 3. Review `allow_credentials=True`
Use it only when needed.

### 4. Match real frontend environments
Include correct:
- dev origin
- staging origin
- production origin

### 5. Test with the actual frontend
CORS issues are browser behavior, so frontend testing matters.

---

## 34. Common JWT + middleware + CORS setup in `main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import auth, users

app = FastAPI(title="Secure API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://myfrontend.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request, call_next):
    response = await call_next(request)
    response.headers["X-App-Version"] = "1.0.0"
    return response


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
```

This gives you:
- CORS support
- custom middleware
- router organization

---

## 35. How the three concepts connect

These three concepts are often used together in real APIs:

### JWT authentication
Protects endpoints and identifies the user.

### Middleware
Applies shared request/response behavior.

### CORS
Allows frontend applications from trusted origins to communicate with the API.

Example real scenario:
- React frontend on port 3000
- FastAPI backend on port 8000
- user logs in and gets a JWT
- frontend sends `Authorization: Bearer <token>`
- backend validates token through dependency
- CORS allows the browser request
- middleware logs request timing and adds headers

---

## 36. Common mistakes

### JWT mistakes
- storing plain passwords
- using weak secret keys
- not setting expiration
- trusting token payload without verification
- returning vague auth behavior

### Middleware mistakes
- putting business logic in middleware
- using middleware when a dependency would be better
- ignoring execution order

### CORS mistakes
- allowing every origin in production
- forgetting frontend dev origins
- misconfiguring credentials
- debugging backend logic when the browser is actually blocking the call

---

## 37. Practical mental model

A useful mental model is:

- **JWT** answers: who is making the request?
- **middleware** answers: what should happen for every request or response?
- **CORS** answers: can this browser frontend call the API from this origin?

That distinction makes architecture decisions much clearer.

---

## 38. Final recommendation

For most FastAPI APIs:

- implement JWT auth through a dedicated security module
- use dependencies for protected routes and current-user resolution
- use middleware for shared HTTP concerns like timing, logging, and headers
- configure CORS explicitly for your real frontend origins

This structure is clean, scalable, and practical for production-oriented projects.

---

## 39. Quick summary

If you only keep the essentials:

1. JWT is used to authenticate users through signed tokens.
2. FastAPI commonly protects routes using bearer token dependencies.
3. Middleware runs around the request-response cycle.
4. CORS allows browser frontends from other origins to call your API.
5. In real APIs, these three usually work together.

---


# Testing API Endpoints with `pytest` + `aiohttp`

## 1. Goal

This guide explains how to test API endpoints using:

- **pytest**
- **aiohttp**
- async test patterns
- assertions for status codes, payloads, and error handling

It is focused on practical testing for Python APIs, especially when working with asynchronous HTTP calls.

---

## 2. What each tool does

### `pytest`
`pytest` is the test runner.  
It helps you write, organize, and execute tests clearly.

### `aiohttp`
`aiohttp` is an asynchronous HTTP library for Python.  
It can be used for:
- building async web apps
- making async HTTP requests
- testing async endpoints and integrations

### Typical use case
You may use `pytest` to run tests and `aiohttp` to:
- create a test client
- call async endpoints
- validate responses

---

## 3. Common scenarios for endpoint testing

You usually want to test things like:

- successful requests
- invalid payloads
- missing fields
- unauthorized access
- not found responses
- server-side errors
- response structure
- headers
- query parameters

The goal is to verify that the API behaves correctly from the client perspective.

---

## 4. Typical project structure

```text
project/
├── app/
│   ├── main.py
│   ├── routes.py
│   └── services/
├── tests/
│   ├── conftest.py
│   ├── test_users.py
│   └── test_items.py
├── requirements.txt
└── pytest.ini
```

### Why this helps
- application code stays separate from test code
- shared fixtures can live in `conftest.py`
- endpoint tests stay organized by domain

---

## 5. Useful packages

A common setup may include:

```text
pytest
pytest-asyncio
aiohttp
aiohttp-devtools
```

In many cases, you will also use:

```text
pytest-cov
```

for test coverage.

---

## 6. Why async testing matters

If your app or client is asynchronous, your tests should respect that execution model.

Why?
Because:
- endpoint handlers may be `async`
- HTTP clients may be async
- database or service calls may be async
- waiting incorrectly can cause false positives or broken tests

---

## 7. Basic async test with `pytest`

For async tests, `pytest` commonly works with `pytest-asyncio`.

```python
import pytest


@pytest.mark.asyncio
async def test_basic_async():
    result = 1 + 1
    assert result == 2
```

### What this does
It tells `pytest` that the test function is asynchronous and must be awaited properly.

---

## 8. Testing with `aiohttp` test utilities

`aiohttp` provides testing helpers such as:
- test client
- test server
- fixtures and utilities for async apps

A typical import pattern is:

```python
from aiohttp import web
```

and for tests you may use helpers from:

```python
from aiohttp.test_utils import TestClient, TestServer
```

---

## 9. Minimal `aiohttp` application example

```python
from aiohttp import web


async def health(request):
    return web.json_response({"status": "ok"})


def create_app():
    app = web.Application()
    app.router.add_get("/health", health)
    return app
```

This gives us a simple endpoint to test.

---

## 10. Basic endpoint test example

```python
import pytest
from aiohttp.test_utils import TestClient, TestServer
from app.main import create_app


@pytest.mark.asyncio
async def test_health_endpoint():
    app = create_app()
    server = TestServer(app)
    client = TestClient(server)

    await client.start_server()

    resp = await client.get("/health")
    data = await resp.json()

    assert resp.status == 200
    assert data == {"status": "ok"}

    await client.close()
```

### What this validates
- the endpoint exists
- it returns HTTP 200
- the JSON body matches the expected output

---

## 11. Better approach with fixtures

Instead of repeating setup in every test, use fixtures.

### Example `conftest.py`

```python
import pytest
from aiohttp.test_utils import TestClient, TestServer
from app.main import create_app


@pytest.fixture
async def client():
    app = create_app()
    server = TestServer(app)
    client = TestClient(server)

    await client.start_server()
    yield client
    await client.close()
```

### Example test file

```python
import pytest


@pytest.mark.asyncio
async def test_health_endpoint(client):
    resp = await client.get("/health")
    data = await resp.json()

    assert resp.status == 200
    assert data["status"] == "ok"
```

### Benefit
This makes tests cleaner and reduces duplication.

---

## 12. Testing POST endpoints

Suppose you have this endpoint:

```python
from aiohttp import web


async def create_user(request):
    payload = await request.json()

    if "username" not in payload:
        return web.json_response(
            {"detail": "username is required"},
            status=400
        )

    return web.json_response(
        {"id": 1, "username": payload["username"]},
        status=201
    )
```

### Test for success

```python
import pytest


@pytest.mark.asyncio
async def test_create_user_success(client):
    payload = {"username": "janette"}

    resp = await client.post("/users", json=payload)
    data = await resp.json()

    assert resp.status == 201
    assert data["id"] == 1
    assert data["username"] == "janette"
```

---

## 13. Testing invalid payloads

```python
import pytest


@pytest.mark.asyncio
async def test_create_user_missing_username(client):
    payload = {}

    resp = await client.post("/users", json=payload)
    data = await resp.json()

    assert resp.status == 400
    assert data["detail"] == "username is required"
```

### Why this matters
Testing only happy paths is not enough.  
APIs must also fail correctly.

---

## 14. Testing query parameters

Suppose the endpoint is:

```python
from aiohttp import web


async def search(request):
    q = request.query.get("q", "")
    return web.json_response({"query": q})
```

### Test example

```python
import pytest


@pytest.mark.asyncio
async def test_search_query_param(client):
    resp = await client.get("/search?q=python")
    data = await resp.json()

    assert resp.status == 200
    assert data["query"] == "python"
```

---

## 15. Testing path parameters

Suppose the endpoint is:

```python
from aiohttp import web


async def get_user(request):
    user_id = request.match_info["user_id"]
    return web.json_response({"user_id": int(user_id)})
```

### Test example

```python
import pytest


@pytest.mark.asyncio
async def test_get_user_by_id(client):
    resp = await client.get("/users/10")
    data = await resp.json()

    assert resp.status == 200
    assert data["user_id"] == 10
```

---

## 16. Testing headers

Some endpoints depend on headers such as authorization or custom tracing headers.

### Example endpoint

```python
from aiohttp import web


async def secure_data(request):
    token = request.headers.get("Authorization")

    if token != "Bearer valid-token":
        return web.json_response({"detail": "Unauthorized"}, status=401)

    return web.json_response({"message": "Authorized"})
```

### Test example

```python
import pytest


@pytest.mark.asyncio
async def test_secure_data_authorized(client):
    resp = await client.get(
        "/secure",
        headers={"Authorization": "Bearer valid-token"}
    )
    data = await resp.json()

    assert resp.status == 200
    assert data["message"] == "Authorized"
```

### Unauthorized case

```python
import pytest


@pytest.mark.asyncio
async def test_secure_data_unauthorized(client):
    resp = await client.get("/secure")
    data = await resp.json()

    assert resp.status == 401
    assert data["detail"] == "Unauthorized"
```

---

## 17. Testing response headers

Sometimes you also need to validate headers returned by the API.

```python
import pytest


@pytest.mark.asyncio
async def test_response_headers(client):
    resp = await client.get("/health")

    assert resp.status == 200
    assert resp.headers["Content-Type"].startswith("application/json")
```

### Common header checks
- `Content-Type`
- `Authorization`
- `Location`
- custom headers such as `X-Request-ID`

---

## 18. Testing JSON body structure

You may want to verify the full shape of the response, not just one field.

```python
import pytest


@pytest.mark.asyncio
async def test_user_response_structure(client):
    resp = await client.get("/users/1")
    data = await resp.json()

    assert resp.status == 200
    assert "id" in data
    assert "username" in data
```

### Better approach
When useful, compare exact structures:

```python
assert data == {
    "id": 1,
    "username": "janette"
}
```

---

## 19. Testing lists

If the endpoint returns a list, validate both type and contents.

```python
import pytest


@pytest.mark.asyncio
async def test_list_users(client):
    resp = await client.get("/users")
    data = await resp.json()

    assert resp.status == 200
    assert isinstance(data, list)
```

You can also validate length and element structure:

```python
assert len(data) >= 1
assert "id" in data[0]
assert "username" in data[0]
```

---

## 20. Testing not found responses

```python
import pytest


@pytest.mark.asyncio
async def test_user_not_found(client):
    resp = await client.get("/users/999")
    data = await resp.json()

    assert resp.status == 404
    assert "detail" in data
```

### Why this matters
404 behavior is part of the API contract too.

---

## 21. Testing internal error handling

If your app has controlled error handling, test that behavior too.

```python
import pytest


@pytest.mark.asyncio
async def test_internal_error_response(client):
    resp = await client.get("/crash")
    data = await resp.json()

    assert resp.status in (500, 503)
    assert "detail" in data
```

### Important
The exact status code depends on your application design.

---

## 22. Mocking dependencies

Endpoint tests often need to isolate external dependencies such as:
- databases
- third-party APIs
- message brokers
- email services

This is where mocking becomes important.

### Example idea
If an endpoint calls a service function:

```python
async def get_user_service(user_id: int):
    ...
```

you can mock that service in tests so the endpoint behavior is tested without calling real infrastructure.

---

## 23. Example with `unittest.mock`

```python
from unittest.mock import AsyncMock, patch
import pytest


@pytest.mark.asyncio
async def test_get_user_with_mock(client):
    with patch("app.services.user_service.get_user", new_callable=AsyncMock) as mock_get_user:
        mock_get_user.return_value = {"id": 1, "username": "janette"}

        resp = await client.get("/users/1")
        data = await resp.json()

        assert resp.status == 200
        assert data["username"] == "janette"
```

### Benefit
This keeps the test focused on the endpoint contract.

---

## 24. Testing authentication flows

For protected endpoints, it is useful to test both:
- valid access
- denied access

Typical cases:
- missing token
- invalid token
- expired token
- wrong role
- valid token

This ensures your endpoint security behavior is correct.

---

## 25. Example auth test cases

```python
import pytest


@pytest.mark.asyncio
async def test_profile_requires_token(client):
    resp = await client.get("/profile")
    assert resp.status == 401


@pytest.mark.asyncio
async def test_profile_with_valid_token(client):
    resp = await client.get(
        "/profile",
        headers={"Authorization": "Bearer valid-token"}
    )
    assert resp.status == 200
```

---

## 26. Testing async behavior carefully

When testing async code:

- always await async client calls
- always await async JSON reads
- avoid mixing sync and async carelessly
- ensure cleanup happens after tests

Common pattern:

```python
resp = await client.get("/endpoint")
data = await resp.json()
```

If you forget `await`, the test may fail in confusing ways.

---

## 27. Pytest markers and configuration

You can configure pytest to handle async tests more comfortably.

### Example `pytest.ini`

```ini
[pytest]
asyncio_mode = auto
```

This can reduce friction when working with async tests.

---

## 28. Shared fixtures for test data

Fixtures are also useful for reusable payloads.

```python
import pytest


@pytest.fixture
def sample_user_payload():
    return {
        "username": "janette"
    }
```

Usage:

```python
import pytest


@pytest.mark.asyncio
async def test_create_user_success(client, sample_user_payload):
    resp = await client.post("/users", json=sample_user_payload)
    assert resp.status == 201
```

### Benefit
This avoids repeating the same dictionaries everywhere.

---

## 29. Naming conventions for endpoint tests

Clear naming makes test suites easier to maintain.

Good examples:
- `test_health_endpoint_returns_200`
- `test_create_user_returns_201_when_payload_is_valid`
- `test_create_user_returns_400_when_username_is_missing`
- `test_get_profile_returns_401_without_token`

A test name should describe:
- what is being tested
- under what condition
- what result is expected

---

## 30. What a strong endpoint test should verify

A strong endpoint test usually checks:

- status code
- response payload
- important headers
- expected behavior for valid and invalid cases

Do not only check that the endpoint “responds”.  
Check that it responds correctly.

---

## 31. Difference between endpoint tests and unit tests

### Endpoint tests
Focus on the HTTP layer:
- routes
- request parsing
- status codes
- serialization
- auth behavior

### Unit tests
Focus on small pieces of logic:
- service functions
- helpers
- validators
- transformations

Both are useful, but they test different layers.

---

## 32. Difference between endpoint tests and full integration tests

### Endpoint tests
Usually isolate some dependencies and focus on API behavior.

### Full integration tests
May use:
- real database
- real services
- fuller environment setup

Integration tests are closer to real behavior, but often slower and harder to maintain.

---

## 33. Best practices

### 1. Test both success and failure cases
Do not stop at the happy path.

### 2. Reuse fixtures
This keeps tests short and consistent.

### 3. Keep tests independent
A test should not depend on another test running first.

### 4. Mock external systems when appropriate
This makes endpoint tests faster and more reliable.

### 5. Use clear assertions
Assert the exact behavior you care about.

### 6. Name tests clearly
Readable test names save time later.

### 7. Keep setup small
Too much setup can hide what the test actually verifies.

---

## 34. Common mistakes

### 1. Forgetting `await`
This is one of the most common async testing mistakes.

### 2. Testing only status codes
A 200 response alone does not prove the response is correct.

### 3. Repeating client setup everywhere
Use fixtures instead.

### 4. Depending on real external services unintentionally
This can make tests flaky.

### 5. Writing tests that depend on execution order
Tests should be isolated.

### 6. Mixing unit and endpoint concerns too much
Keep the purpose of each test clear.

---

## 35. Practical mental model

A useful mental model is:

- `pytest` runs and organizes the tests
- `aiohttp` provides the async HTTP test client and app behavior
- your assertions verify the API contract from the outside

So endpoint testing is essentially checking:

> “If a client sends this request, does the API return the correct HTTP behavior?”

---

## 36. Final recommendation

For APIs tested with `pytest` + `aiohttp`:

- create reusable async fixtures
- test status codes and payloads together
- include negative scenarios
- isolate external dependencies with mocks when needed
- keep tests readable and focused on behavior

That gives you a test suite that is more trustworthy and easier to scale.

---

## 37. Quick summary

If you only keep the essentials:

1. Use `pytest` to organize and run tests.
2. Use `aiohttp` test utilities for async endpoint calls.
3. Mark async tests correctly and use `await`.
4. Verify status codes, payloads, headers, and failure cases.
5. Use fixtures and mocks to keep tests clean and reliable.

---
