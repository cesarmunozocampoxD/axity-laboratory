# Clean Architecture — Clear Summary

## 1. Goal

This document gives a clear summary of these advanced Clean Architecture topics:

- entities, use cases, controllers/presenters/gateways
- dependency rules and layer separation
- Unit of Work and domain events
- migration strategies toward Clean Architecture

The purpose is to keep the big picture simple and practical.

---

## 2. Entities, Use Cases, Controllers, Presenters, and Gateways

### Entities
Entities are the core business objects of the system.

They usually contain:
- identity
- business state
- business rules
- important domain behavior

Example ideas:
- `Order`
- `User`
- `Invoice`

An entity should protect business invariants, such as:
- a shipped order cannot be cancelled
- an account cannot go below allowed limits

### Use Cases
Use cases represent application actions or workflows.

Examples:
- register user
- cancel order
- place order
- approve loan

A use case usually:
- receives input
- loads entities
- invokes domain behavior
- coordinates repositories or gateways
- returns a result

A useful shortcut is:
- **entity** = business object
- **use case** = business workflow

### Controllers
Controllers translate external input into a use case call.

They often:
- receive HTTP, CLI, or message input
- validate or normalize boundary input
- call the use case

They should stay thin.  
They should not hold core business rules.

### Presenters
Presenters transform use case output into a format suitable for delivery.

Examples:
- API response shape
- view model
- response DTO

They answer:
- how should this result be shown or returned?

They should not contain domain rules or persistence logic.

### Gateways
Gateways are abstractions for persistence or external systems.

Examples:
- repository gateway
- payment gateway
- notification gateway
- external API gateway

The use case depends on the gateway contract, not the concrete implementation.

### Main idea
These roles separate responsibilities clearly:
- entities protect business meaning
- use cases orchestrate workflows
- controllers adapt input
- presenters adapt output
- gateways abstract external access

---

## 3. Dependency Rules and Layer Separation

### Core rule
Dependencies should point **inward**, toward the business core.

That usually means:

```text
Infrastructure → Application → Domain
```

### Meaning
- outer layers may depend on inner layers
- inner layers should not depend on outer layers

So:
- domain should not depend on FastAPI, SQLAlchemy, PostgreSQL, or HTTP details
- application should not depend directly on framework or DB implementation details
- infrastructure can depend on application/domain contracts

### Layer responsibilities

#### Domain
Contains:
- entities
- value objects
- domain rules
- invariants

Question it answers:
- what is true in the business?

#### Application
Contains:
- use cases
- orchestration
- ports/protocols for needed capabilities

Question it answers:
- what workflow is being executed?

#### Infrastructure
Contains:
- DB implementations
- external API adapters
- message brokers
- technical integrations

Question it answers:
- how is this done technically?

#### Delivery layer
Contains:
- routes
- controllers
- handlers
- input/output adaptation

Question it answers:
- how does the outside world talk to the app?

### Why this matters
Good separation improves:
- testability
- replaceability
- readability
- maintainability

Bad separation usually leads to:
- business rules in controllers
- framework leakage into the core
- harder refactoring
- fragile tests

---

## 4. Unit of Work and Domain Events

### Unit of Work
Unit of Work defines the transactional boundary of a business operation.

It answers:
- what changes should succeed or fail together?

A Unit of Work usually coordinates:
- repositories
- transaction lifecycle
- commit
- rollback

Typical use:
- open a transaction
- perform changes
- commit once
- rollback if something fails

### Why Unit of Work is useful
It helps prevent partial updates like:
- order saved
- inventory changed
- notification failed
- inconsistent state left behind

It centralizes transaction control and makes the boundary explicit.

### Domain Events
Domain events represent meaningful business facts that already happened.

Examples:
- `OrderPaid`
- `UserRegistered`
- `SubscriptionCancelled`

They are usually named in past tense because they represent facts.

### Why domain events are useful
They let the system say:
- something important happened

and then allow other parts of the system to react, such as:
- send email
- publish a message
- update analytics
- trigger downstream workflows

### Important distinction
- **domain event** = business fact
- **integration event** = event sent to outside systems

They may be related, but they are not always the same thing.

### Unit of Work + Domain Events together
A common good pattern is:

1. perform business changes
2. collect domain events
3. commit transaction
4. dispatch events

This avoids dangerous situations like publishing an event before the transaction is actually committed.

### Main idea
- Unit of Work protects consistency
- Domain Events express important business facts
- together they help coordinate complex workflows safely

---

## 5. Migration Strategies Toward Clean Architecture

### Main principle
Do **not** try to rewrite everything at once.

The safest approach is usually:
- incremental migration
- one use case at a time
- one boundary at a time
- one dependency problem at a time

### Good migration mindset
A practical mindset is:
- preserve behavior first
- improve structure gradually
- move business rules inward
- move technical details outward

### Strong migration strategies

#### 1. Strangler-style migration
Keep the old system running while new or refactored parts follow the cleaner architecture.

#### 2. Use-case-by-use-case migration
Pick one workflow, such as:
- cancel order
- register user
- create invoice

and refactor that slice completely.

#### 3. Domain-first extraction
Move buried business rules from:
- routes
- services
- ORM models

into:
- entities
- domain services

#### 4. Port-first extraction
Introduce ports/protocols when external dependencies are the main pain:
- SQL
- HTTP
- messaging
- cloud SDKs

#### 5. Anti-corruption layer
Wrap ugly or legacy external systems behind adapters so old complexity does not leak into the new core.

### Practical migration steps

1. identify one painful or high-value flow
2. map the current behavior
3. protect it with tests
4. extract the use case
5. move business rules into domain
6. introduce ports where needed
7. move technical details into adapters
8. wire everything at the edge

### Common migration mistakes
- rewriting everything from scratch
- introducing abstractions too early
- moving files without improving responsibilities
- overengineering small problems
- ignoring team conventions and adoption

### Main idea
Migration succeeds when:
- changes are incremental
- responsibilities get clearer
- testing gets easier
- dependency direction improves over time

---

## 6. Unified Big Picture

A practical summary of all four topics is:

- **Entities** protect business rules
- **Use cases** coordinate business workflows
- **Controllers** adapt external input
- **Presenters** adapt output
- **Gateways** abstract external access
- **Dependency rules** keep the core protected from technical details
- **Layer separation** makes responsibilities explicit
- **Unit of Work** protects transactional consistency
- **Domain events** represent meaningful business facts
- **Migration strategy** helps you move toward this structure safely and incrementally

---

## 7. Final takeaway

If you only keep the essentials:

1. Keep business rules in the core.
2. Keep workflows in use cases.
3. Keep controllers and presenters thin.
4. Keep technical implementations behind gateways/adapters.
5. Keep dependencies pointing inward.
6. Use Unit of Work when transactional consistency matters.
7. Use domain events for meaningful business facts.
8. Migrate gradually, not all at once.

---
