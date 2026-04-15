# Python Fundamentals

## 1. Goal

This document gives a clear summary of these Python basics:

- syntax, indentation, variables, and scope
- basic types and collections (`list`, `dict`, `set`, `tuple`)
- control flow (`if`, `for`, `while`, `match`)
- errors and exceptions (`try` / `except`)
- exception control and handling

The purpose is to give you one practical overview of the foundations of everyday Python.

---

## 2. Syntax, Indentation, Variables, and Scope

### Python syntax
Python is designed to be readable and explicit.

Some key characteristics:
- blocks are defined by **indentation**
- statements are usually written one per line
- colons (`:`) introduce blocks such as `if`, `for`, `while`, `def`, and `class`

Example:

```python
age = 20

if age >= 18:
    print("Adult")
```

### Indentation
Indentation is not just style in Python.  
It is part of the syntax.

Example:

```python
if True:
    print("Inside block")
print("Outside block")
```

Bad indentation causes syntax errors or wrong logic.

### Variables
A variable is a name that refers to a value.

Example:

```python
name = "Janette"
age = 25
```

Python is dynamically typed, so you do not declare variable types explicitly before assigning values.

### Scope
Scope means where a variable can be accessed.

Main scopes:
- **local**: inside a function
- **global**: defined at module level
- **enclosing**: in nested functions
- **built-in**: names provided by Python itself

Example:

```python
x = 10  # global

def show():
    y = 5  # local
    print(x, y)
```

### Main idea
Python uses clear syntax and indentation to define structure, and variables follow scope rules that control where names are visible.

---

## 3. Basic Types and Collections

### Basic scalar types
Common built-in types include:

- `int` → integers
- `float` → decimal numbers
- `str` → text
- `bool` → `True` / `False`
- `NoneType` → `None`

Examples:

```python
age = 25
price = 19.99
name = "Janette"
is_active = True
value = None
```

---

## 4. `list`

A `list` is an ordered, mutable collection.

Example:

```python
numbers = [1, 2, 3]
numbers.append(4)
```

Useful when:
- order matters
- items may change
- duplicates are allowed

Main idea:
- ordered
- mutable
- allows duplicates

---

## 5. `tuple`

A `tuple` is an ordered, immutable collection.

Example:

```python
point = (10, 20)
```

Useful when:
- order matters
- values should not change
- you want a fixed grouped value

Main idea:
- ordered
- immutable
- allows duplicates

---

## 6. `dict`

A `dict` stores key-value pairs.

Example:

```python
user = {
    "name": "Janette",
    "age": 25
}
```

Useful when:
- you need named access to values
- data is naturally key-based
- mapping relationships matter

Main idea:
- key-value structure
- mutable
- keys are unique

---

## 7. `set`

A `set` is an unordered collection of unique values.

Example:

```python
tags = {"python", "fastapi", "testing"}
```

Useful when:
- uniqueness matters
- membership checks are frequent
- order is not important

Main idea:
- unordered
- mutable
- no duplicates

---

## 8. Quick collection comparison

### `list`
Use when:
- order matters
- you want to modify the collection
- duplicates are fine

### `tuple`
Use when:
- order matters
- values should stay fixed

### `dict`
Use when:
- data is key-value based

### `set`
Use when:
- uniqueness matters
- order is not important

---

## 9. Control Flow

Control flow decides how code runs depending on conditions or repetition.

Main structures:
- `if`
- `for`
- `while`
- `match`

---

## 10. `if`

`if` is used for conditional execution.

Example:

```python
age = 20

if age >= 18:
    print("Adult")
else:
    print("Minor")
```

You can also use `elif`:

```python
score = 85

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("C or lower")
```

### Main idea
Use `if` when behavior depends on conditions.

---

## 11. `for`

`for` is used for iteration.

Example:

```python
for number in [1, 2, 3]:
    print(number)
```

It is commonly used with:
- lists
- tuples
- strings
- dictionaries
- ranges

Example with `range`:

```python
for i in range(5):
    print(i)
```

### Main idea
Use `for` when iterating over items or a known sequence.

---

## 12. `while`

`while` repeats while a condition stays true.

Example:

```python
count = 0

while count < 3:
    print(count)
    count += 1
```

### Main idea
Use `while` when repetition depends on a condition rather than direct iteration over a collection.

---

## 13. `match` and pattern matching

Python has structural pattern matching through `match` / `case`.

Example:

```python
status = 404

match status:
    case 200:
        print("OK")
    case 404:
        print("Not Found")
    case _:
        print("Other")
```

This is sometimes similar to a `switch` statement in other languages, but Python’s `match` is more powerful.

It can also match structures:

```python
point = (0, 5)

match point:
    case (0, y):
        print(f"On Y axis: {y}")
    case (x, 0):
        print(f"On X axis: {x}")
    case _:
        print("Other point")
```

### Main idea
Use `match` when you want clearer branching over values or structured shapes.

---

## 14. Errors and Exceptions

### What an error is
An error means something went wrong during execution.

Examples:
- dividing by zero
- using an undefined variable
- accessing a missing key
- converting invalid text to a number

In Python, many runtime errors are represented as **exceptions**.

---

## 15. `try` / `except`

Use `try` / `except` to handle exceptions.

Example:

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
```

### Why useful
It allows the program to handle failure gracefully instead of crashing immediately.

---

## 16. Common exception handling structure

Example:

```python
try:
    value = int("123")
except ValueError:
    print("Invalid number")
else:
    print("Conversion worked")
finally:
    print("Finished")
```

### Meaning
- `try` → code that may fail
- `except` → what to do if an exception happens
- `else` → runs only if no exception happens
- `finally` → runs no matter what

---

## 17. Common built-in exceptions

Some important examples are:

- `ValueError`
- `TypeError`
- `KeyError`
- `IndexError`
- `ZeroDivisionError`
- `FileNotFoundError`

### Why this matters
Catching the right exception type is important for safe and precise error handling.

---

## 18. Exception control and handling

Exception handling is not only about catching errors.  
It is also about deciding:

- which errors should be handled
- which should be re-raised
- where the responsibility for handling belongs
- how to keep the program safe and understandable

### Good practice
Catch exceptions only where you can do something meaningful:
- recover
- retry
- log clearly
- translate to a better message
- clean up resources

### Bad practice
Do not blindly catch everything unless you have a strong reason.

Bad example:

```python
try:
    do_something()
except Exception:
    pass
```

This hides problems and makes debugging much harder.

---

## 19. Raising exceptions

You can raise your own exceptions with `raise`.

Example:

```python
age = -1

if age < 0:
    raise ValueError("Age cannot be negative")
```

### Why useful
This lets your code enforce rules explicitly.

---

## 20. Re-raising exceptions

Sometimes you catch an exception to add context, then raise it again.

Example:

```python
try:
    value = int(user_input)
except ValueError as exc:
    raise ValueError("Invalid age input") from exc
```

### Why useful
It preserves the original cause while improving the message or abstraction level.

---

## 21. Main principles for exception management

A good exception strategy usually means:

- catch specific exceptions when possible
- avoid swallowing errors silently
- raise clear exceptions when rules are violated
- handle exceptions at the right layer
- use `finally` or context managers for cleanup
- keep failure paths understandable

### Practical idea
Exception handling should make the program safer and clearer, not hide real problems.

---

## 22. How these topics connect

These topics work together in everyday Python:

- syntax and indentation define structure
- variables and scope define where data lives
- types and collections define how data is represented
- control flow defines how logic branches and repeats
- exceptions define how failure is handled safely

This is the foundation of most Python programs.

---

## 23. Final takeaway

If you only keep the essentials:

1. Python uses indentation as part of its syntax.
2. Variables hold values, and scope controls where they are visible.
3. `list`, `dict`, `set`, and `tuple` solve different collection needs.
4. `if`, `for`, `while`, and `match` control program flow.
5. `try` / `except` handles runtime problems safely.
6. Good exception management means catching the right errors in the right place.

---
