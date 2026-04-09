# Layers: Domain, Application, and Infrastructure

## 1. Goal

This guide explains a common layered architecture based on three core layers:

- **domain**
- **application**
- **infrastructure**

It focuses on:

- what each layer is responsible for
- how the layers relate to each other
- what kind of code belongs in each layer
- common mistakes
- testability implications
- a practical Python-oriented interpretation

The goal is to help you structure code so that business logic stays clearer, dependencies stay more controlled, and the system remains easier to change over time.

---

## 2. Why layered architecture exists

As software grows, code often becomes harder to maintain because concerns get mixed together.

Typical symptoms:
- business rules are mixed with database code
- use cases depend directly on frameworks
- external APIs leak into core logic
- tests require too much setup
- changing one technical detail affects business code everywhere

Layered architecture exists to reduce that kind of entanglement.

### In simple terms
It helps answer:

> “Where should this code live, and what should it depend on?”

---

## 3. The three layers at a glance

A useful first summary is:

- **Domain** → business meaning and business rules
- **Application** → use cases and orchestration
- **Infrastructure** → technical details and external integrations

This is the core mental model.

---

## 4. The big idea

A layered architecture tries to separate:

- **what the business is**
- **what the system does for the business**
- **how the system talks to the outside world**

That usually leads to a cleaner system because:
- domain rules remain more stable
- use cases become easier to follow
- infrastructure can change without contaminating the core logic

---

## 5. A simple visual model

```text
Infrastructure
    ↑
Application
    ↑
Domain
```

### Meaning
The deeper you go:
- the more business-centered the code becomes
- the less it should care about frameworks and technical details

A healthy design usually protects the lower layers from depending on outer technical concerns.

---

# Domain Layer

## 6. What the domain layer is

The **domain layer** contains the core business meaning of the system.

It answers questions like:
- what concepts exist in this business?
- what rules are always true?
- what operations are valid or invalid?
- what invariants must be protected?

### In simple terms
The domain layer is where the system expresses the **business itself**.

---

## 7. What belongs in the domain layer

Typical domain-layer elements include:

- entities
- value objects
- domain services
- business rules
- invariants
- domain exceptions
- domain events in some architectures

### Example concepts
In an e-commerce system:
- `Order`
- `Product`
- `Money`
- `OrderStatus`
- rules like “a shipped order cannot be cancelled”

---

## 8. What should not belong in the domain layer

The domain layer should usually not contain:
- database queries
- HTTP calls
- framework controllers
- ORM-specific persistence logic
- email sending
- logging infrastructure details
- cloud SDK usage

### Why?
Because those are technical concerns, not business meaning.

---

## 9. Domain example

```python
class Order:
    def __init__(self, total: float, status: str = "pending") -> None:
        self.total = total
        self.status = status

    def cancel(self) -> None:
        if self.status == "shipped":
            raise ValueError("A shipped order cannot be cancelled")
        self.status = "cancelled"
```

### Why this is domain logic
The rule:

> “A shipped order cannot be cancelled”

is a business rule.

It belongs in the domain, not in the database layer or HTTP layer.

---

## 10. Domain entities

An **entity** usually represents a business object with identity over time.

Examples:
- `User`
- `Order`
- `Invoice`

Entities usually have:
- identity
- state
- behavior tied to business rules

### Example
Two orders with the same total are not necessarily the same order.  
Identity matters.

---

## 11. Value objects

A **value object** is usually defined by its value, not by identity.

Examples:
- `Money`
- `EmailAddress`
- `DateRange`
- `Coordinate`

### Why useful
Value objects can make business rules clearer and more expressive.

Example:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: float
    currency: str
```

This can be more expressive than passing raw floats everywhere.

---

## 12. Domain services

A **domain service** is useful when business logic does not naturally belong to one entity alone.

Example:
- pricing calculation involving multiple business concepts
- risk evaluation
- eligibility rules spanning multiple entities

### Important
A domain service is still business logic.  
It is not a technical utility service.

---

## 13. Domain invariants

An **invariant** is a rule that must always hold.

Examples:
- account balance cannot go below allowed limits
- shipped orders cannot be edited
- discount percentages cannot exceed a business maximum
- reservation dates must be valid

Protecting invariants is one of the most important jobs of the domain layer.

---

## 14. Why the domain layer should stay clean

The domain layer is often the most valuable part of the system because it captures the actual business knowledge.

If it becomes mixed with:
- framework details
- SQL queries
- HTTP clients
- SDK-specific logic

then business rules become harder to:
- understand
- test
- reuse
- evolve

A clean domain is often one of the strongest maintainability advantages in a system.

---

# Application Layer

## 15. What the application layer is

The **application layer** coordinates use cases.

It answers questions like:
- what is the system trying to do for the user or process?
- in what order should business actions happen?
- which domain objects and ports should be invoked?
- what should happen in this use case?

### In simple terms
The application layer is where the system expresses **use cases and workflows**.

---

## 16. What belongs in the application layer

Typical application-layer elements include:

- use case services
- application services
- command handlers
- orchestration logic
- transaction boundaries
- coordination between domain and infrastructure ports
- input/output DTOs in some designs

### Examples
- `PlaceOrderUseCase`
- `RegisterUserService`
- `CancelSubscriptionHandler`

---

## 17. What the application layer should not do

The application layer should usually not:
- contain low-level database code directly
- contain HTTP framework route handlers
- contain SDK-specific code
- replace domain rules with arbitrary business logic duplication

It can coordinate those things through abstractions, but it should not collapse into infrastructure itself.

---

## 18. Application-layer example

```python
class OrderRepository:
    def get_by_id(self, order_id: int):
        raise NotImplementedError

    def save(self, order) -> None:
        raise NotImplementedError


class CancelOrderUseCase:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    def execute(self, order_id: int) -> None:
        order = self.repository.get_by_id(order_id)
        if order is None:
            raise ValueError("Order not found")

        order.cancel()
        self.repository.save(order)
```

### Why this is application logic
The use case:
- loads the domain object
- calls a domain rule
- persists the result

This is orchestration, not raw business rule definition and not raw infrastructure code.

---

## 19. Domain vs application logic

This distinction is very important.

### Domain logic
Rules like:
- “A shipped order cannot be cancelled.”

### Application logic
Workflow like:
- load order
- call `cancel()`
- save order
- maybe emit an event or notify another system

### Practical shortcut
- **Domain** decides what is valid
- **Application** decides how the use case flows

---

## 20. Application services and use cases

An application service is often a good place for:
- orchestrating repositories
- invoking domain methods
- coordinating external actions through ports
- controlling workflow steps

It should usually be:
- focused
- explicit
- close to one use case or a small related set of use cases

---

## 21. Application layer and transactions

In many systems, transaction boundaries logically sit around application-layer use cases.

Why?
Because the application layer often defines:
- when a use case starts
- what operations happen within it
- what should succeed or fail together

This is one reason the application layer is often the orchestration boundary.

---

## 22. Application layer and ports

A very common pattern is that the application layer depends on **abstractions** such as:
- repository interfaces
- notification sender protocols
- payment gateway ports
- message bus ports

This allows:
- infrastructure replacement
- easier testing
- lower coupling to technical details

---

# Infrastructure Layer

## 23. What the infrastructure layer is

The **infrastructure layer** contains technical implementations and integrations.

It answers questions like:
- how do we store data?
- how do we call external services?
- how do we send email?
- how do we expose HTTP endpoints?
- how do we talk to queues, caches, or cloud services?

### In simple terms
Infrastructure is where the system talks to the outside world.

---

## 24. What belongs in the infrastructure layer

Typical infrastructure elements include:

- database repository implementations
- ORM mappings
- HTTP clients
- external API adapters
- email sender implementations
- message broker clients
- file storage adapters
- framework setup
- persistence details
- cache clients

### Examples
- `SqlAlchemyOrderRepository`
- `S3FileStorage`
- `StripePaymentGateway`
- `FastAPI controller`
- `PostgresUserRepository`

---

## 25. Infrastructure example

```python
class InMemoryOrderRepository:
    def __init__(self) -> None:
        self.data = {}

    def get_by_id(self, order_id: int):
        return self.data.get(order_id)

    def save(self, order) -> None:
        self.data[order.id] = order
```

A more realistic production version might use:
- SQLAlchemy
- PostgreSQL
- Redis
- an HTTP SDK

But the basic idea is the same:
this layer implements technical access, not business meaning.

---

## 26. Infrastructure and frameworks

Framework-specific code often belongs in infrastructure or at the outermost edges.

Examples:
- FastAPI routers
- Django ORM adapters
- Flask request handlers
- Celery integration
- cloud SDK usage

### Why?
Because frameworks are delivery or technical mechanisms, not core business rules.

---

## 27. Infrastructure should be replaceable in principle

A good layered design often allows technical details to be replaced with limited impact on the core.

Examples:
- switch from one database to another
- replace SMTP with a third-party notification API
- change web framework
- change queue technology

That does not mean replacement is always trivial in practice.  
It means the architecture should not make those changes contaminate the business core unnecessarily.

---

# How the layers relate

## 28. A healthy dependency direction

A common healthy direction is:

- infrastructure depends on application/domain contracts
- application depends on domain and abstractions
- domain depends mostly on itself and core language concepts

### Practical intuition
The closer the code is to business meaning, the less it should know about technical delivery details.

---

## 29. Why dependency direction matters

If the domain depends directly on infrastructure, problems often appear:

- business code becomes framework-aware
- tests become harder
- replacing technical choices becomes expensive
- business rules become harder to isolate

Keeping dependency direction under control is one of the most important goals of layered design.

---

## 30. Example directory layout

A practical Python-style structure might look like:

```text
app/
├── domain/
│   ├── entities/
│   ├── value_objects/
│   ├── services/
│   └── exceptions.py
├── application/
│   ├── use_cases/
│   ├── ports/
│   └── dto/
├── infrastructure/
│   ├── persistence/
│   ├── messaging/
│   ├── api_clients/
│   └── web/
└── main.py
```

### Why useful
The folder structure reinforces responsibility boundaries.

---

## 31. Example end-to-end flow

Suppose a user cancels an order through an API.

### Flow
1. HTTP request arrives at a FastAPI route
2. route calls `CancelOrderUseCase`
3. use case loads the `Order` through a repository abstraction
4. `Order.cancel()` enforces business rule
5. repository implementation saves the updated order
6. response is returned

### Layer mapping
- FastAPI route → infrastructure
- `CancelOrderUseCase` → application
- `Order.cancel()` → domain
- concrete repository → infrastructure

This is a very practical way to see the layers working together.

---

## 32. Why this separation improves testability

A layered architecture often improves testing because:

- domain rules can be tested without frameworks
- use cases can be tested with fake repositories
- infrastructure can be tested separately as adapters/integrations
- business rules are not buried in controllers or SQL code

### Example
You can test:

- `Order.cancel()` as pure domain behavior
- `CancelOrderUseCase.execute()` with an in-memory repository
- FastAPI route separately as delivery wiring

That is much cleaner than testing everything through one giant integrated flow every time.

---

## 33. Domain testing

Domain tests are often:
- fast
- focused
- framework-free
- highly valuable

Example:

```python
def test_shipped_order_cannot_be_cancelled():
    order = Order(total=100, status="shipped")

    with pytest.raises(ValueError):
        order.cancel()
```

### Why this is strong
It tests the business rule directly where it belongs.

---

## 34. Application testing

Application tests often verify:
- orchestration
- interaction between domain and ports
- use case flow

Example:
- load order
- cancel it
- save it
- handle not found correctly

These tests often use:
- fake repositories
- fake notifiers
- in-memory adapters

---

## 35. Infrastructure testing

Infrastructure tests often verify:
- repository implementation correctness
- API adapter correctness
- integration with databases
- framework endpoint wiring
- serialization/deserialization behavior

These are usually more integration-oriented than pure domain tests.

---

## 36. Common mistake: putting business logic in controllers

A very common mistake is putting domain rules directly in:
- FastAPI routes
- Flask controllers
- Django views
- ORM models with mixed framework logic
- SQL-heavy service methods

### Why this hurts
It mixes:
- transport concerns
- technical concerns
- business concerns

That usually reduces clarity and testability.

---

## 37. Common mistake: application layer as a dump

Another mistake is turning the application layer into a giant services folder where:
- business rules
- infrastructure calls
- utility helpers
- framework logic

are all mixed together.

### Why this hurts
The application layer should orchestrate use cases, not become a vague dumping ground.

---

## 38. Common mistake: overengineering the layers

Layered architecture can also go too far.

Bad signs:
- too many wrappers with no real purpose
- endless pass-through methods
- interfaces for everything, even trivial cases
- tiny abstractions created before real complexity exists

### Practical rule
The goal is **clear separation**, not maximum ceremony.

---

## 39. Common mistake: anemic domain by accident

Sometimes teams push all logic into application services and leave the domain as empty data containers.

That can produce an **anemic domain model**, where:
- business objects have almost no behavior
- rules live in procedural service code
- invariants become scattered

### Why this matters
A healthy domain often contains important business behavior, not just data fields.

---

## 40. When layered architecture helps most

This style is especially useful when:
- the system has real business rules
- the project is growing
- multiple external integrations exist
- testability matters
- framework independence matters
- technical details change more often than business meaning

For very small scripts or prototypes, a strict layered structure may be too much.

---

## 41. A practical Pythonic interpretation

In Python, layered architecture does not require extreme ceremony.

A Pythonic version often means:
- simple domain classes
- focused use case classes or functions
- clear infrastructure adapters
- Protocols or small abstractions where helpful
- explicit dependency injection
- not turning every concept into a giant inheritance hierarchy

### Important
You can keep the layers clean without making the code feel bureaucratic.

---

## 42. Practical mental model

A useful mental model is:

- **Domain** → “What is true in the business?”
- **Application** → “What use case is being executed?”
- **Infrastructure** → “How do we persist, send, expose, or integrate this technically?”

That distinction alone resolves many design questions.

---

## 43. Decision heuristic

When you are unsure where code belongs, ask:

### Domain?
Is this a business rule, invariant, or business concept behavior?

### Application?
Is this orchestrating a use case or coordinating domain + ports?

### Infrastructure?
Is this about frameworks, databases, APIs, files, queues, or external systems?

These questions are often enough to place code correctly.

---

## 44. Final recommendation

A practical layered architecture should aim for:

- business rules in the domain
- workflow orchestration in the application layer
- technical details in infrastructure
- dependencies pointing inward toward the business core
- enough structure to keep concerns clean
- not so much abstraction that the design becomes heavy

If the layering makes the business easier to understand and the technical details easier to replace or test, it is helping.

---

## 45. Quick summary

If you only keep the essentials:

1. The domain layer contains business concepts and business rules.
2. The application layer contains use cases and orchestration.
3. The infrastructure layer contains technical implementations and integrations.
4. A healthy layered design keeps business logic away from framework and persistence details.
5. This separation usually improves maintainability, testability, and clarity.

---

# Ports (Interfaces / Protocols) and Adapters (SQL, HTTP, Messaging)

## 1. Goal

This guide explains the **Ports and Adapters** style of architecture, often also associated with **Hexagonal Architecture**, in a practical Python-oriented way.

It focuses on:

- what ports are
- what adapters are
- why interfaces or `Protocol` types matter
- how SQL adapters fit
- how HTTP adapters fit
- how messaging adapters fit
- how this design improves testability and flexibility
- common mistakes and practical trade-offs

The goal is to understand how to keep business logic independent from technical details while still integrating cleanly with databases, APIs, and messaging systems.

---

## 2. The basic idea

Ports and Adapters separates:

- **core application logic**
- **external systems and technical integrations**

The core should define what it needs in terms of capabilities.  
The outside world should implement those capabilities.

### In simple terms
The core says:

> “I need a way to load users.”  
> “I need a way to send notifications.”  
> “I need a way to publish an event.”

Those needs are the **ports**.

The concrete implementations are the **adapters**.

---

## 3. Why this architecture exists

Without this separation, business code often becomes tightly coupled to:

- SQL libraries
- HTTP clients
- framework controllers
- queue brokers
- cloud SDKs
- ORM-specific models

That creates problems such as:
- harder testing
- harder replacement of infrastructure
- business logic mixed with technical details
- slower and more fragile refactoring

Ports and Adapters exists to control that coupling.

---

## 4. The mental model

A useful mental model is:

- **Port** = a required or offered capability contract
- **Adapter** = a technical implementation that connects that contract to the outside world

### Another way to say it
- Ports describe **what** the core needs or exposes
- Adapters describe **how** the outside world fulfills or uses that

---

## 5. Inbound vs outbound ports

A very useful distinction is:

### Inbound ports
Ways the outside world calls into the application.

Examples:
- use cases
- command handlers
- application service contracts

### Outbound ports
Ways the application calls outward.

Examples:
- repositories
- notification senders
- payment gateways
- event publishers
- external API clients

### Practical shortcut
- inbound = inputs into the core
- outbound = outputs from the core to external systems

---

## 6. Where ports live

In a clean design, ports usually live close to the core, often in the:

- domain layer
- application layer

depending on the architecture style and the type of port.

### Why?
Because the core should define the capabilities it needs, not the infrastructure.

If the infrastructure defines the contract, the dependency direction often becomes backward.

---

## 7. Where adapters live

Adapters usually live in the **infrastructure** or outer layer.

Examples:
- SQL repository adapters
- HTTP client adapters
- messaging broker adapters
- FastAPI route adapters
- CLI adapters

### Why?
Because adapters are technical details.  
They are the mechanism used to satisfy or expose the port.

---

## 8. A simple visual model

```text
          External World
   (HTTP, DB, queues, frameworks)

              Adapters
   (FastAPI, SQLAlchemy repo, Kafka publisher)

                Ports
   (Protocols / interfaces / use case contracts)

                 Core
      (domain + application logic)
```

This is the core shape of the architecture.

---

# Ports

## 9. What a port is

A **port** is a contract that defines a capability boundary.

Examples:
- “find an order by id”
- “save an order”
- “send a notification”
- “publish an event”
- “fetch exchange rates”

A port should focus on **behavior**, not on implementation details.

---

## 10. Ports in Python

In Python, ports are often expressed using:

- `typing.Protocol`
- abstract base classes
- simple callable contracts
- sometimes just a documented method shape in small systems

A very Pythonic choice is often `Protocol`, because it supports structural typing without forcing inheritance.

---

## 11. Port example with `Protocol`

```python
from typing import Protocol


class OrderRepository(Protocol):
    def get_by_id(self, order_id: int):
        ...

    def save(self, order) -> None:
        ...
```

### Why this is a port
It expresses what the application needs:
- load an order
- save an order

It does not say:
- PostgreSQL
- SQLAlchemy
- Redis
- HTTP
- file storage

That is exactly the point.

---

## 12. Why ports improve design

Ports improve design because they:

- reduce coupling to technical details
- make testing easier
- clarify responsibilities
- support infrastructure replacement
- keep business logic more stable

The core depends on capabilities, not on concrete systems.

---

## 13. Ports should be small and meaningful

A good port usually exposes only what the core actually needs.

Bad example:
- a giant “database interface” with many unrelated methods

Better example:
- a focused repository or gateway contract

### Why this matters
Small ports improve:
- readability
- testability
- substitutability
- cohesion

This connects closely with Interface Segregation and Dependency Inversion.

---

## 14. A repository port example

```python
from typing import Protocol


class UserRepository(Protocol):
    def get_by_id(self, user_id: int) -> dict | None:
        ...

    def save(self, user: dict) -> None:
        ...
```

### Why this is good
The application can use a repository-like capability without knowing whether the storage is:
- SQL
- in-memory
- API-based
- mock-based

---

## 15. A notification port example

```python
from typing import Protocol


class NotificationSender(Protocol):
    def send(self, message: str) -> None:
        ...
```

### Why useful
The application can work with:
- email
- SMS
- push notification
- fake sender in tests

through the same behavioral contract.

---

## 16. A messaging port example

```python
from typing import Protocol


class EventPublisher(Protocol):
    def publish(self, topic: str, payload: dict) -> None:
        ...
```

### Why useful
The application can publish events without caring whether the implementation uses:
- Kafka
- RabbitMQ
- Redis streams
- an in-memory test bus

---

# Adapters

## 17. What an adapter is

An **adapter** is the implementation that connects a port to a real external mechanism.

It translates between:
- the application’s expected port contract
- the external system’s actual API or protocol

### In simple terms
If the port says:

> “save(order)”

the adapter says:

> “I will do that using SQLAlchemy and PostgreSQL.”

---

## 18. Why adapters matter

Adapters matter because they isolate technical details.

That means:
- the core does not have to know SQLAlchemy
- the core does not have to know HTTP request syntax
- the core does not have to know queue SDK details

This gives you cleaner boundaries.

---

## 19. Adapters can translate

An adapter often does translation between worlds:

- domain objects ↔ database records
- application requests ↔ HTTP payloads
- event objects ↔ broker message formats
- external API responses ↔ internal models

This translation role is one of the most important practical jobs of adapters.

---

# SQL adapters

## 20. What a SQL adapter is

A **SQL adapter** is an infrastructure component that implements a persistence port using SQL technology.

Examples:
- PostgreSQL
- MySQL
- SQLite
- SQLAlchemy
- psycopg
- async DB drivers

---

## 21. SQL adapter example

Port:

```python
from typing import Protocol


class UserRepository(Protocol):
    def get_by_id(self, user_id: int) -> dict | None:
        ...

    def save(self, user: dict) -> None:
        ...
```

Adapter:

```python
class InMemoryUserRepository:
    def __init__(self) -> None:
        self.users = {}

    def get_by_id(self, user_id: int) -> dict | None:
        return self.users.get(user_id)

    def save(self, user: dict) -> None:
        self.users[user["id"]] = user
```

### Why this counts as an adapter
It implements the repository port, even though it is in-memory rather than real SQL.

A real SQL version would use database queries behind the same contract.

---

## 22. SQLAlchemy-style adapter example

```python
class SqlAlchemyUserRepository:
    def __init__(self, session) -> None:
        self.session = session

    def get_by_id(self, user_id: int) -> dict | None:
        row = self.session.get(UserModel, user_id)
        if row is None:
            return None
        return {"id": row.id, "username": row.username}

    def save(self, user: dict) -> None:
        row = UserModel(id=user["id"], username=user["username"])
        self.session.merge(row)
        self.session.commit()
```

### Why this is infrastructure
It knows about:
- session
- ORM model
- commit behavior
- database persistence details

The core should not need to know those things.

---

## 23. SQL adapter responsibilities

A SQL adapter often handles:
- queries
- persistence mapping
- transaction usage
- row-to-domain translation
- database-specific error translation

### Important
It should not become the place where business rules are invented.

That belongs in the domain or application core.

---

## 24. Why SQL adapters help testability

If the application depends on a repository port, tests can use:
- fake repositories
- in-memory repositories
- simple stubs

instead of needing:
- a real database
- migrations
- container startup
- full integration setup

This makes application tests much faster and simpler.

---

# HTTP adapters

## 25. What an HTTP adapter is

An **HTTP adapter** can exist in two directions:

### Inbound HTTP adapter
An adapter that exposes the application to the outside world through HTTP.

Examples:
- FastAPI route
- Flask controller
- Django view

### Outbound HTTP adapter
An adapter that lets the application call an external HTTP API.

Examples:
- payment service client
- exchange rate client
- third-party user profile client

Both are adapters, but they face opposite directions.

---

## 26. Inbound HTTP adapter example

Use case:

```python
class RegisterUserUseCase:
    def __init__(self, repository) -> None:
        self.repository = repository

    def execute(self, user_data: dict) -> None:
        self.repository.save(user_data)
```

FastAPI adapter:

```python
from fastapi import APIRouter

router = APIRouter()


@router.post("/users")
def register_user(payload: dict):
    use_case = RegisterUserUseCase(repository=...)
    use_case.execute(payload)
    return {"status": "ok"}
```

### Why this is an adapter
The route adapts:
- HTTP request/response
- JSON payload
- framework-specific mechanics

into a call to the application use case.

---

## 27. What inbound HTTP adapters should do

Inbound HTTP adapters should usually:
- parse request data
- validate request shape
- call the appropriate application use case
- map output to HTTP response format
- translate exceptions into HTTP semantics when appropriate

### What they should not do
They should usually not:
- contain core business rules
- do direct heavy database logic
- coordinate too many unrelated concerns

They should stay thin.

---

## 28. Outbound HTTP adapter example

Port:

```python
from typing import Protocol


class ExchangeRateProvider(Protocol):
    def get_rate(self, base: str, target: str) -> float:
        ...
```

HTTP adapter:

```python
import requests


class HttpExchangeRateProvider:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def get_rate(self, base: str, target: str) -> float:
        response = requests.get(
            f"{self.base_url}/rates",
            params={"base": base, "target": target},
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()
        return float(data["rate"])
```

### Why this is an adapter
It translates a simple application capability into a real HTTP call.

---

## 29. Outbound HTTP adapter responsibilities

An outbound HTTP adapter often handles:
- request construction
- headers and authentication
- timeouts
- error handling
- JSON parsing
- mapping external response shape to internal shape

### Why this matters
The core should say:
- “I need an exchange rate”

not:
- “I need to send this GET request with these headers and parse this JSON schema”

---

## 30. Why HTTP adapters improve maintainability

With a port + adapter design:
- changing API providers is easier
- testing is easier
- HTTP details stay localized
- domain/application logic stays cleaner

This becomes very valuable as integrations multiply.

---

# Messaging adapters

## 31. What a messaging adapter is

A **messaging adapter** connects the application to a message-based system.

Examples:
- Kafka
- RabbitMQ
- Redis Pub/Sub
- SQS
- NATS
- internal event buses

Messaging can also be inbound or outbound.

### Outbound
The app publishes an event or command.

### Inbound
The app consumes a message and triggers a use case.

---

## 32. Outbound messaging port example

```python
from typing import Protocol


class EventPublisher(Protocol):
    def publish(self, topic: str, payload: dict) -> None:
        ...
```

Adapter:

```python
class InMemoryEventPublisher:
    def __init__(self) -> None:
        self.events = []

    def publish(self, topic: str, payload: dict) -> None:
        self.events.append((topic, payload))
```

### Why useful
This fake adapter is very helpful for tests.

A production version could use Kafka or RabbitMQ behind the same port.

---

## 33. Kafka-style adapter example

```python
class KafkaEventPublisher:
    def __init__(self, producer) -> None:
        self.producer = producer

    def publish(self, topic: str, payload: dict) -> None:
        self.producer.send(topic, payload)
        self.producer.flush()
```

### Why this is infrastructure
It knows about:
- Kafka producer API
- broker semantics
- flush behavior

The core should not need that knowledge.

---

## 34. Inbound messaging adapter example

Suppose a queue consumer receives a message and triggers a use case.

```python
class OrderCreatedHandler:
    def __init__(self, use_case) -> None:
        self.use_case = use_case

    def handle(self, message: dict) -> None:
        self.use_case.execute(message["order_id"])
```

### Why this is an adapter
It adapts:
- broker-delivered message format
- technical delivery mechanics

into an application-layer call.

---

## 35. Messaging adapter responsibilities

Messaging adapters often handle:
- serialization/deserialization
- topic/routing binding
- acknowledgment semantics
- retries
- broker-specific delivery details
- message schema translation

### Important
They should not become the place where domain behavior is invented.

They should connect the broker world to the application world.

---

# Putting ports and adapters together

## 36. A full example

Port:

```python
from typing import Protocol


class UserRepository(Protocol):
    def get_by_id(self, user_id: int) -> dict | None:
        ...

    def save(self, user: dict) -> None:
        ...


class NotificationSender(Protocol):
    def send(self, message: str) -> None:
        ...
```

Use case:

```python
class WelcomeUserUseCase:
    def __init__(self, repository: UserRepository, notifier: NotificationSender) -> None:
        self.repository = repository
        self.notifier = notifier

    def execute(self, user_id: int) -> None:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise ValueError("User not found")
        self.notifier.send(f"Welcome {user['username']}")
```

Adapters:

```python
class InMemoryUserRepository:
    def __init__(self) -> None:
        self.users = {1: {"id": 1, "username": "janette"}}

    def get_by_id(self, user_id: int) -> dict | None:
        return self.users.get(user_id)

    def save(self, user: dict) -> None:
        self.users[user["id"]] = user


class ConsoleNotificationSender:
    def send(self, message: str) -> None:
        print(message)
```

Usage:

```python
use_case = WelcomeUserUseCase(
    repository=InMemoryUserRepository(),
    notifier=ConsoleNotificationSender(),
)

use_case.execute(1)
```

### What this shows
- the core depends on ports
- infrastructure provides adapters
- the use case stays independent of SQL, HTTP, or broker details

---

## 37. Why this architecture improves testing

With ports and adapters, tests can often target the application core using:
- fake repositories
- fake HTTP clients
- fake publishers
- in-memory adapters

That allows tests to verify business flow without needing:
- a real database
- a running message broker
- external API access
- framework startup

This is one of the biggest practical benefits.

---

## 38. Fake adapters vs mocks

A very useful testing approach is to use **fake adapters**.

Example:
- `InMemoryUserRepository`
- `FakeEventPublisher`
- `FakeNotificationSender`

### Why this is often better than heavy mocking
Fakes can be:
- simpler
- more realistic
- less brittle
- easier to reason about

This often makes application tests cleaner.

---

## 39. Common mistakes

### 1. Defining ports in infrastructure
This often reverses the dependency direction.

### 2. Making ports too large
A giant interface weakens cohesion and testability.

### 3. Putting business rules in adapters
Adapters should translate and integrate, not own business meaning.

### 4. Making controllers or routes thick
Inbound HTTP adapters should stay relatively thin.

### 5. Overengineering every small project
Ports and adapters is powerful, but not every tiny script needs a full architecture.

### 6. Creating one adapter per method with no real benefit
The boundary should be meaningful, not decorative.

---

## 40. When this approach helps most

Ports and adapters helps especially when:
- the system has real business logic
- infrastructure may change
- external integrations exist
- testing matters
- multiple delivery mechanisms exist
- the project is expected to grow

For a tiny script that reads one file and prints one result, this structure may be too much.

---

## 41. A practical Pythonic interpretation

A Pythonic implementation usually means:
- ports expressed with `Protocol` or small interfaces
- use cases depending on those ports
- adapters implemented in infrastructure
- explicit dependency injection
- keeping adapters simple and focused
- not forcing giant abstraction hierarchies

### Important
You can keep the architecture clean without turning it into ceremony-heavy code.

---

## 42. Practical mental model

A useful mental model is:

- **Port** → “What capability does the core need or expose?”
- **Adapter** → “How do we connect that capability to a real technical mechanism?”

Examples:
- repository port ↔ SQL adapter
- exchange-rate port ↔ HTTP client adapter
- event-publisher port ↔ Kafka adapter
- use case ↔ FastAPI route adapter

That mental model resolves many design questions quickly.

---

## 43. Final recommendation

A practical ports-and-adapters design should aim for:

- ports close to the core
- adapters at the edges
- business logic independent from technical details
- small, meaningful capability contracts
- easy substitution of infrastructure
- easy testing of application logic with fake adapters

If the architecture makes the core easier to understand and the integrations easier to replace or test, it is helping.

---

## 44. Quick summary

If you only keep the essentials:

1. Ports define capability contracts for the core.
2. Adapters implement those contracts using real technologies like SQL, HTTP, or messaging systems.
3. SQL adapters handle persistence details.
4. HTTP adapters handle inbound framework requests or outbound API calls.
5. Messaging adapters handle publishing or consuming broker-based messages.
6. This design usually improves decoupling, testability, and maintainability.

---

# Use Cases and Orchestration; DTOs vs Entities

## 1. Goal

This guide explains two closely related software design topics:

- **use cases and orchestration**
- **DTOs vs entities**

It focuses on:

- what a use case is
- what orchestration means
- where use cases belong in layered architecture
- what DTOs are
- what entities are
- how DTOs and entities differ
- common mistakes
- practical Python-oriented examples

The goal is to help you separate business behavior, workflow coordination, and data transport more clearly.

---

## 2. Why these topics belong together

These topics are strongly related because real application workflows often involve:

- receiving input data
- transforming or validating it
- executing a business use case
- interacting with domain entities
- returning output data

If those responsibilities are mixed together, the code often becomes:
- harder to understand
- harder to test
- harder to maintain
- more coupled to frameworks or transport details

That is why it is useful to understand:
- what the **use case** should do
- what the **entity** should do
- what the **DTO** should do

---

## 3. What a use case is

A **use case** represents an application-level action or workflow that the system performs for a user, another system, or an internal process.

Examples:
- register a user
- place an order
- cancel a subscription
- generate an invoice
- send a welcome email
- approve a loan request

### In simple terms
A use case answers:

> “What is the system trying to accomplish here?”

---

## 4. Use cases are application behavior

A use case is not just one method call.  
It usually describes a meaningful application action.

Examples:
- “Create a new customer account”
- “Transfer money between accounts”
- “Publish an article”
- “Reset a password”

These are not low-level technical actions.  
They are business-relevant workflows exposed by the application.

---

## 5. Where use cases usually live

In a layered or hexagonal architecture, use cases usually belong in the **application layer**.

Why?
Because they coordinate:
- inputs
- domain behavior
- repository access
- service calls through ports
- output preparation

### Practical idea
The use case is where the application says:

> “Given this request, execute this business flow.”

---

## 6. What orchestration means

**Orchestration** means coordinating multiple steps in a workflow.

A use case often orchestrates things like:
- loading data
- calling domain methods
- persisting changes
- publishing events
- sending notifications
- returning a result

### In simple terms
Orchestration answers:

> “In what order should these actions happen to complete this use case?”

---

## 7. What orchestration is not

Orchestration is not the same as business rule definition.

### Business rule
Example:
- “A shipped order cannot be cancelled.”

### Orchestration
Example:
- load order
- call `cancel()`
- save order
- publish event
- return result

### Practical shortcut
- **Domain** decides what is valid
- **Application/use case** decides how the workflow runs

---

## 8. A basic use case example

```python
class CancelOrderUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, order_id: int) -> None:
        order = self.repository.get_by_id(order_id)
        if order is None:
            raise ValueError("Order not found")

        order.cancel()
        self.repository.save(order)
```

### Why this is a use case
This code represents a meaningful application action:
- cancel an order

It coordinates:
- repository access
- domain behavior
- persistence

That is orchestration.

---

## 9. Why use cases are useful

Use cases are useful because they give the application a clear shape.

Instead of putting logic in:
- controllers
- routes
- UI handlers
- repository classes
- random service files

you create explicit application actions.

### Benefits
This often improves:
- readability
- testability
- clarity of system behavior
- separation of concerns

---

## 10. Good use case characteristics

A good use case is usually:

- focused on one business action
- explicit in what it orchestrates
- not overloaded with unrelated responsibilities
- not tied directly to framework details
- easy to test with fake adapters or repositories

### Good examples
- `RegisterUserUseCase`
- `PlaceOrderUseCase`
- `ApproveLoanUseCase`

These names clearly express intent.

---

## 11. Common mistake: giant service classes

A common mistake is creating one huge service class like:

```python
class UserService:
    def create_user(...): ...
    def delete_user(...): ...
    def suspend_user(...): ...
    def reset_password(...): ...
    def calculate_rewards(...): ...
    def export_user_report(...): ...
```

This can become a vague dumping ground.

### Why this is a problem
The code loses focus, and different workflows become mixed together.

A use-case-oriented structure often stays clearer.

---

## 12. Common mistake: putting orchestration in controllers

Another common mistake is putting the full workflow directly inside:
- FastAPI routes
- Flask views
- Django views
- CLI handlers

Example problem:

```python
@router.post("/orders/{order_id}/cancel")
def cancel_order(order_id: int):
    order = db.get_order(order_id)
    if order.status == "shipped":
        raise HTTPException(status_code=400, detail="Cannot cancel shipped order")
    db.cancel_order(order_id)
    send_email(...)
    publish_event(...)
    return {"ok": True}
```

### Why this is problematic
This mixes:
- HTTP concerns
- business rule checks
- persistence
- notifications
- event publishing

That hurts separation and testability.

---

## 13. Better flow with a use case

A cleaner design is:

```python
@router.post("/orders/{order_id}/cancel")
def cancel_order(order_id: int):
    use_case.execute(order_id)
    return {"ok": True}
```

And the use case handles orchestration.

### Why this is better
The route becomes a thin delivery adapter, and the application flow becomes reusable and easier to test.

---

# Orchestration in practice

## 14. Typical orchestration steps

A use case commonly does some combination of:

1. validate or normalize input
2. load relevant entities
3. call domain behavior
4. call external services through ports
5. persist changes
6. publish events or notifications
7. produce output

Not every use case does all these steps, but this is a common pattern.

---

## 15. Example: register user workflow

```python
class RegisterUserUseCase:
    def __init__(self, user_repo, notifier):
        self.user_repo = user_repo
        self.notifier = notifier

    def execute(self, username: str, email: str) -> None:
        if self.user_repo.exists_by_email(email):
            raise ValueError("Email already exists")

        user = User(username=username, email=email)
        self.user_repo.save(user)
        self.notifier.send(f"Welcome {username}")
```

### What is happening here
The use case orchestrates:
- uniqueness check
- entity creation
- persistence
- notification

The `User` entity itself should not be responsible for the whole workflow.

---

## 16. Orchestration should stay focused

A use case should coordinate a workflow, but it should not become a giant “do everything” object.

If a use case starts doing too much, signs may appear:
- many unrelated collaborators
- too many branches
- too many responsibilities
- hard-to-follow workflow
- too many mocks in tests

That may mean the use case is:
- too broad
- mixing concerns
- hiding missing abstractions

---

## 17. Orchestration and transactions

Use cases are often a natural place for transaction boundaries.

Why?
Because a use case usually defines:
- what belongs to one business action
- what must succeed or fail together

For example:
- save order
- reduce inventory
- record payment

These may need to happen as one application action.

---

## 18. Orchestration and events

Sometimes a use case also triggers side effects like:
- domain events
- notification messages
- analytics events
- audit records

### Important
These should usually be coordinated as part of the application workflow, not mixed randomly into entities unless the design explicitly uses domain events.

---

# Entities

## 19. What an entity is

An **entity** is a domain object with identity and business behavior.

Examples:
- `User`
- `Order`
- `Invoice`
- `Account`

Entities often contain:
- identity
- state
- business rules
- business behavior

### In simple terms
An entity represents something that matters in the business model over time.

---

## 20. Entity example

```python
class Order:
    def __init__(self, order_id: int, status: str = "pending") -> None:
        self.order_id = order_id
        self.status = status

    def cancel(self) -> None:
        if self.status == "shipped":
            raise ValueError("A shipped order cannot be cancelled")
        self.status = "cancelled"
```

### Why this is an entity
It has:
- identity (`order_id`)
- state (`status`)
- behavior (`cancel()`)

And the behavior enforces a business rule.

---

## 21. What entities should do

Entities should usually:
- represent business concepts
- protect invariants
- expose meaningful domain behavior
- keep domain state consistent

### Example responsibilities
An `Account` entity may:
- deposit money
- withdraw money
- prevent invalid balance transitions

These are business responsibilities, not transport concerns.

---

## 22. What entities should not do

Entities should usually not:
- run SQL queries
- send HTTP requests
- know about FastAPI request objects
- publish Kafka messages directly
- serialize themselves for APIs in framework-specific ways
- depend heavily on infrastructure details

That would mix the domain with technical concerns.

---

## 23. Entities are not DTOs

This is one of the most important distinctions in this guide.

An entity is not just a bag of fields.

An entity has:
- meaning in the domain
- identity
- business behavior
- rules and invariants

A DTO is different.

---

# DTOs

## 24. What a DTO is

**DTO** stands for **Data Transfer Object**.

A DTO is an object used to carry data between layers, boundaries, or systems.

Examples:
- request payload objects
- response objects
- command input objects
- query result objects
- API response models

### In simple terms
A DTO answers:

> “How do we package data to move it from one place to another?”

---

## 25. DTOs are about transport, not business identity

A DTO usually:
- carries data
- is simple
- does not own deep business behavior
- often has no meaningful identity beyond its data content
- often exists to cross a boundary cleanly

This makes a DTO very different from an entity.

---

## 26. DTO example with dataclass

```python
from dataclasses import dataclass


@dataclass
class RegisterUserRequest:
    username: str
    email: str
```

### Why this is a DTO
It represents structured input data for a use case.  
It does not represent a domain entity with identity and business rules.

---

## 27. Response DTO example

```python
from dataclasses import dataclass


@dataclass
class UserResponse:
    id: int
    username: str
    email: str
```

### Why this is a DTO
It packages output data for an API or another boundary.

It is not the same thing as the domain entity itself.

---

## 28. DTOs are useful at boundaries

DTOs are often useful for:

- controller input
- controller output
- API request/response models
- command/query objects
- inter-service messaging payloads
- external adapter boundaries

### Why?
They help prevent domain entities from being tightly coupled to transport formats or framework-specific concerns.

---

## 29. DTOs and validation

DTOs often carry validation-oriented concerns.

Examples:
- required fields
- input types
- field constraints
- serialization rules
- schema shape

This is especially common in web APIs.

### Important
Validation at the DTO boundary is not the same thing as domain validation.

A DTO may validate:
- shape
- format
- required fields

The domain still validates:
- business meaning
- invariants
- allowed state changes

---

## 30. DTOs vs entities: the core difference

A strong practical distinction is:

### Entity
Represents a business object with identity and behavior.

### DTO
Represents transported data across a boundary.

### Another way to say it
- **Entity** = business meaning
- **DTO** = data packaging

This distinction resolves many architecture confusions.

---

## 31. Example comparison

Entity:

```python
class User:
    def __init__(self, user_id: int, username: str, email: str) -> None:
        self.user_id = user_id
        self.username = username
        self.email = email

    def change_email(self, new_email: str) -> None:
        if "@" not in new_email:
            raise ValueError("Invalid email")
        self.email = new_email
```

DTO:

```python
from dataclasses import dataclass


@dataclass
class UpdateUserEmailRequest:
    user_id: int
    new_email: str
```

### Why they are different
- the DTO carries input for a workflow
- the entity enforces business behavior

They are not interchangeable concepts.

---

## 32. Should entities be returned directly from APIs?

Usually, it is safer not to expose domain entities directly as API responses.

Why?
Because API responses often need:
- controlled field exposure
- transport-friendly shapes
- versioning flexibility
- framework-specific serialization
- decoupling from domain internals

That is why response DTOs are often useful.

---

## 33. Should DTOs contain business logic?

Usually only minimal logic, if any.

DTOs should generally stay focused on:
- structure
- transport
- maybe lightweight validation or normalization

If a DTO starts owning core domain rules, responsibilities are getting mixed.

---

## 34. Mapping DTOs to entities

A common workflow is:

1. receive input DTO
2. use DTO data to load or create entities
3. execute domain behavior
4. return output DTO

Example:

```python
class RegisterUserUseCase:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def execute(self, request: RegisterUserRequest) -> UserResponse:
        user = User(user_id=1, username=request.username, email=request.email)
        self.user_repo.save(user)
        return UserResponse(id=user.user_id, username=user.username, email=user.email)
```

### Why this is clean
DTOs handle input/output boundaries.  
Entities handle domain meaning.

---

## 35. Why this mapping is worth it

Some developers initially feel that DTO ↔ entity mapping is repetitive.

Sometimes it is.  
But the separation often pays off because it protects:
- the domain model
- the API contract
- future flexibility
- test clarity
- transport independence

It is usually a trade-off between:
- some extra mapping code
- and a much cleaner separation of concerns

---

## 36. When DTOs may be unnecessary

DTOs may be unnecessary when:
- the system is very small
- the boundary is simple
- the extra abstraction adds no real value
- a plain dictionary or direct parameters are sufficient

### Practical rule
Do not create DTOs by ritual.  
Create them when the boundary, clarity, or validation concerns justify them.

---

## 37. Common mistake: using entities as request objects

A common mistake is using domain entities directly as API input models.

Problematic because:
- transport shape and domain shape may diverge
- domain objects become coupled to API concerns
- validation concerns get mixed
- persistence identity may leak into boundaries awkwardly

This often creates long-term friction.

---

## 38. Common mistake: anemic entities and fat use cases

Another mistake is:
- DTOs everywhere
- entities with no real behavior
- all rules buried in procedural use case code

That often weakens the domain model.

### Better balance
- use DTOs for transport
- keep domain rules in entities/domain services
- let use cases orchestrate

---

## 39. Common mistake: giant orchestration classes

If one use case coordinates:
- many repositories
- many services
- many branches
- many unrelated workflows

it may be doing too much.

This can signal:
- weak decomposition
- missing smaller abstractions
- poor cohesion
- hidden multiple use cases inside one class

---

## 40. Testing use cases vs entities vs DTOs

### Entities
Usually tested for business rules and invariants.

### Use cases
Usually tested for workflow orchestration and interaction with ports.

### DTOs
Usually do not need deep behavioral testing unless they contain validation or serialization-specific logic.

### Why this matters
The test focus changes depending on the role of the object.

---

## 41. Example test boundaries

Entity test:

```python
def test_shipped_order_cannot_be_cancelled():
    order = Order(order_id=1, status="shipped")

    with pytest.raises(ValueError):
        order.cancel()
```

Use case test:

```python
def test_cancel_order_use_case_saves_cancelled_order():
    repo = FakeOrderRepository(...)
    use_case = CancelOrderUseCase(repo)

    use_case.execute(1)

    assert repo.saved_order.status == "cancelled"
```

### Why this is good
Each test targets the responsibility of the unit under test.

---

## 42. Practical mental model

A useful mental model is:

- **Use case** → “What application action is being executed?”
- **Orchestration** → “What steps must happen, and in what order?”
- **Entity** → “What business object and business rules are involved?”
- **DTO** → “How is data packaged across this boundary?”

That distinction is enough to clean up a lot of architecture confusion.

---

## 43. Decision heuristic

When deciding where code belongs, ask:

### Is this transport data?
Probably a DTO.

### Is this business identity + business rule behavior?
Probably an entity.

### Is this coordinating a workflow?
Probably a use case.

### Is this deciding a domain rule?
Probably domain logic, likely in an entity or domain service.

These questions are often enough to place code correctly.

---

## 44. Final recommendation

A practical design should aim for:

- use cases that clearly express application actions
- orchestration in the application layer
- entities that hold real business behavior
- DTOs that carry data across boundaries cleanly
- explicit mapping when boundaries differ
- enough separation to keep responsibilities clear
- not so much ceremony that the code becomes heavy

If your design makes it easy to answer:
- what is the workflow?
- what is the business rule?
- what is just transported data?

then it is probably on the right track.

---

## 45. Quick summary

If you only keep the essentials:

1. A use case represents a meaningful application action.
2. Orchestration is the coordination of steps in that application workflow.
3. Entities represent domain objects with identity and business behavior.
4. DTOs are data carriers used to cross boundaries cleanly.
5. Entities and DTOs are not the same: entities model business meaning, DTOs model transported data.

---


# Dependency Injection and Wiring in FastAPI

## 1. Goal

This guide explains how **dependency injection** and **wiring** work in **FastAPI**.

It focuses on:

- what dependency injection means in FastAPI
- the `Depends()` mechanism
- function dependencies
- class-based dependencies
- dependencies with `yield`
- global and router-level dependencies
- request-scoped caching behavior
- project wiring patterns for medium and large apps
- test overrides
- practical recommendations

The goal is to help you move from “I know `Depends` exists” to “I know how to structure a real FastAPI app around it.”

---

## 2. What dependency injection means in FastAPI

In FastAPI, dependency injection means your path operation functions can declare what they need, and FastAPI will resolve and provide those dependencies for you.

In simple terms:

> Your endpoint says what it needs.  
> FastAPI figures out how to provide it.

This is one of FastAPI’s most important design features.

---

## 3. Why it matters

FastAPI’s dependency system is useful because many APIs repeatedly need things like:

- database sessions
- current authenticated user
- permission checks
- query parameter parsing
- tenant or account context
- reusable service objects
- request-scoped resources

Without a dependency system, that logic would often be duplicated across many endpoints.

---

## 4. Core building block: `Depends`

The main tool is `Depends()`.

A dependency is usually a callable:
- function
- class
- callable object

FastAPI will call it and inject its result into the endpoint or into another dependency.

Basic example:

```python
from fastapi import Depends, FastAPI

app = FastAPI()


def get_message():
    return "hello"


@app.get("/")
def read_root(message: str = Depends(get_message)):
    return {"message": message}
```

### What happens here
- FastAPI sees that `read_root()` depends on `get_message`
- it calls `get_message()`
- it injects the returned value into `message`

---

## 5. Why this is useful

This pattern lets you move reusable logic out of endpoints.

Instead of repeating:
- authentication checks
- DB session creation
- header validation
- service construction

you centralize them as dependencies.

That usually improves:
- reuse
- readability
- testability
- consistency

---

## 6. Function dependencies

The most common dependencies are plain functions.

Example:

```python
from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()


def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="Invalid token")


@app.get("/items")
def read_items(_: None = Depends(verify_token)):
    return [{"id": 1}, {"id": 2}]
```

### Why useful
This keeps validation logic reusable and separate from the endpoint’s main purpose.

---

## 7. Dependency return values

A dependency can either:

- return a value to be injected
- or perform a check / side effect and return nothing meaningful

Example returning a value:

```python
def get_current_user():
    return {"id": 1, "username": "janette"}
```

Then:

```python
@app.get("/me")
def read_me(user = Depends(get_current_user)):
    return user
```

Example using a dependency mainly for validation:

```python
@app.get("/secure")
def secure_route(_: None = Depends(verify_token)):
    return {"ok": True}
```

Both patterns are valid.

---

## 8. Sub-dependencies

Dependencies can depend on other dependencies.

This is one of the strongest parts of the system.

Example:

```python
from fastapi import Depends


def get_db():
    return "db-session"


def get_user(db = Depends(get_db)):
    return {"username": "janette", "db": db}
```

### Why this matters
You can build layered dependency chains like:
- DB session
- repository
- service
- authenticated user
- permission check

This creates a clean composition model.

---

## 9. Class-based dependencies

FastAPI also supports classes as dependencies.

The class is instantiated and the instance is injected.

Example:

```python
from fastapi import Depends


class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit
```

Usage:

```python
@app.get("/items")
def read_items(params: CommonQueryParams = Depends(CommonQueryParams)):
    return {
        "q": params.q,
        "skip": params.skip,
        "limit": params.limit,
    }
```

### Why useful
Class-based dependencies can group related injected values into one object.

This is especially useful when several parameters belong together conceptually.

---

## 10. When class-based dependencies are helpful

Class-based dependencies are often helpful when:
- you want a small query/filter object
- multiple related request parameters belong together
- you want a reusable parameter bundle
- you want light object-oriented grouping without building a full service layer

### Important
Do not use them just because they are possible.  
Use them when they make the dependency clearer.

---

## 11. Prefer explicit grouping, not random bundling

A class-based dependency should represent something meaningful.

Good example:
- common pagination parameters
- filter object
- auth context object

Less good example:
- arbitrary unrelated values grouped together only to “reduce parameters”

The goal is clearer structure, not hiding too much.

---

## 12. Annotated style

FastAPI documentation strongly encourages the `Annotated` style when possible.

Example:

```python
from typing import Annotated
from fastapi import Depends

CurrentUser = Annotated[dict, Depends(get_current_user)]


@app.get("/me")
def read_me(user: CurrentUser):
    return user
```

### Why useful
This can make endpoint signatures cleaner and more reusable, especially in larger codebases.

---

## 13. Dependencies with `yield`

Some dependencies need setup and teardown.

For those cases, FastAPI supports dependencies with `yield`.

Classic example: database sessions.

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Usage:

```python
@app.get("/users")
def list_users(db = Depends(get_db)):
    return {"db": str(db)}
```

### Why this matters
FastAPI can run setup before the endpoint and cleanup afterward.

This is one of the most important real-world dependency patterns.

---

## 14. Why `yield` dependencies are powerful

They are useful for resources that need managed lifecycle, such as:

- database sessions
- temporary connections
- transaction contexts
- cleanup-sensitive resources
- timing or tracing contexts

This gives you a very practical request-scoped setup/teardown mechanism.

---

## 15. `yield` dependencies are similar to context managers

Any callable pattern that would work as a context manager or async context manager is conceptually aligned with FastAPI’s `yield` dependencies.

That is why they feel natural for resource management.

### Practical idea
Think of them as request-aware dependency-managed context lifecycles.

---

## 16. Dependency scope for `yield` dependencies

FastAPI’s `Depends()` supports a `scope` parameter, especially relevant for `yield` dependencies.

The documented values are:

- `"function"`
- `"request"`

### Meaning
- `"function"`: lifecycle wraps the path operation function and ends before the response is sent
- `"request"`: lifecycle wraps the full request/response cycle and ends after the response is sent

This gives you more control over teardown timing.

---

## 17. Dependency caching within a request

By default, FastAPI caches dependency results within the same request.

This means:
- if the same dependency is declared multiple times in one request
- FastAPI will generally call it once
- then reuse the resolved value

### Why useful
This avoids unnecessary repeated work during one request.

Example use case:
- current user lookup used by several downstream dependencies
- shared DB session reused inside the same request graph

---

## 18. `use_cache=False`

If you do **not** want this per-request caching behavior, `Depends()` supports:

```python
Depends(dependency, use_cache=False)
```

### Why useful
This is helpful when:
- you explicitly want a fresh dependency resolution each time
- the dependency is not meant to be reused
- repeated side effects or recalculation are actually desired

Use it intentionally.  
The default caching is often the right behavior.

---

## 19. Global dependencies

FastAPI allows dependencies at the application level.

Example:

```python
from fastapi import Depends, FastAPI

app = FastAPI(dependencies=[Depends(verify_token)])
```

### What this means
The dependency is applied to all path operations in the app.

### Good use cases
- global token/header checks
- organization-wide request validation
- request-level guards that apply everywhere

### Caution
Global dependencies are powerful, but can make behavior more implicit if overused.

---

## 20. Router-level dependencies

You can also apply dependencies at the router level.

Example:

```python
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(verify_token)]
)
```

### Why useful
This is often a better middle ground than global dependencies.

It lets you enforce shared behavior for:
- admin routes
- internal APIs
- billing routes
- protected sections

without affecting the whole application.

---

## 21. Endpoint-level dependencies

And of course, dependencies can be attached directly to one endpoint.

Example:

```python
@app.get("/secure", dependencies=[Depends(verify_token)])
def secure_route():
    return {"ok": True}
```

### Practical hierarchy
You can think of FastAPI dependency placement like this:

- app-level
- router-level
- endpoint parameter injection
- sub-dependencies

Choosing the right level helps keep the app understandable.

---

## 22. Bigger applications: organizing dependencies

FastAPI’s “bigger applications” guidance explicitly recommends moving shared dependencies into dedicated modules, commonly something like:

```text
app/
├── main.py
├── dependencies.py
├── routers/
│   ├── users.py
│   └── items.py
```

### Why this helps
Shared dependency logic quickly becomes important in medium-sized apps.

Examples:
- `get_db`
- `get_current_user`
- `get_current_admin`
- `get_settings`
- common parameter objects

Keeping them in one clear place improves maintainability.

---

## 23. A practical FastAPI wiring structure

A common practical structure for a medium or large FastAPI project is:

```text
app/
├── main.py
├── core/
│   ├── config.py
│   └── security.py
├── dependencies.py
├── domain/
├── application/
├── infrastructure/
│   ├── db.py
│   ├── repositories/
│   └── clients/
└── routers/
    ├── users.py
    └── orders.py
```

### Possible responsibility split
- `main.py` → app creation and router inclusion
- `dependencies.py` → reusable FastAPI dependencies
- `infrastructure/` → concrete repos, DB clients, adapters
- `application/` → use cases
- `domain/` → business logic

This keeps wiring concerns separate from business logic.

---

## 24. What “wiring” means in FastAPI

In this context, **wiring** means:

> deciding how concrete objects are assembled and injected into the application flow

Examples:
- how `get_db()` creates a session
- how a repository is built from that session
- how a use case is built from that repository
- how an endpoint receives that use case

This is where FastAPI dependencies become architectural tools, not just convenience helpers.

---

## 25. Example of wiring a repository and use case

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_repository(db = Depends(get_db)):
    return SqlAlchemyUserRepository(db)


def get_register_user_use_case(
    repo = Depends(get_user_repository),
):
    return RegisterUserUseCase(repo)
```

Endpoint:

```python
@app.post("/users")
def register_user(payload: dict, use_case = Depends(get_register_user_use_case)):
    use_case.execute(payload)
    return {"status": "ok"}
```

### Why this is good
The endpoint stays thin.  
The wiring logic is explicit and reusable.

---

## 26. Why this style helps architecture

A dependency graph like:

- DB session
- repository
- service/use case
- endpoint

helps because:
- controllers stay thin
- construction logic is centralized
- dependencies are testable
- infrastructure stays replaceable
- application logic remains easier to isolate

This is one of the strongest ways to use FastAPI dependencies well.

---

## 27. Keep endpoints thin

A healthy FastAPI endpoint often does only a few things:

- receive validated input
- call a wired dependency/use case
- return the result or translate it to response shape

It should not usually:
- build all dependencies manually
- embed heavy orchestration
- do raw DB code directly
- duplicate dependency logic that already exists elsewhere

Thin endpoints are one of the cleanest outcomes of proper DI and wiring.

---

## 28. Dependency injection vs global singletons

A common temptation is to avoid proper dependency wiring by using:
- global state
- module-level singletons
- hidden service locators

FastAPI’s dependency system gives you a much cleaner alternative.

### Why DI is better here
It makes dependencies:
- explicit
- replaceable
- testable
- easier to reason about

This is especially important in growing APIs.

---

## 29. FastAPI dependency overrides in tests

FastAPI supports test overrides through:

```python
app.dependency_overrides
```

Example:

```python
def override_get_current_user():
    return {"id": 999, "username": "test-user"}


app.dependency_overrides[get_current_user] = override_get_current_user
```

### Why this matters
This is one of the best testing features in FastAPI.

It lets you replace:
- auth dependencies
- DB dependencies
- service dependencies
- external API dependencies

without changing production code.

---

## 30. Example: override repository dependency in tests

```python
def override_get_user_repository():
    return InMemoryUserRepository()


app.dependency_overrides[get_user_repository] = override_get_user_repository
```

### Why useful
Your endpoint tests can now run with:
- fake repositories
- in-memory stores
- stubbed integrations

instead of real infrastructure.

This greatly improves test speed and reliability.

---

## 31. Dependency injection and security

FastAPI uses the same dependency mechanism heavily for security flows.

Examples:
- current user extraction
- OAuth2 token parsing
- permission checks
- role guards

This is one reason understanding dependencies is so important in FastAPI.  
It is not a side feature. It is a central architectural mechanism.

---

## 32. Parameterized dependencies

FastAPI also supports advanced/parameterized dependency patterns.

These are useful when:
- one dependency pattern has configurable behavior
- you want reusable guards or validators
- you want “dependency factories” that produce dependencies

This is especially useful for:
- role checks
- feature checks
- query requirements
- reusable policy patterns

---

## 33. Example of a parameterized dependency

```python
from fastapi import Depends, HTTPException


def require_role(required_role: str):
    def checker(user = Depends(get_current_user)):
        if user["role"] != required_role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return checker
```

Usage:

```python
@app.get("/admin")
def admin_dashboard(user = Depends(require_role("admin"))):
    return {"message": "Welcome admin"}
```

### Why useful
This avoids duplicating permission logic while keeping it configurable.

---

## 34. Common mistakes

### 1. Putting too much business logic inside dependencies
Dependencies are for wiring, reusable guards, and context resolution—not for turning everything into hidden workflow logic.

### 2. Making dependencies too magical
If it becomes hard to understand where objects come from, the wiring has become too implicit.

### 3. Using global dependencies everywhere
This can make behavior harder to trace.

### 4. Building everything directly inside endpoints
This defeats much of the value of the dependency system.

### 5. Forgetting that dependencies are cached per request by default
This can surprise people if they expected repeated recalculation.

### 6. Mixing framework dependencies deep into the domain
FastAPI-specific constructs should usually stay near the delivery/application wiring edge.

---

## 35. Best practices

### 1. Use dependencies for reusable request-scoped concerns
Examples: DB sessions, auth context, repositories, use cases.

### 2. Keep endpoints thin
Let dependencies assemble what the endpoint needs.

### 3. Organize shared dependencies in dedicated modules
This scales better than scattering them across routers.

### 4. Prefer explicit wiring over hidden magic
A slightly longer but understandable dependency chain is often better than mysterious globals.

### 5. Use `yield` dependencies for managed resources
Especially DB sessions and request-scoped resources.

### 6. Use overrides in tests
This is one of FastAPI’s strongest testing patterns.

### 7. Use router-level dependencies for shared route sections
It is often cleaner than making everything global.

---

## 36. A practical wiring example

```python
from fastapi import Depends, FastAPI

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_order_repository(db = Depends(get_db)):
    return SqlAlchemyOrderRepository(db)


def get_cancel_order_use_case(
    repo = Depends(get_order_repository),
):
    return CancelOrderUseCase(repo)


@app.post("/orders/{order_id}/cancel")
def cancel_order(
    order_id: int,
    use_case = Depends(get_cancel_order_use_case),
):
    use_case.execute(order_id)
    return {"status": "cancelled"}
```

### Why this is a strong pattern
- endpoint is thin
- construction is explicit
- repository wiring is reusable
- DB lifecycle is managed safely
- testing is easier through overrides

---

## 37. Practical mental model

A useful mental model is:

- **dependency injection** = “declare what this function needs”
- **wiring** = “define how those dependencies are assembled”
- **FastAPI dependencies** = the mechanism that connects those two

Examples:
- endpoint declares it needs a use case
- use case dependency declares it needs a repository
- repository dependency declares it needs a DB session
- FastAPI resolves the chain

That is the core idea.

---

## 38. Final recommendation

A practical FastAPI dependency strategy is usually:

- use plain function dependencies first
- use class-based dependencies when grouping really helps
- use `yield` for managed resources
- keep reusable dependencies in dedicated modules
- wire repositories and use cases through dependency chains
- keep endpoints thin
- use dependency overrides in tests

This turns FastAPI’s dependency system from a convenience feature into a strong architectural tool.

---

## 39. Quick summary

If you only keep the essentials:

1. FastAPI’s dependency injection system is based on `Depends()`.
2. Dependencies can be functions, classes, and sub-dependencies.
3. `yield` dependencies are essential for setup/teardown patterns like DB sessions.
4. Dependencies are cached per request by default unless `use_cache=False` is used.
5. Good wiring means endpoints stay thin while repositories, services, and use cases are assembled through explicit dependency chains.

---

# Domain, Contract, and End-to-End Tests

## 1. Goal

This guide explains three important testing categories:

- **domain tests**
- **contract tests**
- **end-to-end tests**

It focuses on:

- what each test type is
- what each one should verify
- how they differ from each other
- where they fit in a layered architecture
- common mistakes
- practical Python-oriented examples

The goal is to help you understand what each test type is for, so you can build a test strategy with clearer responsibilities instead of mixing everything into one giant test layer.

---

## 2. Why these three test types matter together

These three test types often correspond to different architectural concerns:

- **domain tests** protect business rules
- **contract tests** protect boundaries and expectations between components
- **end-to-end tests** protect real user/system flows across the whole stack

If you do not distinguish them clearly, common problems appear:

- too many slow tests
- too few tests around business rules
- brittle integration-heavy test suites
- repeated coverage of the same thing
- confusion about what a failing test actually means

That is why these categories are worth separating.

---

## 3. A useful mental model

A practical mental model is:

- **domain tests** ask:  
  “Are the business rules correct?”

- **contract tests** ask:  
  “Do two sides of a boundary still agree on the expected interaction?”

- **end-to-end tests** ask:  
  “Does the full system work from the outside like a real user or client expects?”

This distinction is the core of the whole topic.

---

# Domain Tests

## 4. What a domain test is

A **domain test** verifies business logic in the domain layer.

Typical things tested here:

- invariants
- business rules
- entity behavior
- value object rules
- domain services
- allowed and forbidden state transitions

### In simple terms
A domain test checks whether the system’s business meaning is correct.

---

## 5. Why domain tests are valuable

Domain tests are often among the highest-value tests because they are usually:

- fast
- focused
- deterministic
- framework-independent
- cheap to maintain
- close to the real business rules

If a business rule is important, domain tests are often the most direct and reliable place to protect it.

---

## 6. Example domain rule

Suppose the business rule is:

> “A shipped order cannot be cancelled.”

Entity:

```python
class Order:
    def __init__(self, status: str = "pending") -> None:
        self.status = status

    def cancel(self) -> None:
        if self.status == "shipped":
            raise ValueError("A shipped order cannot be cancelled")
        self.status = "cancelled"
```

Domain test:

```python
import pytest


def test_shipped_order_cannot_be_cancelled():
    order = Order(status="shipped")

    with pytest.raises(ValueError):
        order.cancel()
```

### Why this is a domain test
It verifies a business rule directly, without involving:
- HTTP
- databases
- frameworks
- messaging
- external services

---

## 7. What domain tests should usually avoid

Domain tests should usually avoid:
- real databases
- web servers
- external APIs
- queue brokers
- framework-specific setup
- slow infrastructure

### Why?
Because the purpose is to verify domain behavior, not technical integration.

If a domain test needs half the system to start up, it is probably no longer a pure domain test.

---

## 8. Domain tests are not “small because they are tiny”

A common misunderstanding is that domain tests are valuable only because they are “unit tests.”

That is not the most important reason.

The real value is that they directly protect:
- rules
- invariants
- core business meaning

They are usually small because the domain should be reasonably isolated, but their value comes from what they protect.

---

## 9. Good candidates for domain tests

Strong candidates include:

- entity methods
- value object validation
- state transitions
- domain service rules
- pricing rules
- discount rules
- eligibility rules
- calculations with business meaning

If the logic is part of the business language of the system, it is probably a good candidate.

---

## 10. Common domain test mistake

A common mistake is to move business rules into controllers, repositories, or infrastructure services.

When that happens:
- domain tests become harder to write
- business logic ends up tested only indirectly
- important rules become buried in slower tests

That often weakens the whole test strategy.

---

# Contract Tests

## 11. What a contract test is

A **contract test** verifies that two sides of a boundary still agree on how they interact.

That boundary might be between:

- application core and adapter
- service and external API
- producer and consumer
- repository port and repository adapter
- HTTP client and remote service
- event publisher and subscriber schema

### In simple terms
A contract test checks that:

> “This component still matches the expected interface, shape, or behavior at the boundary.”

---

## 12. Why contract tests matter

Contract tests are valuable because systems often fail not only from internal logic bugs, but from mismatches between components.

Examples:
- the provider changed a response field name
- the consumer expects a different schema
- the repository adapter no longer satisfies the expected port behavior
- an event payload changed shape
- an HTTP endpoint contract drifted

Contract tests help catch that kind of breakage earlier.

---

## 13. Contract tests are boundary tests

A contract test is usually less about:
- business meaning in isolation

and more about:
- interface agreement
- data shape agreement
- semantic agreement at the integration seam

This is what makes them different from both domain tests and full end-to-end tests.

---

## 14. Port and adapter contract example

Suppose the application defines this port:

```python
from typing import Protocol


class UserRepository(Protocol):
    def get_by_id(self, user_id: int) -> dict | None:
        ...
```

And you build an adapter:

```python
class InMemoryUserRepository:
    def __init__(self) -> None:
        self.users = {1: {"id": 1, "username": "janette"}}

    def get_by_id(self, user_id: int) -> dict | None:
        return self.users.get(user_id)
```

A contract test can verify that the adapter satisfies the expected repository behavior.

Example:

```python
def test_user_repository_returns_expected_shape():
    repo = InMemoryUserRepository()

    user = repo.get_by_id(1)

    assert user == {"id": 1, "username": "janette"}
```

### Why this is a contract-style test
It checks boundary expectations between:
- what the application expects
- what the adapter actually returns

---

## 15. HTTP contract example

Suppose your service depends on an external API returning:

```json
{
  "rate": 17.2
}
```

Your adapter expects that shape.

A contract test can validate that the response shape still matches expectations.

Example idea:

```python
def test_exchange_rate_response_contract():
    payload = {"rate": 17.2}

    assert "rate" in payload
    assert isinstance(payload["rate"], (int, float))
```

In more realistic scenarios, contract tests may validate:
- response fields
- field types
- required keys
- status code expectations
- event/message schema compatibility

---

## 16. Consumer-driven contract perspective

A helpful concept is **consumer-driven contract testing**.

This means:
- the consumer defines the contract it needs
- the provider is checked against that expectation

### Why useful
It helps ensure that the provider can change safely without breaking the consumer unexpectedly.

This concept appears often in:
- API integrations
- event-driven systems
- microservices

---

## 17. Event/message contract example

Suppose your application publishes messages like:

```python
{
    "event_type": "user_registered",
    "user_id": 123,
    "email": "janette@example.com"
}
```

A contract test can verify that:
- required fields exist
- types are correct
- schemas remain stable enough for consumers

Example:

```python
def test_user_registered_event_contract():
    event = {
        "event_type": "user_registered",
        "user_id": 123,
        "email": "janette@example.com",
    }

    assert event["event_type"] == "user_registered"
    assert isinstance(event["user_id"], int)
    assert isinstance(event["email"], str)
```

---

## 18. What contract tests should usually not become

Contract tests should not become:
- giant full-stack user-flow tests
- vague “integration tests” with no clear contract boundary
- tests that assert many unrelated business rules at once

A contract test should be focused on:
- a boundary
- an agreement
- compatibility

That focus is what gives it value.

---

## 19. Good contract test candidates

Strong candidates include:

- request/response schemas
- event payload schemas
- repository port behavior expectations
- adapter behavior expectations
- serialization contracts
- external API integration assumptions

If two components rely on a shared expectation, that expectation is a good contract-test candidate.

---

## 20. Common contract test mistake

A common mistake is writing contract tests that are too weak.

Example weak test:
- only checks status code `200`

But ignores:
- response fields
- response meaning
- required schema shape

A useful contract test must actually protect the agreed boundary.

---

# End-to-End Tests

## 21. What an end-to-end test is

An **end-to-end test** verifies a full system flow from the outside, as realistically as possible.

It usually exercises:
- real entry points
- real infrastructure or realistic environments
- real integration paths across multiple layers

### In simple terms
An end-to-end test asks:

> “Does the system work for a real user or real client across the full path?”

---

## 22. Why end-to-end tests matter

End-to-end tests are valuable because some failures only appear when the full system is assembled.

Examples:
- routing problems
- serialization problems
- auth problems
- infrastructure wiring problems
- database migrations issues
- bad integration between layers
- missing environment configuration
- deployment-specific issues

These problems may not appear in isolated tests.

---

## 23. Example end-to-end flow

Suppose the flow is:

1. user sends an HTTP request to register
2. request passes validation
3. application use case executes
4. data is saved in the database
5. a welcome email event is published
6. response is returned

An end-to-end test may hit the real HTTP endpoint and verify the full flow.

---

## 24. End-to-end test example idea

For an API, an end-to-end test might conceptually do this:

```python
def test_register_user_e2e():
    response = client.post("/users", json={
        "username": "janette",
        "email": "janette@example.com"
    })

    assert response.status_code == 201
    assert response.json()["username"] == "janette"
```

In a true end-to-end scenario, the test would ideally run against:
- the real app
- real routing
- real validation
- real persistence
- realistic external dependencies or controlled test infrastructure

### Why this is end-to-end
It verifies the externally visible system behavior, not just one internal unit.

---

## 25. What end-to-end tests are good at

End-to-end tests are especially good at detecting:

- broken wiring
- missing config
- route/controller mistakes
- serialization mismatches
- DB/integration failures
- full workflow regressions
- infrastructure behavior issues

They answer:
- “Does the system actually work as assembled?”

That is something unit-style tests cannot fully guarantee.

---

## 26. Why end-to-end tests are not enough alone

If you only rely on end-to-end tests, problems appear:

- the suite becomes slower
- debugging failures is harder
- rule coverage may become indirect and fragile
- tests become more expensive to maintain
- business rules may not be protected directly

That is why end-to-end tests should complement, not replace:
- domain tests
- contract tests
- other focused test layers

---

## 27. End-to-end tests are usually fewer

Because they are:
- slower
- broader
- more expensive
- more environment-sensitive

end-to-end tests are usually fewer in number than domain tests.

### Practical strategy
Use end-to-end tests for:
- critical flows
- key integrations
- confidence that the assembled system works

Do not try to test every tiny rule only through end-to-end scenarios.

---

## 28. Common end-to-end test mistake

A common mistake is writing too many end-to-end tests to compensate for poor lower-level testing.

That often leads to:
- slow CI
- flaky tests
- duplicated scenario coverage
- difficult debugging

If every rule is only tested through E2E, the test pyramid becomes unbalanced.

---

# Comparing the three

## 29. Domain vs contract vs end-to-end

### Domain tests
Protect business rules directly.

### Contract tests
Protect agreements at boundaries.

### End-to-end tests
Protect the full real system flow.

### Practical difference
They answer different questions, so they should not be treated as interchangeable.

---

## 30. Example mapping by architecture layer

### Domain tests
Usually target:
- entities
- value objects
- domain services

### Contract tests
Usually target:
- adapters
- schemas
- ports
- message formats
- provider/consumer seams

### End-to-end tests
Usually target:
- full application entry points
- full request-to-response flows
- real system integration behavior

---

## 31. A practical layered example

Suppose you have:
- domain: `Order.cancel()`
- application: `CancelOrderUseCase`
- infrastructure: `SqlAlchemyOrderRepository`
- API: FastAPI route `/orders/{id}/cancel`

You might test this like:

### Domain test
Verify shipped orders cannot be cancelled.

### Contract test
Verify repository adapter returns data in the shape the use case expects.

### End-to-end test
Call the real API endpoint and verify order cancellation works through the whole stack.

This is a strong layered testing approach.

---

## 32. Why this separation helps debugging

If a test fails, the layer tells you a lot about the probable problem.

### Domain test failure
Likely a business-rule bug.

### Contract test failure
Likely a mismatch between components or schemas.

### End-to-end failure
Could be wiring, integration, environment, or broad system behavior.

This is one of the biggest operational benefits of having clear test categories.

---

## 33. Test speed intuition

A rough intuition is:

- domain tests are usually the fastest
- contract tests are often medium-cost
- end-to-end tests are usually the slowest

This is not a law, but it is a useful planning intuition.

---

## 34. Test maintenance intuition

Another useful intuition:

- domain tests are often the cheapest to maintain
- contract tests are valuable when boundaries are meaningful and stable
- end-to-end tests are often the most expensive to maintain

This is why test balance matters.

---

## 35. Common mistake: vague “integration tests”

Many teams call everything that is not a tiny unit test an “integration test.”

That can make the test strategy unclear.

### Why this is a problem
It hides important differences between:
- boundary agreement tests
- full system flow tests
- infrastructure adapter tests

A clearer taxonomy usually improves both communication and strategy.

---

## 36. Domain tests and over-mocking

A domain test should usually need very little or no mocking.

If a supposed domain test requires:
- network stubs
- DB patches
- framework mocks
- many collaborators

then it may not actually be a domain test anymore.

That is often a design or classification smell.

---

## 37. Contract tests and realism

A contract test should be realistic enough to protect the real boundary.

That means the contract should not be:
- too vague
- too minimal
- too idealized
- disconnected from what the real consumer/provider expects

Otherwise it becomes false reassurance.

---

## 38. End-to-end tests and flakiness

End-to-end tests are especially vulnerable to flakiness if:
- they depend on unstable external services
- environments are inconsistent
- test data is not isolated
- timing assumptions are weak
- shared state leaks between tests

### Practical lesson
Critical E2E tests should be:
- controlled
- isolated
- intentional
- not overly numerous

---

## 39. Best practices

### 1. Put business rules under direct domain tests
Do not rely only on indirect coverage.

### 2. Use contract tests at real boundaries
Protect schema and interface agreements where systems meet.

### 3. Keep end-to-end tests for critical flows
Use them for confidence in the assembled system.

### 4. Do not collapse everything into one test type
Different questions need different tests.

### 5. Keep the test suite balanced
Fast focused tests plus fewer broad tests is often a strong strategy.

### 6. Use failures diagnostically
The type of failing test tells you where to look first.

---

## 40. A practical testing mix

A healthy test strategy often looks like:

- many domain tests
- a meaningful number of contract tests where boundaries matter
- a smaller number of high-value end-to-end tests for critical flows

This balance gives:
- good feedback speed
- good rule protection
- good integration confidence

---

## 41. Practical mental model

A useful mental model is:

- **domain tests** protect correctness of the business core
- **contract tests** protect compatibility at seams
- **end-to-end tests** protect real-world system behavior

That distinction is enough to design a much clearer test strategy.

---

## 42. Final recommendation

A strong testing approach should not ask:

> “Which one of these test types is best?”

A better question is:

> “Which risk does each test type protect?”

A practical answer is:

- domain tests protect business meaning
- contract tests protect agreements between components
- end-to-end tests protect real assembled workflows

Using all three intentionally usually gives much better coverage than trying to force one kind of test to do everything.

---

## 43. Quick summary

If you only keep the essentials:

1. Domain tests verify business rules directly.
2. Contract tests verify agreements at boundaries between components or systems.
3. End-to-end tests verify the full system flow from the outside.
4. These test types solve different problems and should not be treated as interchangeable.
5. A strong test strategy usually combines many domain tests, targeted contract tests, and fewer high-value end-to-end tests.

---
