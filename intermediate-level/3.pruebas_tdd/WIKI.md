# pytest: Fixtures, Parametrization, and Markers

## 1. Goal

This guide explains three essential `pytest` concepts:

- **fixtures**
- **parametrization**
- **markers**

These are some of the most useful tools in `pytest` because they help you write tests that are:

- cleaner
- more reusable
- easier to maintain
- easier to organize

---

## 2. What is `pytest`?

`pytest` is one of the most popular testing frameworks in Python.

It is widely used because it offers:

- simple syntax
- powerful assertions
- flexible fixtures
- great plugin support
- good support for unit, integration, and API tests

---

## 3. Why these three concepts matter

If you write tests without fixtures, parametrization, or markers, you often end up with:

- repeated setup code
- duplicated test cases
- messy test organization
- harder maintenance

These three features solve a large part of that problem.

---

## 4. Fixtures

## What is a fixture?

A **fixture** is reusable setup logic for tests.

A fixture can provide things like:

- test data
- database connections
- API clients
- temporary files
- authenticated users
- mock objects

Instead of repeating setup code in many tests, you define it once and reuse it.

---

## 5. Basic fixture example

```python
import pytest


@pytest.fixture
def sample_user():
    return {
        "id": 1,
        "username": "janette"
    }
```

### Using the fixture

```python
def test_user_has_username(sample_user):
    assert sample_user["username"] == "janette"
```

### What happens here
`pytest` sees that the test function needs `sample_user`, so it automatically calls the fixture and injects the returned value.

---

## 6. Why fixtures are useful

Fixtures help you:

- reduce duplication
- centralize setup
- make tests more readable
- reuse common resources
- manage setup and teardown safely

Instead of this:

```python
def test_a():
    user = {"id": 1, "username": "janette"}
    assert user["id"] == 1


def test_b():
    user = {"id": 1, "username": "janette"}
    assert user["username"] == "janette"
```

you can write the data once in a fixture.

---

## 7. Fixtures in `conftest.py`

When a fixture should be shared across many test files, put it in `conftest.py`.

### Example structure

```text
project/
├── app/
├── tests/
│   ├── conftest.py
│   ├── test_users.py
│   └── test_items.py
```

### Example `conftest.py`

```python
import pytest


@pytest.fixture
def sample_user():
    return {
        "id": 1,
        "username": "janette"
    }
```

Now all test files inside that test scope can use `sample_user` without importing it directly.

---

## 8. Fixture scopes

Fixtures can have different lifetimes using `scope`.

Common scopes:
- `function`
- `class`
- `module`
- `package`
- `session`

### Example

```python
import pytest


@pytest.fixture(scope="module")
def db_connection():
    return "connected"
```

### Meaning
- `function`: created for every test function
- `module`: created once per test module
- `session`: created once for the whole test run

### Why scope matters
Some resources are expensive to create.  
Using a broader scope can make tests faster.

---

## 9. Fixture teardown with `yield`

Fixtures can also handle cleanup.

```python
import pytest


@pytest.fixture
def temp_resource():
    print("setup resource")
    yield "resource"
    print("cleanup resource")
```

### What this does
- code before `yield` runs before the test
- the value after `yield` is provided to the test
- code after `yield` runs after the test finishes

This is useful for:
- closing DB connections
- cleaning temp files
- shutting down test clients
- restoring state

---

## 10. Example with setup and teardown

```python
import pytest


@pytest.fixture
def file_handle():
    file = open("test.txt", "w")
    yield file
    file.close()
```

### Why this pattern is important
It keeps resource management inside the fixture, not inside every test.

---

## 11. Fixtures depending on other fixtures

Fixtures can use other fixtures.

```python
import pytest


@pytest.fixture
def sample_user():
    return {"id": 1, "username": "janette"}


@pytest.fixture
def admin_user(sample_user):
    sample_user["role"] = "admin"
    return sample_user
```

### Example test

```python
def test_admin_role(admin_user):
    assert admin_user["role"] == "admin"
```

### Benefit
You can compose setup logic cleanly instead of creating huge fixtures.

---

## 12. Fixture factories

Sometimes you need flexible test data, not just one static object.

### Example

```python
import pytest


@pytest.fixture
def user_factory():
    def create_user(username="janette", role="user"):
        return {
            "username": username,
            "role": role
        }
    return create_user
```

### Usage

```python
def test_custom_user(user_factory):
    user = user_factory(username="ana", role="admin")
    assert user["username"] == "ana"
    assert user["role"] == "admin"
```

This pattern is very useful for test data generation.

---

## 13. Autouse fixtures

An autouse fixture is applied automatically without being requested explicitly in the test function.

```python
import pytest


@pytest.fixture(autouse=True)
def setup_env():
    print("Runs before every test")
```

### Use carefully
Autouse fixtures are convenient, but if overused they can make tests harder to understand because behavior happens implicitly.

Good use cases:
- global environment setup
- resetting global state
- common patching needed everywhere

---

## 14. Parametrization

## What is parametrization?

**Parametrization** lets you run the same test logic with multiple sets of data.

Instead of writing:

```python
def test_add_1():
    assert 1 + 1 == 2


def test_add_2():
    assert 2 + 2 == 4


def test_add_3():
    assert 3 + 3 == 6
```

you can write one parametrized test.

---

## 15. Basic parametrization example

```python
import pytest


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (1, 1, 2),
        (2, 2, 4),
        (3, 3, 6),
    ]
)
def test_addition(a, b, expected):
    assert a + b == expected
```

### What happens here
`pytest` runs the same test function once for each row in the data list.

---

## 16. Why parametrization is useful

Parametrization helps you:

- avoid duplicated test functions
- cover more cases with less code
- make edge cases more visible
- improve readability when multiple inputs should behave similarly

It is especially useful for:
- validation logic
- formatting functions
- API error cases
- mathematical or business rules

---

## 17. Parametrization with one argument

```python
import pytest


@pytest.mark.parametrize("value", [1, 2, 3, 4])
def test_value_is_positive(value):
    assert value > 0
```

This is the simplest form.

---

## 18. Parametrization with descriptive IDs

You can make test output more readable using `ids`.

```python
import pytest


@pytest.mark.parametrize(
    "email, valid",
    [
        ("user@example.com", True),
        ("invalid-email", False),
        ("admin@test.com", True),
    ],
    ids=["valid_user", "invalid_email", "valid_admin"]
)
def test_email_cases(email, valid):
    result = "@" in email
    assert result == valid
```

### Why this helps
If one case fails, the test report is easier to read.

---

## 19. Parametrizing exceptions

You can also test expected failures.

```python
import pytest


@pytest.mark.parametrize(
    "value",
    [0, -1, -10]
)
def test_value_must_be_positive(value):
    assert value <= 0
```

More realistically, you may combine this with `pytest.raises`.

```python
import pytest


def divide(a, b):
    return a / b


@pytest.mark.parametrize("a, b", [(10, 0), (5, 0)])
def test_divide_by_zero(a, b):
    with pytest.raises(ZeroDivisionError):
        divide(a, b)
```

---

## 20. Parametrization with fixtures

You can combine fixtures and parametrization.

```python
import pytest


@pytest.fixture
def multiplier():
    return 2


@pytest.mark.parametrize("value, expected", [(1, 2), (2, 4), (3, 6)])
def test_multiplication(multiplier, value, expected):
    assert value * multiplier == expected
```

This is very common and very useful.

---

## 21. Indirect parametrization

Sometimes you want parameter values to go through a fixture first.

```python
import pytest


@pytest.fixture
def user(request):
    return {"username": request.param}


@pytest.mark.parametrize("user", ["janette", "ana"], indirect=True)
def test_usernames(user):
    assert "username" in user
```

### Why this is useful
It lets fixtures dynamically build data from parametrized inputs.

---

## 22. Markers

## What are markers?

**Markers** are labels you attach to tests.

They help you:
- categorize tests
- select subsets of tests
- skip or conditionally run tests
- organize test suites

Markers become very useful once a project has many tests.

---

## 23. Basic custom marker example

```python
import pytest


@pytest.mark.slow
def test_large_process():
    assert True
```

### Why this helps
You can later run only certain categories of tests.

Example command:

```bash
pytest -m slow
```

---

## 24. Common built-in markers

Some useful built-in markers include:

- `skip`
- `skipif`
- `xfail`
- `parametrize`

### `skip`

```python
import pytest


@pytest.mark.skip(reason="Not ready yet")
def test_feature_not_ready():
    assert False
```

This test is skipped entirely.

---

## 25. `skipif`

```python
import sys
import pytest


@pytest.mark.skipif(sys.platform == "win32", reason="Not supported on Windows")
def test_linux_only_behavior():
    assert True
```

### Why useful
This is practical when tests depend on:
- operating system
- Python version
- environment configuration
- optional dependencies

---

## 26. `xfail`

`xfail` means **expected failure**.

```python
import pytest


@pytest.mark.xfail(reason="Known bug not fixed yet")
def test_known_bug():
    assert False
```

### What this means
The test is allowed to fail without making the whole suite look unexpectedly broken.

Use it for:
- known bugs
- temporary gaps
- unstable external issues you are tracking

---

## 27. Registering custom markers

To avoid warnings, register custom markers in `pytest.ini`.

### Example

```ini
[pytest]
markers =
    slow: marks tests as slow
    api: marks API tests
    integration: marks integration tests
```

### Why this matters
This keeps the test suite cleaner and documents marker meaning.

---

## 28. Running tests by marker

Examples:

```bash
pytest -m slow
pytest -m api
pytest -m "not slow"
pytest -m "integration and not slow"
```

### Why useful
This makes it easy to:
- run quick tests during development
- exclude expensive tests in CI stages
- target only a specific test group

---

## 29. Combining markers and parametrization

You can use both together.

```python
import pytest


@pytest.mark.api
@pytest.mark.parametrize("status_code", [200, 201, 204])
def test_valid_status_codes(status_code):
    assert status_code in [200, 201, 204]
```

This is common in organized test suites.

---

## 30. Marking entire classes or modules

You can apply markers to more than one test at once.

### Whole class

```python
import pytest


@pytest.mark.integration
class TestUserFlows:
    def test_create_user(self):
        assert True

    def test_delete_user(self):
        assert True
```

### Whole module

```python
pytestmark = pytest.mark.api
```

This applies the marker to all tests in that module.

---

## 31. Real-world examples of marker usage

Common categories:
- `unit`
- `integration`
- `api`
- `slow`
- `database`
- `smoke`

### Why this works well
It gives structure to the test suite and helps different workflows.

For example:
- local development may run only `unit`
- CI may run `unit` + `api`
- nightly pipeline may run `slow` + `integration`

---

## 32. Fixtures + parametrization + markers together

These features are often most powerful when combined.

```python
import pytest


@pytest.fixture
def base_value():
    return 10


@pytest.mark.math
@pytest.mark.parametrize("value, expected", [(1, 11), (2, 12), (3, 13)])
def test_add_base(base_value, value, expected):
    assert base_value + value == expected
```

### What this shows
- fixture provides shared setup
- parametrization expands coverage
- marker categorizes the test

That is a very typical `pytest` style.

---

## 33. Best practices

### 1. Keep fixtures focused
A fixture should do one job clearly.

### 2. Avoid giant fixtures
Large fixtures become hard to understand and reuse.

### 3. Use parametrization for repeated logic
If the test body is the same and only values change, parametrize it.

### 4. Use markers for meaningful categories
Markers should reflect real test groups, not random labels.

### 5. Register custom markers
This avoids warnings and documents intent.

### 6. Prefer readable tests over clever tests
Test code should be easy to understand quickly.

### 7. Use `yield` for cleanup
This keeps resource management safe and centralized.

---

## 34. Common mistakes

### 1. Overusing autouse fixtures
Too much implicit setup can make tests confusing.

### 2. Making fixtures too broad
A fixture that does too much becomes fragile.

### 3. Duplicating tests instead of parametrizing
This increases maintenance cost.

### 4. Using markers without registration
This causes warnings and weakens documentation.

### 5. Mixing unrelated concerns in one test
A test should still be focused, even when using powerful `pytest` features.

---

## 35. Practical mental model

A useful mental model is:

- **fixtures** provide reusable setup
- **parametrization** multiplies coverage with the same logic
- **markers** organize and control execution

Together, they help you build a test suite that is:
- scalable
- maintainable
- expressive

---

## 36. Final recommendation

When using `pytest` in real projects:

- define shared setup through fixtures
- reduce repeated test bodies through parametrization
- organize your suite through markers
- keep tests explicit and readable
- register markers in `pytest.ini`

These habits make a very large difference as the number of tests grows.

---

## 37. Quick summary

If you only keep the essentials:

1. Fixtures are reusable setup and teardown tools.
2. Parametrization runs one test with multiple input cases.
3. Markers label and organize tests.
4. These three features reduce duplication and improve maintainability.
5. They are some of the most important `pytest` features to learn early.

---
# Property-Based Testing with Hypothesis

## 1. Goal

This guide explains **property-based testing** in Python using **Hypothesis**.

It focuses on:

- what property-based testing is
- how it differs from example-based testing
- how Hypothesis generates test data
- common strategies
- shrinking
- practical examples
- best practices and common mistakes

The goal is to help you test behavior more deeply by checking general properties instead of only a few hardcoded examples.

---

## 2. What is property-based testing?

In traditional testing, you often write tests like this:

```python
def test_addition():
    assert 2 + 3 == 5
```

This is **example-based testing**.  
You choose specific inputs and check expected outputs.

In **property-based testing**, instead of focusing only on a few examples, you describe a rule or property that should hold for many possible inputs.

Example idea:

> “Adding zero to a number should always return the same number.”

That is a general property, not just one example.

---

## 3. Why property-based testing matters

Example-based tests are useful, but they only cover the exact cases you wrote.

Property-based testing helps you:
- explore many more inputs automatically
- discover edge cases you did not think of
- find bugs in assumptions
- make tests more robust
- validate behavior at a more general level

This is especially useful when logic should hold across a wide range of values.

---

## 4. What is Hypothesis?

**Hypothesis** is a Python library for property-based testing.

It generates many inputs automatically and tries to find cases that break your assumptions.

A simple Hypothesis test usually looks like this:

```python
from hypothesis import given
from hypothesis import strategies as st


@given(st.integers())
def test_adding_zero_returns_same_number(x):
    assert x + 0 == x
```

### What happens here
Hypothesis generates many integers for `x` and checks that the property always holds.

---

## 5. Example-based vs property-based testing

### Example-based testing
You manually choose cases:

```python
def test_reverse():
    assert reverse("abc") == "cba"
    assert reverse("") == ""
```

### Property-based testing
You define a general rule:

```python
from hypothesis import given
from hypothesis import strategies as st


@given(st.text())
def test_reverse_twice_returns_original(text):
    assert text[::-1][::-1] == text
```

### Key difference
- example-based testing checks chosen examples
- property-based testing checks a rule against many generated inputs

Both approaches are useful, and they often work best together.

---

## 6. Installing Hypothesis

A common installation command is:

```bash
pip install hypothesis
```

You usually use it together with `pytest`.

---

## 7. Core concepts

The most important building blocks are:

- `@given`
- strategies
- generated inputs
- shrinking

### `@given`
This decorator tells Hypothesis to generate test inputs.

### Strategies
Strategies define what kinds of data Hypothesis should generate.

Examples:
- integers
- strings
- booleans
- lists
- dictionaries
- dates
- custom objects

### Shrinking
When Hypothesis finds a failing case, it tries to reduce it to the smallest possible example that still fails.

This is one of its most powerful features.

---

## 8. Basic integer example

```python
from hypothesis import given
from hypothesis import strategies as st


@given(st.integers())
def test_multiplication_by_one(x):
    assert x * 1 == x
```

### Property
Multiplying by one should not change the number.

This test is simple, but it shows the structure clearly:
- define the input strategy
- define the property
- let Hypothesis explore many values

---

## 9. Example with strings

```python
from hypothesis import given
from hypothesis import strategies as st


@given(st.text())
def test_string_concatenation_length(s):
    assert len(s + s) == len(s) * 2
```

### Property
Concatenating a string with itself should double its length.

Hypothesis will test this with many different strings, including unusual ones you may not think of manually.

---

## 10. Example with lists

```python
from hypothesis import given
from hypothesis import strategies as st


@given(st.lists(st.integers()))
def test_reversing_twice_returns_original(values):
    assert list(reversed(list(reversed(values)))) == values
```

### Property
Reversing a list twice should return the original list.

This is a classic property-based test shape.

---

## 11. Strategies

Strategies are how you tell Hypothesis what data to generate.

Common strategies include:

- `st.integers()`
- `st.floats()`
- `st.booleans()`
- `st.text()`
- `st.lists(...)`
- `st.tuples(...)`
- `st.dictionaries(...)`
- `st.sampled_from(...)`

### Example

```python
from hypothesis import given
from hypothesis import strategies as st


@given(st.booleans())
def test_boolean_or_self(x):
    assert (x or x) == x
```

---

## 12. Constraining strategies

You can restrict generated data.

### Example with integer bounds

```python
from hypothesis import given
from hypothesis import strategies as st


@given(st.integers(min_value=0, max_value=100))
def test_non_negative_number(x):
    assert x >= 0
```

### Example with list size limits

```python
from hypothesis import given
from hypothesis import strategies as st


@given(st.lists(st.integers(), min_size=1, max_size=10))
def test_list_has_at_least_one_item(values):
    assert len(values) >= 1
```

### Why constraints matter
Sometimes a property only makes sense for certain inputs.  
Constraining strategies helps generate relevant test cases.

---

## 13. Multiple inputs

Hypothesis can generate more than one argument.

```python
from hypothesis import given
from hypothesis import strategies as st


@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    assert a + b == b + a
```

### Property
Addition is commutative.

This is a good example of testing a mathematical property over many values.

---

## 14. Using named arguments

You can also write tests with named strategies.

```python
from hypothesis import given
from hypothesis import strategies as st


@given(a=st.integers(), b=st.integers())
def test_subtraction_relationship(a, b):
    assert (a - b) == -(b - a)
```

This can make tests more readable.

---

## 15. Filtering and assumptions

Sometimes you need to exclude invalid inputs.

### Example with `assume`

```python
from hypothesis import given, assume
from hypothesis import strategies as st


@given(st.integers(), st.integers())
def test_division_inverse(a, b):
    assume(b != 0)
    assert (a / b) * b == a
```

### Important
Use `assume()` carefully.

Why?
Because if too many generated values are rejected, tests become inefficient.

It is usually better to define a narrower strategy when possible.

For example, instead of:

```python
assume(b != 0)
```

prefer:

```python
st.integers().filter(lambda x: x != 0)
```

or an even better direct strategy if possible.

---

## 16. Better input design instead of too many assumptions

A cleaner version:

```python
from hypothesis import given
from hypothesis import strategies as st


non_zero_integers = st.integers().filter(lambda x: x != 0)


@given(a=st.integers(), b=non_zero_integers)
def test_division_result_type(a, b):
    result = a / b
    assert isinstance(result, float)
```

### Note
Filtering is still a form of rejection.  
When possible, define strategies that naturally produce the valid domain you want.

---

## 17. Hypothesis shrinking

One of the best features of Hypothesis is **shrinking**.

If Hypothesis finds a failing input, it tries to reduce it to a smaller and simpler example.

### Why this matters
Suppose a test fails for a very large list.  
Hypothesis may shrink it to a minimal failing example such as:

```python
[0]
```

or:

```python
""
```

or a very small number.

This makes debugging much easier than getting a huge random input.

---

## 18. Example of a failing property

```python
from hypothesis import given
from hypothesis import strategies as st


@given(st.lists(st.integers()))
def test_sort_preserves_first_element(values):
    if values:
        assert sorted(values)[0] == values[0]
```

This property is wrong.

Why?
Because sorting changes order.

Hypothesis will quickly find a counterexample and often shrink it to something very small, such as:

```python
[1, 0]
```

That is very useful because it reveals the exact flaw in the assumption.

---

## 19. Good property examples

A good property usually describes something fundamental and general.

Examples:
- reversing twice returns the original value
- sorting preserves list length
- serializing and deserializing returns equivalent data
- adding zero does not change a number
- valid encoders/decoders are inverse operations
- parsing then formatting then parsing again stays consistent

These are stronger than random example assertions.

---

## 20. Example: sorting properties

```python
from hypothesis import given
from hypothesis import strategies as st


@given(st.lists(st.integers()))
def test_sorted_result_has_same_length(values):
    assert len(sorted(values)) == len(values)


@given(st.lists(st.integers()))
def test_sorted_result_is_ordered(values):
    sorted_values = sorted(values)
    assert sorted_values == sorted(sorted_values)
```

### What these test
- sorting should not change length
- sorting should produce an ordered result

These are meaningful properties.

---

## 21. Example: encode/decode round trip

Round-trip testing is a very strong use case.

```python
import json
from hypothesis import given
from hypothesis import strategies as st


@given(st.dictionaries(st.text(), st.integers()))
def test_json_round_trip(data):
    encoded = json.dumps(data)
    decoded = json.loads(encoded)
    assert decoded == data
```

### Property
Encoding and then decoding should preserve the data.

This pattern appears often in:
- serialization
- parsing
- transformation pipelines
- conversions between formats

---

## 22. Combining Hypothesis with pytest

Hypothesis works very naturally with `pytest`.

Example:

```python
from hypothesis import given
from hypothesis import strategies as st


@given(st.text())
def test_strip_never_increases_length(text):
    assert len(text.strip()) <= len(text)
```

You can run it with `pytest` just like normal tests.

---

## 23. Settings

Hypothesis allows configuration with `settings`.

Example:

```python
from hypothesis import given, settings
from hypothesis import strategies as st


@settings(max_examples=200)
@given(st.integers())
def test_identity(x):
    assert x == x
```

### What `max_examples` does
It changes how many generated examples Hypothesis tries.

This can be useful when:
- the property is cheap and you want wider exploration
- the test is expensive and you need fewer cases

---

## 24. Controlling deadlines

Hypothesis has time-based behavior for detecting very slow tests.

You can configure deadlines if needed.

```python
from hypothesis import given, settings
from hypothesis import strategies as st


@settings(deadline=None)
@given(st.text())
def test_example_without_deadline(text):
    assert isinstance(text, str)
```

### Use carefully
Disabling deadlines may be useful for slower logic, but it can also hide performance issues in test functions.

---

## 25. Stateful and advanced testing

Hypothesis also supports more advanced styles, including:
- stateful testing
- custom strategies
- data-driven generation
- composite strategies

These are very powerful, but for most early use cases, basic properties and standard strategies already provide a lot of value.

---

## 26. Building custom data

Sometimes built-in strategies are not enough.

You can combine strategies.

### Example

```python
from hypothesis import given
from hypothesis import strategies as st


user_strategy = st.fixed_dictionaries({
    "id": st.integers(min_value=1),
    "name": st.text(min_size=1),
    "active": st.booleans(),
})


@given(user_strategy)
def test_user_has_required_keys(user):
    assert "id" in user
    assert "name" in user
    assert "active" in user
```

### Why useful
This helps model realistic application data while still exploring many cases.

---

## 27. Property-based testing for APIs and validation

Property-based testing is useful in application code too.

Good candidates include:
- validators
- parsers
- serializers
- formatters
- normalization logic
- input transformation
- business rules with broad domains

Example:

```python
from hypothesis import given
from hypothesis import strategies as st


def normalize_username(name: str) -> str:
    return name.strip().lower()


@given(st.text())
def test_normalized_username_has_no_surrounding_spaces(name):
    result = normalize_username(name)
    assert result == result.strip()
```

---

## 28. When Hypothesis is especially valuable

Hypothesis is especially strong when:
- you have many possible inputs
- edge cases are easy to miss
- you suspect hidden assumptions
- round-trip invariants exist
- transformations should preserve structure
- manual examples do not give enough confidence

It is less valuable when:
- behavior is highly specific to a tiny set of known cases
- you only need a few explicit contract examples

Usually the best approach is to combine both styles.

---

## 29. Example-based tests and property-based tests together

A healthy test suite often includes both.

### Example-based tests
Good for:
- exact business examples
- regressions
- clear documentation of expected behavior

### Property-based tests
Good for:
- broad invariants
- edge-case discovery
- deep exploration of valid inputs

They complement each other rather than compete.

---

## 30. Common mistakes

### 1. Testing the implementation instead of a real property
A property should describe behavior, not just restate the same logic differently.

### 2. Using too many assumptions
If Hypothesis rejects too many inputs, the test becomes inefficient.

### 3. Writing properties that are too weak
A weak property may always pass without proving much.

### 4. Writing properties that are false
Sometimes the test fails because the claimed property is not actually true.

### 5. Forgetting edge cases in strategy design
The strategy should represent the meaningful input space.

---

## 31. Best practices

### 1. Test real invariants
Choose properties that should genuinely hold.

### 2. Keep the property simple and clear
A good property is usually easy to explain in one sentence.

### 3. Use constrained strategies when needed
Generate meaningful input domains.

### 4. Prefer strategy design over excessive `assume()`
This keeps tests efficient.

### 5. Keep example-based regression tests too
Do not replace everything with Hypothesis.

### 6. Use round-trip tests when possible
They are often strong and elegant properties.

### 7. Let shrinking help you
When a test fails, pay close attention to the minimized counterexample.

---

## 32. Practical mental model

A useful mental model is:

- example-based testing says:  
  “These specific cases should work.”

- property-based testing says:  
  “This rule should hold for many valid cases.”

Hypothesis then acts like an aggressive input explorer that tries to break your assumptions.

That is why it is so useful for finding subtle bugs.

---

## 33. Final recommendation

When learning Hypothesis:

- start with simple invariants
- use built-in strategies first
- write properties for transformations and validations
- keep your properties meaningful and general
- use it alongside `pytest` and example-based tests

This is one of the best ways to increase confidence in code that handles broad or unpredictable inputs.

---

## 34. Quick summary

If you only keep the essentials:

1. Property-based testing checks general rules, not just hardcoded examples.
2. Hypothesis generates many inputs automatically.
3. Strategies define what kinds of inputs are produced.
4. Shrinking reduces failing cases to minimal counterexamples.
5. Hypothesis is especially useful for validators, parsers, transforms, and round-trip tests.

---
# Coverage and CI Integration

## 1. Goal

This guide explains how to work with:

- **test coverage**
- **coverage reports**
- **coverage thresholds**
- **integration with CI pipelines**

It is focused on practical Python testing workflows, especially when using `pytest` in real projects.

---

## 2. What is test coverage?

**Test coverage** measures how much of your code is executed while your tests run.

In simple terms, it answers questions like:

- which files were executed?
- which lines were executed?
- which parts of the project were never touched by tests?

Coverage is useful because it helps reveal untested areas of the codebase.

---

## 3. Why coverage matters

Coverage helps you:

- identify code that is not being exercised
- reduce blind spots in testing
- track testing quality over time
- prevent major drops in test discipline
- define minimum quality gates in CI

It is especially useful in growing codebases, where it becomes harder to know what is really covered.

---

## 4. Important limitation of coverage

Coverage is useful, but it is **not the same as test quality**.

A high coverage percentage does **not** guarantee that tests are good.

For example:
- a line may execute without being asserted properly
- a branch may run but not be validated meaningfully
- poor tests can still produce high coverage

### Practical rule
Use coverage as a **signal**, not as the only quality metric.

---

## 5. Common types of coverage

### Line coverage
Measures which lines of code were executed.

### Branch coverage
Measures whether different logical branches were exercised, such as:
- `if` / `else`
- `try` / `except`
- conditional returns

### Function or statement coverage
Some tools also provide additional execution views.

In practice, line coverage is the most common starting point, but branch coverage is often more informative.

---

## 6. Common Python tools for coverage

A very common setup is:

- `pytest`
- `pytest-cov`
- `coverage.py`

### What they do
- `pytest` runs the tests
- `pytest-cov` connects coverage measurement to pytest
- `coverage.py` is the underlying coverage engine in many setups

---

## 7. Installing the tools

A common installation command is:

```bash
pip install pytest pytest-cov
```

In many projects, `coverage.py` is installed indirectly through `pytest-cov`, but it can also be installed explicitly if needed.

---

## 8. Basic coverage run with pytest

A simple coverage command looks like this:

```bash
pytest --cov=app
```

### What this means
- run tests with `pytest`
- measure coverage for the `app` package

This will usually print a coverage summary at the end of the test run.

---

## 9. Example coverage output

A typical output may look like this:

```text
Name                Stmts   Miss  Cover
---------------------------------------
app/main.py            20      2    90%
app/services.py        50     10    80%
---------------------------------------
TOTAL                  70     12    83%
```

### Meaning
- `Stmts` = number of statements
- `Miss` = number of statements not executed
- `Cover` = percentage covered

This gives a quick view of which files need more attention.

---

## 10. HTML coverage reports

A terminal summary is useful, but sometimes you want a more detailed report.

You can generate HTML output:

```bash
pytest --cov=app --cov-report=html
```

This typically creates a folder such as:

```text
htmlcov/
```

Inside it, you can open `index.html` in a browser to inspect:
- covered lines
- missed lines
- file-by-file breakdown

### Why useful
HTML reports make it easier to locate exactly what is untested.

---

## 11. Terminal and XML reports

You can generate different report formats.

### Terminal with missing lines

```bash
pytest --cov=app --cov-report=term-missing
```

This shows which lines were not executed.

### XML report

```bash
pytest --cov=app --cov-report=xml
```

This generates an XML report, commonly used by CI platforms and code quality tools.

### Example use cases
- terminal reports for local development
- HTML for manual inspection
- XML for CI integrations and dashboards

---

## 12. Measuring branch coverage

Branch coverage is often more meaningful than only line coverage.

Example command:

```bash
pytest --cov=app --cov-branch
```

You can combine it with reports:

```bash
pytest --cov=app --cov-branch --cov-report=term-missing
```

### Why branch coverage matters
Consider this:

```python
def is_adult(age):
    if age >= 18:
        return True
    return False
```

A test with only `age = 20` might execute all lines, but not fully validate both logical outcomes.

Branch coverage helps reveal that kind of gap.

---

## 13. Coverage thresholds

A **coverage threshold** defines the minimum acceptable coverage percentage.

Example:

```bash
pytest --cov=app --cov-fail-under=80
```

### What this does
- if coverage is 80% or higher, the run passes
- if coverage is below 80%, the run fails

This is very useful in CI because it turns coverage into a quality gate.

---

## 14. Why thresholds are useful

Thresholds help you:

- prevent coverage from dropping silently
- maintain quality expectations
- enforce discipline in pull requests
- keep testing standards stable across the team

### Important
A threshold should be realistic.  
An arbitrary target can create pressure for low-value tests.

---

## 15. Choosing a good threshold

A good threshold depends on:
- project maturity
- team size
- code criticality
- legacy code situation

### Common practical approach
- start with a realistic baseline
- avoid forcing an unrealistic number immediately
- increase gradually over time

For example:
- start at 60% for a legacy project
- move to 70%
- then 80% or more when the suite becomes healthier

---

## 16. Excluding files from coverage

Some files are often excluded, such as:
- migration files
- generated code
- trivial `__init__.py` files
- environment-specific bootstrap code
- code not worth measuring directly

You can configure exclusions using coverage settings.

### Example `.coveragerc`

```ini
[run]
omit =
    tests/*
    */__init__.py
    migrations/*
```

### Why useful
This keeps coverage focused on meaningful application logic.

---

## 17. Example `.coveragerc`

A practical config might look like this:

```ini
[run]
branch = True
source = app
omit =
    tests/*
    */__init__.py

[report]
show_missing = True
skip_covered = False
fail_under = 80
```

### What this does
- enables branch coverage
- limits measurement to `app`
- omits selected files
- shows missing lines
- fails if total coverage goes below 80%

This keeps the command line simpler and centralizes configuration.

---

## 18. Example `pytest.ini`

Some projects prefer keeping part of the configuration in `pytest.ini`.

```ini
[pytest]
addopts = --cov=app --cov-branch --cov-report=term-missing
testpaths = tests
```

### Benefit
Now you can run:

```bash
pytest
```

and still get coverage automatically.

---

## 19. Local developer workflow

A simple local workflow might be:

1. write or update code
2. write tests
3. run `pytest`
4. inspect coverage summary
5. improve tests for missed logic if needed

This makes coverage part of normal development instead of something only checked in CI.

---

## 20. What coverage should help you find

Coverage is especially useful for revealing:
- untested error paths
- missing edge case tests
- forgotten branches
- untested service methods
- code added recently without corresponding tests

That makes it useful not just as a score, but as a diagnostic tool.

---

## 21. CI integration

## What is CI?

**CI** stands for **Continuous Integration**.

It is the practice of automatically running checks when code changes are pushed or proposed, usually through:
- pull requests
- merge requests
- branch pushes

Common CI tasks include:
- running tests
- checking linting
- measuring coverage
- building artifacts
- enforcing quality gates

---

## 22. Why integrate coverage into CI

Running coverage only on local machines is not enough.

CI integration helps ensure that:
- all contributors follow the same checks
- results are consistent
- coverage gates are enforced automatically
- regressions are caught before merging

This makes test coverage part of the delivery process.

---

## 23. Typical CI pipeline for Python tests

A typical pipeline may do something like this:

1. set up Python
2. install dependencies
3. run tests
4. generate coverage report
5. fail if coverage is below the threshold

This is simple, but very effective.

---

## 24. Example with GitHub Actions

A common CI platform is **GitHub Actions**.

Example workflow file:

```yaml
name: Python Tests

on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests with coverage
        run: |
          pytest --cov=app --cov-branch --cov-report=term-missing --cov-fail-under=80
```

### What this does
- runs on pushes and pull requests
- installs Python
- installs dependencies
- runs tests with coverage
- fails if coverage drops below 80%

---

## 25. Example with GitLab CI

Example `.gitlab-ci.yml`:

```yaml
stages:
  - test

test:
  stage: test
  image: python:3.11

  before_script:
    - pip install -r requirements.txt
    - pip install pytest pytest-cov

  script:
    - pytest --cov=app --cov-branch --cov-report=term-missing --cov-fail-under=80
```

### Why useful
This provides the same core workflow in GitLab CI.

---

## 26. Example with Azure Pipelines

Example `azure-pipelines.yml`:

```yaml
trigger:
  - main

pool:
  vmImage: "ubuntu-latest"

steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: "3.11"

  - script: |
      python -m pip install --upgrade pip
      pip install -r requirements.txt
      pip install pytest pytest-cov
    displayName: Install dependencies

  - script: |
      pytest --cov=app --cov-branch --cov-report=term-missing --cov-fail-under=80
    displayName: Run tests with coverage
```

---

## 27. Uploading coverage reports to external services

Some teams use external coverage dashboards or code quality platforms.

Common uses:
- tracking coverage history
- visualizing trends
- annotating pull requests
- centralizing reporting

Usually this relies on formats like:
- XML
- LCOV
- JSON, depending on the platform

Example local generation:

```bash
pytest --cov=app --cov-report=xml
```

This XML report can then be consumed by external tools in CI.

---

## 28. Coverage in pull requests

A mature CI setup may use coverage to improve pull request review.

Examples:
- fail if total coverage goes below threshold
- warn if changed files have no test coverage
- show a summary comment in the pull request
- highlight newly uncovered code

This makes coverage directly visible during code review.

---

## 29. Good CI quality gates

Coverage is most effective when combined with other checks.

A practical CI quality gate may include:
- tests must pass
- coverage must stay above threshold
- linting must pass
- build must succeed

### Why this matters
Coverage alone cannot guarantee code quality, but together with other checks it becomes much more valuable.

---

## 30. Common mistakes

### 1. Chasing 100% coverage blindly
This can create low-value tests and wasted effort.

### 2. Using coverage as the only quality signal
Coverage says what ran, not whether it was tested well.

### 3. Excluding too much code
That can make the metric misleading.

### 4. Setting thresholds unrealistically high too early
This can frustrate teams and encourage bad tests.

### 5. Only checking coverage locally
Without CI enforcement, standards are harder to maintain.

### 6. Ignoring branch coverage
Line coverage alone can hide logical gaps.

---

## 31. Best practices

### 1. Use coverage as feedback, not vanity
Focus on meaningful protection.

### 2. Start with a realistic threshold
Increase over time if the project improves.

### 3. Prefer branch coverage when possible
It gives better insight into logic paths.

### 4. Review uncovered lines intentionally
Some gaps matter more than others.

### 5. Integrate coverage into CI
Automated enforcement is more reliable than manual checking.

### 6. Combine with good assertions and good test design
Coverage is strongest when the tests themselves are strong.

### 7. Keep configuration in version control
Use files like `.coveragerc` and `pytest.ini`.

---

## 32. Example practical setup

A simple practical project might have:

### `pytest.ini`

```ini
[pytest]
addopts = --cov=app --cov-branch --cov-report=term-missing
testpaths = tests
```

### `.coveragerc`

```ini
[run]
branch = True
source = app
omit =
    tests/*
    */__init__.py

[report]
show_missing = True
fail_under = 80
```

### CI command

```bash
pytest
```

### Why this setup is good
- simple local workflow
- shared configuration
- consistent CI behavior
- enforced threshold

---

## 33. Practical mental model

A useful mental model is:

- **coverage** tells you what code was exercised
- **thresholds** define the minimum acceptable level
- **CI** enforces those expectations automatically

So the real value is not just getting a number.  
The real value is building a repeatable quality gate for the team.

---

## 34. Final recommendation

When adding coverage and CI integration to a Python project:

- use `pytest-cov`
- enable branch coverage if possible
- generate useful reports
- define a realistic threshold
- enforce it in CI
- treat coverage as one part of a broader quality strategy

This gives you a much more reliable testing workflow as the project grows.

---

## 35. Quick summary

If you only keep the essentials:

1. Coverage shows which code ran during tests.
2. `pytest-cov` is the usual way to measure coverage with pytest.
3. Branch coverage is often more informative than only line coverage.
4. Coverage thresholds can fail CI when standards drop.
5. CI integration makes coverage enforcement automatic and consistent.

---
