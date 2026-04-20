# arquitectura-limpia

Lab: Clean Architecture with Orders — Unit of Work, Presenter, and `OrderCreated` domain event.

When an order is created:

1. The **use case** (`CreateOrderUseCase`) receives `order_id` and `product`.
2. It creates a **domain entity** (`Order`), which automatically records a domain event (`OrderCreated`).
3. It persists the order through a **repository port** inside a **Unit of Work** transaction.
4. It commits the transaction.
5. Only after commit, it publishes the recorded domain events through an **event bus**.
6. It returns a formatted response via a **presenter**.

In this lab, infrastructure is intentionally simple and in-memory (`FakeUnitOfWork`, `FakeOrderRepository`), so you can focus on architecture boundaries and behavior.

## How Unit of Work and Domain Events Are Used

### Unit of Work (UoW)

The use case opens a transaction scope with `with uow:`. Inside that scope, it saves the order and calls `uow.commit()`.

- If everything is correct, commit confirms the changes.
- If an error occurs in a real implementation, rollback should cancel pending changes.

In this project, `FakeUnitOfWork` is in-memory and used for testing the behavior, but the interaction pattern is the same as with a real database-backed UoW.

### Domain Events

The `Order` entity records an `OrderCreated` event as soon as it is created. This keeps business facts inside the domain model.

The use case does not publish events immediately. First it commits the Unit of Work, then it publishes each event through the event bus.

This order is important: it avoids emitting events about changes that were not persisted successfully.

## Architecture Layers

- **Domain**: Business entity and domain event (`Order`, `OrderCreated`).
- **Application**: Use case orchestration, ports, presenters, and event handlers.
- **Infrastructure**: Technical implementations (in-memory UoW/repository and in-process event bus).

The tests validate the full behavior, including an important rule: **events are dispatched only after commit**.

## Project Structure

```text
.
├── pyproject.toml
├── README.md
├── src/
│   └── arquitectura_limpia/
│       ├── domain/
│       │   └── order.py
│       ├── application/
│       │   ├── ports.py
│       │   ├── use_cases/
│       │   │   └── create_order.py
│       │   ├── presenters/
│       │   │   └── order_presenter.py
│       │   └── events/
│       │       └── handlers.py
│       └── infrastructure/
│           ├── fake_uow.py
│           ├── event_bus.py
│           └── http/
│               └── main.py
└── tests/
		└── test_create_order.py
```

### What each folder does

- **`domain/`**: Pure business concepts. Contains `Order` and `OrderCreated`.
- **`application/`**: Use cases and contracts. Defines UoW/repository ports, orchestrates workflows, and shapes output.
- **`infrastructure/`**: Technical adapters and implementations.
	- `fake_uow.py`: in-memory repository/UoW used in tests and demos.
	- `event_bus.py`: in-process event dispatcher.
	- `http/main.py`: FastAPI adapter (`POST /orders`).
- **`tests/`**: Verifies domain rules, use case behavior, presenter output, event publishing, and ordering (commit before publish).

### Request Flow (API -> Use Case -> Domain)

1. FastAPI endpoint receives input in `infrastructure/http/main.py`.
2. Endpoint calls `CreateOrderUseCase` in `application/use_cases/create_order.py`.
3. Use case creates `Order` in `domain/order.py`, where `OrderCreated` is recorded.
4. Use case saves through `uow.orders` and commits the transaction.
5. After commit, use case publishes domain events through `EventBus`.
6. Presenter formats the response and API returns it to the client.

## Requirements

- Python 3.12+
- [Poetry](https://python-poetry.org/docs/#installation)

## Install

```bash
poetry install
```

## Run tests

```bash
poetry run pytest tests/ -v
```

## Run API

Start the FastAPI server:

```bash
poetry run uvicorn arquitectura_limpia.infrastructure.http.main:app --reload
```

Create an order with `POST /orders`:

```bash
curl -X POST http://127.0.0.1:8000/orders \
	-H "Content-Type: application/json" \
	-d '{"order_id": 1, "product": "Laptop"}'
```
