# Python Functions and Core Idioms

## 1. Goal

This document gives a clear summary of these Python topics:

- functions, positional/named arguments, `*args` / `**kwargs`
- lambdas, closures, and decorators
- iterators, generators, and comprehensions
- context managers (`with`)

The purpose is to connect these topics into one practical overview of how Python structures behavior and reusable logic.

---

## 2. Functions, Positional/Named Arguments, `*args`, and `**kwargs`

### What a function is
A function is a reusable block of code that performs a task.

Example:

```python
def greet(name):
    return f"Hello, {name}"
```

Functions help make code:
- reusable
- clearer
- easier to test
- easier to organize

### Positional arguments
A positional argument is matched by its position.

Example:

```python
def add(a, b):
    return a + b

result = add(2, 3)
```

Here:
- `2` goes to `a`
- `3` goes to `b`

### Named arguments
A named argument is passed using the parameter name.

Example:

```python
result = add(a=2, b=3)
```

This can make code more explicit and readable.

### Mixing positional and named arguments
You can mix them, but positional arguments must come first.

Example:

```python
def describe(name, age):
    return f"{name} is {age} years old"

text = describe("Janette", age=25)
```

### Default arguments
Functions can define default values.

Example:

```python
def greet(name, prefix="Hello"):
    return f"{prefix}, {name}"
```

If `prefix` is not provided, `"Hello"` is used.

### `*args`
`*args` collects extra positional arguments into a tuple.

Example:

```python
def total(*args):
    return sum(args)
```

Usage:

```python
total(1, 2, 3, 4)
```

### `**kwargs`
`**kwargs` collects extra named arguments into a dictionary.

Example:

```python
def show_user(**kwargs):
    return kwargs
```

Usage:

```python
show_user(name="Janette", age=25)
```

### Main idea
Functions define reusable behavior, and Python provides flexible argument passing with positional, named, default, `*args`, and `**kwargs` patterns.

---

## 3. Lambdas, Closures, and Decorators

### Lambdas
A lambda is a small anonymous function.

Example:

```python
square = lambda x: x * x
```

This is similar to:

```python
def square(x):
    return x * x
```

### When lambdas are useful
Lambdas are often useful for:
- short inline operations
- sorting keys
- simple mapping/filtering logic

Example:

```python
items = [("a", 3), ("b", 1), ("c", 2)]
items.sort(key=lambda item: item[1])
```

### Practical warning
Lambdas are best when they stay small and simple.  
If the logic becomes complex, a regular function is usually clearer.

### Closures
A closure happens when an inner function remembers values from an outer scope even after the outer function has finished.

Example:

```python
def make_multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply
```

Usage:

```python
double = make_multiplier(2)
result = double(10)
```

Here, `multiply()` remembers `factor`.

### Why closures matter
Closures are useful for:
- creating configurable functions
- encapsulating state
- building decorators
- function factories

### Decorators
A decorator wraps a function and adds behavior around it.

Example:

```python
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

Usage:

```python
@log_calls
def greet(name):
    return f"Hello, {name}"
```

This is equivalent to:

```python
greet = log_calls(greet)
```

### Why decorators are useful
Decorators are useful for reusable cross-cutting behavior such as:
- logging
- timing
- retries
- authentication
- validation
- caching

### Main idea
- lambdas are small anonymous functions
- closures let functions remember outer values
- decorators wrap functions to extend behavior cleanly

---

## 4. Iterators, Generators, and Comprehensions

### Iterators
An iterator is an object that produces values one at a time.

It implements the iteration protocol, which conceptually means:
- it knows how to return the next item
- it raises `StopIteration` when finished

Example:

```python
numbers = iter([1, 2, 3])
print(next(numbers))
print(next(numbers))
```

### Why iterators matter
Iterators allow Python to process data step by step instead of loading everything at once.

You use iterators all the time in:
- `for` loops
- file reading
- generators
- many built-in tools

### Generators
A generator is a simple way to create an iterator using `yield`.

Example:

```python
def count_up_to(n):
    count = 1
    while count <= n:
        yield count
        count += 1
```

Usage:

```python
for value in count_up_to(3):
    print(value)
```

### Why generators are useful
Generators are useful because they:
- produce values lazily
- use less memory for large sequences
- express streaming or step-by-step computation naturally

### Generator expressions
Python also supports generator expressions.

Example:

```python
squares = (x * x for x in range(5))
```

This is lazy, unlike a list comprehension.

### Comprehensions
Comprehensions provide compact ways to build collections.

#### List comprehension

```python
squares = [x * x for x in range(5)]
```

#### Dictionary comprehension

```python
mapping = {x: x * x for x in range(5)}
```

#### Set comprehension

```python
unique_lengths = {len(word) for word in ["hi", "hello", "hey"]}
```

### Why comprehensions are useful
They are useful when:
- the transformation is simple
- the result is clearer than a longer loop
- you want expressive collection building

### Practical warning
Do not make comprehensions overly complex.  
If the logic gets too dense, a normal loop is usually easier to read.

### Main idea
- iterators produce values one by one
- generators are a concise lazy iterator pattern
- comprehensions are compact ways to build collections

---

## 5. Context Managers (`with`)

### What a context manager is
A context manager controls setup and cleanup around a block of code.

It is usually used with `with`.

Example:

```python
with open("file.txt", "r") as f:
    content = f.read()
```

### Why it is useful
A context manager helps guarantee cleanup, even if an error happens.

Common use cases:
- files
- database sessions
- locks
- temporary resources
- managed setup/teardown scopes

### Main idea of `with`
The `with` block means:
- set up resource
- run block
- clean up resource automatically

### Custom context manager
A class-based context manager uses:
- `__enter__`
- `__exit__`

Example:

```python
class DemoContext:
    def __enter__(self):
        print("enter")
        return self

    def __exit__(self, exc_type, exc, tb):
        print("exit")
```

Usage:

```python
with DemoContext():
    print("inside")
```

### `contextlib.contextmanager`
Python also provides a simpler generator-based way to create context managers.

Example:

```python
from contextlib import contextmanager

@contextmanager
def demo():
    print("enter")
    try:
        yield
    finally:
        print("exit")
```

### Why context managers matter
They make resource handling:
- safer
- cleaner
- more explicit
- less error-prone

### Main idea
Use `with` when a block of code needs controlled setup and guaranteed cleanup.

---

## 6. How These Topics Connect

These topics work together in everyday Python design:

- **functions** define reusable behavior
- **lambdas** provide compact inline behavior
- **closures** capture state in functions
- **decorators** wrap and extend behavior
- **iterators and generators** make data flow lazy and efficient
- **comprehensions** build collections concisely
- **context managers** manage resource lifecycles safely

Together, they form a large part of Python’s expressive and idiomatic style.

---

## 7. Final Takeaway

If you only keep the essentials:

1. Functions are the basic unit of reusable behavior in Python.
2. Positional, named, `*args`, and `**kwargs` make function calls flexible.
3. Lambdas are small inline functions, closures capture outer state, and decorators wrap behavior.
4. Iterators and generators produce values one at a time, often lazily.
5. Comprehensions provide compact collection-building syntax.
6. Context managers and `with` handle setup and cleanup safely and clearly.

---
