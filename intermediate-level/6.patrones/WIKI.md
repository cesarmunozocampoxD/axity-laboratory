# Creational Patterns in Python: Factory, Abstract Factory, Builder, Singleton (and When to Avoid It)

## 1. Goal

This guide explains four classic **creational design patterns** in a practical, Python-oriented way:

- **Factory**
- **Abstract Factory**
- **Builder**
- **Singleton**
- and especially **when Singleton should be avoided**

It focuses on:

- what each pattern is for
- when it is useful
- how to express it in Python
- how to avoid overengineering
- common mistakes
- Pythonic alternatives

The goal is not to memorize textbook definitions.  
The goal is to understand when these patterns actually help in real code.

---

## 2. What creational patterns are

Creational patterns are about **object creation**.

They help answer questions like:

- who should create this object?
- how should the object be built?
- how do we vary the implementation?
- how do we hide construction details?
- how do we avoid hardcoding concrete classes everywhere?

### In simple terms
Creational patterns help organize **how objects come into existence**.

---

## 3. Why creational patterns matter

Object creation can look simple at first:

```python
user = User("Janette")
```

But in real systems, creation often becomes more complex:

- different implementations may exist
- configuration may decide what gets built
- object graphs may be large
- setup may be expensive
- some objects may need step-by-step construction
- some objects may need controlled lifecycle

Creational patterns help handle those situations more cleanly.

---

## 4. A Pythonic note before starting

In Python, design patterns should usually be applied with restraint.

A common mistake is to copy pattern-heavy examples from very class-heavy languages and turn simple Python code into something much more complex than needed.

### Pythonic rule of thumb
If a function, a simple class, or a clear module-level helper solves the problem, that may already be enough.

Patterns are useful when they reduce complexity, not when they add ceremony.

---

# Factory

## 5. What Factory means

A **Factory** centralizes object creation.

Instead of scattering construction logic everywhere, you place that logic in one function or class responsible for building the right object.

### Practical question Factory solves
> “How do I create the right implementation without hardcoding it all over the codebase?”

---

## 6. Basic problem Factory solves

Without a factory:

```python
if channel == "email":
    sender = EmailSender()
elif channel == "sms":
    sender = SmsSender()
else:
    raise ValueError("Unsupported channel")
```

If this logic appears in many places, the code becomes repetitive and harder to maintain.

A factory moves that creation decision into one place.

---

## 7. Simple factory function example

```python
class EmailSender:
    def send(self, message: str) -> None:
        print(f"Email: {message}")


class SmsSender:
    def send(self, message: str) -> None:
        print(f"SMS: {message}")


def create_sender(channel: str):
    if channel == "email":
        return EmailSender()
    if channel == "sms":
        return SmsSender()
    raise ValueError(f"Unsupported channel: {channel}")
```

Usage:

```python
sender = create_sender("email")
sender.send("Hello")
```

### Why this helps
Creation logic now lives in one place.

---

## 8. Why Factory is useful

Factory is useful when:
- object creation depends on input or configuration
- object creation is repeated in many places
- you want to hide concrete classes from callers
- you want easier extension or substitution
- creation logic is more complex than a direct constructor call

---

## 9. Factory as a class

Sometimes a class-based factory is helpful.

```python
class SenderFactory:
    def create(self, channel: str):
        if channel == "email":
            return EmailSender()
        if channel == "sms":
            return SmsSender()
        raise ValueError(f"Unsupported channel: {channel}")
```

Usage:

```python
factory = SenderFactory()
sender = factory.create("sms")
```

### When a class factory makes sense
Usually when:
- it needs configuration
- it needs dependencies
- creation is stateful
- you want to replace or mock the factory itself

---

## 10. Pythonic interpretation of Factory

In Python, Factory is often just:
- a function
- a dictionary-based registry
- a callable provider
- a small class when necessary

It does not always need a formal inheritance hierarchy.

### Example with registry

```python
senders = {
    "email": EmailSender,
    "sms": SmsSender,
}


def create_sender(channel: str):
    try:
        return senders[channel]()
    except KeyError:
        raise ValueError(f"Unsupported channel: {channel}")
```

This is often a very Pythonic Factory style.

---

## 11. When Factory may be overkill

Factory may be unnecessary when:
- there is only one simple implementation
- object construction is trivial
- there is no variation in creation
- introducing a factory only adds indirection without solving a real problem

Bad example:
- creating a factory for `Point(x, y)` when `Point(x, y)` is already perfectly clear

---

# Abstract Factory

## 12. What Abstract Factory means

**Abstract Factory** creates **families of related objects**.

While a simple Factory usually creates one product type, an Abstract Factory creates multiple related products that are meant to work together.

### Practical question it solves
> “How do I create a consistent set of related objects for one environment, theme, backend, or platform?”

---

## 13. Example use case for Abstract Factory

Suppose you support two UI themes:
- Light
- Dark

You need related objects:
- Button
- Dialog
- Input

You want the light versions together and the dark versions together.

That is a classic Abstract Factory scenario.

---

## 14. Basic Abstract Factory example

```python
class LightButton:
    def render(self):
        return "Light button"


class DarkButton:
    def render(self):
        return "Dark button"


class LightDialog:
    def render(self):
        return "Light dialog"


class DarkDialog:
    def render(self):
        return "Dark dialog"
```

Factory classes:

```python
class LightUIFactory:
    def create_button(self):
        return LightButton()

    def create_dialog(self):
        return LightDialog()


class DarkUIFactory:
    def create_button(self):
        return DarkButton()

    def create_dialog(self):
        return DarkDialog()
```

Usage:

```python
factory = DarkUIFactory()
button = factory.create_button()
dialog = factory.create_dialog()
```

### Why this helps
You get a consistent family of matching objects from one factory.

---

## 15. Why Abstract Factory is useful

Abstract Factory is useful when:
- there are multiple related product families
- objects must remain consistent with each other
- environment or platform selects a full set of implementations
- you want to swap entire families of components at once

Typical examples:
- UI themes
- database backends
- cloud provider integrations
- environment-specific adapters
- test vs production infrastructure bundles

---

## 16. Pythonic Abstract Factory

In Python, Abstract Factory does not always require formal abstract base classes.

It can be expressed with:
- simple classes with matching methods
- Protocol-based contracts
- module-based families
- even dictionaries or provider objects in simpler cases

Example with Protocol:

```python
from typing import Protocol


class UIFactory(Protocol):
    def create_button(self):
        ...

    def create_dialog(self):
        ...
```

This keeps the abstraction behavioral rather than inheritance-heavy.

---

## 17. Abstract Factory vs simple Factory

### Factory
Creates one kind of product, usually based on some input.

### Abstract Factory
Creates a family of related products that should stay compatible.

### Practical shortcut
If you are only choosing one implementation, it is often just Factory.  
If you are choosing a whole set of related implementations together, it is often Abstract Factory.

---

## 18. When Abstract Factory may be overkill

Abstract Factory may be unnecessary when:
- there is only one product type
- products are not really related families
- the “family” concept is artificial
- a simple factory or provider is enough

It becomes harmful when it introduces many classes without a real coordination problem to solve.

---

# Builder

## 19. What Builder means

**Builder** is used when object creation is:
- step-by-step
- configurable
- complex
- easier to understand as a sequence of construction steps

### Practical question Builder solves
> “How do I build a complex object in a controlled, readable way?”

---

## 20. Basic problem Builder solves

Suppose an object needs many optional parts:

```python
report = Report(
    title="Monthly",
    include_graphs=True,
    include_summary=True,
    include_footer=False,
    theme="dark",
    export_format="pdf",
)
```

Sometimes long constructors become:
- hard to read
- easy to misuse
- difficult to validate
- awkward when steps are conditional

Builder can make that construction clearer.

---

## 21. Basic Builder example

```python
class Report:
    def __init__(self):
        self.title = None
        self.include_summary = False
        self.include_graphs = False
        self.theme = "light"


class ReportBuilder:
    def __init__(self):
        self.report = Report()

    def set_title(self, title: str):
        self.report.title = title
        return self

    def enable_summary(self):
        self.report.include_summary = True
        return self

    def enable_graphs(self):
        self.report.include_graphs = True
        return self

    def set_theme(self, theme: str):
        self.report.theme = theme
        return self

    def build(self):
        return self.report
```

Usage:

```python
report = (
    ReportBuilder()
    .set_title("Monthly")
    .enable_summary()
    .enable_graphs()
    .set_theme("dark")
    .build()
)
```

### Why this helps
The construction becomes more readable and expressive.

---

## 22. Why Builder is useful

Builder is useful when:
- an object has many optional settings
- creation happens in multiple steps
- different configurations must be assembled clearly
- you want fluent chaining
- validation should happen before final creation
- construction logic should be separated from the final object

---

## 23. Builder and validation

One strong use case is validating before `build()` returns the final object.

```python
class ReportBuilder:
    def __init__(self):
        self.report = Report()

    def set_title(self, title: str):
        self.report.title = title
        return self

    def build(self):
        if not self.report.title:
            raise ValueError("Title is required")
        return self.report
```

### Why this helps
The Builder can enforce construction rules in one place.

---

## 24. Pythonic alternatives to Builder

In Python, Builder is often not necessary because the language already supports expressive construction through:
- keyword arguments
- dataclasses
- default values
- helper functions
- dictionaries
- named constructors

Example with dataclass:

```python
from dataclasses import dataclass


@dataclass
class Report:
    title: str
    include_summary: bool = False
    include_graphs: bool = False
    theme: str = "light"
```

This may already be enough.

### Pythonic rule
Use Builder when it genuinely improves clarity, sequencing, or validation, not just because the pattern exists.

---

## 25. Builder vs Factory

### Factory
Focuses on choosing or creating the right object.

### Builder
Focuses on constructing a potentially complex object step by step.

### Practical difference
Factory answers:
- “Which object do I create?”

Builder answers:
- “How do I assemble this object cleanly?”

Sometimes both can be used together.

---

## 26. When Builder may be overkill

Builder may be unnecessary when:
- keyword arguments already make construction clear
- the object is simple
- there are only a few parameters
- a helper function or dataclass is enough

Bad example:
- creating a full Builder for a simple `User(name, email)` object

---

# Singleton

## 27. What Singleton means

**Singleton** is a pattern that ensures there is only **one instance** of a class in a process and provides a global access point to it.

### Practical question it tries to solve
> “How do I guarantee a single shared instance?”

Examples often mentioned:
- logger
- config manager
- cache manager
- database connection manager

---

## 28. Basic Singleton example

```python
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

Usage:

```python
a = Singleton()
b = Singleton()

assert a is b
```

### What this does
It ensures every construction returns the same instance.

---

## 29. Why Singleton is attractive

Singleton is attractive because it seems to offer:
- one shared resource
- easy global access
- controlled lifecycle
- reduced duplication

At first glance, it can look convenient.

---

## 30. Why Singleton is dangerous

Singleton often introduces hidden problems:

- hidden global state
- implicit coupling
- poor testability
- order-dependent behavior
- hard-to-control lifecycle
- surprising state sharing between tests or modules

### Important
Singleton is one of the most overused patterns in software design.

---

## 31. Why Singleton often hurts testability

If code depends on a global singleton, tests may:
- share state accidentally
- depend on test execution order
- require cleanup between runs
- become harder to isolate
- be harder to reason about

Example problem:

```python
class ConfigSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.mode = "prod"
        return cls._instance
```

One test may change `.mode`, and another test may unexpectedly observe that changed state.

That is a classic source of brittle tests.

---

## 32. Singleton and hidden dependencies

A major design problem with Singleton is that it often hides dependencies.

Bad style:

```python
config = ConfigSingleton()

def process_data():
    if config.mode == "prod":
        ...
```

### Why this is problematic
`process_data()` depends on configuration, but that dependency is not explicit in its interface.

That increases coupling and reduces clarity.

---

## 33. When to avoid Singleton

Avoid Singleton when:
- explicit dependency injection is possible
- shared state would make testing harder
- lifecycle control is better handled at the application level
- the “single instance” requirement is not truly necessary
- the pattern is being used mainly for convenience

### Strong rule of thumb
If you mainly want “easy global access,” that is usually a warning sign.

---

## 34. Better alternative: explicit shared instance

Often you do not need Singleton at all.

You can just create one instance at the application boundary and pass it where needed.

```python
class Config:
    def __init__(self, mode: str):
        self.mode = mode


config = Config(mode="prod")
```

Then inject it:

```python
class DataProcessor:
    def __init__(self, config: Config):
        self.config = config
```

### Why this is better
You still have one shared instance if you want it, but without hiding the dependency behind a global Singleton pattern.

---

## 35. Better alternative: module-level object

Sometimes a simple module-level object is enough.

```python
# config.py
class Config:
    def __init__(self):
        self.mode = "prod"


config = Config()
```

### Important nuance
This is still shared state, but it is often simpler and more honest than building a formal Singleton pattern around it.

Even then, explicit injection is usually more testable.

---

## 36. Better alternative: provider or container at app boundary

Another better option is to let an application provider create and manage shared instances.

```python
class AppProvider:
    def __init__(self):
        self.config = Config("prod")

    def get_config(self):
        return self.config
```

### Why this helps
You still centralize lifecycle, but the architecture remains more explicit and testable.

---

## 37. When Singleton may be acceptable

Singleton can sometimes be acceptable when:
- process-wide single-instance semantics are truly required
- the state is minimal and carefully controlled
- the object is infrastructure-like
- alternatives would be clearly worse
- the team fully understands the trade-offs

Even then, it should be a deliberate choice, not a default habit.

---

## 38. Singleton in Pythonic design

In Pythonic design, Singleton is often replaced by:
- module-level state
- explicit dependency injection
- providers
- application wiring
- cached factories
- lazy-loaded services

This usually produces code that is easier to test and reason about.

### Pythonic conclusion
Singleton is often less necessary in Python than people initially think.

---

# Comparing the four patterns

## 39. Quick comparison

### Factory
Creates one appropriate object.

### Abstract Factory
Creates a family of related objects.

### Builder
Constructs a complex object step by step.

### Singleton
Restricts creation to one shared instance.

---

## 40. Practical selection guide

Use **Factory** when:
- you need to choose between implementations
- creation logic should be centralized

Use **Abstract Factory** when:
- multiple related object families must stay consistent

Use **Builder** when:
- an object has many optional parts or staged construction

Use **Singleton** only with caution:
- when single-instance semantics are truly needed
- and explicit alternatives are not better

---

## 41. Common mistakes

### 1. Using Factory for trivial constructors
If construction is already obvious, the factory adds noise.

### 2. Using Abstract Factory when only one product varies
That is often just a normal Factory.

### 3. Using Builder when keyword arguments are already enough
Python often makes complex builders unnecessary.

### 4. Using Singleton for convenience
This is one of the most common design mistakes.

### 5. Forcing patterns because of theory
Patterns should solve actual design pressure, not decorate simple code.

---

## 42. Best practices

### 1. Start simple
Use normal constructors first unless creation logic becomes awkward.

### 2. Introduce Factory when creation logic repeats or varies
This is where it usually pays off.

### 3. Use Abstract Factory only when there is a real product family concept
Do not invent one artificially.

### 4. Use Builder when construction sequencing or readability becomes important
Not just because an object has a few fields.

### 5. Avoid Singleton by default
Prefer explicit dependencies and controlled application wiring.

### 6. Keep patterns Pythonic
Prefer clarity and practicality over ceremony.

---

## 43. Practical mental model

A useful mental model is:

- **Factory** → “Which object should I create?”
- **Abstract Factory** → “Which related family of objects should I create?”
- **Builder** → “How do I assemble this object cleanly?”
- **Singleton** → “Do I really need one instance, or do I just want global convenience?”

That last question is especially important.

---

## 44. Final recommendation

In Python, creational patterns are most useful when they solve real creation problems:

- Factory for varying implementations
- Abstract Factory for consistent product families
- Builder for staged or validated construction
- Singleton only very carefully, and often not at all

A Pythonic approach prefers:
- simple constructors first
- explicit dependencies
- composition
- provider/factory helpers when needed
- avoiding hidden global state whenever possible

If a pattern makes the code clearer and easier to change, it is helping.  
If it makes the code more abstract without solving a real problem, it is probably too much.

---

## 45. Quick summary

If you only keep the essentials:

1. Factory centralizes creation of the right object.
2. Abstract Factory creates consistent families of related objects.
3. Builder helps construct complex objects step by step.
4. Singleton enforces one shared instance, but often harms clarity and testability.
5. In Python, prefer the simplest pattern that solves the real creation problem.

---

# Structural Patterns in Python: Adapter, Facade, Composite, Decorator, Proxy

## 1. Goal

This guide explains five classic **structural design patterns** in a practical, Python-oriented way:

- **Adapter**
- **Facade**
- **Composite**
- **Decorator**
- **Proxy**

It focuses on:

- what each pattern is for
- when each one is useful
- how to express them in Python
- common misunderstandings
- Pythonic alternatives
- practical trade-offs

The goal is not to memorize textbook names.  
The goal is to understand how these patterns help organize relationships between objects and interfaces.

---

## 2. What structural patterns are

Structural patterns are about **how code elements are connected and composed**.

They help answer questions like:

- how do I make incompatible interfaces work together?
- how do I simplify a complicated subsystem?
- how do I represent tree-like structures?
- how do I add behavior without changing the original object?
- how do I control access to another object?

### In simple terms
Structural patterns help shape **how objects fit together**.

---

## 3. A Pythonic note before starting

In Python, structural patterns should be applied pragmatically.

A common mistake is to implement the “full formal pattern” even when:
- a function would be enough
- composition is already obvious
- the problem is smaller than the pattern

### Pythonic rule
Use the pattern when it clarifies the design or isolates complexity.  
Do not force it for its own sake.

---

# Adapter

## 4. What Adapter means

**Adapter** makes one interface work like another expected interface.

### Practical question it solves
> “How do I use this existing object even though its interface does not match what my code expects?”

It is especially useful when:
- integrating third-party libraries
- wrapping legacy code
- unifying multiple APIs behind one expected shape

---

## 5. Basic Adapter idea

Suppose your application expects this:

```python
class MessageSender:
    def send(self, message: str) -> None:
        ...
```

But a third-party library gives you:

```python
class SlackClient:
    def post_message(self, text: str) -> None:
        print(f"Slack: {text}")
```

The interfaces do not match.

Adapter solves that mismatch.

---

## 6. Adapter example

```python
class SlackClient:
    def post_message(self, text: str) -> None:
        print(f"Slack: {text}")


class SlackAdapter:
    def __init__(self, client: SlackClient) -> None:
        self.client = client

    def send(self, message: str) -> None:
        self.client.post_message(message)
```

Usage:

```python
client = SlackClient()
sender = SlackAdapter(client)
sender.send("Hello")
```

### Why this helps
Your application can keep using `.send(...)` even though the third-party client uses `.post_message(...)`.

---

## 7. Why Adapter is useful

Adapter is useful when:
- you cannot change the original class
- you want to keep your internal interface stable
- you need compatibility between systems
- you want to isolate integration code from business logic

### Good design effect
Business code depends on your expected interface, not on every external API variation.

---

## 8. Pythonic Adapter alternatives

In Python, Adapter may be:
- a small wrapper class
- a function wrapper
- a lambda in simple cases
- a protocol-compatible object

### Example with function wrapper

```python
def slack_sender(client):
    def send(message: str) -> None:
        client.post_message(message)
    return send
```

This can be enough when the integration is simple.

---

## 9. When Adapter may be overkill

Adapter may be unnecessary when:
- the interface mismatch is tiny and used only once
- a direct one-line transformation is clearer
- no stable internal contract is needed

But if multiple external systems must conform to one internal interface, Adapter often becomes very valuable.

---

# Facade

## 10. What Facade means

**Facade** provides a simplified interface to a more complex subsystem.

### Practical question it solves
> “How do I make a complicated set of operations easier to use?”

Facade is often about reducing complexity for callers.

---

## 11. Example problem Facade solves

Suppose sending a notification requires:
- formatting a message
- choosing a channel
- logging delivery
- retry handling
- tracking metrics

Without a Facade, callers may need to coordinate all of that.

A Facade can expose something simpler:

```python
notification_service.notify(user, message)
```

while hiding the internal orchestration.

---

## 12. Facade example

```python
class MessageFormatter:
    def format(self, message: str) -> str:
        return f"[Formatted] {message}"


class EmailSender:
    def send(self, message: str) -> None:
        print(f"Email: {message}")


class Logger:
    def info(self, message: str) -> None:
        print(f"LOG: {message}")


class NotificationFacade:
    def __init__(self):
        self.formatter = MessageFormatter()
        self.sender = EmailSender()
        self.logger = Logger()

    def notify(self, message: str) -> None:
        formatted = self.formatter.format(message)
        self.sender.send(formatted)
        self.logger.info("Notification sent")
```

Usage:

```python
facade = NotificationFacade()
facade.notify("Welcome")
```

### Why this helps
Callers interact with one clean interface instead of many subsystem steps.

---

## 13. Why Facade is useful

Facade is useful when:
- a subsystem is hard to use directly
- many callers need the same workflow
- you want to expose a stable simplified API
- you want to isolate internal complexity
- you want to reduce coupling to internal details

---

## 14. Facade is not the same as “god object”

A common mistake is turning Facade into a giant object that does everything.

That is not the goal.

A good Facade:
- simplifies access
- coordinates related subsystem behavior
- does not become a dumping ground for unrelated responsibilities

### Practical distinction
Facade simplifies a subsystem.  
It should not replace all architecture with one huge entry point.

---

## 15. Pythonic Facade

In Python, a Facade can be:
- a class
- a service object
- a module-level helper API
- a function that orchestrates a repeated multi-step flow

### Example with function-style facade

```python
def notify_user(formatter, sender, logger, message: str) -> None:
    formatted = formatter.format(message)
    sender.send(formatted)
    logger.info("Notification sent")
```

This can act like a Facade without requiring a large class, depending on context.

---

## 16. When Facade may be overkill

Facade may be unnecessary when:
- the subsystem is already simple
- callers do not benefit from another abstraction layer
- the orchestration is trivial and only used once

But when complexity repeats, Facade often improves readability a lot.

---

# Composite

## 17. What Composite means

**Composite** lets you treat individual objects and groups of objects in a uniform way.

### Practical question it solves
> “How do I represent part-whole hierarchies so clients can work with leaves and containers similarly?”

This is common in:
- tree structures
- UI component hierarchies
- menu structures
- file systems
- nested rules
- document structures

---

## 18. Composite idea

Suppose you have:
- a single file
- a folder containing files and folders

You want to interact with both using a similar interface like:

```python
node.render()
node.size()
node.print()
```

Composite makes this possible.

---

## 19. Composite example

```python
class File:
    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self.size = size

    def get_size(self) -> int:
        return self.size


class Folder:
    def __init__(self, name: str) -> None:
        self.name = name
        self.children = []

    def add(self, child) -> None:
        self.children.append(child)

    def get_size(self) -> int:
        return sum(child.get_size() for child in self.children)
```

Usage:

```python
file1 = File("a.txt", 10)
file2 = File("b.txt", 20)

folder = Folder("docs")
folder.add(file1)
folder.add(file2)

print(folder.get_size())
```

### Why this helps
Both `File` and `Folder` expose `get_size()`, even though one is a leaf and the other is a container.

---

## 20. Why Composite is useful

Composite is useful when:
- data is naturally hierarchical
- clients should handle single items and nested groups similarly
- recursive composition is natural
- you want cleaner tree traversal logic

---

## 21. Composite and recursion

Composite structures often go naturally with recursion.

```python
class Folder:
    def __init__(self, name: str) -> None:
        self.name = name
        self.children = []

    def add(self, child) -> None:
        self.children.append(child)

    def print_tree(self, level=0) -> None:
        print("  " * level + self.name)
        for child in self.children:
            child.print_tree(level + 1)
```

Leaf:

```python
class File:
    def __init__(self, name: str) -> None:
        self.name = name

    def print_tree(self, level=0) -> None:
        print("  " * level + self.name)
```

### Why this is elegant
The caller can treat folders and files uniformly during traversal.

---

## 22. Pythonic Composite

In Python, Composite often appears naturally through:
- recursive objects
- nested dataclasses
- tree node classes
- recursive protocols or interfaces

It does not always need elaborate pattern ceremony.  
Sometimes the structure itself already suggests the pattern.

---

## 23. When Composite may be overkill

Composite may be unnecessary when:
- the structure is flat
- there is no recursive containment
- leaf and group behavior are too different to benefit from one shared interface

If there is no real “part-whole hierarchy,” Composite is probably not the right tool.

---

# Decorator

## 24. What Decorator means

**Decorator** adds behavior to an object without changing its original class.

### Practical question it solves
> “How do I extend behavior dynamically or compositionally without editing the original implementation?”

Decorator is about wrapping an object and forwarding behavior with additions.

---

## 25. Basic Decorator idea

Suppose you have:

```python
class Text:
    def render(self) -> str:
        return "hello"
```

You want:
- bold text
- italic text
- uppercase text
- combinations of those behaviors

Decorator is a clean way to wrap and compose those effects.

---

## 26. Decorator object example

```python
class Text:
    def render(self) -> str:
        return "hello"


class BoldDecorator:
    def __init__(self, component) -> None:
        self.component = component

    def render(self) -> str:
        return f"<b>{self.component.render()}</b>"
```

Usage:

```python
text = Text()
bold_text = BoldDecorator(text)

print(bold_text.render())
```

### Why this helps
You add behavior without modifying `Text`.

---

## 27. Multiple decorators

Decorators can be composed.

```python
class ItalicDecorator:
    def __init__(self, component) -> None:
        self.component = component

    def render(self) -> str:
        return f"<i>{self.component.render()}</i>"
```

Usage:

```python
text = Text()
decorated = ItalicDecorator(BoldDecorator(text))
print(decorated.render())
```

### Why useful
Behavior can be layered dynamically.

---

## 28. Why Decorator is useful

Decorator is useful when:
- you want to add responsibilities dynamically
- multiple combinations of behavior are possible
- inheritance would explode into many subclasses
- the base class should stay unchanged
- extensions should remain composable

---

## 29. Python decorators vs Decorator pattern

Important distinction:

### Python language decorator
The `@something` syntax applied to functions or classes.

### Decorator design pattern
A structural object pattern that wraps another object and extends behavior.

They are related conceptually because both “wrap behavior,” but they are not identical.

---

## 30. Python function decorator example

Python’s `@decorator` syntax is often a very natural expression of the same core idea.

```python
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


@log_calls
def greet():
    print("hello")
```

### Why this matters
Python has built-in syntactic support for function decoration, which makes the concept feel especially natural in the language.

---

## 31. When Decorator may be overkill

Decorator may be unnecessary when:
- one simple conditional would be clearer
- behavior extension is not composable
- the wrapping adds confusion without real flexibility

But when subclass combinations would explode, Decorator is often a very clean alternative.

---

# Proxy

## 32. What Proxy means

**Proxy** provides a stand-in object that controls access to another object.

### Practical question it solves
> “How do I intercept, delay, restrict, cache, protect, or monitor access to a real object?”

Proxy keeps the same general interface while adding control.

---

## 33. Common Proxy use cases

Proxy is often used for:
- lazy loading
- access control
- caching
- logging
- remote object access
- validation before forwarding
- rate limiting
- permission checks

---

## 34. Basic Proxy example

```python
class RealImage:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        print(f"Loading image from {filename}")

    def display(self) -> None:
        print(f"Displaying {self.filename}")
```

Proxy:

```python
class ImageProxy:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self._real_image = None

    def display(self) -> None:
        if self._real_image is None:
            self._real_image = RealImage(self.filename)
        self._real_image.display()
```

Usage:

```python
image = ImageProxy("photo.png")
image.display()
image.display()
```

### Why this helps
The real image is loaded only when needed.

This is a classic lazy-loading proxy.

---

## 35. Access-control Proxy example

```python
class AdminPanel:
    def delete_user(self, user_id: int) -> None:
        print(f"Deleted user {user_id}")
```

Proxy:

```python
class AdminPanelProxy:
    def __init__(self, panel: AdminPanel, is_admin: bool) -> None:
        self.panel = panel
        self.is_admin = is_admin

    def delete_user(self, user_id: int) -> None:
        if not self.is_admin:
            raise PermissionError("Not allowed")
        self.panel.delete_user(user_id)
```

### Why useful
The proxy controls access before delegating to the real object.

---

## 36. Why Proxy is useful

Proxy is useful when:
- you need control around a real object
- the real object is expensive
- access should be conditional
- lazy creation is valuable
- caching or monitoring should happen transparently
- the caller should not need to know about the control layer

---

## 37. Proxy vs Decorator

These patterns are similar because both wrap another object.

### Decorator
Focuses on **adding behavior or responsibilities**.

### Proxy
Focuses on **controlling access** to the original object.

### Practical shortcut
If the wrapper mainly enriches behavior, think Decorator.  
If the wrapper mainly controls or mediates access, think Proxy.

Sometimes the line can blur, but the design intent is different.

---

## 38. Pythonic Proxy

In Python, Proxy can often be a:
- wrapper object
- lazy-loaded object
- cached service layer
- permission-checked adapter
- remote-call stand-in

It does not always require a formal interface hierarchy.

---

## 39. When Proxy may be overkill

Proxy may be unnecessary when:
- a direct helper function is enough
- there is no real access-control or indirection problem
- lazy loading or mediation is not needed
- the wrapper adds more confusion than value

---

# Comparing the five patterns

## 40. Quick comparison

### Adapter
Makes incompatible interfaces work together.

### Facade
Simplifies access to a complex subsystem.

### Composite
Lets you treat leaves and groups uniformly.

### Decorator
Adds behavior by wrapping an object.

### Proxy
Controls access to another object.

---

## 41. Practical selection guide

Use **Adapter** when:
- you need compatibility between mismatched interfaces

Use **Facade** when:
- you want a simpler entry point to a subsystem

Use **Composite** when:
- you have tree-like part-whole structures

Use **Decorator** when:
- you want composable behavior extension without subclass explosion

Use **Proxy** when:
- you need access control, lazy loading, caching, or mediation

---

## 42. Common mistakes

### 1. Confusing Adapter and Facade
Adapter changes interface compatibility.  
Facade simplifies a subsystem.

### 2. Confusing Decorator and Proxy
Decorator adds responsibilities.  
Proxy controls access.

### 3. Forcing Composite on flat data
Composite only helps when hierarchy is real.

### 4. Overengineering wrappers
Not every small wrapper is a meaningful design pattern.

### 5. Building patterns instead of solving the problem
The pattern should clarify the architecture, not decorate it.

---

## 43. Best practices

### 1. Start from the problem, not the pattern name
Ask what is actually difficult: compatibility, complexity, hierarchy, extension, or access control.

### 2. Keep wrappers focused
A wrapper should have one main structural purpose.

### 3. Prefer composition over inheritance
These patterns often shine through composition.

### 4. Keep interfaces clear
The wrapper should make design easier to reason about, not more obscure.

### 5. Stay Pythonic
Use the lightest implementation that solves the real structural issue.

---

## 44. Practical mental model

A useful mental model is:

- **Adapter** → “Make this fit.”
- **Facade** → “Make this simpler.”
- **Composite** → “Make leaves and groups look consistent.”
- **Decorator** → “Add behavior around this.”
- **Proxy** → “Control access to this.”

That is often enough to identify the right pattern direction quickly.

---

## 45. Final recommendation

In Python, structural patterns are most useful when they isolate a real structural pain point:

- Adapter for mismatched interfaces
- Facade for subsystem complexity
- Composite for recursive hierarchies
- Decorator for composable behavior extension
- Proxy for controlled or delayed access

A Pythonic approach keeps the implementation:
- simple
- explicit
- composition-based
- focused on actual design pressure

If the pattern makes relationships between objects clearer, it is helping.  
If it only adds indirection and vocabulary, it is probably too much.

---

## 46. Quick summary

If you only keep the essentials:

1. Adapter makes incompatible interfaces work together.
2. Facade gives a simpler interface to a complex subsystem.
3. Composite models tree-like structures so leaves and groups can be treated similarly.
4. Decorator adds behavior by wrapping objects instead of modifying them.
5. Proxy controls access to an object, often for lazy loading, permissions, or caching.

---

# Structural Patterns in Python: Adapter, Facade, Composite, Decorator, Proxy

## 1. Goal

This guide explains five classic **structural design patterns** in a practical, Python-oriented way:

- **Adapter**
- **Facade**
- **Composite**
- **Decorator**
- **Proxy**

It focuses on:

- what each pattern is for
- when each one is useful
- how to express them in Python
- common misunderstandings
- Pythonic alternatives
- practical trade-offs

The goal is not to memorize textbook names.  
The goal is to understand how these patterns help organize relationships between objects and interfaces.

---

## 2. What structural patterns are

Structural patterns are about **how code elements are connected and composed**.

They help answer questions like:

- how do I make incompatible interfaces work together?
- how do I simplify a complicated subsystem?
- how do I represent tree-like structures?
- how do I add behavior without changing the original object?
- how do I control access to another object?

### In simple terms
Structural patterns help shape **how objects fit together**.

---

## 3. A Pythonic note before starting

In Python, structural patterns should be applied pragmatically.

A common mistake is to implement the “full formal pattern” even when:
- a function would be enough
- composition is already obvious
- the problem is smaller than the pattern

### Pythonic rule
Use the pattern when it clarifies the design or isolates complexity.  
Do not force it for its own sake.

---

# Adapter

## 4. What Adapter means

**Adapter** makes one interface work like another expected interface.

### Practical question it solves
> “How do I use this existing object even though its interface does not match what my code expects?”

It is especially useful when:
- integrating third-party libraries
- wrapping legacy code
- unifying multiple APIs behind one expected shape

---

## 5. Basic Adapter idea

Suppose your application expects this:

```python
class MessageSender:
    def send(self, message: str) -> None:
        ...
```

But a third-party library gives you:

```python
class SlackClient:
    def post_message(self, text: str) -> None:
        print(f"Slack: {text}")
```

The interfaces do not match.

Adapter solves that mismatch.

---

## 6. Adapter example

```python
class SlackClient:
    def post_message(self, text: str) -> None:
        print(f"Slack: {text}")


class SlackAdapter:
    def __init__(self, client: SlackClient) -> None:
        self.client = client

    def send(self, message: str) -> None:
        self.client.post_message(message)
```

Usage:

```python
client = SlackClient()
sender = SlackAdapter(client)
sender.send("Hello")
```

### Why this helps
Your application can keep using `.send(...)` even though the third-party client uses `.post_message(...)`.

---

## 7. Why Adapter is useful

Adapter is useful when:
- you cannot change the original class
- you want to keep your internal interface stable
- you need compatibility between systems
- you want to isolate integration code from business logic

### Good design effect
Business code depends on your expected interface, not on every external API variation.

---

## 8. Pythonic Adapter alternatives

In Python, Adapter may be:
- a small wrapper class
- a function wrapper
- a lambda in simple cases
- a protocol-compatible object

### Example with function wrapper

```python
def slack_sender(client):
    def send(message: str) -> None:
        client.post_message(message)
    return send
```

This can be enough when the integration is simple.

---

## 9. When Adapter may be overkill

Adapter may be unnecessary when:
- the interface mismatch is tiny and used only once
- a direct one-line transformation is clearer
- no stable internal contract is needed

But if multiple external systems must conform to one internal interface, Adapter often becomes very valuable.

---

# Facade

## 10. What Facade means

**Facade** provides a simplified interface to a more complex subsystem.

### Practical question it solves
> “How do I make a complicated set of operations easier to use?”

Facade is often about reducing complexity for callers.

---

## 11. Example problem Facade solves

Suppose sending a notification requires:
- formatting a message
- choosing a channel
- logging delivery
- retry handling
- tracking metrics

Without a Facade, callers may need to coordinate all of that.

A Facade can expose something simpler:

```python
notification_service.notify(user, message)
```

while hiding the internal orchestration.

---

## 12. Facade example

```python
class MessageFormatter:
    def format(self, message: str) -> str:
        return f"[Formatted] {message}"


class EmailSender:
    def send(self, message: str) -> None:
        print(f"Email: {message}")


class Logger:
    def info(self, message: str) -> None:
        print(f"LOG: {message}")


class NotificationFacade:
    def __init__(self):
        self.formatter = MessageFormatter()
        self.sender = EmailSender()
        self.logger = Logger()

    def notify(self, message: str) -> None:
        formatted = self.formatter.format(message)
        self.sender.send(formatted)
        self.logger.info("Notification sent")
```

Usage:

```python
facade = NotificationFacade()
facade.notify("Welcome")
```

### Why this helps
Callers interact with one clean interface instead of many subsystem steps.

---

## 13. Why Facade is useful

Facade is useful when:
- a subsystem is hard to use directly
- many callers need the same workflow
- you want to expose a stable simplified API
- you want to isolate internal complexity
- you want to reduce coupling to internal details

---

## 14. Facade is not the same as “god object”

A common mistake is turning Facade into a giant object that does everything.

That is not the goal.

A good Facade:
- simplifies access
- coordinates related subsystem behavior
- does not become a dumping ground for unrelated responsibilities

### Practical distinction
Facade simplifies a subsystem.  
It should not replace all architecture with one huge entry point.

---

## 15. Pythonic Facade

In Python, a Facade can be:
- a class
- a service object
- a module-level helper API
- a function that orchestrates a repeated multi-step flow

### Example with function-style facade

```python
def notify_user(formatter, sender, logger, message: str) -> None:
    formatted = formatter.format(message)
    sender.send(formatted)
    logger.info("Notification sent")
```

This can act like a Facade without requiring a large class, depending on context.

---

## 16. When Facade may be overkill

Facade may be unnecessary when:
- the subsystem is already simple
- callers do not benefit from another abstraction layer
- the orchestration is trivial and only used once

But when complexity repeats, Facade often improves readability a lot.

---

# Composite

## 17. What Composite means

**Composite** lets you treat individual objects and groups of objects in a uniform way.

### Practical question it solves
> “How do I represent part-whole hierarchies so clients can work with leaves and containers similarly?”

This is common in:
- tree structures
- UI component hierarchies
- menu structures
- file systems
- nested rules
- document structures

---

## 18. Composite idea

Suppose you have:
- a single file
- a folder containing files and folders

You want to interact with both using a similar interface like:

```python
node.render()
node.size()
node.print()
```

Composite makes this possible.

---

## 19. Composite example

```python
class File:
    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self.size = size

    def get_size(self) -> int:
        return self.size


class Folder:
    def __init__(self, name: str) -> None:
        self.name = name
        self.children = []

    def add(self, child) -> None:
        self.children.append(child)

    def get_size(self) -> int:
        return sum(child.get_size() for child in self.children)
```

Usage:

```python
file1 = File("a.txt", 10)
file2 = File("b.txt", 20)

folder = Folder("docs")
folder.add(file1)
folder.add(file2)

print(folder.get_size())
```

### Why this helps
Both `File` and `Folder` expose `get_size()`, even though one is a leaf and the other is a container.

---

## 20. Why Composite is useful

Composite is useful when:
- data is naturally hierarchical
- clients should handle single items and nested groups similarly
- recursive composition is natural
- you want cleaner tree traversal logic

---

## 21. Composite and recursion

Composite structures often go naturally with recursion.

```python
class Folder:
    def __init__(self, name: str) -> None:
        self.name = name
        self.children = []

    def add(self, child) -> None:
        self.children.append(child)

    def print_tree(self, level=0) -> None:
        print("  " * level + self.name)
        for child in self.children:
            child.print_tree(level + 1)
```

Leaf:

```python
class File:
    def __init__(self, name: str) -> None:
        self.name = name

    def print_tree(self, level=0) -> None:
        print("  " * level + self.name)
```

### Why this is elegant
The caller can treat folders and files uniformly during traversal.

---

## 22. Pythonic Composite

In Python, Composite often appears naturally through:
- recursive objects
- nested dataclasses
- tree node classes
- recursive protocols or interfaces

It does not always need elaborate pattern ceremony.  
Sometimes the structure itself already suggests the pattern.

---

## 23. When Composite may be overkill

Composite may be unnecessary when:
- the structure is flat
- there is no recursive containment
- leaf and group behavior are too different to benefit from one shared interface

If there is no real “part-whole hierarchy,” Composite is probably not the right tool.

---

# Decorator

## 24. What Decorator means

**Decorator** adds behavior to an object without changing its original class.

### Practical question it solves
> “How do I extend behavior dynamically or compositionally without editing the original implementation?”

Decorator is about wrapping an object and forwarding behavior with additions.

---

## 25. Basic Decorator idea

Suppose you have:

```python
class Text:
    def render(self) -> str:
        return "hello"
```

You want:
- bold text
- italic text
- uppercase text
- combinations of those behaviors

Decorator is a clean way to wrap and compose those effects.

---

## 26. Decorator object example

```python
class Text:
    def render(self) -> str:
        return "hello"


class BoldDecorator:
    def __init__(self, component) -> None:
        self.component = component

    def render(self) -> str:
        return f"<b>{self.component.render()}</b>"
```

Usage:

```python
text = Text()
bold_text = BoldDecorator(text)

print(bold_text.render())
```

### Why this helps
You add behavior without modifying `Text`.

---

## 27. Multiple decorators

Decorators can be composed.

```python
class ItalicDecorator:
    def __init__(self, component) -> None:
        self.component = component

    def render(self) -> str:
        return f"<i>{self.component.render()}</i>"
```

Usage:

```python
text = Text()
decorated = ItalicDecorator(BoldDecorator(text))
print(decorated.render())
```

### Why useful
Behavior can be layered dynamically.

---

## 28. Why Decorator is useful

Decorator is useful when:
- you want to add responsibilities dynamically
- multiple combinations of behavior are possible
- inheritance would explode into many subclasses
- the base class should stay unchanged
- extensions should remain composable

---

## 29. Python decorators vs Decorator pattern

Important distinction:

### Python language decorator
The `@something` syntax applied to functions or classes.

### Decorator design pattern
A structural object pattern that wraps another object and extends behavior.

They are related conceptually because both “wrap behavior,” but they are not identical.

---

## 30. Python function decorator example

Python’s `@decorator` syntax is often a very natural expression of the same core idea.

```python
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


@log_calls
def greet():
    print("hello")
```

### Why this matters
Python has built-in syntactic support for function decoration, which makes the concept feel especially natural in the language.

---

## 31. When Decorator may be overkill

Decorator may be unnecessary when:
- one simple conditional would be clearer
- behavior extension is not composable
- the wrapping adds confusion without real flexibility

But when subclass combinations would explode, Decorator is often a very clean alternative.

---

# Proxy

## 32. What Proxy means

**Proxy** provides a stand-in object that controls access to another object.

### Practical question it solves
> “How do I intercept, delay, restrict, cache, protect, or monitor access to a real object?”

Proxy keeps the same general interface while adding control.

---

## 33. Common Proxy use cases

Proxy is often used for:
- lazy loading
- access control
- caching
- logging
- remote object access
- validation before forwarding
- rate limiting
- permission checks

---

## 34. Basic Proxy example

```python
class RealImage:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        print(f"Loading image from {filename}")

    def display(self) -> None:
        print(f"Displaying {self.filename}")
```

Proxy:

```python
class ImageProxy:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self._real_image = None

    def display(self) -> None:
        if self._real_image is None:
            self._real_image = RealImage(self.filename)
        self._real_image.display()
```

Usage:

```python
image = ImageProxy("photo.png")
image.display()
image.display()
```

### Why this helps
The real image is loaded only when needed.

This is a classic lazy-loading proxy.

---

## 35. Access-control Proxy example

```python
class AdminPanel:
    def delete_user(self, user_id: int) -> None:
        print(f"Deleted user {user_id}")
```

Proxy:

```python
class AdminPanelProxy:
    def __init__(self, panel: AdminPanel, is_admin: bool) -> None:
        self.panel = panel
        self.is_admin = is_admin

    def delete_user(self, user_id: int) -> None:
        if not self.is_admin:
            raise PermissionError("Not allowed")
        self.panel.delete_user(user_id)
```

### Why useful
The proxy controls access before delegating to the real object.

---

## 36. Why Proxy is useful

Proxy is useful when:
- you need control around a real object
- the real object is expensive
- access should be conditional
- lazy creation is valuable
- caching or monitoring should happen transparently
- the caller should not need to know about the control layer

---

## 37. Proxy vs Decorator

These patterns are similar because both wrap another object.

### Decorator
Focuses on **adding behavior or responsibilities**.

### Proxy
Focuses on **controlling access** to the original object.

### Practical shortcut
If the wrapper mainly enriches behavior, think Decorator.  
If the wrapper mainly controls or mediates access, think Proxy.

Sometimes the line can blur, but the design intent is different.

---

## 38. Pythonic Proxy

In Python, Proxy can often be a:
- wrapper object
- lazy-loaded object
- cached service layer
- permission-checked adapter
- remote-call stand-in

It does not always require a formal interface hierarchy.

---

## 39. When Proxy may be overkill

Proxy may be unnecessary when:
- a direct helper function is enough
- there is no real access-control or indirection problem
- lazy loading or mediation is not needed
- the wrapper adds more confusion than value

---

# Comparing the five patterns

## 40. Quick comparison

### Adapter
Makes incompatible interfaces work together.

### Facade
Simplifies access to a complex subsystem.

### Composite
Lets you treat leaves and groups uniformly.

### Decorator
Adds behavior by wrapping an object.

### Proxy
Controls access to another object.

---

## 41. Practical selection guide

Use **Adapter** when:
- you need compatibility between mismatched interfaces

Use **Facade** when:
- you want a simpler entry point to a subsystem

Use **Composite** when:
- you have tree-like part-whole structures

Use **Decorator** when:
- you want composable behavior extension without subclass explosion

Use **Proxy** when:
- you need access control, lazy loading, caching, or mediation

---

## 42. Common mistakes

### 1. Confusing Adapter and Facade
Adapter changes interface compatibility.  
Facade simplifies a subsystem.

### 2. Confusing Decorator and Proxy
Decorator adds responsibilities.  
Proxy controls access.

### 3. Forcing Composite on flat data
Composite only helps when hierarchy is real.

### 4. Overengineering wrappers
Not every small wrapper is a meaningful design pattern.

### 5. Building patterns instead of solving the problem
The pattern should clarify the architecture, not decorate it.

---

## 43. Best practices

### 1. Start from the problem, not the pattern name
Ask what is actually difficult: compatibility, complexity, hierarchy, extension, or access control.

### 2. Keep wrappers focused
A wrapper should have one main structural purpose.

### 3. Prefer composition over inheritance
These patterns often shine through composition.

### 4. Keep interfaces clear
The wrapper should make design easier to reason about, not more obscure.

### 5. Stay Pythonic
Use the lightest implementation that solves the real structural issue.

---

## 44. Practical mental model

A useful mental model is:

- **Adapter** → “Make this fit.”
- **Facade** → “Make this simpler.”
- **Composite** → “Make leaves and groups look consistent.”
- **Decorator** → “Add behavior around this.”
- **Proxy** → “Control access to this.”

That is often enough to identify the right pattern direction quickly.

---

## 45. Final recommendation

In Python, structural patterns are most useful when they isolate a real structural pain point:

- Adapter for mismatched interfaces
- Facade for subsystem complexity
- Composite for recursive hierarchies
- Decorator for composable behavior extension
- Proxy for controlled or delayed access

A Pythonic approach keeps the implementation:
- simple
- explicit
- composition-based
- focused on actual design pressure

If the pattern makes relationships between objects clearer, it is helping.  
If it only adds indirection and vocabulary, it is probably too much.

---

## 46. Quick summary

If you only keep the essentials:

1. Adapter makes incompatible interfaces work together.
2. Facade gives a simpler interface to a complex subsystem.
3. Composite models tree-like structures so leaves and groups can be treated similarly.
4. Decorator adds behavior by wrapping objects instead of modifying them.
5. Proxy controls access to an object, often for lazy loading, permissions, or caching.

---

# Behavioral Patterns in Python: Strategy, Observer, Command, Mediator, Template Method, State

## 1. Goal

This guide explains six classic **behavioral design patterns** in a practical, Python-oriented way:

- **Strategy**
- **Observer**
- **Command**
- **Mediator**
- **Template Method**
- **State**

It focuses on:

- what each pattern is for
- when each one is useful
- how to express them in Python
- practical trade-offs
- common mistakes
- Pythonic alternatives

The goal is not to memorize textbook definitions.  
The goal is to understand how these patterns organize **behavior**, **interaction**, and **decision flow**.

---

## 2. What behavioral patterns are

Behavioral patterns are about **how objects behave and collaborate over time**.

They help answer questions like:

- how do I swap algorithms cleanly?
- how do I notify many listeners about a change?
- how do I package an action as an object?
- how do I reduce many-to-many communication chaos?
- how do I define a reusable algorithm skeleton?
- how do I change behavior depending on current state?

### In simple terms
Behavioral patterns help organize **who does what**, **when**, and **how behavior changes**.

---

## 3. A Pythonic note before starting

In Python, behavioral patterns should usually be implemented with as little ceremony as possible.

A common mistake is to take a pattern that could be expressed with:
- functions
- callables
- small classes
- Protocols
- simple composition

and inflate it into many abstract classes and files.

### Pythonic rule
Use the smallest design that makes behavior clearer, more flexible, or easier to test.

---

# Strategy

## 4. What Strategy means

**Strategy** encapsulates interchangeable algorithms or behaviors behind a common interface.

### Practical question it solves
> “How do I switch between different ways of doing the same job without filling the code with conditionals?”

---

## 5. Basic Strategy problem

Suppose discount calculation depends on the selected rule:

```python
def calculate_discount(customer_type, amount):
    if customer_type == "regular":
        return amount * 0.05
    elif customer_type == "vip":
        return amount * 0.10
    elif customer_type == "employee":
        return amount * 0.20
    return 0
```

This works at first, but repeated branching logic can spread and grow.

Strategy moves each variation into its own interchangeable unit.

---

## 6. Strategy class-based example

```python
class RegularDiscount:
    def apply(self, amount: float) -> float:
        return amount * 0.05


class VipDiscount:
    def apply(self, amount: float) -> float:
        return amount * 0.10


class EmployeeDiscount:
    def apply(self, amount: float) -> float:
        return amount * 0.20


class DiscountCalculator:
    def __init__(self, strategy) -> None:
        self.strategy = strategy

    def calculate(self, amount: float) -> float:
        return self.strategy.apply(amount)
```

Usage:

```python
calculator = DiscountCalculator(VipDiscount())
print(calculator.calculate(100))
```

### Why this helps
The algorithm can be changed without rewriting the caller.

---

## 7. Pythonic Strategy with functions

In Python, Strategy is often simpler with callables.

```python
def regular_discount(amount: float) -> float:
    return amount * 0.05


def vip_discount(amount: float) -> float:
    return amount * 0.10


def calculate_discount(strategy, amount: float) -> float:
    return strategy(amount)
```

Usage:

```python
print(calculate_discount(vip_discount, 100))
```

### Why this is Pythonic
Functions are first-class objects, so a callable often works perfectly as a strategy.

---

## 8. Why Strategy is useful

Strategy is useful when:
- multiple algorithms solve the same kind of problem
- behavior must be swapped dynamically
- branching logic is spreading
- testing each behavior separately would help
- you want to extend without constantly editing the core flow

---

## 9. When Strategy may be overkill

Strategy may be unnecessary when:
- there are only one or two very stable variants
- the branching is tiny and local
- introducing extra abstractions adds more complexity than value

Use it when the variation is meaningful, not just because there are two `if`s.

---

# Observer

## 10. What Observer means

**Observer** defines a one-to-many relationship where one object notifies many dependents when something changes.

### Practical question it solves
> “How do I let multiple listeners react to an event or state change without tightly coupling them together?”

---

## 11. Basic Observer idea

Suppose an order changes status.

Many things may care:
- email notification
- metrics
- audit logging
- analytics
- UI refresh
- inventory updates

Without Observer, the order logic may directly know too much about all these concerns.

Observer lets listeners subscribe and react separately.

---

## 12. Observer example

```python
class Order:
    def __init__(self) -> None:
        self._observers = []

    def attach(self, observer) -> None:
        self._observers.append(observer)

    def notify(self, event: str) -> None:
        for observer in self._observers:
            observer.update(event)

    def place(self) -> None:
        print("Order placed")
        self.notify("order_placed")
```

Observers:

```python
class EmailNotifier:
    def update(self, event: str) -> None:
        print(f"Email event: {event}")


class AuditLogger:
    def update(self, event: str) -> None:
        print(f"Audit event: {event}")
```

Usage:

```python
order = Order()
order.attach(EmailNotifier())
order.attach(AuditLogger())
order.place()
```

---

## 13. Why Observer is useful

Observer is useful when:
- many consumers react to the same event
- event producers should stay decoupled from event handlers
- new reactions may be added later
- direct dependencies would create a tangled design

---

## 14. Pythonic Observer alternatives

In Python, Observer may also appear as:
- callback lists
- event handlers
- signals
- pub/sub systems
- async event buses
- framework hooks

A simple callback list is often enough.

```python
class EventSource:
    def __init__(self):
        self._handlers = []

    def subscribe(self, handler):
        self._handlers.append(handler)

    def emit(self, event):
        for handler in self._handlers:
            handler(event)
```

This is still Observer in spirit.

---

## 15. Common Observer caution

Observer can become messy if:
- event names are vague
- too many hidden listeners exist
- debugging event flow becomes hard
- ordering assumptions appear accidentally

### Practical lesson
Observer reduces direct coupling, but it can increase system invisibility if used carelessly.

---

# Command

## 16. What Command means

**Command** encapsulates an action or request as an object.

### Practical question it solves
> “How do I turn an operation into something I can store, queue, pass around, retry, or undo?”

---

## 17. Basic Command idea

Instead of calling an operation directly, you package it into an object with a common method such as:

```python
execute()
```

This lets you:
- queue commands
- log commands
- retry commands
- schedule commands
- undo commands in some designs

---

## 18. Command example

```python
class CreateUserCommand:
    def __init__(self, user_service, username: str) -> None:
        self.user_service = user_service
        self.username = username

    def execute(self) -> None:
        self.user_service.create_user(self.username)
```

Receiver:

```python
class UserService:
    def create_user(self, username: str) -> None:
        print(f"Created user: {username}")
```

Usage:

```python
service = UserService()
command = CreateUserCommand(service, "janette")
command.execute()
```

---

## 19. Why Command is useful

Command is useful when:
- actions must be queued
- actions must be scheduled
- actions must be logged or replayed
- actions should be decoupled from the invoker
- actions need undo/redo semantics
- different operations should share a common interface

---

## 20. Pythonic Command

In Python, a command can often be:
- a callable object
- a function
- a closure
- a dataclass with `execute()`

Example with callable object:

```python
class PrintCommand:
    def __init__(self, message: str) -> None:
        self.message = message

    def __call__(self) -> None:
        print(self.message)
```

Usage:

```python
cmd = PrintCommand("Hello")
cmd()
```

This can feel very natural in Python.

---

## 21. Command vs plain function

A plain function may already be enough if:
- the action is simple
- you do not need metadata
- you do not need object-level state
- you do not need a common command interface

But if actions need richer packaging, Command becomes helpful.

---

# Mediator

## 22. What Mediator means

**Mediator** centralizes communication between objects so they do not talk to each other directly in many tangled ways.

### Practical question it solves
> “How do I reduce complex many-to-many communication between objects?”

---

## 23. Basic Mediator idea

Suppose several UI widgets or domain objects interact:
- when one changes, others must react
- each object may otherwise need to know too much about the others

Mediator introduces a central coordinator.

Instead of:
- A talks to B and C
- B talks to A and D
- C talks to A and D

you get:
- all talk to Mediator
- Mediator coordinates the interaction

---

## 24. Mediator example

```python
class ChatMediator:
    def __init__(self) -> None:
        self.users = []

    def register(self, user) -> None:
        self.users.append(user)

    def send(self, message: str, sender) -> None:
        for user in self.users:
            if user is not sender:
                user.receive(message)
```

Colleague objects:

```python
class User:
    def __init__(self, name: str, mediator: ChatMediator) -> None:
        self.name = name
        self.mediator = mediator

    def send(self, message: str) -> None:
        self.mediator.send(f"{self.name}: {message}", self)

    def receive(self, message: str) -> None:
        print(f"{self.name} received: {message}")
```

Usage:

```python
mediator = ChatMediator()
a = User("A", mediator)
b = User("B", mediator)

mediator.register(a)
mediator.register(b)

a.send("Hello")
```

---

## 25. Why Mediator is useful

Mediator is useful when:
- object interactions become tangled
- many objects depend on each other’s state
- communication logic should be centralized
- the system becomes hard to reason about because of cross-links

---

## 26. Mediator caution

Mediator can become a **god object** if it absorbs too much logic.

That is one of the biggest risks.

### Good Mediator
Coordinates related interaction.

### Bad Mediator
Becomes a giant central brain for the entire application.

Keep the mediator focused on one collaboration context.

---

## 27. Pythonic Mediator

In Python, Mediator may appear as:
- service coordinators
- domain orchestrators
- workflow managers
- event coordinators
- UI coordination controllers

It does not always need a formal pattern-heavy class structure.  
Sometimes a focused orchestration service already plays the mediator role.

---

# Template Method

## 28. What Template Method means

**Template Method** defines the skeleton of an algorithm in a base structure and lets subclasses redefine some steps.

### Practical question it solves
> “How do I keep a common algorithm structure while allowing specific steps to vary?”

---

## 29. Basic Template Method idea

Suppose all report generation follows the same flow:

1. fetch data
2. format data
3. export output

But different report types vary in the implementation of those steps.

Template Method keeps the skeleton stable and customizes selected parts.

---

## 30. Template Method example

```python
class ReportGenerator:
    def generate(self) -> str:
        data = self.fetch_data()
        formatted = self.format_data(data)
        return self.export(formatted)

    def fetch_data(self):
        raise NotImplementedError

    def format_data(self, data):
        raise NotImplementedError

    def export(self, formatted):
        return formatted
```

Subclass:

```python
class SalesReportGenerator(ReportGenerator):
    def fetch_data(self):
        return ["sale1", "sale2"]

    def format_data(self, data):
        return ", ".join(data)
```

Usage:

```python
generator = SalesReportGenerator()
print(generator.generate())
```

---

## 31. Why Template Method is useful

Template Method is useful when:
- multiple variants share the same algorithm structure
- only some steps differ
- you want to avoid duplicated control flow
- the sequence of operations should remain fixed

---

## 32. Pythonic caution for Template Method

Python often prefers:
- composition
- injected callables
- Strategy
- higher-order functions

instead of inheritance-heavy solutions.

So while Template Method is useful, it is not always the most Pythonic default.

### Example alternative
You might inject step functions instead of subclassing.

---

## 33. Template Method vs Strategy

### Template Method
Varies steps through inheritance.

### Strategy
Varies behavior through composition.

### Pythonic shortcut
If inheritance feels heavy and step variation is independent, Strategy is often cleaner in Python.

Use Template Method when the algorithm skeleton itself is central and stable.

---

# State

## 34. What State means

**State** changes an object’s behavior when its internal state changes.

### Practical question it solves
> “How do I avoid giant conditionals when behavior depends on current state?”

---

## 35. Basic State problem

Suppose an order can be:
- pending
- paid
- shipped
- cancelled

Different actions are allowed depending on the current state.

A naive version often becomes:

```python
if state == "pending":
    ...
elif state == "paid":
    ...
elif state == "shipped":
    ...
```

As behavior grows, this becomes harder to maintain.

State pattern moves state-specific behavior into dedicated objects.

---

## 36. State example

```python
class PendingState:
    def pay(self, order) -> None:
        print("Order paid")
        order.state = PaidState()

    def ship(self, order) -> None:
        raise ValueError("Cannot ship pending order")
```

```python
class PaidState:
    def pay(self, order) -> None:
        raise ValueError("Order already paid")

    def ship(self, order) -> None:
        print("Order shipped")
        order.state = ShippedState()
```

```python
class ShippedState:
    def pay(self, order) -> None:
        raise ValueError("Cannot pay shipped order")

    def ship(self, order) -> None:
        raise ValueError("Order already shipped")
```

Context:

```python
class Order:
    def __init__(self) -> None:
        self.state = PendingState()

    def pay(self) -> None:
        self.state.pay(self)

    def ship(self) -> None:
        self.state.ship(self)
```

Usage:

```python
order = Order()
order.pay()
order.ship()
```

---

## 37. Why State is useful

State is useful when:
- behavior changes significantly by current state
- the code is growing many state-based conditionals
- transitions matter
- invalid actions should be state-specific
- the object should appear to “change behavior” over time

---

## 38. State vs Strategy

These patterns can look similar because both use interchangeable objects.

### Strategy
Chooses among interchangeable algorithms.

### State
Represents evolving behavior depending on current internal state.

### Practical shortcut
If the behavior changes because the object is in a different lifecycle phase, think State.  
If the behavior changes because the caller selected an algorithm, think Strategy.

---

## 39. Pythonic State caution

State may be overkill when:
- only a few simple conditionals exist
- state transitions are minimal
- the behavior does not justify multiple classes

Sometimes a simple enum plus small methods is enough.

State pattern becomes valuable when the conditional explosion is real.

---

# Comparing the six patterns

## 40. Quick comparison

### Strategy
Swap algorithms or behaviors cleanly.

### Observer
Notify many listeners about changes or events.

### Command
Package an action as an object or callable.

### Mediator
Centralize collaboration between related objects.

### Template Method
Keep an algorithm skeleton while varying steps.

### State
Change behavior according to internal lifecycle state.

---

## 41. Practical selection guide

Use **Strategy** when:
- one job has multiple interchangeable algorithms

Use **Observer** when:
- many listeners react to one event source

Use **Command** when:
- actions should be queued, stored, scheduled, or treated uniformly

Use **Mediator** when:
- direct communication between many objects becomes tangled

Use **Template Method** when:
- the algorithm structure is fixed, but some steps vary

Use **State** when:
- object behavior changes significantly by current state

---

## 42. Common mistakes

### 1. Using Strategy when a simple parameter would do
Not every minor variation needs a pattern.

### 2. Using Observer and creating invisible event spaghetti
Loose coupling can become hidden complexity.

### 3. Using Command for trivial direct calls
Packaging everything as a command can add noise.

### 4. Letting Mediator become a god object
Coordination should stay focused.

### 5. Using Template Method when composition would be simpler
Inheritance is not always the best fit in Python.

### 6. Using State for tiny finite condition sets
Sometimes a few conditionals are honestly enough.

---

## 43. Best practices

### 1. Start from the behavioral pain point
Is it algorithm variation, event reaction, action packaging, coordination complexity, algorithm skeleton reuse, or lifecycle behavior?

### 2. Prefer Pythonic simplicity
Use functions, callables, and composition when enough.

### 3. Keep responsibilities focused
A pattern should clarify behavior, not spread it across many arbitrary abstractions.

### 4. Make behavior visible
Especially with Observer and Mediator, hidden flows can become hard to debug.

### 5. Refactor toward patterns when complexity becomes real
Do not force them too early.

---

## 44. Practical mental model

A useful mental model is:

- **Strategy** → “Choose how to do it.”
- **Observer** → “Tell others it happened.”
- **Command** → “Package the action.”
- **Mediator** → “Coordinate the interaction.”
- **Template Method** → “Keep the steps, vary some parts.”
- **State** → “Act differently depending on current phase.”

That is often enough to identify the right pattern direction quickly.

---

## 45. Final recommendation

In Python, behavioral patterns are most useful when they isolate a real behavioral complexity:

- Strategy for algorithm variation
- Observer for event fan-out
- Command for packaged actions
- Mediator for tangled collaboration
- Template Method for reusable algorithm skeletons
- State for lifecycle-dependent behavior

A Pythonic implementation should stay:
- simple
- explicit
- focused on real change points
- as light as the problem allows

If the pattern makes behavior easier to understand, extend, and test, it is helping.  
If it mainly adds vocabulary and indirection, it is probably too much.

---

## 46. Quick summary

If you only keep the essentials:

1. Strategy swaps algorithms cleanly.
2. Observer lets many listeners react to one event source.
3. Command packages an action so it can be passed around or scheduled.
4. Mediator centralizes complex collaboration.
5. Template Method preserves an algorithm skeleton while varying steps.
6. State changes behavior according to internal state.

---
# Python Idiomatic Patterns: Decorators, Context Managers, and Dataclasses

## 1. Goal

This guide explains three very Pythonic and widely used idiomatic patterns:

- **decorators**
- **context managers**
- **dataclasses**

It focuses on:

- what each one is
- why it matters in real Python code
- how it improves readability and maintainability
- practical examples
- common mistakes
- when not to use it

The goal is to understand these tools not just as syntax features, but as recurring design patterns in Python codebases.

---

## 2. What “idiomatic” means in Python

When something is **idiomatic** in Python, it usually means:

- it fits the language naturally
- it is readable to other Python developers
- it uses Python’s built-in strengths
- it avoids unnecessary ceremony
- it solves problems in a way that feels native to the language

These patterns are idiomatic because they are not just technical tricks.  
They are common ways of structuring behavior and data in real Python projects.

---

## 3. Why these three matter together

These three tools appear constantly in Python code:

- **decorators** help wrap or modify behavior
- **context managers** help manage resources and scope-based setup/cleanup
- **dataclasses** help represent structured data clearly and with less boilerplate

They are different features, but all three help make Python code:
- cleaner
- more expressive
- easier to maintain

---

# Decorators

## 4. What is a decorator?

A **decorator** is something that wraps a function, method, or class and changes or extends its behavior.

In Python, decorators are often written using the `@decorator_name` syntax.

Example:

```python
@my_decorator
def greet():
    print("hello")
```

This is equivalent to:

```python
def greet():
    print("hello")

greet = my_decorator(greet)
```

### Key idea
A decorator takes something callable and returns a new callable with added behavior.

---

## 5. Why decorators are useful

Decorators are useful when you want to add behavior such as:

- logging
- timing
- caching
- validation
- authentication
- retry logic
- access control
- registration in frameworks

### Why this is powerful
They let you separate **cross-cutting behavior** from the core logic of the function.

---

## 6. Basic decorator example

```python
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


@log_calls
def greet():
    print("hello")
```

Usage:

```python
greet()
```

Output:

```text
Calling greet
hello
```

### What happened
The original function was wrapped with extra logging behavior.

---

## 7. Why decorators feel Pythonic

Decorators feel very Pythonic because they let you express:

> “This function has the same core job, but with extra behavior around it.”

That is concise and expressive, especially when many functions need the same wrapper logic.

---

## 8. Decorators with arguments

Some decorators need configuration.

Example:

```python
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)
        return wrapper
    return decorator


@repeat(3)
def greet():
    print("hello")
```

### What this shows
`repeat(3)` returns the actual decorator, which then wraps the function.

This is a very common pattern in real Python code.

---

## 9. Why `functools.wraps` matters

A common decorator mistake is forgetting to preserve the original function metadata.

Example fix:

```python
from functools import wraps


def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

### Why this matters
Without `@wraps`, the wrapped function may lose:
- its original name
- docstring
- metadata
- debugging clarity

### Rule
When writing custom decorators, use `functools.wraps` unless you have a reason not to.

---

## 10. Practical decorator example: timing

```python
import time
from functools import wraps


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.6f}s")
        return result
    return wrapper


@timeit
def compute():
    return sum(range(100000))
```

### Why useful
This keeps timing logic separate from the business logic.

---

## 11. Practical decorator example: access control

```python
from functools import wraps


def require_admin(func):
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        if user.get("role") != "admin":
            raise PermissionError("Admin access required")
        return func(user, *args, **kwargs)
    return wrapper


@require_admin
def delete_account(user, account_id):
    print(f"Deleted account {account_id}")
```

### Why useful
Cross-cutting security checks stay separate from the core action.

---

## 12. Decorators and frameworks

Decorators are heavily used in Python frameworks.

Examples:
- route registration in web frameworks
- test markers in pytest
- dependency registration
- task scheduling
- event handlers

This is one reason decorators are so central in Python style.

---

## 13. Class decorators

Decorators can also be applied to classes.

```python
def add_repr(cls):
    def __repr__(self):
        return f"{cls.__name__}({self.__dict__})"
    cls.__repr__ = __repr__
    return cls


@add_repr
class User:
    def __init__(self, name):
        self.name = name
```

### Why useful
Class decorators can modify or enhance class behavior without subclassing.

That said, they are less common than function decorators.

---

## 14. Decorators vs inheritance

Decorators can sometimes be a better choice than inheritance when:
- you want to add behavior without creating subclasses
- the behavior is reusable across unrelated callables
- the enhancement is orthogonal to the main business logic

This is part of what makes decorators so flexible.

---

## 15. Common decorator mistakes

### 1. Forgetting `@wraps`
This hurts introspection and debugging.

### 2. Hiding too much behavior
A decorator can make behavior less visible if it becomes too magical.

### 3. Putting too much business logic in decorators
Decorators are often best for reusable, cross-cutting concerns.

### 4. Making decorator stacks hard to reason about
Too many layers of decoration can reduce clarity.

---

## 16. When not to use a decorator

Do not use a decorator when:
- a direct function call is clearer
- the behavior is very local and not reusable
- it makes the flow too implicit
- the wrapping logic depends too heavily on internal function details

A decorator should improve clarity, not hide the program’s meaning.

---

# Context Managers

## 17. What is a context manager?

A **context manager** controls setup and cleanup around a block of code.

It is typically used with the `with` statement.

Example:

```python
with open("file.txt", "r") as f:
    content = f.read()
```

### What this means
The file is opened before the block and properly cleaned up after the block, even if an exception occurs.

---

## 18. Why context managers are useful

Context managers are useful for things that require:
- acquisition and release
- setup and teardown
- temporary state changes
- cleanup that must always happen

Common examples:
- files
- database sessions
- locks
- network connections
- temporary config/state changes
- timing scopes

---

## 19. Basic idea behind a context manager

A context manager defines two main moments:

- what happens when entering the block
- what happens when leaving the block

The object used in `with` typically implements:
- `__enter__`
- `__exit__`

---

## 20. Custom context manager example

```python
class FileLogger:
    def __enter__(self):
        print("Opening resource")
        return self

    def __exit__(self, exc_type, exc, tb):
        print("Closing resource")
```

Usage:

```python
with FileLogger() as logger:
    print("Inside context")
```

Output:

```text
Opening resource
Inside context
Closing resource
```

### Why useful
The lifecycle is explicit and safely scoped to the `with` block.

---

## 21. Resource safety

One of the biggest benefits of context managers is that cleanup still happens even if the block raises an exception.

That makes them ideal for resource safety.

Without a context manager, you might need:

```python
resource = acquire()
try:
    do_work(resource)
finally:
    release(resource)
```

With a context manager, this becomes cleaner and less error-prone.

---

## 22. Context managers with exceptions

Example:

```python
class DemoContext:
    def __enter__(self):
        print("enter")
        return self

    def __exit__(self, exc_type, exc, tb):
        print("exit")
        print(f"Exception type: {exc_type}")
```

Usage:

```python
with DemoContext():
    raise ValueError("Something went wrong")
```

### Why this matters
`__exit__` still runs even when an exception occurs.

This is exactly why context managers are so valuable for safe cleanup.

---

## 23. Context managers with `contextlib.contextmanager`

Python also provides a simpler way to create context managers using a generator.

```python
from contextlib import contextmanager


@contextmanager
def managed_resource():
    print("setup")
    try:
        yield "resource"
    finally:
        print("cleanup")
```

Usage:

```python
with managed_resource() as resource:
    print(resource)
```

### Why this is Pythonic
This style is often simpler than writing a full class when the logic is straightforward.

---

## 24. Practical context manager example: timing a block

```python
import time
from contextlib import contextmanager


@contextmanager
def timer(label: str):
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        print(f"{label} took {end - start:.6f}s")
```

Usage:

```python
with timer("compute"):
    total = sum(range(100000))
```

### Why useful
This is a block-level timing idiom that is very common and expressive.

---

## 25. Practical context manager example: temporary state

```python
from contextlib import contextmanager


settings = {"debug": False}


@contextmanager
def temporary_debug():
    old_value = settings["debug"]
    settings["debug"] = True
    try:
        yield
    finally:
        settings["debug"] = old_value
```

### Why useful
It safely restores the old state after the block ends.

This pattern is common for:
- feature flags
- temporary environment settings
- monkeypatch-like behavior in tests
- scoped configuration changes

---

## 26. Async context managers

In async code, you can also use context managers with:

- `__aenter__`
- `__aexit__`
- `async with`

Example conceptually:

```python
class AsyncResource:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass
```

Usage:

```python
async with AsyncResource():
    ...
```

This is common in async database sessions and network clients.

---

## 27. Common context manager mistakes

### 1. Using `with` for things that do not need scoped lifecycle
Not everything needs a context manager.

### 2. Hiding too much logic inside setup/cleanup
The scope behavior should still be understandable.

### 3. Forgetting exception behavior
You should know whether exceptions are suppressed or allowed to propagate.

### 4. Writing a class-based context manager when `contextmanager` would be simpler
Sometimes the generator-based style is the clearer choice.

---

## 28. When not to use a context manager

Do not use a context manager when:
- there is no meaningful setup/cleanup boundary
- the code would become more confusing than helpful
- lifecycle management is not actually scoped to one block

Context managers are best when the block itself defines a natural lifetime.

---

# Dataclasses

## 29. What is a dataclass?

A **dataclass** is a Python feature for defining classes that mainly store data.

It automatically generates common methods such as:
- `__init__`
- `__repr__`
- `__eq__`

based on declared fields.

Example:

```python
from dataclasses import dataclass


@dataclass
class User:
    name: str
    age: int
```

### Why this matters
It removes a lot of boilerplate for data-centric classes.

---

## 30. Why dataclasses are useful

Dataclasses are useful when a class is mainly about:
- holding structured data
- representing a domain value
- carrying configuration
- transporting input/output data
- making code more readable with named fields

They help express intent clearly:
> “This class is mostly data with optional light behavior.”

---

## 31. Dataclass vs regular class

Without dataclass:

```python
class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"User(name={self.name!r}, age={self.age!r})"
```

With dataclass:

```python
from dataclasses import dataclass


@dataclass
class User:
    name: str
    age: int
```

### Why this is Pythonic
It is shorter, clearer, and communicates that the class is fundamentally data-oriented.

---

## 32. Default values in dataclasses

```python
from dataclasses import dataclass


@dataclass
class User:
    name: str
    active: bool = True
```

### Why useful
Default values make configuration and optional fields cleaner.

---

## 33. Avoiding mutable default mistakes

A very important dataclass rule:

Do not do this:

```python
from dataclasses import dataclass


@dataclass
class Group:
    members: list = []
```

This creates a shared mutable default.

Correct approach:

```python
from dataclasses import dataclass, field


@dataclass
class Group:
    members: list = field(default_factory=list)
```

### Why this matters
Each instance gets its own list.

This is one of the most important practical dataclass details.

---

## 34. Dataclass with behavior

Dataclasses can still have methods.

```python
from dataclasses import dataclass


@dataclass
class Rectangle:
    width: float
    height: float

    def area(self) -> float:
        return self.width * self.height
```

### Important
A dataclass is not “data only forever.”  
It simply means the class is primarily data-centric.

Light, relevant behavior is perfectly fine.

---

## 35. `frozen=True`

Dataclasses can be made immutable-like.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int
```

### Why useful
This is helpful when the object represents a value that should not change after creation.

Examples:
- coordinates
- configuration values
- domain value objects
- cache keys

---

## 36. Ordering and comparison

Dataclasses can also generate ordering methods.

```python
from dataclasses import dataclass


@dataclass(order=True)
class Product:
    price: float
    name: str
```

### Why useful
This allows comparison and sorting based on field order.

Use it only when the ordering semantics actually make sense.

---

## 37. `__post_init__`

If you need extra initialization logic after automatic field assignment, use `__post_init__`.

```python
from dataclasses import dataclass


@dataclass
class User:
    name: str
    normalized_name: str = ""

    def __post_init__(self):
        self.normalized_name = self.name.strip().lower()
```

### Why useful
It lets you keep dataclass convenience while still applying derived initialization logic.

---

## 38. Practical dataclass example: configuration

```python
from dataclasses import dataclass


@dataclass
class AppConfig:
    debug: bool
    database_url: str
    max_connections: int = 10
```

### Why useful
Dataclasses are excellent for configuration objects because they are:
- readable
- explicit
- easy to construct
- easy to inspect

---

## 39. Practical dataclass example: DTO-like object

```python
from dataclasses import dataclass


@dataclass
class UserDTO:
    id: int
    username: str
    email: str
```

### Why useful
Dataclasses work well for transport-style data where named fields matter more than complex behavior.

---

## 40. When not to use a dataclass

Dataclasses may be a bad fit when:
- the class is behavior-heavy rather than data-heavy
- the invariants are complex and require tight control over state changes
- automatic method generation creates misleading semantics
- identity matters more than field values

### Practical rule
Use dataclasses when the class is primarily a structured data object with maybe some light related behavior.

---

## 41. Decorators, context managers, and dataclasses together

These idioms often appear together in real codebases.

Examples:
- a dataclass represents configuration
- a decorator logs function timing
- a context manager manages a DB session
- all three improve readability in different ways

They are not competing ideas.  
They complement each other as Python-native design tools.

---

## 42. Common mistakes across all three

### 1. Using the feature just because it exists
Not every function needs a decorator, not every resource needs a custom context manager, and not every class should be a dataclass.

### 2. Making behavior too implicit
Idiomatic code should still be understandable.

### 3. Choosing magic over clarity
Pythonic does not mean clever or hidden.

### 4. Ignoring the maintenance cost
A shorter syntax is only better if it still makes the code easier to reason about.

---

## 43. Best practices

### 1. Use decorators for reusable cross-cutting behavior
Examples: logging, timing, retries, validation.

### 2. Use context managers for scoped lifecycle management
Examples: files, locks, DB sessions, temporary state.

### 3. Use dataclasses for data-centric classes
Examples: configs, DTOs, value objects, simple domain records.

### 4. Preserve clarity
A Python idiom should make code easier to read, not more magical.

### 5. Prefer the simplest form that works
Often the generator-style context manager or function decorator is enough.

### 6. Be deliberate with defaults and mutability
Especially with dataclasses.

---

## 44. Practical mental model

A useful mental model is:

- **decorator** → “Wrap this behavior.”
- **context manager** → “Manage setup and cleanup around this block.”
- **dataclass** → “Represent this structured data cleanly.”

That is often enough to identify when each idiom fits naturally.

---

## 45. Final recommendation

In Python, these idiomatic patterns are valuable because they solve common problems in a language-native way:

- decorators for reusable behavior wrapping
- context managers for safe scoped resource management
- dataclasses for clear data modeling with less boilerplate

Use them when they improve:
- readability
- correctness
- maintainability
- testability

Avoid them when they add indirection or hidden behavior without real value.

The best Pythonic code is not the code that uses the most idioms.  
It is the code that uses them where they genuinely clarify the design.

---

## 46. Quick summary

If you only keep the essentials:

1. Decorators wrap and extend behavior around functions, methods, or classes.
2. Context managers handle setup and cleanup safely around a block of code.
3. Dataclasses reduce boilerplate for data-centric classes.
4. All three are highly idiomatic Python tools.
5. They are most valuable when they make code clearer, safer, and easier to maintain.

---
