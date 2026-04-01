# Python: Syntax, Indentation, Variables, and Scope

## 1. Syntax in Python

Python syntax is designed to be simple and readable.

### Basic example
```python
name = "Janette"
age = 25

print(name)
print(age)
```

### Important syntax rules
- You do not need semicolons at the end of lines.
- You do not use `{}` to define blocks.
- Python uses indentation to group code.
- Variable names are case-sensitive.

```python
user = "A"
User = "B"

print(user)  # A
print(User)  # B
```

### Comments
```python
# This is a comment
print("Hello")
```

## 2. Indentation in Python

Indentation is not just style in Python. It is part of the language.

### Correct indentation
```python
if True:
    print("This is inside the if")
    print("This too")

print("This is outside the if")
```

### Incorrect indentation
```python
if True:
print("Hello")  # Error
```

That causes an `IndentationError` because Python expects the block to be indented.

### Standard convention
Use **4 spaces** per indentation level.

```python
def greet():
    print("Hello")
```

Do not mix tabs and spaces.

## 3. Variables in Python

A variable stores a value.

```python
name = "Janette"
age = 24
height = 1.65
is_student = True
```

Python is **dynamically typed**, so you do not need to declare the type explicitly.

```python
x = 10
x = "now I am a string"
```

### Variable naming rules
A variable name:
- can contain letters, numbers, and `_`
- cannot start with a number
- cannot use reserved words like `if`, `for`, `class`

### Valid examples
```python
user_name = "Ana"
age2 = 30
_total = 100
```

### Invalid examples
```python
# 2age = 30      # invalid
# class = "test" # invalid
```

### Good naming style
Python convention uses **snake_case**:

```python
first_name = "Janette"
total_price = 150
```

## 4. Scope in Python

Scope means **where a variable can be accessed**.

Python mainly works with these scopes:
- Local scope
- Enclosing scope
- Global scope
- Built-in scope

This is often called **LEGB**:
- Local
- Enclosing
- Global
- Built-in

### Local scope

A variable created inside a function usually only exists there.

```python
def greet():
    message = "Hello"
    print(message)

greet()
# print(message)  # Error
```

### Global scope

A variable created outside functions is global.

```python
name = "Janette"

def show_name():
    print(name)

show_name()
print(name)
```

### Modifying a global variable

If you want to change a global variable inside a function, use `global`.

```python
count = 0

def increase():
    global count
    count += 1

increase()
print(count)  # 1
```

Without `global`, Python treats it as a new local variable and raises an error if you try to modify it.

```python
count = 0

def increase():
    count += 1  # Error
```

### Enclosing scope

This happens with nested functions.

```python
def outer():
    message = "Hello"

    def inner():
        print(message)

    inner()

outer()
```

If you want to modify that enclosing variable, use `nonlocal`.

```python
def outer():
    count = 0

    def inner():
        nonlocal count
        count += 1
        print(count)

    inner()

outer()
```

## 5. Example Combining Everything

```python
x = "global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print(x)

    inner()
    print(x)

outer()
print(x)
```

Output:
```python
local
enclosing
global
```

This shows how Python looks for variables depending on scope.

## 6. Common Beginner Mistakes

### Wrong indentation
```python
if True:
    print("A")
      print("B")  # Error
```

### Using a variable before defining it
```python
print(name)  # Error
name = "Janette"
```

### Confusing local and global variables
```python
x = 5

def test():
    x = 10
    print(x)

test()
print(x)
```

Output:
```python
10
5
```

The `x` inside `test()` is local, so it does not change the global `x`.

## 7. Summary

- **Syntax**: Python is clean and readable.
- **Indentation**: defines code blocks, usually 4 spaces.
- **Variables**: store values, no type declaration required.
- **Scope**: determines where variables can be used.
- Python follows **LEGB** for variable lookup.


# Python: Basic Types and Collections

## 1. Basic Types in Python

Python has several built-in basic data types.

### Integer (`int`)
Used for whole numbers.

```python
age = 24
score = 100
temperature = -5
```

### Float (`float`)
Used for decimal numbers.

```python
price = 19.99
pi = 3.1416
discount = 0.25
```

### String (`str`)
Used for text.

```python
name = "Janette"
message = 'Hello, world'
```

### Boolean (`bool`)
Used for `True` or `False` values.

```python
is_active = True
is_admin = False
```

### None (`NoneType`)
Represents the absence of a value.

```python
result = None
```

## 2. Checking Types

You can check the type of a value with `type()`.

```python
print(type(10))         # <class 'int'>
print(type(3.14))       # <class 'float'>
print(type("hello"))    # <class 'str'>
print(type(True))       # <class 'bool'>
print(type(None))       # <class 'NoneType'>
```

## 3. Type Conversion

Python lets you convert between types.

```python
age = "24"
age_number = int(age)

price = 10
price_decimal = float(price)

number = 123
text = str(number)
```

Be careful: not every conversion is valid.

```python
# int("hello")  # Error
```

## 4. Collections in Python

Collections store multiple values. The main built-in collections are:

- `list`
- `tuple`
- `set`
- `dict`

---

## 5. List

A `list` is:
- ordered
- mutable
- allows duplicate values

### Creating a list
```python
fruits = ["apple", "banana", "orange"]
numbers = [1, 2, 3, 4]
mixed = ["Janette", 24, True]
```

### Accessing elements
```python
fruits = ["apple", "banana", "orange"]

print(fruits[0])   # apple
print(fruits[1])   # banana
print(fruits[-1])  # orange
```

### Modifying a list
```python
fruits = ["apple", "banana", "orange"]
fruits[1] = "grape"

print(fruits)
```

### Common list methods
```python
numbers = [1, 2, 3]

numbers.append(4)        # add one item
numbers.insert(1, 10)    # insert at position
numbers.remove(2)        # remove by value
last = numbers.pop()     # remove last item
numbers.sort()           # sort the list
```

### Example
```python
colors = ["red", "blue", "green"]
colors.append("yellow")

print(colors)
```

---

## 6. Tuple

A `tuple` is:
- ordered
- immutable
- allows duplicate values

### Creating a tuple
```python
coordinates = (10, 20)
colors = ("red", "blue", "red")
single_value = (5,)  # note the comma
```

### Accessing elements
```python
coordinates = (10, 20)

print(coordinates[0])  # 10
print(coordinates[1])  # 20
```

### Important
You cannot change a tuple after it is created.

```python
coordinates = (10, 20)

# coordinates[0] = 99  # Error
```

### When to use tuple
Use a tuple when the data should not change.

```python
rgb = (255, 100, 50)
```

---

## 7. Set

A `set` is:
- unordered
- mutable
- does not allow duplicate values

### Creating a set
```python
numbers = {1, 2, 3, 4}
letters = {"a", "b", "c"}
```

### Duplicate values are removed
```python
values = {1, 2, 2, 3, 3, 3}
print(values)  # {1, 2, 3}
```

### Common set methods
```python
numbers = {1, 2, 3}

numbers.add(4)
numbers.remove(2)
numbers.discard(10)   # does not fail if value is missing
```

### Set operations
```python
a = {1, 2, 3}
b = {3, 4, 5}

print(a | b)  # union
print(a & b)  # intersection
print(a - b)  # difference
```

### Important
Because sets are unordered, you cannot access items by index.

```python
# numbers[0]  # Error
```

---

## 8. Dictionary

A `dict` stores data as key-value pairs.

A dictionary is:
- ordered (in modern Python)
- mutable
- keys must be unique

### Creating a dictionary
```python
person = {
    "name": "Janette",
    "age": 24,
    "is_student": False
}
```

### Accessing values
```python
person = {"name": "Janette", "age": 24}

print(person["name"])      # Janette
print(person.get("age"))   # 24
```

### Modifying a dictionary
```python
person = {"name": "Janette", "age": 24}

person["age"] = 25
person["city"] = "Mexico City"

print(person)
```

### Common dictionary methods
```python
person = {"name": "Janette", "age": 24}

print(person.keys())
print(person.values())
print(person.items())

person.pop("age")
```

### Example
```python
student = {
    "name": "Ana",
    "grade": 9.5,
    "passed": True
}

print(student["grade"])
```

---

## 9. Comparison of Collections

### List
```python
data = [1, 2, 3]
```
- ordered
- mutable
- duplicates allowed

### Tuple
```python
data = (1, 2, 3)
```
- ordered
- immutable
- duplicates allowed

### Set
```python
data = {1, 2, 3}
```
- unordered
- mutable
- no duplicates

### Dict
```python
data = {"a": 1, "b": 2}
```
- key-value pairs
- mutable
- keys must be unique

---

## 10. Common Beginner Mistakes

### Forgetting that strings are text
```python
age = "24"
# print(age + 1)  # Error
```

### Trying to modify a tuple
```python
point = (10, 20)
# point[0] = 99  # Error
```

### Expecting order in a set
```python
numbers = {5, 1, 3}
# print(numbers[0])  # Error
```

### Using a missing key in a dictionary
```python
person = {"name": "Janette"}
# print(person["age"])  # Error
```

Safer option:
```python
print(person.get("age"))  # None
```

---

## 11. Summary

- **Basic types**: `int`, `float`, `str`, `bool`, `None`
- **List**: ordered, mutable, duplicates allowed
- **Tuple**: ordered, immutable, duplicates allowed
- **Set**: unordered, mutable, no duplicates
- **Dict**: key-value pairs, mutable, unique keys


# Python: Control Flow (`if`, `switch`, `for`, `while`) and Pattern Matching

## 1. Control Flow in Python

Control flow determines the order in which code runs.

Python uses control flow statements to:
- make decisions
- repeat actions
- handle different cases

The main control flow structures are:
- `if`
- `for`
- `while`
- `match` / `case` (pattern matching)

---

## 2. The `if` Statement

Use `if` to run code only when a condition is true.

### Basic example
```python
age = 20

if age >= 18:
    print("You are an adult")
```

### `if` and `else`
```python
age = 16

if age >= 18:
    print("You are an adult")
else:
    print("You are a minor")
```

### `if`, `elif`, and `else`
```python
score = 85

if score >= 90:
    print("Excellent")
elif score >= 70:
    print("Good")
else:
    print("Needs improvement")
```

### Comparison operators
```python
x == y   # equal
x != y   # different
x > y    # greater than
x < y    # less than
x >= y   # greater or equal
x <= y   # less or equal
```

### Logical operators
```python
and
or
not
```

### Example with logical operators
```python
age = 25
has_id = True

if age >= 18 and has_id:
    print("Access granted")
```

---

## 3. Nested `if`

You can place one `if` inside another.

```python
age = 20
has_id = True

if age >= 18:
    if has_id:
        print("You may enter")
```

Use nested conditions only when they improve clarity.

---

## 4. The `for` Loop

Use `for` to iterate over a sequence.

### Example with a list
```python
fruits = ["apple", "banana", "orange"]

for fruit in fruits:
    print(fruit)
```

### Example with a string
```python
for letter in "Python":
    print(letter)
```

### Using `range()`
`range()` is commonly used with `for`.

```python
for i in range(5):
    print(i)
```

Output:
```python
0
1
2
3
4
```

### More `range()` examples
```python
for i in range(1, 6):
    print(i)
```

```python
for i in range(0, 10, 2):
    print(i)
```

### Looping through a dictionary
```python
person = {"name": "Janette", "age": 24}

for key in person:
    print(key, person[key])
```

### Using `enumerate()`
```python
colors = ["red", "blue", "green"]

for index, color in enumerate(colors):
    print(index, color)
```

---

## 5. The `while` Loop

Use `while` when code should repeat as long as a condition is true.

### Basic example
```python
count = 1

while count <= 5:
    print(count)
    count += 1
```

### Example with user-controlled logic
```python
number = 3

while number > 0:
    print(number)
    number -= 1

print("Finished")
```

### Important
Be careful with infinite loops.

```python
# while True:
#     print("This runs forever")
```

If the condition never becomes false, the loop never ends.

---

## 6. `break`, `continue`, and `pass`

These statements are often used inside loops.

### `break`
Stops the loop immediately.

```python
for number in range(10):
    if number == 5:
        break
    print(number)
```

### `continue`
Skips the current iteration and moves to the next one.

```python
for number in range(5):
    if number == 2:
        continue
    print(number)
```

### `pass`
Does nothing. It is a placeholder.

```python
for number in range(3):
    pass
```

---

## 7. Does Python Have `switch`?

Python does **not** have a classic `switch` statement like Java, JavaScript, or C.

Instead, Python traditionally uses:
- `if` / `elif` / `else`

And in modern Python (3.10+), it also has:
- `match` / `case`

So, when people say **switch in Python**, they usually mean either:
- an `if-elif-else` chain
- `match-case`

### `if-elif-else` as a switch-style structure
```python
day = "monday"

if day == "monday":
    print("Start of the week")
elif day == "friday":
    print("Almost weekend")
else:
    print("Regular day")
```

---

## 8. Pattern Matching with `match` / `case`

Pattern matching was introduced in Python 3.10.

It allows you to compare a value or structure against different patterns.

### Basic syntax
```python
day = "monday"

match day:
    case "monday":
        print("Start of the week")
    case "friday":
        print("Almost weekend")
    case _:
        print("Regular day")
```

### Important
The underscore `_` works like a default case.

---

## 9. Simple Pattern Matching Examples

### Matching numbers
```python
status = 404

match status:
    case 200:
        print("OK")
    case 404:
        print("Not found")
    case 500:
        print("Server error")
    case _:
        print("Unknown status")
```

### Matching strings
```python
command = "save"

match command:
    case "open":
        print("Opening file")
    case "save":
        print("Saving file")
    case "exit":
        print("Closing program")
    case _:
        print("Invalid command")
```

---

## 10. Matching Multiple Values

You can match several alternatives in one case.

```python
day = "saturday"

match day:
    case "saturday" | "sunday":
        print("Weekend")
    case "monday":
        print("Start of week")
    case _:
        print("Weekday")
```

---

## 11. Pattern Matching with Variables

You can capture values from a pattern.

```python
point = (3, 7)

match point:
    case (x, y):
        print(f"x = {x}, y = {y}")
```

In this example, `x` and `y` receive the values from the tuple.

---

## 12. Matching Specific Structures

Pattern matching becomes more powerful with lists, tuples, and other structures.

### Matching tuples
```python
point = (0, 5)

match point:
    case (0, y):
        print(f"On the Y axis at {y}")
    case (x, 0):
        print(f"On the X axis at {x}")
    case (x, y):
        print(f"Point at ({x}, {y})")
```

### Matching lists
```python
data = [1, 2, 3]

match data:
    case [1, 2, 3]:
        print("Exact match")
    case [1, *rest]:
        print("Starts with 1", rest)
    case _:
        print("No match")
```

---

## 13. Guards in Pattern Matching

A guard adds an extra condition to a case.

```python
number = 10

match number:
    case x if x > 0:
        print("Positive number")
    case x if x < 0:
        print("Negative number")
    case _:
        print("Zero")
```

This makes pattern matching more flexible.

---

## 14. `for` vs `while`

### Use `for` when:
- you iterate over a sequence
- you know the collection or range

```python
for i in range(5):
    print(i)
```

### Use `while` when:
- repetition depends on a condition
- you do not know in advance how many times it will run

```python
count = 0

while count < 5:
    print(count)
    count += 1
```

---

## 15. Common Beginner Mistakes

### Forgetting indentation
```python
if True:
print("Hello")  # Error
```

### Infinite `while` loop
```python
count = 0

while count < 5:
    print(count)
# missing count += 1
```

### Using `=` instead of `==`
```python
# if x = 5:   # Error
if x == 5:
    print("Correct")
```

### Expecting classic `switch`
Python does not have:
```python
# switch (value) { ... }   # Not valid Python
```

Use `if-elif-else` or `match-case` instead.

### Using `match` in old Python versions
`match` / `case` only works in **Python 3.10 or newer**.

---

## 16. Summary

- **`if`** is used for decisions
- **`for`** is used to iterate over sequences
- **`while`** is used to repeat while a condition is true
- Python has **no classic `switch`**
- Use **`if-elif-else`** or **`match-case`**
- **Pattern matching** with `match` is available in Python 3.10+


# Python: Errors and Exceptions (`try-except`)

## 1. Errors in Python

An error happens when Python finds a problem while running or parsing code.

There are two broad categories:

- **Syntax errors**
- **Exceptions**

---

## 2. Syntax Errors

A syntax error happens when the code does not follow Python's rules.

### Example
```python
if True
    print("Hello")
```

This causes an error because the colon `:` is missing.

Python stops before running the program.

---

## 3. Exceptions

An exception happens while the program is running.

The code is valid Python, but something goes wrong during execution.

### Example
```python
print(10 / 0)
```

This raises:
```python
ZeroDivisionError
```

Another example:
```python
numbers = [1, 2, 3]
print(numbers[5])
```

This raises:
```python
IndexError
```

---

## 4. Common Exceptions in Python

### `ZeroDivisionError`
```python
print(10 / 0)
```

### `TypeError`
```python
print("Age: " + 24)
```

### `ValueError`
```python
number = int("hello")
```

### `IndexError`
```python
items = [1, 2, 3]
print(items[10])
```

### `KeyError`
```python
person = {"name": "Janette"}
print(person["age"])
```

### `NameError`
```python
print(username)
```

### `AttributeError`
```python
number = 10
number.append(5)
```

### `FileNotFoundError`
```python
with open("missing_file.txt") as file:
    print(file.read())
```

---

## 5. Handling Exceptions with `try-except`

You can prevent the program from crashing by handling exceptions.

### Basic syntax
```python
try:
    # code that may fail
except:
    # code that runs if an error happens
```

### Example
```python
try:
    result = 10 / 0
except:
    print("An error occurred")
```

Instead of stopping the program, Python runs the `except` block.

---

## 6. Catching a Specific Exception

It is better to catch specific exceptions instead of using a generic `except`.

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("You cannot divide by zero")
```

### Another example
```python
try:
    number = int("hello")
except ValueError:
    print("That is not a valid number")
```

---

## 7. Catching Multiple Exceptions

You can handle different exceptions in different ways.

```python
try:
    value = int(input("Enter a number: "))
    print(10 / value)
except ValueError:
    print("You must enter a valid integer")
except ZeroDivisionError:
    print("You cannot divide by zero")
```

---

## 8. Catching Multiple Exceptions in One Line

You can also group exceptions.

```python
try:
    value = int("hello")
except (ValueError, TypeError):
    print("Conversion failed")
```

---

## 9. Using `as` to Access the Error Message

You can store the exception object in a variable.

```python
try:
    number = int("hello")
except ValueError as error:
    print("Error:", error)
```

This is useful when you want more information about what happened.

---

## 10. The `else` Block

The `else` block runs only if no exception happens.

```python
try:
    result = 10 / 2
except ZeroDivisionError:
    print("Division by zero")
else:
    print("Result:", result)
```

### Why use `else`?
It helps separate:
- code that may fail
- code that should run only if everything worked

---

## 11. The `finally` Block

The `finally` block always runs, whether there is an exception or not.

```python
try:
    file = open("example.txt")
    content = file.read()
except FileNotFoundError:
    print("File not found")
finally:
    print("This always runs")
```

### Common use
`finally` is often used for cleanup:
- closing files
- releasing resources
- disconnecting from services

---

## 12. Full Example with `try`, `except`, `else`, and `finally`

```python
try:
    number = int(input("Enter a number: "))
    result = 10 / number
except ValueError:
    print("Invalid number")
except ZeroDivisionError:
    print("Cannot divide by zero")
else:
    print("Result:", result)
finally:
    print("Execution finished")
```

---

## 13. Raising Exceptions with `raise`

You can create your own exception intentionally using `raise`.

```python
age = -5

if age < 0:
    raise ValueError("Age cannot be negative")
```

This is useful when you want to enforce rules in your program.

---

## 14. Re-raising an Exception

Sometimes you catch an exception, do something, and then raise it again.

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Logging the error")
    raise
```

This keeps the original exception after handling part of it.

---

## 15. Creating Custom Exceptions

You can define your own exception classes.

```python
class InvalidAgeError(Exception):
    pass

age = -1

if age < 0:
    raise InvalidAgeError("Age must be 0 or more")
```

This is useful in larger applications when built-in exceptions are not specific enough.

---

## 16. Best Practices

### Catch specific exceptions
Good:
```python
try:
    value = int("hello")
except ValueError:
    print("Invalid value")
```

Less good:
```python
try:
    value = int("hello")
except:
    print("Something went wrong")
```

### Do not hide errors unnecessarily
A broad `except` can make debugging harder.

### Keep `try` blocks small
Put only the code that may fail inside `try`.

Good:
```python
try:
    number = int(user_input)
except ValueError:
    print("Invalid input")
```

Less good:
```python
try:
    number = int(user_input)
    print("Number entered")
    total = 100 / number
    print("Done")
except ValueError:
    print("Invalid input")
```

### Use `finally` for cleanup
```python
file = None

try:
    file = open("data.txt")
    print(file.read())
except FileNotFoundError:
    print("Missing file")
finally:
    if file:
        file.close()
```

---

## 17. Common Beginner Mistakes

### Catching everything with bare `except`
```python
try:
    x = 10 / 0
except:
    print("Error")
```

This works, but it is usually too broad.

### Catching the wrong exception
```python
try:
    number = int("hello")
except ZeroDivisionError:
    print("Wrong exception type")
```

This will not handle the real error.

### Forgetting that `finally` always runs
```python
try:
    print("Hello")
finally:
    print("Always runs")
```

### Using exceptions instead of normal logic
Exceptions should handle unexpected problems, not replace normal checks in simple cases.

Good:
```python
if age >= 18:
    print("Adult")
else:
    print("Minor")
```

Not ideal:
```python
try:
    if age < 18:
        raise ValueError("Minor")
except ValueError:
    print("Minor")
```

---

## 18. Summary

- **Syntax errors** happen before the program runs
- **Exceptions** happen during execution
- Use **`try-except`** to handle runtime errors
- Use **specific exceptions** when possible
- **`else`** runs if no exception occurs
- **`finally`** always runs
- Use **`raise`** to create exceptions intentionally
- You can define **custom exceptions** for your own programs
