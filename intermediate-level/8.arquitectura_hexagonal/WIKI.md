# Clean Architecture and FastAPI

## 1. Purpose

This wiki gives a medium-length overview of five connected architecture topics:

- layers: domain, application, and infrastructure
- ports (`interfaces` / `Protocol`) and adapters (SQL, HTTP, messaging)
- use cases and orchestration; DTOs vs entities
- dependency injection and wiring in FastAPI
- domain, contract, and end-to-end tests

These topics belong together because they all answer one practical question:

> How do you build a Python application that stays understandable, replaceable, and testable as it grows?

The goal is not to force one rigid architecture style.  
The goal is to explain the responsibilities of each piece and how they fit together in a real Python + FastAPI project.

---

## 2. The big picture

A useful high-level model is:

- **domain** = business meaning
- **application** = workflows and use cases
- **infrastructure** = technical implementation details
- **delivery layer** = how the outside world talks to the app, often through FastAPI routes

And a second useful model is:

- **ports** define capabilities the core needs or exposes
- **adapters** implement those capabilities using real technologies

When you combine those two views, you get a practical architecture where:
- business rules stay near the center
- framework and database details stay near the edges
- testing becomes easier because responsibilities are clearer

---

# Part I — Layers: Domain, Application, and Infrastructure

## 3. Why layers exist

As systems grow, code often becomes hard to change because different concerns get mixed together.

Typical symptoms:
- business rules are buried in route handlers
- use cases know too much about SQL or HTTP details
- infrastructure logic leaks into domain objects
- tests require too much setup for simple business rules

Layering exists to reduce that entanglement.

The idea is not just “put files in different folders.”  
The idea is to separate **responsibilities** and control **dependency direction**.

---

## 4. Domain layer

### What it is
The domain layer contains the core business concepts and business rules.

Typical domain elements:
- entities
- value objects
- domain services
- invariants
- domain exceptions
- domain events in some designs

### What it should answer
The domain should answer:

> What is true in the business?

### Example responsibilities
- an order can be cancelled only in certain states
- a discount cannot exceed a business limit
- a balance cannot go below allowed constraints

### What should not be there
The domain should usually not know about:
- FastAPI
- SQLAlchemy sessions
- HTTP request objects
- JSON response formatting
- message broker clients

Those are outer technical concerns.

---

## 5. Application layer

### What it is
The application layer coordinates use cases.

It expresses things like:
- register user
- cancel order
- approve invoice
- send welcome notification
- generate report

### What it should answer
The application layer should answer:

> What workflow is being executed?

### Typical responsibilities
- loading domain objects
- invoking domain behavior
- coordinating repositories and gateways
- managing transaction boundaries
- deciding what the use case returns

### Important distinction
The application layer is about **orchestration**, not about low-level infrastructure details and not about replacing the domain’s core rules.

---

## 6. Infrastructure layer

### What it is
The infrastructure layer contains technical implementations.

Typical examples:
- repository implementations
- ORM mapping
- external API clients
- message publishers
- email senders
- file storage
- cache adapters

### What it should answer
Infrastructure should answer:

> How is this done technically?

### Why it should stay outside
Databases, HTTP clients, and brokers change more easily than business meaning.  
That is why infrastructure should depend inward on the application/domain contracts rather than the reverse.

---

## 7. Delivery layer

Although not always listed as a “core” layer, it is useful to call out the delivery edge explicitly.

Examples:
- FastAPI routes
- CLI commands
- queue consumers
- schedulers

Its job is to:
- receive external input
- call the appropriate application logic
- return or emit output

In FastAPI projects, this is where the web framework lives.

---

# Part II — Ports and Adapters

## 8. What ports are

A **port** is a capability contract.

Examples:
- “find user by id”
- “save order”
- “send notification”
- “publish event”
- “fetch exchange rate”

Ports define what the core needs without saying how it is implemented.

In Python, ports are often represented with:
- `Protocol`
- abstract base classes
- small callable contracts

A very Pythonic default is `Protocol` because it supports structural typing without forcing inheritance.

---

## 9. What adapters are

An **adapter** is the concrete implementation that connects a port to a real system.

Examples:
- SQL adapter for a repository
- HTTP adapter for an external API
- messaging adapter for an event publisher

The adapter translates between:
- the core’s expected behavior
- the real technical API of the outside system

This is one of the most useful practical boundaries in architecture.

---

## 10. SQL adapters

A SQL adapter typically implements a repository-like port using:
- SQLite
- PostgreSQL
- SQL Server
- SQLAlchemy
- direct driver access

Example responsibilities:
- queries
- inserts and updates
- row-to-domain mapping
- transaction participation

A SQL adapter should not be where core business rules live.  
Its job is persistence, not business meaning.

---

## 11. HTTP adapters

HTTP adapters can exist in two directions:

### Inbound HTTP adapter
This is how an HTTP request enters the app.
In a FastAPI project, routes often play this role.

### Outbound HTTP adapter
This is how the app calls an external API.

For example:
- payment provider
- exchange-rate service
- third-party identity service

The same architectural idea applies in both directions:
- the core works with a stable capability
- the adapter handles HTTP details

---

## 12. Messaging adapters

Messaging adapters connect the application to:
- Kafka
- RabbitMQ
- Redis streams
- internal event buses
- other broker-based systems

Typical responsibilities:
- publish a message
- consume a message
- transform payloads
- deal with broker-specific behavior

Again, the adapter should isolate technical messaging concerns from business logic.

---

## 13. Why ports and adapters help

This structure helps because it:
- reduces coupling
- makes testing easier
- supports replacement of infrastructure
- makes the core easier to reason about
- prevents framework or SDK details from leaking everywhere

A practical shortcut is:

- **port** = what capability is needed
- **adapter** = how that capability is implemented

---

# Part III — Use Cases, Orchestration, DTOs, and Entities

## 14. What a use case is

A use case is a meaningful application action.

Examples:
- create account
- cancel order
- update subscription
- resend invoice
- mark shipment as delivered

A use case usually:
- receives structured input
- loads domain objects
- calls domain behavior
- uses gateways/repositories
- returns structured output

This makes the application flow explicit.

---

## 15. What orchestration means

Orchestration is the coordination of steps in a workflow.

For example:
1. load order
2. validate user permission
3. call `order.cancel()`
4. save changes
5. publish event
6. return response model

That is orchestration.

The important distinction is:

- **domain** decides what is valid
- **application** decides how the workflow is carried out

---

## 16. Entities vs DTOs

This distinction is essential.

### Entities
Entities represent business objects with:
- identity
- state
- business behavior
- invariants

Example:
- `Order`
- `User`
- `Invoice`

### DTOs
DTOs are data-transfer objects used to move structured data across boundaries.

Examples:
- request models
- response models
- command objects
- query results

### Practical difference
- **entity** = business meaning
- **DTO** = transport shape

This is one of the most useful architecture distinctions in Python web systems.

---

## 17. Why DTOs matter

DTOs help prevent:
- leaking domain internals into APIs
- tying domain entities to transport concerns
- mixing validation shape with business behavior

In FastAPI, Pydantic models often act as boundary DTOs.

That is a very practical and common pattern.

---

## 18. Why entities should not become request/response models

If you use domain entities directly as API models, problems often appear:

- response shape becomes coupled to domain shape
- validation concerns get mixed with domain concerns
- API versioning becomes harder
- persistence/domain decisions leak outward

It is usually cleaner to:
- accept input DTOs
- map them into domain/use-case inputs
- return output DTOs or response models

---

# Part IV — Dependency Injection and Wiring in FastAPI

## 19. Why FastAPI matters here

FastAPI’s dependency system is especially relevant in a layered architecture because it provides a natural place for **wiring**.

FastAPI documents dependencies as a central mechanism where path operation functions can declare what they need, and FastAPI resolves and injects those dependencies. citeturn971290search1turn971290search4

This fits very well with:
- use case construction
- repository injection
- auth context resolution
- request-scoped resources

---

## 20. Project structure in bigger FastAPI apps

FastAPI’s official “bigger applications” guidance explicitly shows splitting applications into multiple files and modules, including `main.py`, `dependencies.py`, and routers built with `APIRouter`. citeturn971290search0turn971290search6

A practical project shape might look like:

```text
app/
├── main.py
├── dependencies.py
├── domain/
├── application/
├── infrastructure/
└── routers/
```

This structure is not mandatory, but it is a strong fit for layered design because it gives each concern an obvious home.

---

## 21. Routers and route handlers

FastAPI’s `APIRouter` is the standard way to group endpoints into modules, and router-level dependencies are supported directly by the framework. citeturn971290search3

A good design keeps route handlers thin:
- parse already-validated input
- call a use case
- return a response model

Route handlers should not become the main place for business rules or orchestration.

---

## 22. Dependencies as wiring

FastAPI dependencies can be:
- functions
- classes
- dependency chains with sub-dependencies
- dependencies with `yield` for setup/teardown

The official docs describe dependencies, class-based dependencies, sub-dependencies, and dependencies with `yield` as supported patterns. citeturn971290search1turn971290search9turn971290search17turn971290search20

This makes FastAPI a very practical place to wire:
- DB sessions
- repositories
- use cases
- auth context
- configuration

A common pattern is:
- `get_db()`
- `get_repository(db=Depends(get_db))`
- `get_use_case(repo=Depends(get_repository))`

That keeps construction logic outside business code.

---

## 23. Global, router-level, and endpoint-level dependencies

FastAPI supports dependencies at multiple levels:
- application-wide
- router-wide
- endpoint parameter level

This is documented both in the tutorial and reference pages. citeturn971290search11turn971290search3

A practical recommendation is:
- use global dependencies sparingly
- prefer router-level dependencies for shared sections
- use parameter-level dependencies for local and explicit needs

That keeps the wiring understandable.

---

## 24. Testing with dependency overrides

FastAPI documents `app.dependency_overrides` as the mechanism for replacing dependencies during tests. citeturn971290search2turn971290search15

This is extremely useful because it lets you replace:
- real repositories with fakes
- real auth dependencies with test users
- real external clients with fake implementations

That gives FastAPI a very strong testing story when combined with clean architecture boundaries.

---

# Part V — Domain, Contract, and End-to-End Tests

## 25. Domain tests

Domain tests verify:
- business rules
- invariants
- entity behavior
- value object behavior
- domain service logic

These should usually be:
- fast
- framework-free
- infrastructure-free
- highly focused

If a business rule matters, a direct domain test is often the best protection.

---

## 26. Contract tests

Contract tests verify a boundary agreement.

Typical contract boundaries:
- port ↔ adapter
- API client ↔ external service schema
- message producer ↔ message consumer expectations
- repository contract ↔ concrete repository behavior

Their job is not to test the whole system.  
Their job is to ensure that both sides of a seam still agree on what is expected.

This is especially valuable in ports-and-adapters designs.

---

## 27. End-to-end tests

End-to-end tests verify the full assembled system flow from the outside.

In a FastAPI project, an end-to-end test might:
- call the real HTTP endpoint
- pass through validation
- hit the application layer
- use real infrastructure or controlled near-real test infrastructure
- verify the final response and side effects

These tests are important, but they are usually:
- slower
- broader
- more expensive to maintain

That is why they should complement, not replace, lower-level tests.

---

## 28. Why the three test types work together

A practical mental model is:

- **domain tests** protect business meaning
- **contract tests** protect seams
- **end-to-end tests** protect real system behavior

If you only write end-to-end tests, you usually get:
- slow suites
- weaker debugging signal
- poor direct business-rule coverage

If you only write domain tests, you may miss:
- wiring issues
- boundary mismatches
- deployment-level failures

A strong architecture benefits from all three.

---

# Part VI — Putting It Together

## 29. A practical end-to-end architecture flow

A realistic request flow in a FastAPI application may look like this:

1. an HTTP request hits a FastAPI route
2. FastAPI validates boundary input with a DTO/schema
3. FastAPI resolves dependencies and wires a use case
4. the use case loads entities through ports/gateways
5. the domain enforces business rules
6. infrastructure adapters persist or call external systems
7. output is returned as a response DTO
8. tests protect the domain, boundaries, and full flow at different levels

This is a very practical synthesis of all the topics in this wiki.

---

## 30. Typical design mistakes

Some common mistakes in this architecture space are:

- putting business rules in FastAPI routes
- letting DTOs replace entities entirely
- making repositories or adapters responsible for business decisions
- treating dependency injection as magic instead of explicit wiring
- overusing interfaces where no real variation exists
- using only end-to-end tests and neglecting domain-level checks

These mistakes usually make code harder to test and harder to evolve.

---

## 31. Final recommendations

A practical approach is:

1. Keep domain rules in the domain.
2. Keep workflows in use cases.
3. Use ports to define what the core needs.
4. Use adapters to implement those needs with SQL, HTTP, or messaging.
5. Use FastAPI dependencies as a wiring mechanism, not as a place to hide business logic.
6. Keep routes thin.
7. Use DTOs for boundaries and entities for business meaning.
8. Build a balanced test strategy with domain, contract, and end-to-end tests.

This does not require maximum ceremony.  
It requires clear responsibilities and healthy dependency direction.

---

## 32. Quick summary

If you only keep the essentials:

- **domain** holds business meaning and invariants
- **application** holds use cases and orchestration
- **infrastructure** holds technical implementations
- **ports** define capabilities
- **adapters** implement those capabilities
- **DTOs** carry data across boundaries
- **entities** model business objects and behavior
- **FastAPI dependencies** are a strong wiring mechanism in layered apps citeturn971290search1turn971290search0turn971290search2
- **domain, contract, and end-to-end tests** protect different but complementary risks

---
