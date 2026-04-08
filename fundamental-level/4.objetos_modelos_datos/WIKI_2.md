# Python: Type Hints and Advanced Typing (`Union`, `Literal`, `TypedDict`, `Protocol`)

## 1. What Are Type Hints?

**Type hints** are annotations that describe the expected types of variables, function arguments, and return values.

They improve:
- readability
- editor support
- static analysis
- refactoring safety

### Basic example
```python
def greet(name: str) -> str:
    return f"Hello, {name}"
```

Here:
- `name: str` means `name` is expected to be a string
- `-> str` means the function is expected to return a string

### Important
Python does **not** enforce type hints automatically at runtime.

This means code like this can still run:

```python
def add(a: int, b: int) -> int:
    return a + b

print(add("2", "3"))  # Produces "23"
```

Type hints are mainly for:
- type checkers like `mypy`
- IDEs
- linters
- documentation

---

## 2. Simple Type Hints

### Variables
```python
age: int = 24
name: str = "Janette"
is_active: bool = True
price: float = 19.99
```

### Functions
```python
def square(x: int) -> int:
    return x * x
```

### Collections
```python
numbers: list[int] = [1, 2, 3]
names: set[str] = {"Ana", "Luis"}
scores: dict[str, int] = {"math": 95, "english": 88}
point: tuple[int, int] = (10, 20)
```

---

## 3. Why Type Hints Matter

Type hints help make intent explicit.

Without hints:
```python
def process(data):
    ...
```

With hints:
```python
def process(data: list[str]) -> dict[str, int]:
    ...
```

The second version immediately tells you:
- what kind of data the function expects
- what kind of result it returns

---

## 4. The `typing` Module

Many advanced typing tools come from the `typing` module.

```python
from typing import Union, Literal, TypedDict, Protocol
```

Modern Python also supports many built-in generic forms like:
- `list[int]`
- `dict[str, int]`
- `tuple[str, int]`

---

## 5. `Union`

`Union` means a value can be one of several types.

### Example
```python
from typing import Union

def stringify(value: Union[int, float]) -> str:
    return str(value)
```

This means `value` can be:
- an `int`
- a `float`

### Modern syntax
In modern Python, `Union[int, str]` can be written as:

```python
def process(value: int | str) -> None:
    print(value)
```

This is now the preferred style in newer Python code.

### Example
```python
def get_id(value: int | str) -> str:
    return str(value)
```

---

## 6. `Optional`

`Optional[X]` means `X | None`.

```python
from typing import Optional

def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Janette"
    return None
```

Modern equivalent:
```python
def find_user(user_id: int) -> str | None:
    if user_id == 1:
        return "Janette"
    return None
```

### Important
`Optional[int]` does **not** mean “the argument is optional”.
It means the value itself may be `None`.

This is different:

```python
def foo(x: int = 0) -> None:
    ...
```

The parameter has a default, but its type is still just `int`.

---

## 7. Narrowing a `Union`

When working with a union, you often need to check which type you actually got.

```python
def double(value: int | str) -> int | str:
    if isinstance(value, int):
        return value * 2
    return value * 2
```

This works because:
- if `value` is `int`, `value * 2` is arithmetic
- if `value` is `str`, `value * 2` repeats the string

### Clearer example
```python
def describe(value: int | str) -> str:
    if isinstance(value, int):
        return f"Integer: {value}"
    return f"String: {value}"
```

---

## 8. `Literal`

`Literal` lets you specify that a value must be one of a fixed set of exact values.

### Example
```python
from typing import Literal

def set_mode(mode: Literal["light", "dark"]) -> None:
    print(f"Mode set to {mode}")
```

This tells type checkers that only these exact strings are valid:
- `"light"`
- `"dark"`

### Valid call
```python
set_mode("light")
```

### Invalid for a type checker
```python
set_mode("blue")
```

A type checker would flag `"blue"` as invalid.

---

## 9. Why `Literal` Is Useful

`Literal` is useful when a function accepts only specific known values.

Examples:
- modes
- statuses
- actions
- command names
- configuration flags

### Example
```python
from typing import Literal

def send_request(method: Literal["GET", "POST", "PUT", "DELETE"]) -> None:
    print(method)
```

This is much more precise than:

```python
def send_request(method: str) -> None:
    print(method)
```

---

## 10. `Literal` with Numbers and Booleans

`Literal` is not limited to strings.

```python
from typing import Literal

def move(direction: Literal[1, -1]) -> None:
    print(direction)
```

Another example:
```python
from typing import Literal

flag: Literal[True] = True
```

---

## 11. `TypedDict`

A `TypedDict` describes the expected structure of a dictionary.

It is useful when you want a dictionary with specific keys and value types.

### Example
```python
from typing import TypedDict

class UserData(TypedDict):
    name: str
    age: int
```

Now a dictionary like this matches that type:

```python
user: UserData = {
    "name": "Janette",
    "age": 24
}
```

---

## 12. Why `TypedDict` Is Useful

Without `TypedDict`, this type is vague:

```python
user: dict[str, object]
```

That does not tell you:
- which keys should exist
- which value type belongs to each key

With `TypedDict`, the expected structure is explicit.

```python
from typing import TypedDict

class UserData(TypedDict):
    name: str
    age: int
```

This is especially helpful for:
- JSON-like objects
- API payloads
- config dictionaries
- structured internal data

---

## 13. Basic `TypedDict` Example

```python
from typing import TypedDict

class Product(TypedDict):
    name: str
    price: float
    in_stock: bool

product: Product = {
    "name": "Keyboard",
    "price": 49.99,
    "in_stock": True
}
```

---

## 14. Required and Optional Keys in `TypedDict`

By default, all keys in a `TypedDict` are required.

```python
from typing import TypedDict

class Point(TypedDict):
    x: int
    y: int
```

This means both `x` and `y` are required.

### `NotRequired`
You can make individual keys optional.

```python
from typing import TypedDict, NotRequired

class Point(TypedDict):
    x: int
    y: int
    label: NotRequired[str]
```

Now `label` does not have to be present.

### Example
```python
point1: Point = {"x": 1, "y": 2}
point2: Point = {"x": 1, "y": 2, "label": "A"}
```

---

## 15. `total=False`

Another way to make keys optional is `total=False`.

```python
from typing import TypedDict

class UserData(TypedDict, total=False):
    name: str
    age: int
```

Now all keys are optional.

### Example
```python
user: UserData = {"name": "Janette"}
```

### Mixing required and optional keys
You can combine `total=False` with `Required`.

```python
from typing import TypedDict, Required

class UserData(TypedDict, total=False):
    name: Required[str]
    age: int
```

Now:
- `name` is required
- `age` is optional

---

## 16. Inheriting from `TypedDict`

A `TypedDict` can inherit from another `TypedDict`.

```python
from typing import TypedDict

class Point2D(TypedDict):
    x: int
    y: int

class Point3D(Point2D):
    z: int
```

Now `Point3D` includes:
- `x`
- `y`
- `z`

---

## 17. Generic `TypedDict`

A `TypedDict` can also be generic.

```python
from typing import TypedDict, TypeVar, Generic

T = TypeVar("T")

class Group(TypedDict, Generic[T]):
    key: T
    group: list[T]
```

This is useful when the dictionary structure stays the same, but the element type changes.

---

## 18. `Protocol`

A `Protocol` defines a required interface.

It is used for **structural subtyping**, also called **static duck typing**.

That means:
- a class does not need to explicitly inherit from the protocol
- it only needs to provide the expected methods or attributes

### Example
```python
from typing import Protocol

class Closable(Protocol):
    def close(self) -> None:
        ...
```

Any object with a compatible `close()` method can satisfy this protocol.

---

## 19. Why `Protocol` Is Useful

Normally, Python classes are typed nominally:
- a class matches because it inherits from another class

With `Protocol`, a class can match just by having the right shape.

This is useful when:
- you want flexible interfaces
- you want duck typing with static checking
- you do not control the original class
- multiple unrelated classes share the same behavior

---

## 20. Basic `Protocol` Example

```python
from typing import Protocol

class SupportsSpeak(Protocol):
    def speak(self) -> str:
        ...

class Dog:
    def speak(self) -> str:
        return "Woof"

class Person:
    def speak(self) -> str:
        return "Hello"

def make_it_speak(obj: SupportsSpeak) -> None:
    print(obj.speak())

make_it_speak(Dog())
make_it_speak(Person())
```

Even though `Dog` and `Person` do not inherit from `SupportsSpeak`, they still match the protocol because they implement `speak()`.

---

## 21. Protocol with Attributes

Protocols can require attributes too.

```python
from typing import Protocol

class HasName(Protocol):
    name: str

class User:
    def __init__(self, name: str):
        self.name = name

def greet(entity: HasName) -> None:
    print(f"Hello, {entity.name}")

greet(User("Janette"))
```

---

## 22. Generic Protocols

Protocols can be generic.

```python
from typing import Protocol, TypeVar

T = TypeVar("T")

class Getter(Protocol[T]):
    def get(self) -> T:
        ...
```

Example implementation:
```python
class IntBox:
    def get(self) -> int:
        return 10
```

`IntBox` is compatible with `Getter[int]`.

---

## 23. `runtime_checkable`

By default, protocols are mainly for static type checking.

If you want to use `isinstance()` with a protocol, decorate it with `@runtime_checkable`.

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Closable(Protocol):
    def close(self) -> None:
        ...

class FileLike:
    def close(self) -> None:
        print("Closed")

obj = FileLike()
print(isinstance(obj, Closable))  # True
```

### Important
At runtime, this only checks whether the required attributes/methods exist.
It does **not** verify full type signatures.

---

## 24. `Protocol` vs Abstract Base Class

### Abstract Base Class (ABC)
Usually requires inheritance.

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self) -> str:
        pass
```

### Protocol
Does not require explicit inheritance.

```python
from typing import Protocol

class SupportsSpeak(Protocol):
    def speak(self) -> str:
        ...
```

### Rule of thumb
Use:
- **ABC** when you want formal inheritance and shared base behavior
- **Protocol** when you want flexible structural typing

---

## 25. `Union` vs `Literal`

These two are different.

### `Union`
Means “one of several types”.

```python
int | str
```

### `Literal`
Means “one of these exact values”.

```python
Literal["GET", "POST"]
```

### Example
```python
from typing import Literal

def request(method: Literal["GET", "POST"], retries: int | None) -> None:
    print(method, retries)
```

Here:
- `method` must be one of two exact strings
- `retries` can be `int` or `None`

---

## 26. `TypedDict` vs Dataclass

These are different tools.

### `TypedDict`
Describes a dictionary shape.

```python
from typing import TypedDict

class UserData(TypedDict):
    name: str
    age: int
```

### Dataclass
Creates a real class with attributes.

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
```

### Use `TypedDict` when:
- data is still dictionary-shaped
- you are dealing with JSON-like structures
- you want key-based access

### Use a dataclass when:
- you want objects
- you want methods
- you want attribute access

---

## 27. `Protocol` vs Duck Typing

Python already supports duck typing naturally:

```python
def speak(obj):
    print(obj.speak())
```

That works at runtime.

But `Protocol` adds:
- explicit documentation
- better editor support
- static checking
- safer refactoring

So `Protocol` is like **typed duck typing**.

---

## 28. Type Aliases

If a type becomes long or repetitive, use a type alias.

### Modern syntax
```python
type UserId = int
type JsonDict = dict[str, str | int | bool]
```

### Example
```python
type Point = tuple[int, int]

def move(point: Point) -> Point:
    x, y = point
    return (x + 1, y + 1)
```

### Older style
In older code, you may still see:

```python
UserId = int
Point = tuple[int, int]
```

---

## 29. `typing_extensions`

Some typing features appear first in newer Python versions.

If you need compatibility with older Python versions, use `typing_extensions`.

```python
from typing_extensions import Protocol, TypedDict, Literal
```

This is common in libraries that support multiple Python versions.

---

## 30. Common Beginner Mistakes

### Thinking type hints are enforced automatically
```python
def add(a: int, b: int) -> int:
    return a + b
```

Python will not stop you from passing wrong types unless you add runtime checks yourself.

### Confusing optional argument with `Optional`
Wrong idea:
```python
def foo(x: int = 0) -> None:
    ...
```

This does **not** mean `x` is `Optional[int]`.

### Using `dict[str, object]` when a `TypedDict` is clearer
This:
```python
user: dict[str, object]
```

is often less useful than:
```python
class UserData(TypedDict):
    name: str
    age: int
```

### Confusing `Union` and `Literal`
- `int | str` means different possible **types**
- `Literal["GET", "POST"]` means specific exact **values**

### Expecting `runtime_checkable` to validate signatures
It only checks that the required members exist, not that their full type signatures match exactly.

---

## 31. Summary

- **Type hints** describe expected types for variables, parameters, and return values
- Python does **not** enforce them automatically at runtime
- **`Union`** means a value can be one of several types
- Modern `Union` syntax is `X | Y`
- **`Optional[X]`** means `X | None`
- **`Literal`** restricts a value to exact known values
- **`TypedDict`** describes the structure of a dictionary with known keys
- `TypedDict` supports:
  - required keys
  - optional keys
  - inheritance
- **`Protocol`** defines an interface using structural typing
- `Protocol` is useful for typed duck typing
- **`runtime_checkable`** allows limited runtime `isinstance()` checks for protocols
- **type aliases** help simplify long type signatures
- **`typing_extensions`** helps with compatibility on older Python versions

# Python: `mypy`, `Pyright`, and the Limits of Dynamic Typing

## 1. What Are `mypy` and `Pyright`?

`mypy` and `Pyright` are **static type checkers** for Python.

They analyze your code **without running it** and report type-related problems such as:

- passing the wrong argument type
- returning the wrong type
- using `None` where a value is required
- treating one type as if it were another

They work with Python type hints, such as:

```python
def greet(name: str) -> str:
    return f"Hello, {name}"
```

---

## 2. Why Use a Static Type Checker in Python?

Python is a **dynamic language**.

That means many type errors appear only at runtime.

Example:

```python
def add(a, b):
    return a + b

print(add("2", 3))
```

This code is valid Python syntax, but it fails only when it runs.

With type hints plus a static checker, you can detect many errors earlier.

```python
def add(a: int, b: int) -> int:
    return a + b
```

A type checker can warn you before execution if you pass the wrong types.

---

## 3. `mypy`

`mypy` is one of the most widely used static type checkers in Python.

It focuses on checking code that uses standard Python type hints.

### Installation
```bash
pip install mypy
```

### Basic usage
```bash
mypy app.py
```

### Example
```python
def greet(name: str) -> str:
    return "Hello, " + name

greet(123)
```

Running `mypy` on that file would report that `123` is not compatible with `str`.

---

## 4. `Pyright`

`Pyright` is another static type checker for Python.

It is known for:
- speed
- strong editor integration
- good support for large codebases

### Installation
```bash
npm install -g pyright
```

### Basic usage
```bash
pyright
```

Or:
```bash
pyright app.py
```

### Example
```python
def greet(name: str) -> str:
    return "Hello, " + name

greet(123)
```

Pyright would also report a type mismatch here.

---

## 5. `mypy` vs `Pyright`

Both tools solve a similar problem:
they check whether your Python type hints are used correctly.

### `mypy`
Often used when:
- teams want a very established checker
- projects already use `mypy.ini` or `pyproject.toml`
- plugins and gradual typing are important

### `Pyright`
Often used when:
- fast feedback is important
- editor integration matters a lot
- projects want strong support for modern typing features

### Practical reality
Many teams choose one primary checker, but the general typing concepts are shared.

---

## 6. Static Typing vs Dynamic Typing

### Dynamic typing
In Python, variable types are not fixed at compile time.

```python
x = 10
x = "hello"
```

This is valid Python.

### Static type checking
A static checker looks at annotations and tries to verify consistency.

```python
x: int = 10
x = "hello"  # type checker should complain
```

Python may still run this, but the checker flags it as a problem.

---

## 7. Python Does Not Enforce Type Hints at Runtime

This is very important.

Type hints are mainly for:
- type checkers
- IDEs
- linters
- documentation

Python itself does not automatically stop you from violating them.

```python
def square(x: int) -> int:
    return x * x

print(square("hello"))
```

A type checker warns about this, but Python itself will still try to run it.

---

## 8. First Example with `mypy`

```python
def repeat(text: str, times: int) -> str:
    return text * times

result = repeat("Hi", "3")
print(result)
```

### What happens?
- Python may fail only when the wrong operation becomes a problem
- `mypy` can detect that `"3"` is not an `int`

This is one of the main advantages of static checking.

---

## 9. First Example with `Pyright`

```python
def divide(a: float, b: float) -> float:
    return a / b

value = divide(10, "2")
```

A static checker like Pyright can warn that `"2"` is not a `float`.

---

## 10. Gradual Typing

Python typing is often called **gradual typing**.

That means:
- you can type some code
- leave other parts untyped
- improve coverage step by step

Example:

```python
def typed_function(name: str) -> str:
    return name.upper()

def untyped_function(data):
    return data
```

This flexibility is useful in real projects because you do not have to type everything at once.

---

## 11. What Static Checkers Catch Well

Static type checkers are good at catching problems like:

- wrong argument types
- wrong return types
- missing attributes
- invalid use of `None`
- inconsistent reassignment
- bad assumptions about collections
- mismatched overrides in class hierarchies

### Example
```python
def get_length(items: list[str]) -> int:
    return len(items)

get_length("hello")
```

A checker can report that `str` is not `list[str]`.

---

## 12. Configuration in `mypy`

`mypy` can be configured with files such as:

- `mypy.ini`
- `.mypy.ini`
- `pyproject.toml`
- `setup.cfg`

### Example `mypy.ini`
```ini
[mypy]
python_version = 3.12
warn_return_any = True
disallow_untyped_defs = True
```

### Example `pyproject.toml`
```toml
[tool.mypy]
python_version = "3.12"
warn_return_any = true
disallow_untyped_defs = true
```

---

## 13. Configuration in `Pyright`

`Pyright` is commonly configured with:

- `pyrightconfig.json`
- `pyproject.toml`

### Example `pyrightconfig.json`
```json
{
  "include": ["src"],
  "typeCheckingMode": "basic"
}
```

### Stricter example
```json
{
  "include": ["src"],
  "typeCheckingMode": "strict"
}
```

### Example in `pyproject.toml`
```toml
[tool.pyright]
include = ["src"]
typeCheckingMode = "basic"
```

---

## 14. Strictness Levels

Both tools can be used more loosely or more strictly.

### Why that matters
In a large existing codebase, fully strict typing may produce too many errors at first.

So teams often start with:
- partial typing
- moderate rules
- gradual improvement

### Example strategy
1. add annotations to new code
2. type core modules
3. enable stricter checks over time
4. reduce `Any`
5. fix ignored warnings gradually

---

## 15. The Role of `Any`

`Any` means “skip precise checking here”.

```python
from typing import Any

def process(data: Any) -> Any:
    return data
```

This is sometimes useful, but too much `Any` weakens type checking.

### Example
```python
from typing import Any

value: Any = "hello"
print(value.not_a_real_method())
```

A checker often cannot protect you much here because `Any` disables a lot of checking.

---

## 16. Type Narrowing

Static checkers can narrow types based on control flow.

```python
def print_length(value: str | None) -> None:
    if value is not None:
        print(len(value))
```

Inside the `if`, the checker understands that `value` is now `str`, not `None`.

This is called **type narrowing**.

---

## 17. Limits of Dynamic Typing

Dynamic typing gives flexibility, but it also has limits.

### Common limitations
- some bugs appear only at runtime
- refactoring is riskier without type information
- large codebases become harder to reason about
- interfaces are less explicit
- IDE support is weaker without annotations
- data shape mistakes may go unnoticed until execution

### Example
```python
def send_email(user):
    print(user["email"].lower())
```

If `user` has the wrong structure, the failure happens only at runtime.

With typing:
```python
from typing import TypedDict

class User(TypedDict):
    email: str

def send_email(user: User) -> None:
    print(user["email"].lower())
```

Now tools can help more.

---

## 18. Static Typing Does Not Solve Everything

Type checkers are helpful, but they do not replace testing.

They do **not** prove that your program is correct.

They mainly help with:
- type consistency
- interface correctness
- safer refactoring

They do **not** automatically verify:
- business rules
- performance
- security
- correct algorithms
- correct database state
- correct API behavior in the real world

So typing and tests complement each other.

---

## 19. Runtime vs Static Problems

### Static type checker can catch
```python
def add(a: int, b: int) -> int:
    return a + b

result = add("2", 3)
```

### But runtime-only issues still exist
```python
def divide(a: float, b: float) -> float:
    return a / b

print(divide(10, 0))
```

Even with perfect type hints, division by zero is still a runtime problem.

---

## 20. Highly Dynamic Code Is Harder to Type

Some Python patterns are harder for static checkers to analyze precisely.

Examples:
- dynamic attribute creation
- metaprogramming
- monkey patching
- runtime-generated objects
- heavy reflection
- code that changes behavior based on strings or external metadata

### Example
```python
class DynamicObject:
    pass

obj = DynamicObject()
setattr(obj, "name", "Janette")
print(obj.name)
```

This works at runtime, but static tools may know little about `obj.name` unless you annotate it explicitly.

---

## 21. Monkey Patching and Typing Limits

Monkey patching means changing objects or classes at runtime.

```python
class User:
    pass

def say_hello(self):
    return "Hello"

User.say_hello = say_hello
```

This is valid Python, but it is harder for static type checkers to model accurately.

This is one reason dynamic typing is flexible but less predictable.

---

## 22. Reflection and `getattr`

Reflection-heavy code often reduces static precision.

```python
def call_method(obj, method_name: str):
    method = getattr(obj, method_name)
    return method()
```

This may be valid Python, but a static checker cannot always know:
- whether the method exists
- what parameters it expects
- what it returns

So the more dynamic the code is, the less precise static typing becomes.

---

## 23. Untyped Code Reduces Checker Power

If a lot of your code is untyped, the checker has less information to work with.

```python
def load_data(source):
    return source.fetch()

def process_data(data: list[str]) -> int:
    return len(data)

result = process_data(load_data(obj))
```

If `load_data` is untyped, the checker may not be able to guarantee much about the result.

This is why gradual typing works best when type coverage improves over time.

---

## 24. Third-Party Libraries and Stubs

Sometimes a library is dynamic or has incomplete typing support.

In those cases, static checking may depend on:
- inline type hints
- `.pyi` stub files
- community-provided stubs
- your own local stubs

Without good type information, checker accuracy drops.

---

## 25. When `mypy` or `Pyright` Help the Most

They are especially useful in:

- medium and large codebases
- APIs and data pipelines
- backend services
- teams with many contributors
- refactoring-heavy projects
- libraries with public interfaces

They are most valuable when code changes frequently and mistakes need to be caught early.

---

## 26. When Dynamic Python Still Shines

Dynamic Python is still very useful for:

- scripts
- prototypes
- quick automation
- experiments
- highly flexible metaprogramming
- rapid iteration

The point is not that static checking replaces Python’s dynamic nature.

The point is that static checking helps control complexity when needed.

---

## 27. Common Beginner Mistakes

### Thinking type hints are enforced automatically
```python
def square(x: int) -> int:
    return x * x
```

This annotation alone does not stop bad calls at runtime.

### Using too much `Any`
```python
from typing import Any

def process(data: Any) -> Any:
    return data
```

This removes many of the benefits of static typing.

### Expecting the checker to understand every dynamic trick
Highly dynamic patterns often need extra annotations or redesign.

### Ignoring checker warnings completely
The tool is most useful when warnings are reviewed and fixed intentionally.

### Turning on strict mode too early for a legacy project
This can create frustration if the codebase has very low type coverage.

---

## 28. Practical Recommendation

A good practical approach is:

1. type all new code
2. annotate function boundaries first
3. avoid unnecessary `Any`
4. enable checker rules gradually
5. use stricter settings in core modules
6. combine static typing with tests

This gives most of the benefits without trying to force everything at once.

---

## 29. Summary

- `mypy` and `Pyright` are static type checkers for Python
- they analyze code without running it
- they use type hints to detect type-related problems early
- `mypy` and `Pyright` both support gradual typing
- `mypy` is commonly configured with `mypy.ini` or `pyproject.toml`
- `Pyright` is commonly configured with `pyrightconfig.json` or `pyproject.toml`
- Python remains a dynamic language even when you use type hints
- type hints are not enforced automatically by Python at runtime
- static typing helps with correctness, readability, and refactoring
- dynamic typing remains flexible, but highly dynamic code is harder to check precisely
- typing improves reliability, but it does not replace tests or runtime validation