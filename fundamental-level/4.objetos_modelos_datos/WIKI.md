# Python OOP, Data Models, and Validation

## 1. Goal

This document gives a clear summary of these Python topics:

- classes, inheritance, composition, and dunder methods
- `dataclasses` and `attrs`
- Pydantic for validation and serialization

The purpose is to connect object-oriented design, data modeling, and structured validation into one practical overview.

---

## 2. Classes, Inheritance, Composition, and Dunder Methods

### Classes
A class is a blueprint for creating objects.

It lets you group:
- data
- behavior
- state
- rules

Example:

```python
class User:
    def __init__(self, name: str):
        self.name = name

    def greet(self) -> str:
        return f"Hello, {self.name}"
```

### Why classes are useful
Classes are useful when you want to model:
- entities
- services
- domain concepts
- stateful objects
- reusable behavior bundles

### Inheritance
Inheritance lets one class reuse or extend another.

Example:

```python
class Animal:
    def speak(self) -> str:
        return "sound"


class Dog(Animal):
    def speak(self) -> str:
        return "bark"
```

### When inheritance is useful
Inheritance is useful when:
- there is a real “is-a” relationship
- behavior is meaningfully shared
- substitution makes sense

### Practical caution
Inheritance can become hard to maintain if:
- hierarchies get deep
- reuse is forced
- subclasses break expectations

### Composition
Composition means building objects from other objects instead of inheriting from them.

Example:

```python
class Engine:
    def start(self) -> str:
        return "engine started"


class Car:
    def __init__(self, engine: Engine):
        self.engine = engine

    def drive(self) -> str:
        return self.engine.start()
```

### Why composition is often preferred
Composition is often preferred because it:
- reduces tight coupling
- is more flexible
- avoids fragile inheritance trees
- makes dependencies explicit

### Practical shortcut
- **inheritance** → “is a”
- **composition** → “has a” or “uses a”

### Dunder methods
Dunder methods are “double underscore” special methods such as:
- `__init__`
- `__repr__`
- `__str__`
- `__len__`
- `__eq__`
- `__iter__`

They define how objects behave with Python syntax and built-in operations.

Example:

```python
class Box:
    def __init__(self, items):
        self.items = items

    def __len__(self):
        return len(self.items)
```

Now `len(box)` works.

### Why dunder methods matter
They let your objects integrate naturally with Python’s data model.

### Main idea
Classes model behavior and state, inheritance shares behavior through hierarchy, composition builds behavior through collaboration, and dunder methods make objects feel native in Python.

---

## 3. `dataclasses` and `attrs`

### `dataclasses`
`dataclasses` are part of Python’s standard library and are designed for classes that mainly store data.

Example:

```python
from dataclasses import dataclass


@dataclass
class User:
    name: str
    age: int
```

This automatically gives useful methods like:
- `__init__`
- `__repr__`
- `__eq__`

### Why `dataclasses` are useful
They reduce boilerplate and make data-oriented classes much cleaner.

They are a good fit when:
- the class mainly stores fields
- you want readable model objects
- you want less manual class code
- the behavior is light or secondary

### Common features
`dataclasses` support:
- default values
- frozen/immutable-like models
- ordering
- post-initialization logic with `__post_init__`

### Example with defaults

```python
from dataclasses import dataclass


@dataclass
class Config:
    debug: bool = False
    port: int = 8000
```

### Example with `__post_init__`

```python
from dataclasses import dataclass


@dataclass
class User:
    name: str
    normalized_name: str = ""

    def __post_init__(self):
        self.normalized_name = self.name.strip().lower()
```

### `attrs`
`attrs` is a third-party library that also helps build classes with less boilerplate.

It plays a role similar to `dataclasses`, but it has long been known for:
- flexibility
- strong ergonomics
- advanced validation/conversion features
- rich data-class-like modeling

Example:

```python
import attrs


@attrs.define
class User:
    name: str
    age: int
```

### Why `attrs` is useful
`attrs` is useful when:
- you want dataclass-like convenience
- you want richer validation or conversion tools
- you prefer its API and features
- your project already uses it

### `dataclasses` vs `attrs`
A useful shortcut is:

- **`dataclasses`** → standard library, simple and common
- **`attrs`** → third-party, flexible, feature-rich

### Practical comparison
Choose `dataclasses` when:
- standard library is enough
- the model is relatively simple
- you want fewer dependencies

Choose `attrs` when:
- you want more advanced class helpers
- richer field behavior matters
- your team already uses it heavily

### Main idea
Both `dataclasses` and `attrs` help define data-oriented classes cleanly, with less manual boilerplate than regular class definitions.

---

## 4. Pydantic for Validation and Serialization

### What Pydantic is
Pydantic is a library for:
- data validation
- parsing
- serialization
- structured model definition

It is especially common in:
- APIs
- FastAPI projects
- configuration models
- request/response models
- typed data boundaries

### Why Pydantic is useful
Pydantic is useful when you need to:
- validate external input
- ensure data shape is correct
- coerce values into expected types when appropriate
- serialize structured output

### Basic example

```python
from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int
```

Usage:

```python
user = User(name="Janette", age=25)
```

### Validation idea
If the data does not match the model, Pydantic raises validation errors instead of silently accepting bad input.

This is especially valuable at boundaries such as:
- API input
- config loading
- message payloads
- external service responses

### Serialization
Pydantic models can also be serialized cleanly.

Example idea:
- convert model to JSON-friendly output
- produce structured responses
- pass validated objects across layers

### Why this matters
Pydantic is not mainly about business-domain objects.  
It is especially strong at **boundary models** where validation and serialization matter.

---

## 5. Practical Role Differences

A very useful distinction is:

### Regular classes
Good for:
- general object-oriented modeling
- behavior-heavy objects
- entities
- services
- custom Python objects

### `dataclasses` / `attrs`
Good for:
- data-centric classes
- light behavior plus structured fields
- DTO-like objects
- config-like objects
- readable value objects

### Pydantic
Good for:
- input validation
- parsing external data
- API schemas
- serialization
- boundary models

### Practical shortcut
- **class** → behavior and state
- **dataclass / attrs** → structured data with less boilerplate
- **Pydantic** → validated and serialized structured data at boundaries

---

## 6. Common Mistakes

### Overusing inheritance
Not every reuse problem should be solved with inheritance.  
Composition is often safer and more flexible.

### Using `dataclasses` for everything
A class with heavy business behavior may be better as a regular class.

### Confusing domain entities with Pydantic models
Pydantic models are excellent at validation and serialization, but they are not automatically the best place for core business behavior.

### Treating Pydantic as a replacement for all class design
Pydantic is strongest at boundaries, not as the answer to every modeling problem.

### Forgetting dunder methods when object behavior matters
If you want objects to work naturally with Python operations, special methods often matter.

---

## 7. How These Topics Connect

These topics work together in everyday Python design:

- **classes** define objects with behavior and state
- **inheritance** shares behavior through hierarchy
- **composition** combines objects for flexibility
- **dunder methods** integrate objects with Python syntax
- **`dataclasses` and `attrs`** reduce boilerplate for data-centric classes
- **Pydantic** validates and serializes structured data at boundaries

A healthy design often uses more than one of these tools depending on the responsibility of the object.

---

## 8. Final Takeaway

If you only keep the essentials:

1. Classes are the base tool for object-oriented design in Python.
2. Inheritance shares behavior, but composition is often more flexible.
3. Dunder methods make objects behave naturally with Python operations.
4. `dataclasses` and `attrs` are great for data-oriented models with less boilerplate.
5. Pydantic is best for validation and serialization at input/output boundaries.
6. The right choice depends on whether the object is mainly about behavior, structured data, or validated external data.

---
# Advanced Typing, Style, and Automated Checks

## 1. Goal

This document gives a clear summary of these practical Python topics:

- type hints and advanced typing (`Union`, `Literal`, `TypedDict`, `Protocol`)
- `mypy` and `pyright`, plus the limits of dynamic typing
- PEP 8 with `ruff`, `black`, and `isort`; PEP 20 as a design guide
- `pre-commit` and checks in CI

The purpose is to connect typing, code style, and automated quality checks into one practical mental model.

---

## 2. Type Hints and Advanced Typing

### What type hints are
Type hints let you describe the expected types of variables, parameters, and return values.

Example:

```python
def greet(name: str) -> str:
    return f"Hello, {name}"
```

### Why type hints are useful
Type hints help with:
- readability
- editor support
- static analysis
- refactoring safety
- API clarity

They do not change Python into a fully statically typed language, but they make code easier to understand and check.

### `Union`
`Union` means a value may be one of several possible types.

Example:

```python
from typing import Union

def parse_id(value: Union[int, str]) -> str:
    return str(value)
```

In modern Python, this is often written as:

```python
def parse_id(value: int | str) -> str:
    return str(value)
```

### `Literal`
`Literal` restricts a value to specific allowed constants.

Example:

```python
from typing import Literal

def set_mode(mode: Literal["dev", "prod", "test"]) -> None:
    ...
```

This is useful when only a small fixed set of values is valid.

### `TypedDict`
`TypedDict` describes the expected shape of a dictionary.

Example:

```python
from typing import TypedDict

class UserData(TypedDict):
    name: str
    age: int
```

Now a dictionary can be typed by keys and value types.

This is useful when:
- dictionaries represent structured data
- you want more safety without creating full classes

### `Protocol`
`Protocol` defines a structural contract based on behavior.

Example:

```python
from typing import Protocol

class SupportsSend(Protocol):
    def send(self, message: str) -> None:
        ...
```

Any object with a compatible `send()` method can satisfy this protocol, even without explicit inheritance.

This is very useful for:
- dependency inversion
- loose coupling
- duck typing with static checking

### Main idea
Advanced typing helps describe richer expectations about values, structures, and behavior, not just simple `int` or `str` annotations.

---

## 3. `mypy`, `pyright`, and the Limits of Dynamic Typing

### What `mypy` is
`mypy` is a static type checker for Python.

It reads type hints and checks whether the code matches those hints.

### What `pyright` is
`pyright` is another static type checker, also widely used and known for speed and strong editor integration.

### Why type checkers are useful
Type checkers help detect issues such as:
- wrong argument types
- missing return values
- bad assumptions about `None`
- inconsistent dictionary shapes
- incorrect use of protocols or generics

### Main difference in practice
A useful shortcut is:

- **`mypy`** → very established and common in Python projects
- **`pyright`** → very fast, often strong in editor and IDE workflows

### Limits of typing in Python
Python is still dynamically typed at runtime.

That means:
- many type checks happen only through tools, not at runtime
- not every dynamic pattern can be expressed cleanly
- some runtime behavior is difficult for static analysis to prove
- you can still write code that passes type checking but fails at runtime

### Why this matters
Type hints improve safety, but they do not eliminate:
- runtime bugs
- bad external input
- logic errors
- incorrect assumptions about side effects

### Practical idea
Static typing in Python is a strong support tool, not a total replacement for:
- tests
- runtime validation
- careful design

### Main idea
`mypy` and `pyright` improve correctness and maintainability, but Python remains a dynamic language, so static typing has useful but real limits.

---

## 4. PEP 8 with `ruff`, `black`, and `isort`; PEP 20 as a Design Guide

### PEP 8
PEP 8 is the main style guide for Python code.

It covers things like:
- naming
- spacing
- line length
- imports
- formatting conventions
- general readability

### Why PEP 8 matters
The goal is not “style for style’s sake.”  
The goal is:
- consistency
- readability
- maintainability
- easier collaboration

### `black`
`black` is an automatic code formatter.

Its main value is:
- consistent formatting
- fewer style debates
- less manual formatting work

A common practical rule is:
- let `black` decide formatting automatically

### `isort`
`isort` organizes imports consistently.

It helps:
- group imports cleanly
- sort them predictably
- reduce import-style noise in reviews

### `ruff`
`ruff` is a fast linter and code-quality tool that can cover:
- many linting rules
- style checks
- import checks
- some automatic fixes

In many modern Python projects, `ruff` is used heavily because it is fast and can replace or reduce multiple older tooling combinations.

### Practical shortcut
- **`black`** → formatting
- **`isort`** → import ordering
- **`ruff`** → linting and many code-quality checks

### PEP 20
PEP 20 is “The Zen of Python.”

It is not a syntax standard like PEP 8.  
It is a design philosophy guide.

Famous ideas from it include:
- explicit is better than implicit
- simple is better than complex
- readability counts

### Why PEP 20 matters
PEP 20 helps guide code design decisions, not just formatting.

It is especially useful when choosing between:
- clever code vs clear code
- magical abstractions vs explicit behavior
- dense tricks vs maintainable design

### Main idea
PEP 8 helps keep code consistent, while PEP 20 helps keep code thoughtful and readable.

---

## 5. `pre-commit` and Checks in CI

### What `pre-commit` is
`pre-commit` is a tool that runs checks automatically before commits are created.

Examples of checks:
- formatting
- linting
- type checking
- trailing whitespace cleanup
- file validation
- import sorting

### Why `pre-commit` is useful
It helps catch issues early, before code reaches:
- pull requests
- CI pipelines
- main branches

This improves feedback speed and reduces avoidable review noise.

### What checks in CI mean
CI checks are automated validations that run in pipelines such as:
- GitHub Actions
- Azure DevOps
- other CI systems

Typical CI checks include:
- tests
- linting
- formatting validation
- type checking
- dependency security checks

### Why both matter
A useful pattern is:

- **`pre-commit`** catches problems early on the developer machine
- **CI** enforces the same checks centrally for the whole team

### Practical idea
`pre-commit` is convenient, but CI is the real enforcement point.

If a rule matters for the repository, it should exist in CI as well.

### Main idea
Automated checks should run both locally and centrally so quality does not depend only on manual discipline.

---

## 6. How These Topics Connect

These topics work together as one quality workflow:

- **type hints** make intent explicit
- **advanced typing** models richer contracts
- **`mypy` / `pyright`** verify those contracts statically
- **PEP 8 and tooling** keep code consistent and readable
- **PEP 20** guides better design decisions
- **`pre-commit`** gives fast local feedback
- **CI** enforces standards at the team and repository level

This creates a strong loop of:
- clearer code
- earlier feedback
- safer refactoring
- more predictable quality

---

## 7. Final Takeaway

If you only keep the essentials:

1. Advanced typing tools such as `Union`, `Literal`, `TypedDict`, and `Protocol` make Python contracts clearer.
2. `mypy` and `pyright` improve safety, but Python remains dynamically typed at runtime.
3. PEP 8 supports consistent style, and PEP 20 supports good design thinking.
4. `black`, `isort`, and `ruff` automate formatting, imports, and linting.
5. `pre-commit` catches issues early, while CI enforces the same standards for the whole project.
6. Together, these tools create a practical quality system for modern Python development.

---
