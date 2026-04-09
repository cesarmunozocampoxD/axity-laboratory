# Hexagonal Architecture — CreateOrder Lab

Practical example of Hexagonal Architecture (Ports & Adapters) in Python.

Implements a `CreateOrder` use case with:
- In-memory and SQLAlchemy repository adapters
- Simulated HTTP notification adapter
- Contract tests to verify every adapter satisfies the port

---

## Project structure

```
src/arquitectura_hexagonal/
├── domain/
│   └── entities/
│       └── order.py                        # Order entity + business invariants
├── application/
│   ├── ports/
│   │   ├── order_repository.py             # Repository port (Protocol)
│   │   └── notification_service.py         # Notification port (Protocol)
│   └── use_cases/
│       └── create_order.py                 # CreateOrder use case
└── infrastructure/
    ├── persistence/
    │   ├── in_memory_order_repository.py   # In-memory adapter (dict)
    │   └── sqlalchemy_order_repository.py  # SQLAlchemy adapter (SQLite / PostgreSQL)
    └── notifications/
        └── http_notification_adapter.py    # HTTP adapter (requests)

tests/
├── domain/
│   └── test_order.py                       # Pure domain tests
├── application/
│   └── test_create_order.py                # Use case tests with FakeNotifier
└── infrastructure/
    ├── contracts/
    │   └── order_repository_contract.py    # Shared contract base class
    ├── test_in_memory_repository.py        # Contract tests for in-memory adapter
    ├── test_sqlalchemy_repository.py       # Contract tests for SQLAlchemy adapter
    └── test_http_notification_adapter.py   # Adapter tests with mocked requests
```

---

## Requirements

- Python 3.12+
- [Poetry](https://python-poetry.org/)

---

## Setup

```bash
# Install dependencies (runtime + dev)
poetry install --with dev
```

---

## Run tests

```bash
poetry run pytest -v
```

Expected output: **24 tests passing**.

---

## Architecture overview

### Dependency rule

```
Infrastructure  →  Application  →  Domain
```

Outer layers depend on inner layers. The domain knows nothing about databases or HTTP.

### Layers

| Layer | Responsibility | Examples |
|---|---|---|
| **Domain** | Business entities and invariants | `Order` |
| **Application** | Use case orchestration + port contracts | `CreateOrderUseCase`, `OrderRepository` (Protocol), `NotificationService` (Protocol) |
| **Infrastructure** | Technical adapters | `InMemoryOrderRepository`, `SqlAlchemyOrderRepository`, `HttpNotificationAdapter` |

### Ports and Adapters

**Ports** are Python `Protocol` classes defined in the application layer. They describe *what* the use case needs without caring *how* it is implemented.

**Adapters** are concrete classes in the infrastructure layer that satisfy a port:

| Port | Adapters |
|---|---|
| `OrderRepository` | `InMemoryOrderRepository`, `SqlAlchemyOrderRepository` |
| `NotificationService` | `HttpNotificationAdapter` (mocked in tests) |

---

## Contract tests

Contract tests ensure that every adapter implementing a port behaves correctly. The base class `OrderRepositoryContract` defines the shared test cases. Each adapter test class inherits it and provides a `make_repository()` factory:

```python
class TestInMemoryOrderRepository(OrderRepositoryContract):
    def make_repository(self):
        return InMemoryOrderRepository()

class TestSqlAlchemyOrderRepository(OrderRepositoryContract):
    def make_repository(self):
        engine = create_in_memory_engine()
        session = Session(engine)
        return SqlAlchemyOrderRepository(session)
```

Adding a new adapter only requires creating a new subclass — all existing contract tests run automatically.

---

## Adding a new adapter

1. Create the class in `src/arquitectura_hexagonal/infrastructure/`.
2. Implement `save(order)` and `get_by_id(order_id)` to satisfy the `OrderRepository` port.
3. Add a test class that inherits `OrderRepositoryContract` and implements `make_repository()`.

No changes to the domain or application layer are required.

---

## Key concepts illustrated

- **Domain invariants** enforced inside the entity (`quantity > 0`, `total > 0`).
- **Ports as `Protocol`** — structural typing, no inheritance needed.
- **Use case isolation** — `CreateOrderUseCase` only depends on port protocols, never on concrete adapters.
- **Fake/stub in tests** — `FakeNotifier` and `InMemoryOrderRepository` keep unit tests fast and framework-free.
- **HTTP adapter simulation** — `unittest.mock.patch` replaces `requests` so no real network call is made.
