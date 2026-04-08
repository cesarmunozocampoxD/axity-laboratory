# Python: Functions, Positional/Keyword Arguments, `*args`, and `**kwargs`

## 1. Functions in Python

A **function** is a reusable block of code that performs a task.

### Basic syntax
```python
def greet():
    print("Hello")
```

To run it:
```python
greet()
```

### Function with a return value
```python
def add():
    return 2 + 3

result = add()
print(result)  # 5
```

`return` sends a value back to the place where the function was called.

---

## 2. Parameters and Arguments

A **parameter** is the variable inside the function definition.

An **argument** is the actual value you pass when calling the function.

```python
def greet(name):   # name = parameter
    print("Hello,", name)

greet("Janette")   # "Janette" = argument
```

---

## 3. Positional Arguments

These depend on the **order** in which values are passed.

```python
def introduce(name, age):
    print(name, age)

introduce("Janette", 24)
```

Here:
- `"Janette"` goes to `name`
- `24` goes to `age`

If you change the order, the meaning changes.

```python
introduce(24, "Janette")  # incorrect meaning
```

---

## 4. Keyword Arguments

These are passed using the parameter name, so order does not matter.

```python
def introduce(name, age):
    print(name, age)

introduce(age=24, name="Janette")
```

This is often clearer, especially when a function has many parameters.

---

## 5. Mixing Positional and Keyword Arguments

You can mix them, but positional arguments must come first.

Correct:
```python
def introduce(name, age, city):
    print(name, age, city)

introduce("Janette", age=24, city="Mexico City")
```

Incorrect:
```python
# introduce(name="Janette", 24, city="Mexico City")
```

---

## 6. Default Arguments

You can give a parameter a default value.

```python
def greet(name="Guest"):
    print("Hello,", name)

greet()          # Hello, Guest
greet("Janette") # Hello, Janette
```

This makes the argument optional.

---

## 7. `*args`

`*args` lets a function receive a variable number of **positional arguments**.

```python
def add_all(*args):
    print(args)

add_all(1, 2, 3)
```

Output:
```python
(1, 2, 3)
```

Inside the function, `args` is a **tuple**.

### Example
```python
def add_all(*args):
    total = 0
    for number in args:
        total += number
    return total

print(add_all(1, 2, 3))      # 6
print(add_all(10, 20, 30))   # 60
```

Use `*args` when you do not know in advance how many positional arguments will be passed.

---

## 8. `**kwargs`

`**kwargs` lets a function receive a variable number of **keyword arguments**.

```python
def show_info(**kwargs):
    print(kwargs)

show_info(name="Janette", age=24)
```

Output:
```python
{'name': 'Janette', 'age': 24}
```

Inside the function, `kwargs` is a **dictionary**.

### Example
```python
def show_info(**kwargs):
    for key, value in kwargs.items():
        print(key, "=", value)

show_info(name="Janette", age=24, city="Mexico City")
```

Use `**kwargs` when you do not know in advance which named arguments will be sent.

---

## 9. Using Normal Parameters with `*args` and `**kwargs`

You can combine them in one function.

```python
def demo(a, b, *args, **kwargs):
    print("a =", a)
    print("b =", b)
    print("args =", args)
    print("kwargs =", kwargs)

demo(1, 2, 3, 4, name="Janette", age=24)
```

Output:
```python
a = 1
b = 2
args = (3, 4)
kwargs = {'name': 'Janette', 'age': 24}
```

---

## 10. Order of Parameters

The usual order is:

```python
def func(positional, default_value=10, *args, **kwargs):
    pass
```

Python expects parameters in a valid order. `**kwargs` usually goes last.

---

## 11. Unpacking with `*` and `**`

You can also use `*` and `**` when calling functions.

### Unpacking a list or tuple with `*`
```python
def add(a, b):
    print(a + b)

numbers = [3, 5]
add(*numbers)
```

This is the same as:
```python
add(3, 5)
```

### Unpacking a dictionary with `**`
```python
def introduce(name, age):
    print(name, age)

data = {"name": "Janette", "age": 24}
introduce(**data)
```

This is the same as:
```python
introduce(name="Janette", age=24)
```

---

## 12. Common Beginner Mistakes

### Forgetting `return`
```python
def add(a, b):
    a + b

result = add(2, 3)
print(result)  # None
```

Because the function did not return anything.

Correct:
```python
def add(a, b):
    return a + b
```

### Confusing `print()` with `return`
```python
def add(a, b):
    print(a + b)
```

This prints the result, but does not return it.

### Using `*args` like a list
`args` is a tuple, not a list.

```python
def test(*args):
    print(type(args))  # tuple
```

### Using `**kwargs` like a list
`kwargs` is a dictionary.

```python
def test(**kwargs):
    print(type(kwargs))  # dict
```

---

## 13. Summary

- A **function** groups reusable code.
- **Positional arguments** depend on order.
- **Keyword arguments** depend on parameter names.
- **Default arguments** make parameters optional.
- `*args` collects extra positional arguments into a tuple.
- `**kwargs` collects extra keyword arguments into a dictionary.
- `return` sends a value back from the function.
 


 # Python: Lambdas, Closures, and Decorators

## 1. Lambda Functions

A **lambda** is a small anonymous function.

It is useful when you need a simple function for a short time and do not want to define it with `def`.

### Basic syntax
```python
lambda arguments: expression
```

### Example
```python
add = lambda a, b: a + b

print(add(2, 3))  # 5
```

This is similar to:

```python
def add(a, b):
    return a + b
```

### Important
A lambda can only contain **one expression**, not multiple statements.

Valid:
```python
square = lambda x: x * x
```

Not valid:
```python
# lambda x:
#     y = x * 2
#     return y
```

---

## 2. Common Uses of Lambdas

Lambdas are often used with functions like:
- `map()`
- `filter()`
- `sorted()`

### With `map()`
```python
numbers = [1, 2, 3, 4]
squared = list(map(lambda x: x * x, numbers))

print(squared)  # [1, 4, 9, 16]
```

### With `filter()`
```python
numbers = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, numbers))

print(evens)  # [2, 4, 6]
```

### With `sorted()`
```python
students = [
    {"name": "Ana", "grade": 90},
    {"name": "Luis", "grade": 85},
    {"name": "Mia", "grade": 95}
]

sorted_students = sorted(students, key=lambda student: student["grade"])
print(sorted_students)
```

---

## 3. When to Use Lambdas

Use lambdas when:
- the function is short
- the logic is simple
- the function is only needed once

Do not use lambdas when:
- the logic is complex
- readability becomes worse

Less readable:
```python
result = lambda x: x ** 2 + 10 if x > 0 else x - 10
```

In those cases, `def` is usually better.

---

## 4. Closures

A **closure** is a function that remembers values from the scope where it was created, even after that outer function has finished.

This happens when:
- one function is defined inside another
- the inner function uses variables from the outer function
- the inner function is returned or kept alive somehow

### Basic example
```python
def outer():
    message = "Hello"

    def inner():
        print(message)

    return inner

my_function = outer()
my_function()  # Hello
```

### Why is this a closure?
Even though `outer()` already finished, `inner()` still remembers the value of `message`.

---

## 5. Closure Example with Parameters

```python
def make_multiplier(n):
    def multiplier(x):
        return x * n
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15
```

Here:
- `double` remembers `n = 2`
- `triple` remembers `n = 3`

This is one of the most common examples of closures.

---

## 6. Why Closures Are Useful

Closures are useful when you want:
- functions with remembered configuration
- private state without using a class
- function factories

### Example: counter
```python
def make_counter():
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count

    return counter

c = make_counter()

print(c())  # 1
print(c())  # 2
print(c())  # 3
```

The inner function keeps access to `count`.

### `nonlocal`
`nonlocal` is used when you want to modify a variable from the enclosing scope.

Without `nonlocal`, Python would treat `count` as a new local variable inside `counter()`.

---

## 7. Decorators

A **decorator** is a function that takes another function and adds or changes its behavior.

In Python, functions are first-class objects, which means:
- you can pass them as arguments
- you can return them from other functions
- you can store them in variables

This makes decorators possible.

---

## 8. Basic Decorator Structure

```python
def decorator(func):
    def wrapper():
        print("Before the function")
        func()
        print("After the function")
    return wrapper
```

### Using it manually
```python
def say_hello():
    print("Hello")

say_hello = decorator(say_hello)
say_hello()
```

Output:
```python
Before the function
Hello
After the function
```

---

## 9. Decorator Syntax with `@`

Python provides a cleaner way to apply decorators.

```python
def decorator(func):
    def wrapper():
        print("Before the function")
        func()
        print("After the function")
    return wrapper

@decorator
def say_hello():
    print("Hello")

say_hello()
```

This is equivalent to:

```python
say_hello = decorator(say_hello)
```

---

## 10. Decorators with Arguments

If the decorated function receives arguments, the wrapper must also receive them.

```python
def decorator(func):
    def wrapper(name):
        print("Before the function")
        func(name)
        print("After the function")
    return wrapper

@decorator
def greet(name):
    print(f"Hello, {name}")

greet("Janette")
```

---

## 11. Using `*args` and `**kwargs` in Decorators

A more flexible decorator uses `*args` and `**kwargs` so it can work with many functions.

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        print("Before the function")
        result = func(*args, **kwargs)
        print("After the function")
        return result
    return wrapper

@decorator
def add(a, b):
    return a + b

print(add(2, 3))
```

This is the most common structure for decorators.

---

## 12. Realistic Decorator Example: Logging

```python
def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}...")
        result = func(*args, **kwargs)
        print(f"{func.__name__} finished")
        return result
    return wrapper

@log_call
def multiply(a, b):
    return a * b

print(multiply(4, 5))
```

---

## 13. Realistic Decorator Example: Access Control

```python
def require_admin(func):
    def wrapper(user_role):
        if user_role != "admin":
            print("Access denied")
            return
        return func(user_role)
    return wrapper

@require_admin
def open_panel(user_role):
    print("Welcome to the admin panel")

open_panel("guest")
open_panel("admin")
```

---

## 14. Preserving Metadata with `functools.wraps`

A decorator can hide the original function's metadata, such as its name.

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

Problem:
```python
@decorator
def greet():
    print("Hello")

print(greet.__name__)  # wrapper
```

To preserve metadata, use `functools.wraps`.

```python
from functools import wraps

def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorator
def greet():
    print("Hello")

print(greet.__name__)  # greet
```

This is considered best practice in real decorators.

---

## 15. Decorator with Parameters

A decorator can also receive its own arguments.

This requires one more level of nesting.

```python
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def say_hi():
    print("Hi")

say_hi()
```

Output:
```python
Hi
Hi
Hi
```

---

## 16. Lambdas vs Closures vs Decorators

### Lambda
A short anonymous function.

```python
square = lambda x: x * x
```

### Closure
A function that remembers variables from its enclosing scope.

```python
def outer(x):
    def inner():
        return x
    return inner
```

### Decorator
A function that wraps another function to modify its behavior.

```python
def decorator(func):
    def wrapper():
        return func()
    return wrapper
```

---

## 17. Common Beginner Mistakes

### Using lambda for complex logic
```python
# Hard to read
func = lambda x: x * 2 if x > 0 else x / 2 if x < 0 else 0
```

Use `def` if readability suffers.

### Forgetting `nonlocal` in closures
```python
def outer():
    count = 0

    def inner():
        count += 1  # Error
        return count
```

Correct:
```python
def outer():
    count = 0

    def inner():
        nonlocal count
        count += 1
        return count
```

### Decorator wrapper not accepting arguments
```python
def decorator(func):
    def wrapper():
        return func()
    return wrapper
```

This fails if the decorated function needs parameters.

Safer version:
```python
def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### Forgetting to return the result in a decorator
```python
def decorator(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
    return wrapper
```

If the original function returns something, that value is lost.

Correct:
```python
def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

---

## 18. Summary

- A **lambda** is a short anonymous function
- A **closure** is a function that remembers variables from its enclosing scope
- A **decorator** wraps another function to extend or modify its behavior
- Use **`nonlocal`** when a closure needs to modify an enclosing variable
- Use **`*args` and `**kwargs`** in decorators for flexibility
- Use **`functools.wraps`** to preserve function metadata


# Python: Iterators, Generators, and Comprehensions

## 1. Iterators

An **iterator** is an object that lets you go through values one at a time.

In Python, an iterator follows the **iterator protocol**, which means it implements:

- `__iter__()`
- `__next__()`

### Basic idea

When you use a `for` loop, Python usually works with an iterator behind the scenes.

```python
numbers = [10, 20, 30]

for number in numbers:
    print(number)
```

Even though you do not see it directly, Python is internally getting an iterator from `numbers`.

---

## 2. Iterable vs Iterator

These two concepts are related, but they are not the same.

### Iterable
An **iterable** is an object you can loop over.

Examples:
- `list`
- `tuple`
- `str`
- `dict`
- `set`

```python
text = "Python"
numbers = [1, 2, 3]
```

These are iterables.

### Iterator
An **iterator** is the object that produces the next value one at a time.

You usually get an iterator from an iterable by using `iter()`.

```python
numbers = [1, 2, 3]
iterator = iter(numbers)

print(next(iterator))  # 1
print(next(iterator))  # 2
print(next(iterator))  # 3
```

If you ask for another value after the iterator is exhausted, Python raises:

```python
StopIteration
```

---

## 3. Using `iter()` and `next()`

### Example
```python
colors = ["red", "blue", "green"]
it = iter(colors)

print(next(it))  # red
print(next(it))  # blue
print(next(it))  # green
# print(next(it))  # StopIteration
```

This is the manual way to consume an iterator.

A `for` loop does this automatically for you.

---

## 4. How a `for` Loop Works Internally

This:

```python
for item in [1, 2, 3]:
    print(item)
```

is conceptually similar to:

```python
iterator = iter([1, 2, 3])

while True:
    try:
        item = next(iterator)
        print(item)
    except StopIteration:
        break
```

This is why iterators are so important in Python.

---

## 5. Creating a Custom Iterator

You can define your own iterator class.

```python
class CountUpTo:
    def __init__(self, limit):
        self.limit = limit
        self.current = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.limit:
            raise StopIteration
        value = self.current
        self.current += 1
        return value

counter = CountUpTo(3)

for number in counter:
    print(number)
```

Output:
```python
1
2
3
```

### Explanation
- `__iter__()` returns the iterator object
- `__next__()` returns the next value
- when there are no more values, it raises `StopIteration`

---

## 6. Generators

A **generator** is a simpler way to create iterators.

Instead of writing a full class with `__iter__()` and `__next__()`, you can write a function with `yield`.

### Basic example
```python
def count_up_to(limit):
    current = 1
    while current <= limit:
        yield current
        current += 1

for number in count_up_to(3):
    print(number)
```

Output:
```python
1
2
3
```

---

## 7. `yield` vs `return`

### `return`
- ends the function completely
- sends back one final value

### `yield`
- pauses the function
- remembers its state
- resumes later from the same place

Example with `yield`:
```python
def simple_generator():
    yield 1
    yield 2
    yield 3

gen = simple_generator()

print(next(gen))  # 1
print(next(gen))  # 2
print(next(gen))  # 3
```

After the last `yield`, the generator is exhausted and raises `StopIteration`.

---

## 8. Why Generators Are Useful

Generators are useful because they:

- use less memory
- produce values lazily
- are great for large sequences or streaming data

### List approach
```python
numbers = [x * 2 for x in range(1000000)]
```

This builds the whole list in memory.

### Generator approach
```python
numbers = (x * 2 for x in range(1000000))
```

This creates values only when needed.

---

## 9. Generator Functions

A function becomes a generator function when it uses `yield`.

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

for value in countdown(5):
    print(value)
```

Output:
```python
5
4
3
2
1
```

---

## 10. Generator Expressions

A **generator expression** is like a list comprehension, but with parentheses instead of brackets.

### List comprehension
```python
squares = [x * x for x in range(5)]
print(squares)
```

### Generator expression
```python
squares = (x * x for x in range(5))
print(squares)
```

The second one does not immediately produce a full list. It creates a generator object.

To see the values:
```python
for value in squares:
    print(value)
```

Or:
```python
print(list(squares))
```

---

## 11. Comprehensions

A **comprehension** is a compact way to build collections.

Python has several kinds of comprehensions:

- list comprehensions
- dictionary comprehensions
- set comprehensions
- generator expressions

---

## 12. List Comprehensions

A **list comprehension** creates a list in a concise way.

### Basic syntax
```python
[expression for item in iterable]
```

### Example
```python
squares = [x * x for x in range(5)]
print(squares)
```

Output:
```python
[0, 1, 4, 9, 16]
```

### With a condition
```python
evens = [x for x in range(10) if x % 2 == 0]
print(evens)
```

Output:
```python
[0, 2, 4, 6, 8]
```

### Equivalent normal loop
```python
evens = []

for x in range(10):
    if x % 2 == 0:
        evens.append(x)
```

---

## 13. Dictionary Comprehensions

A **dictionary comprehension** creates a dictionary.

### Syntax
```python
{key_expression: value_expression for item in iterable}
```

### Example
```python
squares = {x: x * x for x in range(5)}
print(squares)
```

Output:
```python
{0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

### With a condition
```python
even_squares = {x: x * x for x in range(10) if x % 2 == 0}
print(even_squares)
```

---

## 14. Set Comprehensions

A **set comprehension** creates a set.

### Example
```python
values = {x * 2 for x in range(5)}
print(values)
```

Output:
```python
{0, 2, 4, 6, 8}
```

This is useful when you want unique values.

---

## 15. Generator Expressions

A **generator expression** looks similar to a list comprehension, but it creates a generator instead of a list.

```python
gen = (x * x for x in range(5))
print(gen)
```

To consume it:
```python
for value in gen:
    print(value)
```

Or:
```python
print(list(gen))
```

---

## 16. Comprehensions with `if-else`

You can also use conditional expressions inside comprehensions.

```python
labels = ["even" if x % 2 == 0 else "odd" for x in range(5)]
print(labels)
```

Output:
```python
['even', 'odd', 'even', 'odd', 'even']
```

### Important
This is different from filtering:

Filtering:
```python
[x for x in range(5) if x % 2 == 0]
```

Conditional expression:
```python
["even" if x % 2 == 0 else "odd" for x in range(5)]
```

---

## 17. Nested Comprehensions

You can nest loops inside comprehensions.

### Example
```python
pairs = [(x, y) for x in range(2) for y in range(3)]
print(pairs)
```

Output:
```python
[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
```

This is equivalent to:

```python
pairs = []

for x in range(2):
    for y in range(3):
        pairs.append((x, y))
```

---

## 18. When to Use Comprehensions

Comprehensions are good when:

- the logic is short
- the result is easy to read
- you want concise code

Use normal loops instead when:

- the logic becomes too complex
- readability suffers
- multiple steps are needed

Readable:
```python
squares = [x * x for x in range(10)]
```

Less readable:
```python
result = [x * 2 if x % 2 == 0 else x * 3 for x in range(20) if x > 5 and x != 11]
```

In those cases, a normal loop may be better.

---

## 19. Common Beginner Mistakes

### Confusing iterable and iterator
```python
numbers = [1, 2, 3]
print(next(numbers))  # Error
```

A list is iterable, but it is not an iterator.

Correct:
```python
numbers = [1, 2, 3]
it = iter(numbers)
print(next(it))
```

### Forgetting that generators are consumed
```python
gen = (x for x in range(3))

print(list(gen))  # [0, 1, 2]
print(list(gen))  # []
```

Once a generator is exhausted, it does not restart automatically.

### Using parentheses when you wanted a list
```python
values = (x * 2 for x in range(5))
```

This creates a generator, not a list.

If you want a list:
```python
values = [x * 2 for x in range(5)]
```

### Making comprehensions too complex
A comprehension should usually stay short and readable.

---

## 20. Summary

- An **iterable** is something you can loop over
- An **iterator** produces values one at a time with `__next__()`
- `iter()` gets an iterator from an iterable
- `next()` gets the next value from an iterator
- A **generator** is an easier way to create iterators using `yield`
- A **generator expression** creates values lazily
- **Comprehensions** are compact ways to build lists, dictionaries, sets, or generators
- Use comprehensions for clear and concise transformations
- Use normal loops when the logic becomes too complex

# Python: Context Managers (`with`)

## 1. What Is a Context Manager?

A **context manager** is a Python object that manages resources automatically.

It is commonly used for things like:

- opening and closing files
- managing database connections
- acquiring and releasing locks
- setting up and cleaning up temporary state

The main keyword used with context managers is:

```python
with
```

---

## 2. Why Context Managers Matter

Some resources must be cleaned up after use.

For example:
- a file should be closed
- a lock should be released
- a network connection should be cleaned up

Without a context manager, you usually have to do that manually.

### Example without `with`
```python
file = open("example.txt", "r")
content = file.read()
file.close()
```

This works, but it has a problem:
if an error happens before `file.close()`, the file may stay open longer than expected.

---

## 3. Using `with`

The `with` statement handles setup and cleanup automatically.

### Example
```python
with open("example.txt", "r") as file:
    content = file.read()
    print(content)
```

When the block finishes, Python automatically closes the file.

This is the main reason `with` is preferred.

---

## 4. Basic Syntax of `with`

```python
with expression as variable:
    # block of code
```

### Example
```python
with open("notes.txt", "r") as file:
    text = file.read()
```

Here:
- `open("notes.txt", "r")` creates a context manager
- `as file` assigns the managed object to `file`
- when the block ends, cleanup happens automatically

---

## 5. Most Common Example: Files

### Reading a file
```python
with open("data.txt", "r") as file:
    print(file.read())
```

### Writing to a file
```python
with open("data.txt", "w") as file:
    file.write("Hello, Python")
```

### Appending to a file
```python
with open("data.txt", "a") as file:
    file.write("\\nNew line")
```

In all cases, the file is automatically closed after the block.

---

## 6. `with` vs Manual `try-finally`

A context manager is often similar to writing `try-finally`.

### Without `with`
```python
file = open("example.txt", "r")
try:
    content = file.read()
    print(content)
finally:
    file.close()
```

### With `with`
```python
with open("example.txt", "r") as file:
    content = file.read()
    print(content)
```

The second version is shorter, cleaner, and less error-prone.

---

## 7. What Happens If an Exception Occurs?

A very important point:
**cleanup still happens even if an exception is raised inside the `with` block.**

### Example
```python
with open("example.txt", "r") as file:
    content = file.read()
    raise ValueError("Something went wrong")
```

Even though an error occurs, Python still closes the file properly.

This is one of the biggest advantages of context managers.

---

## 8. Multiple Context Managers in One `with`

You can manage multiple resources in the same statement.

```python
with open("input.txt", "r") as source, open("output.txt", "w") as target:
    data = source.read()
    target.write(data)
```

This opens both files and closes both automatically when the block ends.

---

## 9. Context Manager Protocol

A context manager works through two special methods:

- `__enter__()`
- `__exit__()`

### `__enter__()`
Runs when execution enters the `with` block.

### `__exit__()`
Runs when execution leaves the `with` block, even if an exception happened.

This is the protocol Python uses behind the scenes.

---

## 10. Creating a Custom Context Manager with a Class

You can create your own context manager by defining `__enter__()` and `__exit__()`.

### Example
```python
class MyContext:
    def __enter__(self):
        print("Entering the block")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting the block")

with MyContext() as obj:
    print("Inside the block")
```

Output:
```python
Entering the block
Inside the block
Exiting the block
```

---

## 11. Understanding `__enter__()` and `__exit__()`

### Example with explanation
```python
class MyContext:
    def __enter__(self):
        print("Setup")
        return "resource"

    def __exit__(self, exc_type, exc_value, traceback):
        print("Cleanup")
```

Usage:
```python
with MyContext() as value:
    print("Using", value)
```

Output:
```python
Setup
Using resource
Cleanup
```

### Notes
- the value returned by `__enter__()` is assigned after `as`
- `__exit__()` receives exception information if an error happened

Parameters of `__exit__()`:
- `exc_type`: the exception type
- `exc_value`: the exception object
- `traceback`: the traceback information

If no exception occurs, those values are usually `None`.

---

## 12. Handling Exceptions in `__exit__()`

A context manager can inspect exceptions in `__exit__()`.

```python
class SafeContext:
    def __enter__(self):
        print("Start")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("End")
        print("Exception type:", exc_type)
        print("Exception value:", exc_value)
```

Usage:
```python
with SafeContext():
    print("Inside")
    raise ValueError("Oops")
```

### Important
By default, the exception still propagates after `__exit__()` finishes.

---

## 13. Suppressing Exceptions

If `__exit__()` returns `True`, Python treats the exception as handled and suppresses it.

```python
class IgnoreValueError:
    def __enter__(self):
        print("Entering")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is ValueError:
            print("ValueError handled")
            return True
```

Usage:
```python
with IgnoreValueError():
    print("Inside block")
    raise ValueError("This will be suppressed")

print("Program continues")
```

### Be careful
Suppressing exceptions should be done only when it is truly appropriate.

---

## 14. Context Managers with `contextlib.contextmanager`

Python also allows you to create context managers using a generator and the `contextlib` module.

### Example
```python
from contextlib import contextmanager

@contextmanager
def my_context():
    print("Setup")
    yield
    print("Cleanup")

with my_context():
    print("Inside block")
```

Output:
```python
Setup
Inside block
Cleanup
```

This is often simpler than writing a full class.

---

## 15. `contextmanager` with a Returned Value

You can also yield a value that becomes available after `as`.

```python
from contextlib import contextmanager

@contextmanager
def managed_resource():
    print("Opening resource")
    yield "my resource"
    print("Closing resource")

with managed_resource() as resource:
    print("Using", resource)
```

Output:
```python
Opening resource
Using my resource
Closing resource
```

---

## 16. Realistic Example: Timing Code

A context manager can be used for measuring execution time.

```python
from contextlib import contextmanager
import time

@contextmanager
def timer():
    start = time.time()
    yield
    end = time.time()
    print("Elapsed:", end - start)

with timer():
    total = sum(range(1000000))
```

This is a practical example of setup before the block and cleanup after it.

---

## 17. Realistic Example: Temporary Message

```python
from contextlib import contextmanager

@contextmanager
def log_section(name):
    print(f"Starting {name}")
    yield
    print(f"Ending {name}")

with log_section("data processing"):
    print("Working...")
```

---

## 18. When to Use Context Managers

Use a context manager when you need:

- automatic cleanup
- safer resource handling
- setup before a block and cleanup after it
- cleaner replacement for `try-finally`

Typical use cases:
- files
- locks
- database sessions
- temporary configuration changes
- timers and logging wrappers

---

## 19. Common Beginner Mistakes

### Forgetting `with` for files
```python
file = open("data.txt", "r")
content = file.read()
```

This works, but cleanup is manual.

Better:
```python
with open("data.txt", "r") as file:
    content = file.read()
```

### Confusing `__enter__()` return value
```python
class Example:
    def __enter__(self):
        return "hello"

    def __exit__(self, exc_type, exc_value, traceback):
        pass

with Example() as value:
    print(value)  # hello
```

The variable after `as` gets the result of `__enter__()`.

### Forgetting the `yield` in `@contextmanager`
```python
from contextlib import contextmanager

@contextmanager
def broken():
    print("Setup")
```

This will not work correctly because a `@contextmanager` function must use `yield`.

### Returning `True` from `__exit__()` by accident
```python
def __exit__(self, exc_type, exc_value, traceback):
    return True
```

That suppresses exceptions, which may hide bugs.

---

## 20. Summary

- A **context manager** handles setup and cleanup automatically
- The `with` statement is the main way to use a context manager
- It is commonly used for files and other resources
- Context managers make code safer and cleaner than manual cleanup
- The protocol uses `__enter__()` and `__exit__()`
- You can create custom context managers with:
  - a class
  - `contextlib.contextmanager`
- `with` is especially useful when cleanup must happen even if an exception occurs