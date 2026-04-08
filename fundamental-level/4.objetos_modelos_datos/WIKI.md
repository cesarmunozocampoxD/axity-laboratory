# Python: Classes, Inheritance, Composition, and Dunder Methods

## 1. Classes in Python

A **class** is a blueprint for creating objects.

An object is an instance of a class.

Classes let you group together:

- data
- behavior
- related logic

### Basic example
```python
class Dog:
    pass
```

This creates a class, but it does not do anything useful yet.

### Creating an object
```python
class Dog:
    pass

my_dog = Dog()
print(my_dog)
```

`my_dog` is an instance of the `Dog` class.

---

## 2. Attributes and Methods

A class can have:

- **attributes**: variables that belong to the object
- **methods**: functions defined inside the class

### Example
```python
class Dog:
    def bark(self):
        print("Woof!")
```

### Using the method
```python
dog = Dog()
dog.bark()
```

---

## 3. The `self` Parameter

In instance methods, the first parameter is usually called `self`.

`self` refers to the current object.

```python
class Dog:
    def bark(self):
        print("Woof!")
```

When you call:

```python
dog.bark()
```

Python automatically passes `dog` as `self`.

---

## 4. The `__init__` Method

`__init__` is a special method used to initialize new objects.

It runs automatically when you create an instance.

### Example
```python
class Dog:
    def __init__(self, name):
        self.name = name
```

### Creating objects
```python
dog1 = Dog("Max")
dog2 = Dog("Luna")

print(dog1.name)  # Max
print(dog2.name)  # Luna
```

Here:
- `name` is a parameter
- `self.name` is an attribute of the object

---

## 5. Instance Attributes

Instance attributes belong to each object separately.

```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

dog1 = Dog("Max", 3)
dog2 = Dog("Luna", 5)

print(dog1.name)  # Max
print(dog2.name)  # Luna
```

Each object has its own values.

---

## 6. Class Attributes

A class attribute belongs to the class itself and is shared by all instances.

```python
class Dog:
    species = "Canis familiaris"

    def __init__(self, name):
        self.name = name
```

Usage:
```python
dog1 = Dog("Max")
dog2 = Dog("Luna")

print(dog1.species)
print(dog2.species)
print(Dog.species)
```

### Difference
- `self.name` → instance attribute
- `species` → class attribute

---

## 7. Example: Simple Class

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"My name is {self.name} and I am {self.age} years old.")

person = Person("Janette", 24)
person.introduce()
```

---

## 8. Inheritance

**Inheritance** lets one class reuse and extend another class.

The new class is called a **child class** or **subclass**.

The original class is called a **parent class** or **base class**.

### Basic example
```python
class Animal:
    def eat(self):
        print("Eating...")

class Dog(Animal):
    def bark(self):
        print("Woof!")
```

### Usage
```python
dog = Dog()
dog.eat()
dog.bark()
```

`Dog` inherits the `eat()` method from `Animal`.

---

## 9. Why Use Inheritance?

Inheritance is useful when classes share common behavior.

For example:

- `Animal` can define shared behavior
- `Dog`, `Cat`, and `Bird` can inherit from it

### Example
```python
class Animal:
    def sleep(self):
        print("Sleeping...")

class Cat(Animal):
    def meow(self):
        print("Meow")

class Bird(Animal):
    def sing(self):
        print("Tweet")
```

---

## 10. Overriding Methods

A child class can replace a method from the parent class.

This is called **method overriding**.

```python
class Animal:
    def speak(self):
        print("Some animal sound")

class Dog(Animal):
    def speak(self):
        print("Woof!")

class Cat(Animal):
    def speak(self):
        print("Meow")
```

### Usage
```python
dog = Dog()
cat = Cat()

dog.speak()  # Woof!
cat.speak()  # Meow
```

---

## 11. Using `super()`

`super()` lets you access methods from the parent class.

It is commonly used in `__init__`.

### Example
```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed
```

### Usage
```python
dog = Dog("Max", "Labrador")
print(dog.name)   # Max
print(dog.breed)  # Labrador
```

`super().__init__(name)` calls the parent constructor.

---

## 12. Composition

**Composition** means building a class using other objects instead of inheriting from them.

A common way to describe it is:

- inheritance = **is-a**
- composition = **has-a**

### Example
A car **has an** engine.

```python
class Engine:
    def start(self):
        print("Engine started")

class Car:
    def __init__(self):
        self.engine = Engine()

    def start(self):
        self.engine.start()
        print("Car is moving")
```

### Usage
```python
car = Car()
car.start()
```

Here:
- `Car` does not inherit from `Engine`
- `Car` contains an `Engine`

That is composition.

---

## 13. Inheritance vs Composition

### Inheritance
Use inheritance when one class is a specialized version of another.

Example:
- `Dog` is an `Animal`

### Composition
Use composition when one object contains or uses another object.

Example:
- `Car` has an `Engine`

### Rule of thumb
Prefer composition when the relationship is not naturally hierarchical.

---

## 14. Example of Composition with Multiple Objects

```python
class Battery:
    def charge(self):
        print("Battery charging")

class Screen:
    def turn_on(self):
        print("Screen on")

class Phone:
    def __init__(self):
        self.battery = Battery()
        self.screen = Screen()

    def power_on(self):
        self.battery.charge()
        self.screen.turn_on()
        print("Phone is ready")
```

This shows how one class can be composed of several other objects.

---

## 15. Dunder Methods

**Dunder methods** are special methods with double underscores before and after the name.

Examples:

- `__init__`
- `__str__`
- `__repr__`
- `__len__`
- `__add__`

They are also called **magic methods** or **special methods**.

Python uses them to define how objects behave with built-in syntax and functions.

---

## 16. `__init__`

You already saw this one.

It initializes a new object.

```python
class Person:
    def __init__(self, name):
        self.name = name
```

---

## 17. `__str__`

`__str__` defines the human-friendly string representation of an object.

```python
class Person:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Person: {self.name}"

person = Person("Janette")
print(person)
```

Output:
```python
Person: Janette
```

Without `__str__`, printing the object usually shows a generic memory-based representation.

---

## 18. `__repr__`

`__repr__` defines the developer-oriented representation of an object.

```python
class Person:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Person(name={self.name!r})"

person = Person("Janette")
print(person)
```

Output:
```python
Person(name='Janette')
```

### Difference between `__str__` and `__repr__`
- `__str__` → readable for users
- `__repr__` → useful for debugging and developers

If `__str__` does not exist, Python may fall back to `__repr__`.

---

## 19. `__len__`

`__len__` defines what `len(object)` returns.

```python
class Team:
    def __init__(self, members):
        self.members = members

    def __len__(self):
        return len(self.members)

team = Team(["Ana", "Luis", "Mia"])
print(len(team))  # 3
```

---

## 20. `__add__`

`__add__` defines behavior for the `+` operator.

```python
class Number:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        return Number(self.value + other.value)

    def __str__(self):
        return str(self.value)

a = Number(10)
b = Number(5)
c = a + b

print(c)  # 15
```

---

## 21. `__eq__`

`__eq__` defines behavior for `==`.

```python
class Person:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

p1 = Person("Ana")
p2 = Person("Ana")
p3 = Person("Luis")

print(p1 == p2)  # True
print(p1 == p3)  # False
```

---

## 22. `__iter__`

`__iter__` defines how an object becomes iterable.

```python
class MyNumbers:
    def __init__(self):
        self.data = [1, 2, 3]

    def __iter__(self):
        return iter(self.data)

numbers = MyNumbers()

for n in numbers:
    print(n)
```

---

## 23. `__call__`

`__call__` lets an object behave like a function.

```python
class Greeter:
    def __call__(self, name):
        return f"Hello, {name}"

greet = Greeter()
print(greet("Janette"))
```

Because of `__call__`, `greet("Janette")` works.

---

## 24. Simple Example Combining Class Features

```python
class Book:
    category = "Reading"

    def __init__(self, title, pages):
        self.title = title
        self.pages = pages

    def __str__(self):
        return f"{self.title} ({self.pages} pages)"

    def __len__(self):
        return self.pages

book = Book("Python Basics", 120)

print(book)       # Python Basics (120 pages)
print(len(book))  # 120
```

---

## 25. Common Beginner Mistakes

### Forgetting `self`
```python
class Dog:
    def bark():
        print("Woof")
```

This is wrong for an instance method.

Correct:
```python
class Dog:
    def bark(self):
        print("Woof")
```

### Using instance attributes without `self`
```python
class Dog:
    def __init__(self, name):
        name = name
```

This does not store the value in the object.

Correct:
```python
class Dog:
    def __init__(self, name):
        self.name = name
```

### Confusing inheritance and composition
Inheritance:
```python
class Dog(Animal):
    pass
```

Composition:
```python
class Car:
    def __init__(self):
        self.engine = Engine()
```

### Returning the wrong type in dunder methods
For example, `__len__` should return an integer.

Wrong:
```python
def __len__(self):
    return "five"
```

Correct:
```python
def __len__(self):
    return 5
```

---

## 26. Summary

- A **class** is a blueprint for creating objects
- Objects can have **attributes** and **methods**
- `__init__` initializes object data
- **Inheritance** lets one class reuse and extend another
- **Composition** means one object contains another object
- Inheritance is often an **is-a** relationship
- Composition is often a **has-a** relationship
- **Dunder methods** define built-in behavior for objects
- Common dunder methods include:
  - `__init__`
  - `__str__`
  - `__repr__`
  - `__len__`
  - `__add__`
  - `__eq__`
  - `__iter__`
  - `__call__`



  # Python: `dataclasses` and `attrs`

## 1. What Are `dataclasses` and `attrs`?

Both `dataclasses` and `attrs` help you write classes that mainly store data without having to write a lot of repetitive code.

They can automatically generate things like:

- `__init__`
- `__repr__`
- `__eq__`

This is useful for classes whose main purpose is to hold structured information.

---

## 2. `dataclasses`

`dataclasses` is part of the Python standard library.

It was introduced in Python 3.7.

To use it:

```python
from dataclasses import dataclass
```

### Basic example
```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int

person = Person("Janette", 24)
print(person)
```

Possible output:
```python
Person(name='Janette', age=24)
```

### What `@dataclass` generates automatically
By default, it generates:

- `__init__`
- `__repr__`
- `__eq__`

So this:

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
```

is similar to writing:

```python
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Person(name={self.name!r}, age={self.age!r})"

    def __eq__(self, other):
        return self.name == other.name and self.age == other.age
```

---

## 3. Type Annotations in `dataclasses`

Fields in a dataclass are usually declared with type annotations.

```python
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: float
    in_stock: bool
```

### Important
Type annotations help readability and tools like type checkers, but Python does not strictly enforce them by default.

This means this is still possible:

```python
product = Product("Phone", "cheap", "yes")
```

Even if the types are not correct.

---

## 4. Default Values in `dataclasses`

You can define default values.

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    active: bool = True
```

Usage:
```python
user1 = User("Janette")
user2 = User("Ana", False)

print(user1)
print(user2)
```

---

## 5. Field Order Rule

In dataclasses, fields without defaults must come before fields with defaults.

Correct:
```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    active: bool = True
```

Incorrect:
```python
from dataclasses import dataclass

# @dataclass
# class User:
#     active: bool = True
#     name: str
```

That would raise an error.

---

## 6. `field()`

For more control over dataclass fields, use `field()`.

```python
from dataclasses import dataclass, field

@dataclass
class Product:
    name: str
    tags: list[str] = field(default_factory=list)
```

### Why `default_factory`?
Because mutable defaults like lists should not be shared between instances.

Bad:
```python
from dataclasses import dataclass

# @dataclass
# class Product:
#     name: str
#     tags: list[str] = []
```

This is dangerous because all instances could share the same list.

Correct:
```python
from dataclasses import dataclass, field

@dataclass
class Product:
    name: str
    tags: list[str] = field(default_factory=list)
```

---

## 7. `__post_init__`

If you need extra logic after the generated `__init__`, use `__post_init__`.

```python
from dataclasses import dataclass

@dataclass
class Rectangle:
    width: float
    height: float
    area: float = 0

    def __post_init__(self):
        self.area = self.width * self.height

r = Rectangle(4, 5)
print(r.area)  # 20
```

### Common use cases
- derived values
- validation
- normalization

Example with validation:
```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int

    def __post_init__(self):
        if self.age < 0:
            raise ValueError("age cannot be negative")
```

---

## 8. Frozen Dataclasses

If you want an immutable dataclass, use `frozen=True`.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: int
    y: int

p = Point(1, 2)
print(p.x)

# p.x = 10  # Error
```

This is useful when the object should not change after creation.

---

## 9. Ordering in Dataclasses

You can ask dataclasses to generate comparison methods.

```python
from dataclasses import dataclass

@dataclass(order=True)
class Player:
    score: int
    name: str

p1 = Player(100, "Ana")
p2 = Player(200, "Luis")

print(p1 < p2)  # True
```

This generates methods like:
- `__lt__`
- `__le__`
- `__gt__`
- `__ge__`

---

## 10. Excluding Fields from `repr` or Comparison

You can customize field behavior with `field()`.

```python
from dataclasses import dataclass, field

@dataclass
class User:
    name: str
    password: str = field(repr=False)
```

Usage:
```python
user = User("Janette", "secret123")
print(user)
```

Output:
```python
User(name='Janette')
```

The password is hidden from `repr`.

Another example:
```python
from dataclasses import dataclass, field

@dataclass
class Item:
    id: int
    metadata: dict = field(compare=False)
```

Here, `metadata` is ignored in equality comparisons.

---

## 11. Utility Functions in `dataclasses`

### `asdict()`
Converts a dataclass instance into a dictionary.

```python
from dataclasses import dataclass, asdict

@dataclass
class Person:
    name: str
    age: int

person = Person("Janette", 24)
print(asdict(person))
```

Output:
```python
{'name': 'Janette', 'age': 24}
```

### `astuple()`
Converts a dataclass instance into a tuple.

```python
from dataclasses import dataclass, astuple

@dataclass
class Person:
    name: str
    age: int

person = Person("Janette", 24)
print(astuple(person))
```

Output:
```python
('Janette', 24)
```

---

## 12. Example: Dataclass for Configuration

```python
from dataclasses import dataclass, field

@dataclass
class AppConfig:
    host: str
    port: int = 8080
    debug: bool = False
    allowed_ips: list[str] = field(default_factory=list)

config = AppConfig("localhost", debug=True)
print(config)
```

This is a good example of a data-focused class.

---

## 13. What Is `attrs`?

`attrs` is a third-party library that solves a similar problem to `dataclasses`.

It existed before `dataclasses` and is still widely used.

You install it with:

```bash
pip install attrs
```

Basic import:
```python
import attrs
```

Or:
```python
from attrs import define, field
```

### Basic example
```python
from attrs import define

@define
class Person:
    name: str
    age: int

person = Person("Janette", 24)
print(person)
```

This looks very similar to a dataclass.

---

## 14. `attrs` vs `dataclasses`

They are similar, but `attrs` is often considered more flexible and feature-rich.

### `dataclasses`
- built into Python
- simple and standard
- great for many everyday cases

### `attrs`
- external library
- more features
- strong support for validators, converters, and advanced customization

A simple rule:
- use `dataclasses` when standard library is enough
- use `attrs` when you need more advanced behavior

---

## 15. Basic `attrs` Example

```python
from attrs import define

@define
class Product:
    name: str
    price: float

product = Product("Laptop", 999.99)
print(product)
```

Like `dataclasses`, `attrs` generates methods automatically.

---

## 16. Default Values in `attrs`

```python
from attrs import define

@define
class User:
    name: str
    active: bool = True
```

Usage:
```python
user = User("Janette")
print(user)
```

---

## 17. `field()` in `attrs`

`attrs` also uses `field()` for customization.

```python
from attrs import define, field

@define
class Product:
    name: str
    tags: list[str] = field(factory=list)
```

### Note
In `attrs`, the equivalent of `default_factory` is usually `factory`.

---

## 18. Validators in `attrs`

One major strength of `attrs` is validation.

```python
from attrs import define, field, validators

@define
class Person:
    name: str
    age: int = field(validator=validators.ge(0))
```

Usage:
```python
person = Person("Janette", 24)
# person = Person("Janette", -1)  # Error
```

This makes `attrs` very useful when data must follow strict rules.

Another example:
```python
from attrs import define, field, validators

@define
class User:
    name: str = field(validator=validators.instance_of(str))
    age: int = field(validator=validators.instance_of(int))
```

---

## 19. Converters in `attrs`

A converter automatically transforms input values.

```python
from attrs import define, field

@define
class User:
    name: str
    age: int = field(converter=int)

user = User("Janette", "24")
print(user.age)        # 24
print(type(user.age))  # <class 'int'>
```

This is another very useful `attrs` feature.

---

## 20. `attrs` Frozen Classes

Like dataclasses, `attrs` can also create immutable objects.

```python
from attrs import define

@define(frozen=True)
class Point:
    x: int
    y: int

p = Point(1, 2)
# p.x = 10  # Error
```

---

## 21. `attrs` and Post-Initialization Logic

`attrs` supports logic after initialization through `__attrs_post_init__`.

```python
from attrs import define, field

@define
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)

    def __attrs_post_init__(self):
        self.area = self.width * self.height

r = Rectangle(4, 5)
print(r.area)  # 20
```

This is similar to `__post_init__` in dataclasses.

---

## 22. Example: Validation + Conversion in `attrs`

```python
from attrs import define, field, validators

@define
class Employee:
    name: str = field(validator=validators.instance_of(str))
    age: int = field(converter=int, validator=validators.ge(18))
    salary: float = field(converter=float)

employee = Employee("Ana", "25", "1200.50")
print(employee)
```

This is a good example of where `attrs` can be more convenient than plain dataclasses.

---

## 23. Comparison: `dataclasses` vs `attrs`

### Dataclass example
```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
```

### Attrs example
```python
from attrs import define

@define
class User:
    name: str
    age: int
```

Very similar on the surface.

### Main differences
- `dataclasses` is built into Python
- `attrs` is a third-party package
- `attrs` has stronger built-in validation and conversion tools
- `dataclasses` is often enough for simpler cases
- `attrs` is often chosen for more complex data modeling

---

## 24. When to Use `dataclasses`

Use `dataclasses` when:
- you want a standard-library solution
- your class is mainly for storing data
- you do not need advanced validation/conversion built in
- you want simple, readable code

Example:
- app config
- DTO-like objects
- small models
- immutable value objects

---

## 25. When to Use `attrs`

Use `attrs` when:
- you want built-in validators
- you want converters
- you want more advanced customization
- your project already uses `attrs`

Example:
- strict data models
- validated objects
- configuration with automatic normalization
- larger codebases that need more control

---

## 26. Common Beginner Mistakes

### Using mutable defaults directly
Bad:
```python
from dataclasses import dataclass

# @dataclass
# class Item:
#     tags: list[str] = []
```

Better:
```python
from dataclasses import dataclass, field

@dataclass
class Item:
    tags: list[str] = field(default_factory=list)
```

And in `attrs`:
```python
from attrs import define, field

@define
class Item:
    tags: list[str] = field(factory=list)
```

### Expecting type annotations to be enforced automatically
This is not guaranteed by `dataclasses` alone.

```python
from dataclasses import dataclass

@dataclass
class User:
    age: int

user = User("not an int")  # Python allows this at runtime
```

### Forgetting that `attrs` is not in the standard library
You usually need to install it first:

```bash
pip install attrs
```

### Confusing `__post_init__` and `__attrs_post_init__`
- `dataclasses` uses `__post_init__`
- `attrs` uses `__attrs_post_init__`

---

## 27. Summary

- `dataclasses` and `attrs` reduce boilerplate for data-focused classes
- `dataclasses` is part of the Python standard library
- `attrs` is a third-party library with more advanced features
- Both can generate methods like:
  - `__init__`
  - `__repr__`
  - `__eq__`
- Use `field()` for field customization
- Use:
  - `default_factory` in `dataclasses`
  - `factory` in `attrs`
- `dataclasses` supports `__post_init__`
- `attrs` supports `__attrs_post_init__`
- `attrs` is especially strong for:
  - validators
  - converters
  - stricter data handling

  # Python: Pydantic for Validation and Serialization

## 1. What Is Pydantic?

**Pydantic** is a Python library for validating, parsing, and serializing data using type annotations.

It is especially useful when:
- data comes from APIs
- users send JSON or forms
- you need strict input validation
- you want clean Python objects from untrusted input

Pydantic is widely used with frameworks like **FastAPI**, but it is also useful in scripts, backends, ETL jobs, CLIs, and background workers.

---

## 2. Installation

```bash
pip install pydantic
```

---

## 3. Basic Idea

You define a model as a class that inherits from `BaseModel`.

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    active: bool = True
```

Now Pydantic will validate incoming data against those field types.

### Example
```python
user = User(id="123", name="Janette")
print(user)
print(user.id)
print(type(user.id))
```

Possible output:
```python
id=123 name='Janette' active=True
123
<class 'int'>
```

Pydantic converted `"123"` into `123`.

---

## 4. Why Pydantic Is Useful

Without Pydantic, you often have to:

- check types manually
- convert strings to numbers or dates
- validate required fields
- handle nested dictionaries by hand

With Pydantic, much of that logic is automatic and centralized in the model.

---

## 5. Basic Validation Example

```python
from pydantic import BaseModel, ValidationError

class Product(BaseModel):
    name: str
    price: float
    stock: int

try:
    product = Product(name="Keyboard", price="49.99", stock="10")
    print(product)
except ValidationError as e:
    print(e)
```

Pydantic will try to coerce valid values when possible.

---

## 6. Validation Errors

If validation fails, Pydantic raises `ValidationError`.

```python
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    id: int
    age: int

try:
    user = User(id="abc", age="hello")
except ValidationError as e:
    print(e)
```

This gives structured, readable errors explaining:
- which field failed
- why it failed
- what value caused the problem

You can also get structured error data:

```python
try:
    user = User(id="abc", age="hello")
except ValidationError as e:
    print(e.errors())
```

---

## 7. Default Values

Fields can have default values.

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    active: bool = True
    country: str = "MX"

user = User(name="Janette")
print(user)
```

---

## 8. Optional Fields

Use `| None` or `Optional[...]` for nullable values.

```python
from pydantic import BaseModel
from typing import Optional

class Profile(BaseModel):
    username: str
    bio: Optional[str] = None
```

Or with modern syntax:

```python
from pydantic import BaseModel

class Profile(BaseModel):
    username: str
    bio: str | None = None
```

---

## 9. Nested Models

Pydantic works very well with nested data.

```python
from pydantic import BaseModel

class Address(BaseModel):
    city: str
    zip_code: str

class User(BaseModel):
    name: str
    address: Address

data = {
    "name": "Janette",
    "address": {
        "city": "Mexico City",
        "zip_code": "01234"
    }
}

user = User(**data)
print(user)
print(user.address.city)
```

---

## 10. Lists, Dicts, and Other Typed Structures

Pydantic validates collections too.

```python
from pydantic import BaseModel

class Order(BaseModel):
    items: list[str]
    quantities: dict[str, int]

order = Order(
    items=["apple", "banana"],
    quantities={"apple": 2, "banana": 3}
)

print(order)
```

---

## 11. Using `model_validate()`

In Pydantic v2, one of the main validation methods is `model_validate()`.

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str

data = {"id": "123", "name": "Janette"}

user = User.model_validate(data)
print(user)
```

This is especially useful when validating data from dictionaries or external sources.

---

## 12. Using `model_validate_json()`

If your input is a JSON string, you can validate it directly.

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str

json_data = '{"id": "123", "name": "Janette"}'

user = User.model_validate_json(json_data)
print(user)
```

This is convenient when receiving raw JSON payloads.

---

## 13. Serialization with `model_dump()`

Once data is validated, you often want to convert it back into a Python dictionary.

Use `model_dump()`.

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str

user = User(id=1, name="Janette")
print(user.model_dump())
```

Output:
```python
{'id': 1, 'name': 'Janette'}
```

---

## 14. Serialization with `model_dump_json()`

If you want a JSON string:

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str

user = User(id=1, name="Janette")
print(user.model_dump_json())
```

Possible output:
```python
{"id":1,"name":"Janette"}
```

---

## 15. Validation vs Serialization

This distinction is important.

### Validation
Validation means:
- accept input
- check it
- convert it to expected Python types

### Serialization
Serialization means:
- take the validated model
- convert it into `dict`, JSON, or another export format

So:

- `model_validate()` → input to model
- `model_dump()` → model to dict
- `model_dump_json()` → model to JSON string

---

## 16. Field Constraints with `Field`

You can add metadata and constraints using `Field()`.

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)

product = Product(name="Mouse", price=25.5, stock=10)
print(product)
```

### Common constraints
- `gt` → greater than
- `ge` → greater than or equal
- `lt` → less than
- `le` → less than or equal
- `min_length`
- `max_length`

---

## 17. Aliases

Sometimes external data uses different field names than your Python code.

For that, use aliases.

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")

data = {"firstName": "Janette", "lastName": "Cerecedo"}

user = User.model_validate(data)
print(user)
print(user.first_name)
```

---

## 18. Validation Alias vs Serialization Alias

Pydantic v2 supports more precise alias control.

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    first_name: str = Field(
        validation_alias="firstName",
        serialization_alias="first_name"
    )
```

This is useful when:
- input format uses one naming convention
- output format uses another

---

## 19. Dumping with Aliases

If you want serialized output to use aliases:

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    first_name: str = Field(alias="firstName")

user = User(firstName="Janette")
print(user.model_dump(by_alias=True))
```

Output:
```python
{'firstName': 'Janette'}
```

---

## 20. Model Configuration with `ConfigDict`

In Pydantic v2, model configuration is usually done with `model_config`.

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str

user = User(name="   Janette   ")
print(user.name)
```

Possible output:
```python
Janette
```

---

## 21. Common Useful Config Options

### Strip whitespace
```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str
```

### Forbid extra fields
```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
```

Now this would fail:

```python
User(name="Janette", unknown_field=123)
```

### Strict mode
```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(strict=True)

    id: int
```

In strict mode, `"123"` would no longer be accepted for `int`.

---

## 22. Field Validators with `@field_validator`

Use `@field_validator` when you want custom validation for a field.

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("name cannot be blank")
        return value
```

### Example
```python
user = User(name="Janette")
```

This works, but:

```python
user = User(name="   ")
```

raises a validation error.

---

## 23. Validator Example: Normalize Input

Validators can also transform data.

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        return value.strip().title()

user = User(name="   janette cerecedo   ")
print(user.name)
```

Output:
```python
Janette Cerecedo
```

---

## 24. Model Validators

If validation depends on multiple fields, use `@model_validator`.

```python
from pydantic import BaseModel, model_validator

class Passwords(BaseModel):
    password1: str
    password2: str

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password1 != self.password2:
            raise ValueError("passwords do not match")
        return self
```

This is useful when rules involve the model as a whole.

---

## 25. Serializers with `@field_serializer`

Validation transforms input **into** the model.

Serialization transforms model data **out of** the model.

Use `@field_serializer` when you want custom output formatting.

```python
from datetime import datetime
from pydantic import BaseModel, field_serializer

class Event(BaseModel):
    created_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime):
        return value.strftime("%Y-%m-%d")
```

Now:

```python
event = Event(created_at="2024-01-10T12:30:00")
print(event.model_dump())
```

Possible output:
```python
{'created_at': '2024-01-10'}
```

---

## 26. Example: Full Validation + Serialization Flow

```python
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, field_serializer

class User(BaseModel):
    id: int
    name: str = Field(min_length=2)
    email: str
    created_at: datetime

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        return value.strip().title()

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime):
        return value.isoformat()

data = {
    "id": "123",
    "name": "   janette   ",
    "email": "janette@example.com",
    "created_at": "2024-01-10T12:30:00"
}

user = User.model_validate(data)

print(user)
print(user.model_dump())
print(user.model_dump_json())
```

This example shows:
- coercion of `"123"` to `123`
- custom validation for `name`
- custom serialization for `created_at`

---

## 27. `TypeAdapter`

You do not always need a full `BaseModel`.

If you want to validate a type directly, use `TypeAdapter`.

```python
from pydantic import TypeAdapter

adapter = TypeAdapter(list[int])

data = ["1", "2", "3"]
result = adapter.validate_python(data)

print(result)
print(type(result[0]))
```

Output:
```python
[1, 2, 3]
<class 'int'>
```

This is useful for:
- validating lists
- validating dicts
- validating `TypedDict`
- validating standalone types

---

## 28. Example with `TypedDict`

```python
from typing_extensions import TypedDict
from pydantic import TypeAdapter

class UserData(TypedDict):
    name: str
    age: int

adapter = TypeAdapter(UserData)

data = {"name": "Janette", "age": "24"}
validated = adapter.validate_python(data)

print(validated)
```

---

## 29. Strict vs Non-Strict Validation

By default, Pydantic is often flexible and tries to coerce values.

Example:
```python
from pydantic import BaseModel

class User(BaseModel):
    id: int

user = User(id="123")
print(user.id)  # 123
```

This is convenient, but sometimes you want exact types only.

For that, use strict mode:

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(strict=True)

    id: int
```

Now:
```python
User(id="123")
```

would fail.

---

## 30. Common Use Cases

Pydantic is commonly used for:

- API request validation
- API response serialization
- config parsing
- JSON payload validation
- ETL pipelines
- CLI input normalization
- message queue payload validation
- nested business objects

---

## 31. Common Beginner Mistakes

### Using old v1 methods in v2
In Pydantic v2, prefer:
- `model_validate()` instead of old parsing patterns
- `model_dump()` instead of `.dict()`
- `model_dump_json()` instead of `.json()`

### Expecting strict typing by default
Pydantic often coerces values unless you configure strict behavior.

### Confusing validation with serialization
- validation = input to model
- serialization = model to dict/JSON

### Forgetting `by_alias=True`
If you want aliases in output:
```python
model.model_dump(by_alias=True)
```

### Using validators when a field constraint is enough
Sometimes this:
```python
age: int = Field(ge=0)
```

is better than writing a custom validator.

---

## 32. Summary

- **Pydantic** validates and serializes data using Python type hints
- The main base class is `BaseModel`
- Use:
  - `model_validate()` for Python input
  - `model_validate_json()` for JSON strings
  - `model_dump()` for dictionaries
  - `model_dump_json()` for JSON output
- Use `Field(...)` for constraints and aliases
- Use `ConfigDict` for model settings
- Use `@field_validator` and `@model_validator` for custom validation
- Use `@field_serializer` for custom output formatting
- Use `TypeAdapter` when you want validation without creating a full model
- Pydantic is especially useful for APIs, config, and any external/untrusted data