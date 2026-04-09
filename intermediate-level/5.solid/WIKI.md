# SOLID in a Pythonic Key: SRP, OCP, LSP, ISP, DIP

## 1. Goal

This guide explains the five **SOLID** principles in a more **Pythonic** way.

It focuses on:

- what each principle means
- how to interpret it in Python
- how Pythonic design sometimes differs from classic OOP-heavy styles
- practical examples
- common mistakes
- how to apply SOLID without overengineering

The goal is not to turn Python into Java with different syntax.  
The goal is to understand SOLID in a way that fits Python’s strengths.

---

## 2. What “Pythonic” means here

When people say **Pythonic**, they usually mean code that is:

- clear
- simple
- expressive
- practical
- easy to change
- not overloaded with unnecessary abstraction

So a Pythonic reading of SOLID usually means:

- prefer clarity over ceremony
- prefer simple composition over deep inheritance trees
- prefer protocols and duck typing when appropriate
- do not create interfaces or classes unless they solve a real problem
- keep design flexible, but not artificially abstract

---

## 3. SOLID in Python is not “copy enterprise Java”

A common mistake is to learn SOLID from strongly OOP-centered examples and then force exactly the same structure into Python.

That often leads to:
- too many classes
- too many tiny wrappers
- interfaces everywhere
- unnecessary inheritance
- code that is abstract but not actually simpler

In Python, SOLID should usually be applied with:
- fewer layers
- more pragmatism
- more composition
- more explicitness
- more trust in duck typing and simple contracts

---

## 4. Quick overview of SOLID

SOLID stands for:

- **S**RP → Single Responsibility Principle
- **O**CP → Open/Closed Principle
- **L**SP → Liskov Substitution Principle
- **I**SP → Interface Segregation Principle
- **D**IP → Dependency Inversion Principle

These principles are not rigid laws.  
They are design heuristics that help code stay easier to maintain.

---

# SRP — Single Responsibility Principle

## 5. What SRP means

**Single Responsibility Principle** says:

> A module, class, or function should have one reason to change.

A practical interpretation is:

- one unit of code should focus on one kind of job
- it should not mix unrelated concerns

### Important
“Single responsibility” does **not** mean “must be tiny.”  
It means the code should have a coherent purpose.

---

## 6. Pythonic interpretation of SRP

In Python, SRP often applies strongly to:
- functions
- modules
- services
- utility layers
- adapters

It does not only apply to classes.

That is important because Python often solves problems with:
- functions
- plain modules
- simple objects
- composition

rather than always with large class hierarchies.

---

## 7. Bad SRP example

```python
class ReportManager:
    def fetch_data(self):
        return ["a", "b", "c"]

    def format_html(self, data):
        return "<br>".join(data)

    def save_to_file(self, content, filename):
        with open(filename, "w") as f:
            f.write(content)

    def send_email(self, content, to_email):
        print(f"Sending email to {to_email}: {content}")
```

### Why this is problematic
This class is doing too many unrelated jobs:
- data fetching
- formatting
- file persistence
- email sending

These concerns change for different reasons.

---

## 8. Better SRP example

```python
class ReportRepository:
    def fetch_data(self):
        return ["a", "b", "c"]


class ReportFormatter:
    def format_html(self, data):
        return "<br>".join(data)


class FileWriter:
    def save(self, content, filename):
        with open(filename, "w") as f:
            f.write(content)


class EmailSender:
    def send(self, content, to_email):
        print(f"Sending email to {to_email}: {content}")
```

### Why this is better
Each class has a more focused responsibility.

### Pythonic note
You do not always need four classes.  
Sometimes the cleanest solution is just a few well-scoped functions.

---

## 9. Very Pythonic SRP example with functions

```python
def fetch_report_data():
    return ["a", "b", "c"]


def format_report_html(data):
    return "<br>".join(data)


def save_text_file(content, filename):
    with open(filename, "w") as f:
        f.write(content)


def send_email(content, to_email):
    print(f"Sending email to {to_email}: {content}")
```

### Why this is Pythonic
If you do not need state or polymorphism, simple functions may express SRP better than a class-heavy design.

---

## 10. SRP practical questions

To evaluate SRP, ask:

- Does this code do more than one kind of job?
- Would different people change this code for different reasons?
- Are formatting, persistence, transport, and business logic mixed together?
- Is this unit hard to test because it combines unrelated concerns?

If the answer is yes, SRP may be weak.

---

## 11. SRP common mistake

A common mistake is to split code into too many micro-objects or micro-functions with no real gain.

Bad interpretation:
- every line becomes a class
- every three lines become a helper

Good interpretation:
- keep responsibilities cohesive
- separate concerns that change independently

SRP is about **cohesion**, not fragmentation.

---

# OCP — Open/Closed Principle

## 12. What OCP means

**Open/Closed Principle** says:

> Software entities should be open for extension but closed for modification.

In practical terms:
- you should be able to add new behavior
- without constantly editing stable existing code

---

## 13. Pythonic interpretation of OCP

In Python, OCP often appears through:
- composition
- polymorphism
- dependency injection
- function dispatch
- registries
- protocols
- plugin-like patterns

It does **not** require giant inheritance hierarchies.

In many Python projects, a dictionary of strategies or a callable registry is more Pythonic than a deep abstract class tree.

---

## 14. Bad OCP example

```python
def calculate_discount(customer_type, amount):
    if customer_type == "regular":
        return amount * 0.05
    elif customer_type == "vip":
        return amount * 0.10
    elif customer_type == "employee":
        return amount * 0.20
    else:
        return 0
```

### Why this is weak
Every time you add a new customer type, you must modify the function.

That means the core logic keeps changing.

---

## 15. Better OCP example with strategy objects

```python
class DiscountStrategy:
    def apply(self, amount):
        raise NotImplementedError


class RegularDiscount(DiscountStrategy):
    def apply(self, amount):
        return amount * 0.05


class VipDiscount(DiscountStrategy):
    def apply(self, amount):
        return amount * 0.10


class EmployeeDiscount(DiscountStrategy):
    def apply(self, amount):
        return amount * 0.20


def calculate_discount(strategy, amount):
    return strategy.apply(amount)
```

### Why this is better
New discount types can be added by creating new strategy classes rather than rewriting the central function.

---

## 16. More Pythonic OCP with callables

Python often does not need a whole class hierarchy for this.

```python
def regular_discount(amount):
    return amount * 0.05


def vip_discount(amount):
    return amount * 0.10


def employee_discount(amount):
    return amount * 0.20


def calculate_discount(discount_func, amount):
    return discount_func(amount)
```

### Why this is Pythonic
Functions are first-class objects in Python.  
A callable can often serve as the extension point.

---

## 17. OCP with a registry

```python
discounts = {
    "regular": lambda amount: amount * 0.05,
    "vip": lambda amount: amount * 0.10,
    "employee": lambda amount: amount * 0.20,
}


def calculate_discount(customer_type, amount):
    discount_func = discounts.get(customer_type, lambda amount: 0)
    return discount_func(amount)
```

### Why useful
To extend behavior, you add to the registry instead of rewriting branching logic everywhere.

### Pythonic caution
A registry is elegant when the variants are simple.  
Do not turn every tiny condition into a complex plugin framework.

---

## 18. OCP practical questions

Ask:
- Can I add a new behavior without editing the stable core too much?
- Am I repeatedly adding `if/elif` branches for every new variant?
- Would a strategy, callable, registry, or protocol simplify extension?

If yes, OCP can help.

---

# LSP — Liskov Substitution Principle

## 19. What LSP means

**Liskov Substitution Principle** says:

> Subtypes should be usable in place of their base types without breaking expected behavior.

In simpler terms:
- if something claims to be a kind of another thing
- it should behave compatibly with that expectation

---

## 20. Why LSP matters

LSP is really about **behavioral compatibility**.

This is not just:
- “does inheritance compile?”
- “does the method exist?”

It is:
- does the subtype preserve the contract?
- does it surprise the caller?
- does it break assumptions of the code using the base type?

---

## 21. Classic bad LSP example

```python
class Bird:
    def fly(self):
        print("Flying")


class Penguin(Bird):
    def fly(self):
        raise NotImplementedError("Penguins cannot fly")
```

### Why this violates LSP
If code expects every `Bird` to be able to `fly()`, a `Penguin` breaks that expectation.

The subtype cannot safely replace the base type in that behavioral contract.

---

## 22. Better design for LSP

```python
class Bird:
    pass


class FlyingBird(Bird):
    def fly(self):
        print("Flying")


class Penguin(Bird):
    def swim(self):
        print("Swimming")
```

### Why this is better
The hierarchy reflects real behavior more accurately.

---

## 23. Pythonic interpretation of LSP

In Python, LSP often matters more in terms of:
- duck typing contracts
- protocol behavior
- expected method semantics
- consistent return values
- not surprising callers

Even without formal inheritance, you can still violate LSP in spirit.

---

## 24. Pythonic LSP example without inheritance

```python
class JsonSerializer:
    def serialize(self, data):
        return '{"value": 123}'


class BrokenSerializer:
    def serialize(self, data):
        return None
```

If client code expects `.serialize(data)` to return a string, then `BrokenSerializer` breaks the behavioral contract, even if Python allows it structurally.

That is an LSP-style problem.

---

## 25. LSP practical questions

Ask:
- Can this subtype really stand in for the base type?
- Does it keep the same essential expectations?
- Does it narrow behavior in a surprising way?
- Does it raise unexpected exceptions?
- Does it return incompatible shapes or meanings?

If yes, LSP may be violated.

---

## 26. LSP common mistake

A common mistake is using inheritance for code reuse instead of conceptual substitutability.

Bad reason for inheritance:
- “it shares some code”

Better reason for inheritance:
- “it is behaviorally a valid subtype”

In Python, composition is often safer than inheritance when LSP is unclear.

---

# ISP — Interface Segregation Principle

## 27. What ISP means

**Interface Segregation Principle** says:

> Clients should not be forced to depend on methods they do not use.

In simpler terms:
- do not make consumers depend on large, bloated interfaces
- give them only the capabilities they actually need

---

## 28. Pythonic interpretation of ISP

In Python, ISP often means:
- prefer small protocols
- prefer narrow contracts
- do not force giant base classes
- accept only what you truly need
- design APIs around real usage, not around hypothetical completeness

Because Python supports duck typing well, ISP can often be expressed naturally.

---

## 29. Bad ISP example

```python
class Worker:
    def code(self):
        raise NotImplementedError

    def test(self):
        raise NotImplementedError

    def deploy(self):
        raise NotImplementedError

    def design_ui(self):
        raise NotImplementedError
```

### Why this is problematic
Not every worker needs every method.  
Clients depending on `Worker` are forced to carry unrelated capabilities.

---

## 30. Better ISP example

```python
class Coder:
    def code(self):
        raise NotImplementedError


class Tester:
    def test(self):
        raise NotImplementedError


class Deployer:
    def deploy(self):
        raise NotImplementedError
```

### Why this is better
Capabilities are narrower and more focused.

---

## 31. More Pythonic ISP with Protocol

Python can express ISP nicely with `typing.Protocol`.

```python
from typing import Protocol


class SupportsWrite(Protocol):
    def write(self, data: str) -> None:
        ...
```

Now a function can depend only on what it actually needs:

```python
def export_report(writer: SupportsWrite, content: str) -> None:
    writer.write(content)
```

### Why this is Pythonic
The function does not care about the full class.  
It only cares that the object supports the required capability.

That is a very elegant ISP-style design in Python.

---

## 32. ISP practical questions

Ask:
- Does this consumer need everything in this API?
- Is this interface mixing unrelated capabilities?
- Could I express the dependency as a smaller contract?
- Would a protocol, callable, or narrow helper be clearer?

If yes, ISP may improve the design.

---

# DIP — Dependency Inversion Principle

## 33. What DIP means

**Dependency Inversion Principle** says:

> High-level modules should not depend on low-level modules directly.  
> Both should depend on abstractions.

And:

> Abstractions should not depend on details.  
> Details should depend on abstractions.

---

## 34. Practical meaning of DIP

The main idea is:
- business logic should not be tightly coupled to infrastructure details

Examples of low-level details:
- database libraries
- HTTP clients
- file systems
- email services
- external APIs

A high-level use case should depend on a contract or capability, not a concrete implementation whenever flexibility matters.

---

## 35. Bad DIP example

```python
class EmailService:
    def send(self, message):
        print(f"Sending email: {message}")


class UserNotifier:
    def __init__(self):
        self.email_service = EmailService()

    def notify(self, message):
        self.email_service.send(message)
```

### Why this is tightly coupled
`UserNotifier` creates and depends directly on the concrete `EmailService`.

That makes testing and replacement harder.

---

## 36. Better DIP example

```python
class EmailService:
    def send(self, message):
        print(f"Sending email: {message}")


class UserNotifier:
    def __init__(self, message_sender):
        self.message_sender = message_sender

    def notify(self, message):
        self.message_sender.send(message)
```

Usage:

```python
email_service = EmailService()
notifier = UserNotifier(email_service)
notifier.notify("Hello")
```

### Why this is better
The high-level module depends on an injected collaborator instead of constructing it directly.

That is a core DIP move.

---

## 37. More Pythonic DIP with duck typing

In Python, you often do not need a formal abstract base class.

```python
class SmsService:
    def send(self, message):
        print(f"Sending SMS: {message}")


class UserNotifier:
    def __init__(self, sender):
        self.sender = sender

    def notify(self, message):
        self.sender.send(message)
```

Now anything with a compatible `.send()` method can work.

### Why this is Pythonic
The abstraction is behavioral, not necessarily a formal class hierarchy.

---

## 38. DIP with Protocol

If you want stronger type clarity, Protocol works very well.

```python
from typing import Protocol


class MessageSender(Protocol):
    def send(self, message: str) -> None:
        ...


class UserNotifier:
    def __init__(self, sender: MessageSender):
        self.sender = sender

    def notify(self, message: str) -> None:
        self.sender.send(message)
```

### Why this is elegant
You get:
- loose coupling
- clear capability contract
- Pythonic structural typing

This is often a very good DIP expression in modern Python.

---

## 39. DIP and testing

One of the biggest practical benefits of DIP is testing.

```python
class FakeSender:
    def __init__(self):
        self.messages = []

    def send(self, message):
        self.messages.append(message)
```

Test:

```python
def test_notifier():
    fake = FakeSender()
    notifier = UserNotifier(fake)

    notifier.notify("Hello")

    assert fake.messages == ["Hello"]
```

### Why this matters
You can test high-level logic without depending on real infrastructure.

---

## 40. DIP practical questions

Ask:
- Is my business logic tightly tied to a concrete library or service?
- Am I instantiating dependencies deep inside high-level code?
- Would injection make this easier to test or replace?
- Do I really need a formal interface, or is a protocol/callable enough?

These questions often reveal where DIP is useful.

---

# Pythonic SOLID as a whole

## 41. The Pythonic flavor of SOLID

A Pythonic use of SOLID usually looks like:

- smaller, cohesive functions and classes
- composition over inheritance
- duck typing over forced interface hierarchies
- Protocol when explicit structural contracts help
- injected dependencies when flexibility matters
- simple data flow when abstractions are unnecessary

The important thing is not to worship the acronym.  
The important thing is to improve maintainability.

---

## 42. When SOLID helps

SOLID tends to help most when:
- the codebase is growing
- behavior varies by type or strategy
- infrastructure dependencies make testing hard
- responsibilities are tangled
- inheritance is getting fragile
- multiple developers need shared design clarity

---

## 43. When SOLID becomes overengineering

SOLID can become harmful when it leads to:
- unnecessary abstraction
- interface explosion
- too many tiny classes
- indirection with no real flexibility gain
- architecture designed for imaginary future requirements

### Pythonic warning
In Python, overdesign can be especially easy to spot because the language is good at solving many problems simply.

If a dictionary, function, or Protocol solves the problem cleanly, that may be better than five abstract classes.

---

## 44. Practical Pythonic alternatives

Sometimes the most Pythonic expression of SOLID is:

### For SRP
A clean module with a few focused functions.

### For OCP
A registry of callables.

### For LSP
Avoiding bad inheritance and using composition.

### For ISP
A narrow Protocol or simply accepting a callable.

### For DIP
Passing dependencies in as constructor arguments or function parameters.

This is still SOLID.  
It is just less ceremonial.

---

## 45. Common mistakes

### 1. Turning every concept into a class
Python often does not need that.

### 2. Using inheritance for reuse instead of substitutability
This often causes LSP problems.

### 3. Creating abstract base classes too early
Sometimes a simple behavioral contract is enough.

### 4. Confusing SRP with “tiny everything”
Small is not automatically cohesive.

### 5. Applying DIP everywhere blindly
Injection is useful when the dependency boundary matters, not for every trivial helper.

### 6. Using OCP to justify endless abstraction
Sometimes editing a simple function is the correct and simplest choice.

---

## 46. Best practices

### 1. Start simple
Do not build abstractions before the variation is real.

### 2. Refactor toward SOLID when pressure appears
Use the principles to improve code under real design stress.

### 3. Prefer composition over deep inheritance
This fits Python well.

### 4. Use Protocol when you want explicit capability contracts
It is often more Pythonic than heavy interface hierarchies.

### 5. Keep behavior coherent
That is one of the best ways to respect SRP and LSP.

### 6. Inject dependencies where boundaries matter
Especially for infrastructure and testing.

### 7. Optimize for readability and changeability
That is the real spirit behind SOLID.

---

## 47. Practical mental model

A useful Pythonic mental model is:

- **SRP** → keep concerns cohesive
- **OCP** → make variation extendable without constant rewriting
- **LSP** → subtypes must behave compatibly
- **ISP** → depend on small, relevant capabilities
- **DIP** → keep high-level logic away from concrete infrastructure details

Then add the Pythonic layer:

- use functions when classes are unnecessary
- use Protocol when structure matters
- use composition before inheritance
- avoid abstraction unless it earns its cost

---

## 48. Final recommendation

The best Pythonic use of SOLID is pragmatic, not doctrinaire.

A good target is:

- clean responsibilities
- flexible extension points where needed
- minimal surprise in behavior
- narrow, useful contracts
- loosely coupled business logic
- as little ceremony as possible

If SOLID makes the code clearer and easier to evolve, it is helping.  
If it makes the code noisier and more artificial, it is probably being applied badly.

---

## 49. Quick summary

If you only keep the essentials:

1. SRP means keeping responsibilities cohesive, often at the function or module level too.
2. OCP in Python is often better expressed with composition, callables, registries, or protocols than with deep inheritance.
3. LSP is about behavioral compatibility, not just matching method names.
4. ISP means depending on small capabilities, which Python expresses well through duck typing and Protocol.
5. DIP in Python often means dependency injection plus behavioral contracts, not necessarily formal interfaces everywhere.

---

# Dependency Inversion in Python with Protocols, Factories, and Provider Patterns

## 1. Goal

This guide explains how to apply **Dependency Inversion** in Python using:

- **Protocols**
- **factories**
- **provider patterns**

It focuses on a practical, Pythonic interpretation of dependency inversion rather than a ceremony-heavy approach.

The main goals are:

- reducing coupling
- improving testability
- separating business logic from infrastructure
- making object creation more flexible
- keeping designs explicit and maintainable

---

## 2. What dependency inversion means

The **Dependency Inversion Principle (DIP)** says:

> High-level modules should not depend on low-level modules directly.  
> Both should depend on abstractions.

And also:

> Abstractions should not depend on details.  
> Details should depend on abstractions.

### In practical terms
Your core business logic should not be tightly tied to:
- a specific database client
- a specific HTTP client
- a specific email service
- a specific cache implementation
- a specific external SDK

Instead, it should depend on a **capability contract**.

---

## 3. Pythonic interpretation of dependency inversion

In Python, dependency inversion often does **not** require:
- heavy interface hierarchies
- many abstract base classes
- enterprise-style class explosion

Instead, Python often expresses DIP through:
- duck typing
- `typing.Protocol`
- dependency injection
- factories
- providers
- composition

### Key idea
The important part is not “having an interface file.”  
The important part is making high-level code depend on **behavior**, not **concrete implementation details**.

---

## 4. Why this matters

Without dependency inversion, code often becomes:
- harder to test
- harder to replace
- harder to extend
- more coupled to infrastructure
- more painful to refactor

Typical warning signs:
- business classes instantiate dependencies directly
- concrete clients are hardcoded deep inside use cases
- tests require real external systems
- changing providers forces edits across many modules

---

## 5. A simple bad example

```python
class EmailSender:
    def send(self, message: str) -> None:
        print(f"Sending email: {message}")


class WelcomeService:
    def __init__(self) -> None:
        self.sender = EmailSender()

    def send_welcome(self, user_email: str) -> None:
        self.sender.send(f"Welcome, {user_email}")
```

### Why this is tightly coupled
`WelcomeService` directly creates `EmailSender`.

That means:
- it is hard to replace with SMS, push, or fake senders
- tests depend on the concrete implementation choice
- object creation is mixed into business logic

This is exactly the kind of situation DIP tries to improve.

---

## 6. First improvement: constructor injection

A simple and very Pythonic fix is dependency injection.

```python
class EmailSender:
    def send(self, message: str) -> None:
        print(f"Sending email: {message}")


class WelcomeService:
    def __init__(self, sender) -> None:
        self.sender = sender

    def send_welcome(self, user_email: str) -> None:
        self.sender.send(f"Welcome, {user_email}")
```

Usage:

```python
sender = EmailSender()
service = WelcomeService(sender)
service.send_welcome("janette@example.com")
```

### Why this is better
Now the service does not decide **how** the dependency is created.  
It only uses it.

This is one of the simplest and best dependency inversion moves in Python.

---

## 7. Why raw duck typing is sometimes enough

Python often does not require a formal interface.

If an object has the expected behavior, it can be used.

For example, any object with:

```python
send(message: str) -> None
```

can work with `WelcomeService`.

This is already a form of abstraction through behavior.

### But
When a project grows, or when you want stronger type clarity, `Protocol` becomes very useful.

---

## 8. What is `Protocol`?

`Protocol` comes from `typing` and supports **structural typing**.

That means a class does not need to explicitly inherit from the protocol.  
It only needs to implement the required behavior.

### Why this is good for DIP
It gives you:
- clear contracts
- better editor/type-checker support
- loose coupling
- no forced inheritance hierarchy

---

## 9. Basic `Protocol` example

```python
from typing import Protocol


class MessageSender(Protocol):
    def send(self, message: str) -> None:
        ...
```

Now the service can depend on `MessageSender`:

```python
class WelcomeService:
    def __init__(self, sender: MessageSender) -> None:
        self.sender = sender

    def send_welcome(self, user_email: str) -> None:
        self.sender.send(f"Welcome, {user_email}")
```

### Why this is elegant
The service now depends on a **capability contract**, not on a specific sender class.

---

## 10. Multiple implementations with the same protocol

```python
class EmailSender:
    def send(self, message: str) -> None:
        print(f"Email: {message}")


class SmsSender:
    def send(self, message: str) -> None:
        print(f"SMS: {message}")
```

Both are compatible with:

```python
class MessageSender(Protocol):
    def send(self, message: str) -> None:
        ...
```

Usage:

```python
service = WelcomeService(EmailSender())
service.send_welcome("janette@example.com")

service = WelcomeService(SmsSender())
service.send_welcome("janette@example.com")
```

### Why this matters
The business service can remain stable while implementations change.

That is dependency inversion in practice.

---

## 11. Testing benefit with `Protocol`

A fake implementation becomes easy.

```python
class FakeSender:
    def __init__(self) -> None:
        self.messages = []

    def send(self, message: str) -> None:
        self.messages.append(message)
```

Test:

```python
def test_send_welcome():
    fake = FakeSender()
    service = WelcomeService(fake)

    service.send_welcome("janette@example.com")

    assert fake.messages == ["Welcome, janette@example.com"]
```

### Why this is powerful
The test does not depend on:
- network calls
- real email services
- infrastructure setup

This is one of the biggest real-world advantages of dependency inversion.

---

## 12. Protocols for repositories

Dependency inversion is especially common in repository-style patterns.

Example protocol:

```python
from typing import Protocol


class UserRepository(Protocol):
    def get_by_id(self, user_id: int) -> dict | None:
        ...
```

Business service:

```python
class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    def get_username(self, user_id: int) -> str | None:
        user = self.repo.get_by_id(user_id)
        if not user:
            return None
        return user["username"]
```

### Why useful
The service does not care whether the repository uses:
- PostgreSQL
- SQLite
- an API
- an in-memory dictionary
- a fake test implementation

---

## 13. Concrete repository implementations

```python
class InMemoryUserRepository:
    def __init__(self) -> None:
        self.users = {
            1: {"id": 1, "username": "janette"}
        }

    def get_by_id(self, user_id: int) -> dict | None:
        return self.users.get(user_id)
```

And another implementation:

```python
class ApiUserRepository:
    def get_by_id(self, user_id: int) -> dict | None:
        # Example placeholder for external API call
        return {"id": user_id, "username": "remote_user"}
```

Both can satisfy the same protocol contract.

---

## 14. Protocols vs abstract base classes

You could use abstract base classes too, but `Protocol` is often more Pythonic for dependency inversion.

### Abstract base class
Good when:
- you need shared base behavior
- you want stricter inheritance structure
- runtime subclass checks matter

### Protocol
Good when:
- you want structural typing
- you want loose coupling
- you do not want forced inheritance
- you want a clean “if it behaves like this, it fits” model

In many modern Python projects, `Protocol` is an excellent fit for DIP.

---

## 15. What is a factory?

A **factory** is a function or object responsible for creating other objects.

### Why factories matter for DIP
Sometimes the issue is not only **what dependency is used**, but also **how and when it is created**.

Factories help when:
- construction is conditional
- creation is expensive
- configuration decides the implementation
- you want to centralize object creation logic

---

## 16. Basic factory function example

```python
class EmailSender:
    def send(self, message: str) -> None:
        print(f"Email: {message}")


class SmsSender:
    def send(self, message: str) -> None:
        print(f"SMS: {message}")


def build_sender(channel: str) -> MessageSender:
    if channel == "email":
        return EmailSender()
    if channel == "sms":
        return SmsSender()
    raise ValueError(f"Unsupported channel: {channel}")
```

Usage:

```python
sender = build_sender("email")
service = WelcomeService(sender)
```

### Why useful
Creation logic is now separate from business logic.

---

## 17. Why factories can improve architecture

Factories help you:
- avoid hardcoding construction inside use cases
- centralize branching logic for implementations
- keep configuration decisions in one place
- make replacement easier

This can be especially useful when the object graph is not trivial.

---

## 18. Factory class example

Sometimes a class-based factory is useful.

```python
class SenderFactory:
    def build(self, channel: str) -> MessageSender:
        if channel == "email":
            return EmailSender()
        if channel == "sms":
            return SmsSender()
        raise ValueError(f"Unsupported channel: {channel}")
```

Usage:

```python
factory = SenderFactory()
sender = factory.build("sms")
service = WelcomeService(sender)
```

### Why choose a class factory?
Usually when:
- the factory needs configuration
- the factory needs collaborators
- the build logic is more complex
- you want to mock or replace the factory itself

---

## 19. Factory with configuration

```python
class AppConfig:
    def __init__(self, channel: str) -> None:
        self.channel = channel


class SenderFactory:
    def __init__(self, config: AppConfig) -> None:
        self.config = config

    def build(self) -> MessageSender:
        if self.config.channel == "email":
            return EmailSender()
        if self.config.channel == "sms":
            return SmsSender()
        raise ValueError("Unsupported channel")
```

### Why this is practical
Factory decisions are often driven by environment or app configuration.

---

## 20. A factory is not always necessary

A common overengineering mistake is creating factories for trivial construction.

Bad example:
- a factory for `User(id, name)` when the constructor is already simple and stable

Factories are useful when they solve a real creation problem, not as a ritual.

### Good reasons for a factory
- variant selection
- hidden construction complexity
- expensive initialization
- integration with configuration
- object graph assembly

---

## 21. What is a provider pattern?

A **provider** is an object or function that supplies dependencies to consumers.

The term can mean slightly different things in different codebases, but the general idea is:

> A provider is responsible for giving you the dependency instance you need.

This can include:
- lazy creation
- caching
- configuration-based creation
- lifecycle control
- central dependency access

---

## 22. Provider vs factory

They are related, but not always identical.

### Factory
Primarily about **creating** an object.

### Provider
Primarily about **supplying** an object.

A provider may:
- create a new instance every time
- return the same shared instance
- wrap a factory
- manage dependency lifecycle

So a provider is often broader than a factory.

---

## 23. Simple provider function example

```python
def get_sender() -> MessageSender:
    return EmailSender()
```

Usage:

```python
sender = get_sender()
service = WelcomeService(sender)
```

### Why useful
Even a simple provider function creates a clean seam between:
- usage
- construction

This can be enough in many projects.

---

## 24. Provider with caching

Sometimes you want one shared dependency instance.

```python
class SenderProvider:
    def __init__(self) -> None:
        self._sender = None

    def get_sender(self) -> MessageSender:
        if self._sender is None:
            self._sender = EmailSender()
        return self._sender
```

### Why useful
This provides lazy initialization and reuse.

Possible use cases:
- expensive clients
- shared configuration-heavy objects
- singleton-like lifecycle within an app process

---

## 25. Provider for repository selection

```python
class RepositoryProvider:
    def __init__(self, use_api: bool) -> None:
        self.use_api = use_api

    def get_user_repository(self) -> UserRepository:
        if self.use_api:
            return ApiUserRepository()
        return InMemoryUserRepository()
```

Usage:

```python
provider = RepositoryProvider(use_api=False)
repo = provider.get_user_repository()
service = UserService(repo)
```

### Why this helps
The service does not know which repository variant exists.  
The provider decides that detail.

---

## 26. Provider for application wiring

Provider patterns become especially useful when assembling an application.

```python
class AppProvider:
    def __init__(self, use_sms: bool) -> None:
        self.use_sms = use_sms

    def get_sender(self) -> MessageSender:
        return SmsSender() if self.use_sms else EmailSender()

    def get_welcome_service(self) -> WelcomeService:
        return WelcomeService(self.get_sender())
```

Usage:

```python
provider = AppProvider(use_sms=True)
service = provider.get_welcome_service()
service.send_welcome("janette@example.com")
```

### Why useful
This centralizes dependency wiring in one place.

---

## 27. Why provider patterns help

Provider patterns are useful when:
- many objects depend on shared infrastructure
- object assembly is repeated
- lifecycle matters
- you want a clear wiring layer
- you want to separate composition from business logic

They are especially common in:
- web applications
- service-oriented apps
- layered architectures
- dependency injection frameworks

---

## 28. Provider patterns and FastAPI-style dependency injection

A practical connection:
many Python frameworks effectively use provider-like patterns.

For example, dependency functions in frameworks can act like providers:
- building repositories
- building service instances
- injecting configuration-aware dependencies

This means provider patterns are not theoretical.  
They map directly to real Python app architecture.

---

## 29. Combining Protocols + factories + providers

These patterns work very well together.

### Protocol
Defines the capability contract.

### Factory
Handles construction logic.

### Provider
Supplies and wires dependencies for the application.

This combination often gives a clean architecture with:
- low coupling
- good testability
- clear composition boundaries

---

## 30. Full example

```python
from typing import Protocol


class MessageSender(Protocol):
    def send(self, message: str) -> None:
        ...


class EmailSender:
    def send(self, message: str) -> None:
        print(f"Email: {message}")


class SmsSender:
    def send(self, message: str) -> None:
        print(f"SMS: {message}")


class WelcomeService:
    def __init__(self, sender: MessageSender) -> None:
        self.sender = sender

    def send_welcome(self, user_email: str) -> None:
        self.sender.send(f"Welcome, {user_email}")


class SenderFactory:
    def __init__(self, channel: str) -> None:
        self.channel = channel

    def build(self) -> MessageSender:
        if self.channel == "email":
            return EmailSender()
        if self.channel == "sms":
            return SmsSender()
        raise ValueError("Unsupported channel")


class AppProvider:
    def __init__(self, channel: str) -> None:
        self.sender_factory = SenderFactory(channel)

    def get_welcome_service(self) -> WelcomeService:
        sender = self.sender_factory.build()
        return WelcomeService(sender)
```

Usage:

```python
provider = AppProvider(channel="email")
service = provider.get_welcome_service()
service.send_welcome("janette@example.com")
```

### What this shows
- `Protocol` defines the dependency contract
- factory handles implementation creation
- provider assembles the app-level object graph
- business logic remains decoupled from infrastructure details

---

## 31. Testing the combined pattern

```python
class FakeSender:
    def __init__(self) -> None:
        self.messages = []

    def send(self, message: str) -> None:
        self.messages.append(message)
```

Test:

```python
def test_send_welcome():
    fake = FakeSender()
    service = WelcomeService(fake)

    service.send_welcome("janette@example.com")

    assert fake.messages == ["Welcome, janette@example.com"]
```

### Why this stays simple
Even though the application may use factories and providers at runtime, the core service still remains easy to test directly.

That is a strong sign that dependency inversion is working well.

---

## 32. Common mistakes

### 1. Creating factories for trivial objects
Not every constructor needs a factory.

### 2. Creating providers that become service locators everywhere
A provider should help composition, not become a global hidden dependency lookup tool.

### 3. Overusing abstraction too early
If the variation is imaginary, the abstraction may be wasted complexity.

### 4. Confusing protocols with implementation inheritance
Protocols define required behavior. They do not require class hierarchy coupling.

### 5. Hiding too much wiring
Dependency creation should be organized, but not so hidden that the architecture becomes hard to follow.

---

## 33. A warning about the service locator anti-pattern

A provider can become harmful if code starts doing this everywhere:

```python
service = global_provider.get_service()
```

inside arbitrary business logic.

### Why this can be bad
It hides dependencies instead of making them explicit.

A healthier pattern is:
- providers assemble objects at boundaries
- services receive dependencies explicitly

This keeps dependency flow easier to understand and test.

---

## 34. Best practices

### 1. Use `Protocol` for capability-based abstraction
It is often the most Pythonic contract mechanism for DIP.

### 2. Inject dependencies explicitly
Constructor or function injection is simple and effective.

### 3. Use factories only when creation logic deserves its own place
Do not create them by habit.

### 4. Use providers for wiring and lifecycle management
Especially at application boundaries.

### 5. Keep business logic focused on behavior, not construction
That is the heart of dependency inversion.

### 6. Prefer explicit object graphs over hidden magic
Readable composition usually wins.

### 7. Keep tests direct
A well-inverted design should remain easy to test with fakes or mocks.

---

## 35. Practical mental model

A useful mental model is:

- **Protocol** answers:  
  “What behavior is required?”

- **Factory** answers:  
  “How do we create the right implementation?”

- **Provider** answers:  
  “How does the application supply and wire dependencies together?”

That separation is often enough to organize dependency inversion cleanly in Python.

---

## 36. When to use each pattern

### Use `Protocol`
when:
- you want a clear behavioral contract
- you want loose coupling
- you want type-checker support

### Use a factory
when:
- creation logic varies
- configuration selects the implementation
- construction is non-trivial

### Use a provider
when:
- you need centralized wiring
- you want lifecycle handling
- many objects need shared dependencies

You often do not need all three at once.  
Use the smallest set that solves the actual problem.

---

## 37. Final recommendation

A Pythonic approach to dependency inversion is usually:

- define behavior with `Protocol` when helpful
- inject dependencies explicitly
- use factories to separate construction logic when creation becomes non-trivial
- use providers at application boundaries to assemble dependencies cleanly

The goal is not abstraction for its own sake.  
The goal is to make code easier to test, change, and reason about.

---

## 38. Quick summary

If you only keep the essentials:

1. Dependency inversion means high-level logic should depend on capabilities, not concrete infrastructure details.
2. `Protocol` is a very Pythonic way to define those capabilities.
3. Factories help when object creation logic becomes conditional or complex.
4. Provider patterns help wire dependencies and manage lifecycle at the application level.
5. The best design keeps business logic explicit, decoupled, and easy to test.

---

# Coupling, Cohesion, and Testability

## 1. Goal

This guide explains three closely related software design concepts:

- **coupling**
- **cohesion**
- **testability**

It focuses on:

- what each concept means
- how they affect design quality
- how they influence maintainability
- how they relate to unit testing and integration testing
- practical examples in Python-style architecture
- common mistakes
- useful design heuristics

The goal is to help you design code that is easier to understand, change, and test.

---

## 2. Why these three concepts belong together

These concepts are deeply connected.

- **High coupling** often makes code harder to test.
- **Low cohesion** often makes code harder to understand and maintain.
- **Poor testability** is often a symptom of design problems in coupling or cohesion.

A lot of testing pain is actually design pain.

That is why these concepts are worth learning together instead of in isolation.

---

## 3. What is coupling?

**Coupling** describes how strongly one part of a system depends on another.

In simpler terms:

> Coupling answers: “How entangled are these pieces of code?”

If one class, module, or function cannot work without knowing too much about another, coupling is usually high.

---

## 4. What low coupling means

**Low coupling** means one component depends on another in a limited and clean way.

Examples:
- a service depends on a small protocol
- a function receives plain data instead of reaching into global state
- a class uses a repository abstraction instead of hardcoding a database client

### Why low coupling is good
It usually makes code:
- easier to replace
- easier to test
- easier to refactor
- easier to understand in isolation

---

## 5. What high coupling looks like

High coupling often appears when code:
- directly instantiates many concrete dependencies
- knows too much about infrastructure details
- depends on global state
- depends on deep internal behavior of another module
- mixes responsibilities across layers
- requires many unrelated objects just to run one small behavior

### Practical sign
If changing one file breaks many unrelated places, coupling may be too high.

---

## 6. What is cohesion?

**Cohesion** describes how well the parts inside a unit of code belong together.

In simpler terms:

> Cohesion answers: “Do these responsibilities naturally fit together?”

A highly cohesive function, class, or module has a clear, unified purpose.

A low-cohesion unit mixes unrelated concerns.

---

## 7. What high cohesion means

**High cohesion** means the code inside a unit is strongly related to one main responsibility.

Examples:
- a parser module focused on parsing
- a repository focused on persistence access
- a formatter focused on presentation formatting
- a validator focused on input rules

### Why high cohesion is good
It usually makes code:
- easier to name
- easier to read
- easier to change safely
- easier to test in focused ways

---

## 8. What low cohesion looks like

Low cohesion often appears when one unit tries to do too many unrelated things.

Example:

```python
class UserManager:
    def validate_email(self, email):
        ...

    def save_user(self, user):
        ...

    def send_welcome_email(self, user):
        ...

    def generate_pdf_report(self, user):
        ...

    def call_external_billing_api(self, user):
        ...
```

### Why this is problematic
This class is handling:
- validation
- persistence
- messaging
- reporting
- billing integration

These concerns do not naturally belong together.

That is a cohesion problem.

---

## 9. What is testability?

**Testability** describes how easily code can be tested in a reliable and focused way.

In simpler terms:

> Testability answers: “How easy is it to verify this code correctly?”

Testability depends on things like:
- how isolated the logic is
- how explicit dependencies are
- how deterministic behavior is
- how easy it is to control inputs and observe outputs

---

## 10. Why testability matters

Highly testable code is usually:
- faster to validate
- safer to refactor
- easier to debug
- easier to evolve

Poor testability usually causes:
- fragile tests
- slow tests
- hard-to-write tests
- too much mocking
- overdependence on integration environments

### Important
Testability is not only about tests.  
It is also about design quality.

---

## 11. Coupling and testability

Coupling strongly affects testability.

### Example of high coupling

```python
class OrderService:
    def place_order(self, order):
        db = PostgresClient()
        email = SmtpClient()
        logger = Logger()

        db.save(order)
        email.send("Order placed")
        logger.info("Order stored")
```

### Why this is hard to test
This method:
- creates concrete dependencies directly
- mixes infrastructure with business behavior
- forces tests to deal with database, email, and logging concerns

Even if you mock some parts, the design is already pushing complexity into testing.

---

## 12. Better example with lower coupling

```python
class OrderService:
    def __init__(self, repository, notifier, logger):
        self.repository = repository
        self.notifier = notifier
        self.logger = logger

    def place_order(self, order):
        self.repository.save(order)
        self.notifier.send("Order placed")
        self.logger.info("Order stored")
```

### Why this is better
Now:
- dependencies are explicit
- the service focuses on orchestration
- tests can use fakes or mocks easily

This improves coupling and testability at the same time.

---

## 13. Cohesion and testability

Cohesion also strongly affects testability.

A highly cohesive unit is easier to test because:
- the behavior is focused
- the number of test scenarios is more manageable
- the inputs and outputs are clearer

A low-cohesion unit is harder to test because:
- it contains multiple unrelated behaviors
- tests become large and confusing
- one test may need to verify too many concerns at once

---

## 14. Example of low cohesion hurting tests

```python
class ReportService:
    def build_report(self, user_id):
        user = self.fetch_user(user_id)
        text = self.format_report(user)
        self.save_to_disk(text)
        self.send_report_email(user, text)
        return text
```

### Why this becomes awkward to test
A test of `build_report()` may now need to care about:
- fetching data
- formatting
- disk writing
- email sending

That is a lot for one method.

It may still be a valid orchestration method, but if all details are embedded tightly, testing becomes harder.

---

## 15. Better cohesion through separated responsibilities

```python
class ReportBuilder:
    def build(self, user):
        return f"Report for {user['name']}"


class ReportService:
    def __init__(self, user_repo, report_builder, storage, notifier):
        self.user_repo = user_repo
        self.report_builder = report_builder
        self.storage = storage
        self.notifier = notifier

    def build_report(self, user_id):
        user = self.user_repo.get_by_id(user_id)
        report = self.report_builder.build(user)
        self.storage.save(report)
        self.notifier.send(report)
        return report
```

### Why this helps
Now different concerns are separated:
- fetching
- building
- saving
- notifying

This improves cohesion and gives more focused test points.

---

## 16. Testability is not only about mocking

A common mistake is to think:

> “If I can mock everything, the design is testable.”

Not necessarily.

A design can still be poor even if mocking makes tests possible.

Signs of weak design despite mocking:
- too many mocks per test
- tests that mostly verify implementation details
- brittle tests that break after harmless refactors
- confusing setup just to test one small behavior

Good testability usually means the code is naturally easy to test, not only mock-heavy.

---

## 17. Good signs of testable code

Code is often reasonably testable when:
- inputs are explicit
- outputs are clear
- side effects are isolated
- dependencies are injectable
- logic is deterministic
- responsibilities are focused
- hidden state is minimal

These qualities often improve both production code and test code.

---

## 18. Bad signs of poor testability

Common warning signs:
- methods require many unrelated dependencies
- code reads from globals, environment, or singletons everywhere
- functions do multiple unrelated things
- important behavior is buried in side effects
- tests need large setup for simple cases
- tests are slow because everything is integration-heavy
- tiny refactors break many tests

These are often design smells, not just testing inconveniences.

---

## 19. Types of coupling

You do not always need the formal taxonomy, but some distinctions are helpful.

### Structural coupling
One unit directly depends on another unit’s concrete implementation.

### Temporal coupling
Things must happen in a specific order to work correctly.

### Global coupling
Multiple parts depend on shared global state.

### Data-shape coupling
A consumer depends on too much of a large data object instead of only the needed fields.

### Why this matters
Different kinds of coupling create different maintenance and testing problems.

---

## 20. Global state and testability

Global state is a common source of high coupling and poor testability.

Example:

```python
CURRENT_ENV = "prod"


def calculate_price(base_price):
    if CURRENT_ENV == "prod":
        return base_price * 1.16
    return base_price
```

### Why this is problematic
The function depends on hidden external state.

That makes testing and reasoning harder because behavior is not fully controlled by the function inputs.

Better:

```python
def calculate_price(base_price, env):
    if env == "prod":
        return base_price * 1.16
    return base_price
```

### Why this is better
Now behavior depends on explicit input.

That reduces coupling and improves testability.

---

## 21. Hidden dependencies

A hidden dependency is a dependency the code uses without making it clear at the boundary.

Examples:
- imported globals
- environment access inside business logic
- implicit database calls
- singleton services
- module-level side effects

### Why hidden dependencies are dangerous
They make code:
- harder to reason about
- harder to isolate
- harder to test
- more surprising to maintain

Explicit dependencies usually improve both readability and testability.

---

## 22. Cohesion at function level

Cohesion is not only a class-level concern.

A function with high cohesion usually:
- does one clear job
- has a clear name
- has one main reason to change

Example:

```python
def normalize_email(email: str) -> str:
    return email.strip().lower()
```

This is focused and highly cohesive.

A low-cohesion function might:
- normalize the email
- validate permissions
- call an API
- write a file
- send a notification

That would make the function harder to test and understand.

---

## 23. Cohesion at module level

Modules can also be cohesive or non-cohesive.

A cohesive module groups related things, such as:
- only formatting helpers
- only user repository logic
- only date parsing utilities

A non-cohesive module becomes a dump of unrelated helpers.

Example bad module:
- email sending
- date parsing
- JSON validation
- file deletion
- payment calculation

That weakens discoverability and maintainability.

---

## 24. Coupling at module boundaries

Modules should usually depend on each other through stable, intentional boundaries.

Healthy examples:
- service depends on repository protocol
- API layer depends on service layer
- storage adapter depends on persistence library

Unhealthy examples:
- business logic depends directly on framework internals everywhere
- modules reach into each other’s private behavior
- one module imports many unrelated details from another

This kind of coupling often makes systems fragile.

---

## 25. Testability and determinism

Testable code is often deterministic.

**Deterministic** means:
- same input
- same controlled environment
- same output

Things that reduce determinism:
- current time
- random numbers
- external API state
- file system state
- environment variables
- global mutable state

### Better design approach
Isolate those unstable concerns so core logic remains deterministic.

---

## 26. Example with time dependency

Bad:

```python
from datetime import datetime


def is_morning():
    return datetime.now().hour < 12
```

### Problem
The result depends on the real clock.

Better:

```python
def is_morning(current_hour: int) -> bool:
    return current_hour < 12
```

Or inject a clock dependency:

```python
class Clock:
    def current_hour(self) -> int:
        ...
```

### Why this helps
Core behavior becomes easier to test without relying on real time.

---

## 27. Side effects and testability

Side effects are not bad by themselves, but they should be managed carefully.

Common side effects:
- writing files
- sending emails
- saving to DB
- network calls
- changing shared state

### Why side effects matter
The more side effects are mixed directly into core logic, the harder focused tests become.

A common design improvement is:
- keep pure logic separate
- isolate side effects at edges

---

## 28. Pure logic is usually highly testable

A **pure function**:
- depends only on its inputs
- has no hidden state
- has no side effects
- returns a value

Example:

```python
def apply_discount(price: float, percentage: float) -> float:
    return price * (1 - percentage)
```

### Why this is easy to test
It is:
- deterministic
- isolated
- explicit
- focused

Pure logic often represents the best-case scenario for testability.

---

## 29. Orchestration code can still be testable

Not all useful code is pure.

Some code coordinates:
- repositories
- external services
- notifications
- workflows

That orchestration code can still be testable if:
- dependencies are explicit
- behavior is focused
- side effects are delegated cleanly

This is why not every testable design must be “pure functional.”  
But purity often helps where possible.

---

## 30. Coupling, cohesion, and architecture layers

These concepts often appear clearly in layered architecture.

### Example layers
- API layer
- service/use-case layer
- repository layer
- infrastructure/adapters layer

Healthy structure often means:
- service layer is cohesive around business behavior
- service layer is loosely coupled to infra through contracts
- infra can change without rewriting core use cases

This improves maintainability and testability significantly.

---

## 31. Example: layered testability

Suppose you have:

- `UserService` for business logic
- `UserRepository` protocol
- `PostgresUserRepository` for real DB
- `FakeUserRepository` for tests

### Why this is strong
The service is:
- cohesive around business logic
- loosely coupled to storage details
- easy to test with a fake repo

This is a strong example of design supporting testability.

---

## 32. Coupling and mocking pressure

Too much mocking can be a sign of too much coupling.

If a simple unit test needs:
- 6 mocks
- 10 lines of stubbing
- 8 interaction assertions

then maybe the problem is not the test framework.

Maybe the unit itself:
- depends on too many collaborators
- does too many things
- has weak cohesion
- is too coupled to implementation details

This is a useful diagnostic mindset.

---

## 33. Cohesion and naming

Cohesion often appears in naming quality.

If a class or module is hard to name clearly, that can be a sign of low cohesion.

Good cohesive names tend to be easier:
- `EmailSender`
- `UserRepository`
- `PriceCalculator`
- `ReportFormatter`

Bad low-cohesion names tend to become vague:
- `Manager`
- `Processor`
- `Handler`
- `Utils`
- `Helper`

These names often hide mixed responsibilities.

---

## 34. Cohesion and change patterns

A practical question for cohesion is:

> “Do the things inside this unit tend to change together?”

If yes, they may belong together.

If not, cohesion may be weak.

For example:
- report formatting and email transport probably do not change together
- password hashing and image resizing probably do not belong together
- tax calculation and UI CSS generation definitely do not belong together

This “change together” heuristic is very useful.

---

## 35. Coupling and refactoring difficulty

High coupling often makes refactoring scary because:
- you are not sure what depends on what
- changes ripple unpredictably
- side effects are hidden
- tests become brittle or incomplete

Low coupling usually makes refactoring safer because:
- dependencies are explicit
- boundaries are clearer
- isolated tests give better confidence

This is one of the biggest practical reasons to care about coupling.

---

## 36. Common mistakes

### 1. Thinking “more abstraction” always means lower coupling
Bad abstractions can still create strong coupling.

### 2. Splitting code too aggressively in the name of cohesion
Tiny fragmented units are not automatically better.

### 3. Treating testability as “just use mocks”
That often hides deeper design problems.

### 4. Mixing orchestration, pure logic, and infrastructure in one place
This often hurts both cohesion and testability.

### 5. Depending on globals or hidden environment state
This increases coupling and reduces determinism.

### 6. Designing only for production flow and ignoring test boundaries
This usually makes later testing painful.

---

## 37. Best practices

### 1. Keep responsibilities cohesive
Units should have a clear, focused purpose.

### 2. Make dependencies explicit
Prefer injection or explicit parameters over hidden lookups.

### 3. Isolate side effects
Keep them at the edges when possible.

### 4. Prefer stable contracts over concrete details
This reduces coupling.

### 5. Keep core logic deterministic
This improves testability a lot.

### 6. Watch mocking pressure
Too many mocks may signal a design smell.

### 7. Use tests as feedback on design
If testing is painful, design may need improvement.

---

## 38. Practical mental model

A useful mental model is:

- **coupling** asks:  
  “How dependent is this on other parts?”

- **cohesion** asks:  
  “How well do the responsibilities inside this unit belong together?”

- **testability** asks:  
  “How easy is it to verify this behavior in a focused, reliable way?”

Good design often looks like:
- lower coupling
- higher cohesion
- higher testability

These qualities often reinforce each other.

---

## 39. A simple design heuristic

When reviewing a class, function, or module, ask:

1. Does it have one clear purpose?
2. Are its dependencies explicit?
3. Does it rely on hidden state?
4. Can I test it without spinning up half the system?
5. Does testing it require too much mocking or setup?
6. Would a change here force unrelated changes elsewhere?

These questions quickly reveal many design problems.

---

## 40. Final recommendation

A good practical goal is not:

- zero coupling
- maximum fragmentation
- perfect theoretical purity

A better goal is:

- keep code cohesive enough to understand
- keep coupling low enough to change safely
- keep behavior testable enough to verify confidently

That balance is what usually produces maintainable systems.

---

## 41. Quick summary

If you only keep the essentials:

1. Coupling is about how strongly code depends on other code.
2. Cohesion is about how well the responsibilities inside a unit fit together.
3. Testability is about how easily behavior can be verified reliably.
4. Low coupling and high cohesion usually improve testability.
5. If code is painful to test, that is often a design signal worth paying attention to.

---
