# Pythonic Design Wiki: SOLID, Dependency Inversion, and Design Quality

## 1. Purpose

This wiki gives a medium-depth overview of three closely related design topics in Python:

- SOLID principles in a Pythonic style
- dependency inversion using `Protocol`, factories, and provider patterns
- coupling, cohesion, and testability

These topics belong together because they all affect the same practical question:

> How do you design Python code that is easier to understand, extend, and test?

This is not a purely theoretical guide.  
The goal is to explain the ideas in a way that is useful for real Python applications.

---

## 2. Why “Pythonic” matters

A common mistake is to learn design principles from very class-heavy ecosystems and then apply them mechanically in Python.

That often leads to:
- too many classes
- too many interfaces
- artificial abstraction
- code that feels ceremonial instead of clear

A Pythonic interpretation means:
- prefer clarity over ceremony
- use functions when they are enough
- use classes when they add real value
- use protocols and composition where they improve flexibility
- avoid unnecessary abstraction

The principles still matter, but the implementation style should fit Python.

---

# Part I — SOLID in a Pythonic Style

## 3. What SOLID is

SOLID is a group of five design principles:

- **SRP** — Single Responsibility Principle
- **OCP** — Open/Closed Principle
- **LSP** — Liskov Substitution Principle
- **ISP** — Interface Segregation Principle
- **DIP** — Dependency Inversion Principle

These principles are not strict laws.  
They are design heuristics that help reduce brittle and tangled code.

---

## 4. SRP — Single Responsibility Principle

### Core idea
A module, class, or function should have one main reason to change.

### In practice
SRP is really about **focused responsibility**.

Bad example:

```python
class UserManager:
    def validate_email(self, email: str) -> bool:
        return "@" in email

    def save_user(self, user: dict) -> None:
        ...

    def send_welcome_email(self, user: dict) -> None:
        ...

    def export_pdf_report(self, user: dict) -> bytes:
        ...
```

This mixes:
- validation
- persistence
- messaging
- reporting

That is too many responsibilities.

Better direction:

```python
class UserValidator:
    def validate_email(self, email: str) -> bool:
        return "@" in email


class UserRepository:
    def save(self, user: dict) -> None:
        ...


class WelcomeNotifier:
    def send(self, user: dict) -> None:
        ...
```

### Pythonic interpretation
SRP does not mean “every class must be tiny.”  
It means responsibilities should be coherent.

In Python, SRP often applies just as strongly to:
- functions
- modules
- services
- packages

A long function doing parsing, DB writing, HTTP calling, and formatting probably violates SRP just as much as a bloated class does.

---

## 5. OCP — Open/Closed Principle

### Core idea
Code should be open for extension but closed for modification.

### Meaning
When requirements grow, you should ideally add behavior without constantly editing fragile existing code.

Bad example:

```python
def send_notification(channel: str, message: str) -> None:
    if channel == "email":
        print(f"Email: {message}")
    elif channel == "sms":
        print(f"SMS: {message}")
    elif channel == "push":
        print(f"Push: {message}")
    else:
        raise ValueError("Unsupported channel")
```

Every new channel requires editing the function.

Better direction:

```python
from typing import Protocol


class Notifier(Protocol):
    def send(self, message: str) -> None:
        ...


class EmailNotifier:
    def send(self, message: str) -> None:
        print(f"Email: {message}")


class SmsNotifier:
    def send(self, message: str) -> None:
        print(f"SMS: {message}")
```

Now the caller can work with a `Notifier`, and new implementations can be added without rewriting the main orchestration logic.

### Pythonic interpretation
OCP in Python often means:
- use polymorphism or protocols when variation is real
- use functions or dictionaries for simple extension points
- do not overbuild abstractions before they are needed

OCP is helpful when behavior varies repeatedly.  
It is overkill when the system has only one trivial implementation.

---

## 6. LSP — Liskov Substitution Principle

### Core idea
A subtype should be usable wherever its base type is expected, without breaking behavior assumptions.

### Meaning
If something claims to be a replacement for another thing, it should behave in a compatible way.

Bad example:

```python
class Bird:
    def fly(self) -> None:
        print("Flying")


class Penguin(Bird):
    def fly(self) -> None:
        raise NotImplementedError("Penguins can't fly")
```

This is a substitution problem.  
`Penguin` technically inherits from `Bird`, but it breaks the expectation of `fly()`.

### Pythonic interpretation
LSP matters even without classical inheritance.

It also applies when:
- one object is passed where another is expected
- a protocol is claimed but behavior is incompatible
- a mock or fake behaves too differently from the real thing

If your fake repository behaves in a way the real repository never would, you may also be violating substitutability at a practical level.

### Good design direction
Model abstractions around real shared behavior, not around forced taxonomy.

---

## 7. ISP — Interface Segregation Principle

### Core idea
Clients should not be forced to depend on methods they do not need.

Bad example:

```python
class Machine:
    def print(self) -> None:
        ...

    def scan(self) -> None:
        ...

    def fax(self) -> None:
        ...
```

A simple printer should not be forced to care about scanning or faxing.

Better direction:

```python
from typing import Protocol


class Printer(Protocol):
    def print(self) -> None:
        ...


class Scanner(Protocol):
    def scan(self) -> None:
        ...
```

### Pythonic interpretation
ISP is especially natural in Python because:
- protocols can be very small
- duck typing already encourages behavior-based design
- small interfaces are often easier than big inheritance trees

In practice, ISP often means:
- make repository contracts focused
- avoid “god services”
- avoid giant utility objects
- keep protocols narrow and task-oriented

---

## 8. DIP — Dependency Inversion Principle

### Core idea
High-level policy should not depend directly on low-level implementation details.  
Both should depend on abstractions.

Bad example:

```python
class ReportService:
    def __init__(self) -> None:
        self.client = SmtpClient()

    def send_report(self, text: str) -> None:
        self.client.send(text)
```

This tightly couples business logic to a concrete implementation.

Better direction:

```python
from typing import Protocol


class MessageSender(Protocol):
    def send(self, text: str) -> None:
        ...


class ReportService:
    def __init__(self, sender: MessageSender) -> None:
        self.sender = sender

    def send_report(self, text: str) -> None:
        self.sender.send(text)
```

Now the service depends on a capability, not a specific vendor/client.

### Pythonic interpretation
DIP in Python is often implemented with:
- `Protocol`
- callables
- constructor injection
- provider/factory functions

You usually do not need heavy interface hierarchies.  
You need clear boundaries and explicit dependencies.

---

# Part II — Dependency Inversion with Protocols, Factories, and Providers

## 9. Why dependency inversion matters in practice

Dependency inversion gives you cleaner code because it helps with:

- replacing infrastructure
- testing without real side effects
- reducing framework coupling
- keeping business logic more stable
- separating wiring from behavior

This becomes especially important in applications with:
- databases
- HTTP clients
- messaging systems
- authentication providers
- cloud SDKs

---

## 10. `Protocol` as a Pythonic abstraction tool

`Protocol` lets you define behavior contracts without requiring explicit inheritance.

Example:

```python
from typing import Protocol


class UserRepository(Protocol):
    def get_by_id(self, user_id: int) -> dict | None:
        ...

    def save(self, user: dict) -> None:
        ...
```

Any object with compatible methods can satisfy this contract.

### Why this is useful
It supports:
- loose coupling
- structural typing
- easier testing
- better editor and type-checker support

It also fits Python better than forcing every implementation to inherit from a base interface class.

---

## 11. Constructor injection

One of the simplest dependency inversion techniques is constructor injection.

Example:

```python
class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    def get_user(self, user_id: int) -> dict | None:
        return self.repo.get_by_id(user_id)
```

### Why this is good
Dependencies are:
- explicit
- replaceable
- easy to fake in tests

This is usually the first and best default step.

---

## 12. Factories

A factory centralizes object creation.

Example:

```python
class EmailSender:
    def send(self, text: str) -> None:
        print(f"Email: {text}")


def create_sender(channel: str):
    if channel == "email":
        return EmailSender()
    raise ValueError("Unsupported channel")
```

### Why factories matter
Factories are useful when:
- creation depends on config
- creation logic is repeated
- object graphs are getting more complex
- the caller should not know construction details

### Pythonic note
A factory in Python is often just:
- a function
- a small class
- a provider method

It does not need a big pattern-heavy implementation.

---

## 13. Provider patterns

A provider pattern means having a dedicated place that assembles and returns dependencies.

Example:

```python
class AppProvider:
    def __init__(self, repo: UserRepository, sender: MessageSender) -> None:
        self.repo = repo
        self.sender = sender

    def user_service(self) -> "UserService":
        return UserService(self.repo)
```

In real apps, providers often live near the application boundary or wiring layer.

### Why useful
Provider-style wiring helps separate:
- construction
- configuration
- environment-specific assembly

from:
- business behavior

### Typical use cases
Providers are useful in:
- FastAPI dependency wiring
- CLI app setup
- service composition
- background worker startup

---

## 14. Factories vs providers

A simple distinction:

- **factory** → creates one object or family of objects
- **provider** → acts as an assembly/wiring source for dependencies

They overlap, but providers are often more about application composition.

---

## 15. Example: protocol + provider + fake test implementation

```python
from typing import Protocol


class PaymentGateway(Protocol):
    def charge(self, amount: float) -> None:
        ...


class StripePaymentGateway:
    def charge(self, amount: float) -> None:
        print(f"Charging {amount}")


class FakePaymentGateway:
    def __init__(self) -> None:
        self.charges = []

    def charge(self, amount: float) -> None:
        self.charges.append(amount)


class CheckoutService:
    def __init__(self, gateway: PaymentGateway) -> None:
        self.gateway = gateway

    def checkout(self, amount: float) -> None:
        self.gateway.charge(amount)
```

This gives:
- a clear abstraction
- easy production replacement
- easy testing with a fake

That is dependency inversion working in a Pythonic way.

---

# Part III — Coupling, Cohesion, and Testability

## 16. Coupling

### What it is
Coupling describes how strongly one part of the system depends on another.

High coupling usually means:
- a class knows too much about concrete dependencies
- changes ripple across many files
- tests require lots of setup
- code cannot be understood in isolation

Low coupling usually means:
- dependencies are limited and clear
- components can change more independently
- fakes or replacements are easier to use

### Example of high coupling

```python
class BillingService:
    def charge(self, amount: float) -> None:
        db = DatabaseClient()
        smtp = SmtpClient()
        db.save_charge(amount)
        smtp.send_receipt(amount)
```

This is tightly coupled to specific infrastructure details.

Better direction:

```python
class BillingService:
    def __init__(self, repo, notifier) -> None:
        self.repo = repo
        self.notifier = notifier

    def charge(self, amount: float) -> None:
        self.repo.save_charge(amount)
        self.notifier.send_receipt(amount)
```

Now the service is less entangled.

---

## 17. Cohesion

### What it is
Cohesion describes how well the responsibilities inside one unit belong together.

High cohesion means:
- the class/function/module has one strong focus
- naming is clearer
- change reasons are more coherent

Low cohesion means:
- unrelated behaviors are mixed
- naming becomes vague
- tests become broad and confusing

Bad example:

```python
class UserTools:
    def validate_email(self, email): ...
    def save_user(self, user): ...
    def send_email(self, user): ...
    def export_csv(self, users): ...
```

This unit is doing too many different kinds of work.

### Good design direction
A cohesive unit should be easy to describe in one clear sentence.

---

## 18. Testability

### What it is
Testability describes how easily code can be verified in a reliable and focused way.

Highly testable code usually has:
- explicit inputs
- clear outputs
- isolated side effects
- injectable dependencies
- focused responsibilities
- deterministic behavior

Low-testability code often has:
- hidden dependencies
- global state
- direct infrastructure coupling
- mixed concerns
- too many side effects in one place

### Important idea
Testing pain is often a design signal.

If a piece of code is difficult to test, the issue may not only be the test.  
The issue may be the design itself.

---

## 19. How coupling, cohesion, and testability relate

These three ideas strongly reinforce each other.

- **Lower coupling** usually improves testability.
- **Higher cohesion** usually improves readability and focused tests.
- **Poor testability** often reveals weak separation of concerns.

A practical design goal is:
- lower coupling
- higher cohesion
- higher testability

Not because these are buzzwords, but because they make real systems easier to change.

---

## 20. Signs of healthy design

A unit is often in decent shape when:
- it has one clear purpose
- it depends on abstractions instead of concrete infrastructure
- it is easy to name
- it can be tested without spinning up the whole system
- it does not require many mocks for a simple test
- a small change does not create ripple effects everywhere

---

## 21. Signs of unhealthy design

Warning signs include:
- giant service classes
- hidden global state
- many unrelated responsibilities in one unit
- direct construction of infrastructure inside business logic
- many mocks just to test one method
- one class knowing DB, HTTP, serialization, formatting, and messaging all at once

These are usually not isolated test problems.  
They are architectural and design problems.

---

# Part IV — Putting Everything Together

## 22. Practical combined view

A strong Pythonic design often looks like this:

- business logic is focused and cohesive
- dependencies are injected explicitly
- infrastructure is abstracted with protocols where needed
- factories/providers assemble objects at the edge
- high-level logic depends on behavior contracts, not vendors
- units are easier to test because coupling is controlled

This is where SOLID stops being theory and becomes practical engineering.

---

## 23. Example architecture direction

A simple layered direction might be:

```text
Infrastructure implementations
        ↓
Provider / wiring layer
        ↓
Use cases / services
        ↓
Domain objects and rules
```

And with abstractions:

```text
Use case depends on Protocol
Concrete adapter implements Protocol
Provider wires them together
```

This is a realistic and Pythonic application of:
- DIP
- ISP
- SRP
- lower coupling
- higher cohesion
- better testability

---

## 24. Final recommendations

A practical approach is:

1. Keep responsibilities focused.
2. Prefer composition over inheritance unless inheritance is truly natural.
3. Use `Protocol` for behavior contracts when abstraction adds value.
4. Inject dependencies explicitly.
5. Use factories/providers to keep wiring out of business logic.
6. Watch for high coupling and low cohesion as warning signs.
7. Treat testing difficulty as feedback about design.

You do not need maximum abstraction.  
You need enough structure to keep the code understandable, replaceable, and testable.

---

## 25. Quick summary

If you only keep the essentials:

- **SRP** means focused responsibility.
- **OCP** means extend behavior without constantly rewriting stable logic.
- **LSP** means replacements should behave compatibly.
- **ISP** means keep contracts small and relevant.
- **DIP** means depend on abstractions, not concrete low-level details.
- **Protocols** are a Pythonic way to express those abstractions.
- **Factories and providers** help keep construction and wiring outside business logic.
- **Low coupling + high cohesion** usually lead to better testability.
- **Hard-to-test code** is often a design smell, not just a testing inconvenience.

---
