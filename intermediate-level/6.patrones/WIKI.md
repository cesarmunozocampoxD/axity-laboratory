# Python Design Patterns Wiki

## 1. Purpose

This wiki gives a medium-length overview of four major groups of design patterns in a **Pythonic** style:

- **Creational patterns**: Factory, Abstract Factory, Builder, Singleton, and when to avoid Singleton
- **Structural patterns**: Adapter, Facade, Composite, Decorator, Proxy
- **Behavioral patterns**: Strategy, Observer, Command, Mediator, Template Method, State
- **Idiomatic Python patterns**: decorators and context managers

The goal is not to memorize names.  
The goal is to understand:

- what problem each pattern solves
- when it helps
- when it is unnecessary
- how it usually looks in Python
- what trade-offs it introduces

A good pattern should make code easier to change and easier to reason about.  
If it only adds ceremony, it is probably the wrong tool.

---

## 2. A Pythonic note before starting

Python supports many of these patterns naturally, but often in lighter forms than class-heavy languages.

That means:

- a function may replace a formal factory class
- a protocol or duck-typed object may replace a deep interface hierarchy
- a context manager may express resource control better than a large pattern abstraction
- composition usually matters more than inheritance-heavy frameworks

So the question is not:

> “Can I apply the pattern?”

The better question is:

> “Does this pattern make the code clearer and more maintainable here?”

---

# Part I — Creational Patterns

## 3. What creational patterns are

Creational patterns are about **how objects are created**.

They become useful when object creation is no longer trivial, for example when:

- creation depends on configuration
- multiple implementations exist
- object construction is complex
- object lifecycle should be controlled
- you want to hide construction details from the caller

---

## 4. Factory

### Core idea
A **Factory** centralizes object creation.

Instead of scattering `if/elif` logic or direct constructors everywhere, you put creation in one place.

### Example problem
You want different notifiers:

- email
- SMS
- push

Naive approach:

```python
if channel == "email":
    notifier = EmailNotifier()
elif channel == "sms":
    notifier = SmsNotifier()
```

A factory moves this logic into one creation function or object.

### Pythonic interpretation
In Python, a factory is often just:
- a function
- a dictionary registry
- a small provider object

It does not always need a dedicated “Factory” class.

### When it helps
Use Factory when:
- creation varies by input or config
- creation logic repeats
- callers should not know concrete classes
- you want one stable creation entry point

### When it is too much
Do not create a factory for every trivial constructor.  
If `User(name)` is already clear, a `UserFactory.create(name)` may add no value.

---

## 5. Abstract Factory

### Core idea
An **Abstract Factory** creates **families of related objects**.

This is different from simple Factory because the goal is not only to create one thing, but to create a **coherent set** of related things.

### Example
Suppose you support:
- Light UI theme
- Dark UI theme

For each theme, you need:
- button
- dialog
- input

A Light factory creates all the light components.  
A Dark factory creates all the dark components.

### Why it helps
It keeps related families consistent.

### Pythonic interpretation
In Python, this may be:
- a class with matching methods
- a protocol describing the factory behavior
- a module acting as a “family provider”
- a configuration-based provider object

### When it helps
Use Abstract Factory when:
- multiple related product families exist
- all the chosen objects must fit together
- a whole environment or backend is selected as one package

### When it is too much
If you only vary one object type, you probably just need Factory, not Abstract Factory.

---

## 6. Builder

### Core idea
A **Builder** constructs an object step by step.

This is useful when:
- an object has many optional parts
- construction is staged
- validation should happen before the final object is returned
- a fluent style improves clarity

### Example
A report may include:
- title
- theme
- summary
- graphs
- export format

A Builder can make that construction more readable than a very long constructor.

### Pythonic interpretation
Python often reduces the need for Builder because it already supports:
- keyword arguments
- default values
- `dataclass`
- helper functions

So Builder is most useful when the construction flow itself matters, not just the parameter list.

### When it helps
Use Builder when:
- object construction is genuinely multi-step
- optional combinations are many
- the build process needs validation or ordering

### When it is too much
If a `dataclass` or a simple constructor already expresses the object clearly, a Builder may just add noise.

---

## 7. Singleton

### Core idea
A **Singleton** ensures there is only one instance of a class in a process and gives global access to it.

### Why people use it
Common motivations include:
- one config object
- one logger
- one cache manager
- one service registry

### Why it is dangerous
Singleton often introduces:
- hidden global state
- poor testability
- order-dependent behavior
- implicit coupling
- surprising shared state between tests or modules

### When to avoid it
Singleton should usually be avoided when:
- explicit dependency injection is possible
- you mainly want convenience, not true single-instance semantics
- test isolation matters
- shared mutable state would be risky

### Better alternatives
In Python, better alternatives often include:
- creating one instance at the application boundary
- passing it explicitly where needed
- using provider/factory wiring
- using a module-level object when appropriate and controlled

### Practical rule
If the real desire is “easy access everywhere,” that is often a warning sign.

---

# Part II — Structural Patterns

## 8. What structural patterns are

Structural patterns are about **how objects fit together**.

They help when the problem is about:
- adapting interfaces
- simplifying subsystems
- combining objects into trees
- wrapping behavior
- controlling access to another object

---

## 9. Adapter

### Core idea
An **Adapter** makes one interface look like another expected interface.

### Example
Your app expects:

```python
sender.send(message)
```

But a third-party library offers:

```python
client.post_message(text)
```

An Adapter wraps the third-party client so the application can keep using the interface it expects.

### Why it helps
It isolates integration mismatch.

### Pythonic interpretation
An Adapter may be:
- a small wrapper class
- a function wrapper
- a callable object

### When it helps
Use Adapter when:
- you cannot change the original interface
- you want stable internal contracts
- you are integrating external or legacy systems

---

## 10. Facade

### Core idea
A **Facade** gives a simplified interface to a more complex subsystem.

### Example
Sending a notification may involve:
- formatting
- choosing a channel
- logging
- retry handling
- metrics

A Facade may expose:

```python
notification_service.notify(user, message)
```

instead of making every caller coordinate all those steps.

### Why it helps
It hides complexity and reduces coupling to subsystem details.

### Pythonic interpretation
A Facade may be:
- a service class
- a module-level function
- a small orchestration object

### When it helps
Use Facade when:
- many callers need the same orchestration
- the subsystem is too hard to use directly
- you want a stable simplified entry point

---

## 11. Composite

### Core idea
A **Composite** lets you treat individual objects and groups of objects in a uniform way.

### Example
A file system has:
- files
- folders containing files and folders

If both support something like `get_size()`, callers can work with either without caring whether they are looking at a leaf or a container.

### Why it helps
It makes hierarchical structures easier to traverse and reason about.

### Pythonic interpretation
Composite often appears naturally in:
- trees
- nested nodes
- recursive structures
- UI hierarchies

### When it helps
Use Composite when:
- you have a true part-whole hierarchy
- single items and groups should share the same interface

---

## 12. Decorator

### Core idea
A **Decorator** adds behavior to an object by wrapping it rather than modifying the original class.

### Example
A text renderer may be wrapped with:
- bold
- italic
- uppercase

Multiple decorators can be layered.

### Why it helps
It avoids subclass explosion and supports composable behavior extension.

### Pythonic note
This is related to Python’s `@decorator` syntax, but they are not identical concepts.

- **Decorator pattern** → object wrapper pattern
- **Python decorator syntax** → function/class wrapper syntax

Both share the same core idea: wrap behavior.

### When it helps
Use Decorator when:
- behavior should be added dynamically
- many combinations are possible
- inheritance would create too many subclasses

---

## 13. Proxy

### Core idea
A **Proxy** stands in front of another object and controls access to it.

### Typical uses
- lazy loading
- access control
- caching
- logging
- remote access mediation

### Example
An image proxy may delay loading the real image until `display()` is actually called.

### Why it helps
It adds control without changing the caller-facing interface much.

### Difference from Decorator
- **Decorator** mainly adds responsibilities
- **Proxy** mainly controls access

That distinction matters more than exact syntax.

---

# Part III — Behavioral Patterns

## 14. What behavioral patterns are

Behavioral patterns are about **how objects behave and collaborate**.

They are useful when the problem is about:
- choosing algorithms
- reacting to events
- packaging actions
- reducing collaboration tangles
- varying steps in workflows
- changing behavior by state

---

## 15. Strategy

### Core idea
A **Strategy** encapsulates interchangeable algorithms or behaviors.

### Example
Discount calculation may vary by:
- regular customer
- VIP customer
- employee

Instead of filling one function with many `if/elif` branches, each discount rule can become its own strategy.

### Pythonic interpretation
In Python, Strategy is often just:
- a function
- a callable object
- a protocol-based behavior object

### When it helps
Use Strategy when:
- one task has multiple interchangeable behaviors
- variation is growing
- you want cleaner testing of each behavior

---

## 16. Observer

### Core idea
An **Observer** lets multiple listeners react when something changes.

### Example
When an order is placed, several things may react:
- email notification
- analytics
- audit logging
- inventory update

Observer avoids hardcoding every reaction directly into the order logic.

### Pythonic interpretation
Observer can appear as:
- callback lists
- event handlers
- pub/sub patterns
- signal systems

### When it helps
Use Observer when:
- one event source has many listeners
- you want looser coupling between the producer and reactions

### Caution
Too much Observer usage can create hidden event flow that becomes difficult to trace.

---

## 17. Command

### Core idea
A **Command** turns an action into an object.

### Why it helps
This is useful when actions need to be:
- queued
- retried
- logged
- scheduled
- passed around
- undone/redone in some designs

### Pythonic interpretation
In Python, a Command may be:
- a function
- a callable object
- a small class with `execute()`

### When it helps
Use Command when actions need lifecycle or metadata, not just immediate execution.

---

## 18. Mediator

### Core idea
A **Mediator** centralizes communication between objects so they do not all talk to each other directly.

### Example
If many UI components or services all know too much about each other, a Mediator can become the coordination point.

### Why it helps
It reduces many-to-many coupling.

### Caution
Mediator can become a “god object” if it absorbs too much logic.

### When it helps
Use Mediator when collaboration itself is the complexity problem.

---

## 19. Template Method

### Core idea
A **Template Method** defines the skeleton of an algorithm while allowing subclasses to vary some steps.

### Example
All report generation may follow:
1. fetch data
2. transform data
3. export result

Different subclasses vary the details of fetching or formatting.

### Pythonic interpretation
Python often prefers composition or Strategy instead of inheritance-heavy Template Method usage.

### When it helps
Use Template Method when:
- the step order is fixed
- only some steps vary
- the algorithm skeleton is central

---

## 20. State

### Core idea
A **State** pattern changes behavior depending on the object’s current state.

### Example
An order may be:
- pending
- paid
- shipped
- cancelled

Different actions are valid or invalid depending on that state.

### Why it helps
It avoids giant state-based conditionals and localizes behavior by state.

### When it helps
Use State when:
- behavior really changes by lifecycle phase
- transitions matter
- conditionals are becoming large and repetitive

### Difference from Strategy
- **Strategy** = choose an algorithm
- **State** = behavior changes because the object is in a different lifecycle condition

---

# Part IV — Idiomatic Python Patterns

## 21. Decorators

### What they are
Python decorators wrap functions, methods, or classes to add behavior.

Typical uses:
- logging
- timing
- caching
- retries
- auth checks
- registration

### Why they matter
Decorators are one of the most Pythonic ways to express reusable cross-cutting behavior.

### Good practice
Use decorators when:
- the added behavior is reusable
- wrapping keeps the core function clearer
- the behavior is orthogonal to the main business logic

### Caution
Too many stacked decorators can make behavior harder to follow.

---

## 22. Context managers

### What they are
Context managers control setup and cleanup around a block of code using `with`.

Typical uses:
- files
- DB sessions
- locks
- temporary configuration changes
- managed resources

### Why they matter
They make cleanup reliable, even if an exception happens.

### Pythonic significance
Context managers are one of the strongest examples of Python offering a language-native pattern for safe resource handling.

### Good fit
Use `with` when:
- a block defines a natural lifecycle
- setup and cleanup should be guaranteed
- the code would otherwise require `try/finally`

---

# Part V — How These Patterns Relate

## 23. Practical selection guide

A practical way to choose among patterns is:

- **Factory** → “Which object should I create?”
- **Abstract Factory** → “Which related family of objects should I create?”
- **Builder** → “How do I assemble this complex object?”
- **Singleton** → “Do I really need a single instance, or am I hiding global state?”

- **Adapter** → “How do I make this interface fit?”
- **Facade** → “How do I simplify this subsystem?”
- **Composite** → “How do I treat leaves and groups uniformly?”
- **Decorator** → “How do I add behavior around this?”
- **Proxy** → “How do I control access to this?”

- **Strategy** → “How should this task be done?”
- **Observer** → “Who should react when this happens?”
- **Command** → “How do I package this action?”
- **Mediator** → “How do I reduce tangled communication?”
- **Template Method** → “How do I keep the workflow skeleton while varying steps?”
- **State** → “How should behavior change with lifecycle state?”

- **Decorators / context managers** → “How do I express Python behavior and resource patterns idiomatically?”

---

## 24. Common mistakes across patterns

A few mistakes appear again and again:

- using patterns just because they are famous
- introducing abstractions before real variation exists
- forcing inheritance where composition would be better
- turning simple Python code into ceremony-heavy code
- using Singleton for convenience instead of real lifecycle need
- confusing event-driven decoupling with hidden system behavior

A good pattern reduces complexity.  
A bad pattern relocates complexity and gives it a fancy name.

---

## 25. Final recommendations

A practical Pythonic approach is:

1. Start simple.
2. Add a pattern only when a real design pressure appears.
3. Prefer composition over deep inheritance.
4. Use functions and protocols where they express the idea more naturally.
5. Avoid Singleton by default.
6. Use decorators and context managers when they clearly improve clarity and safety.
7. Keep behavior explicit enough that another developer can still follow the flow.

Patterns are not the goal.  
Clear, adaptable, testable code is the goal.

---

## 26. Quick summary

If you only keep the essentials:

- **Creational patterns** help manage object creation.
- **Structural patterns** help organize how objects fit together.
- **Behavioral patterns** help organize how objects act and collaborate.
- **Idiomatic Python patterns** like decorators and context managers express common wrapping and lifecycle ideas naturally.
- In Python, lighter implementations are often better than textbook-heavy ones.
- The best pattern is the one that solves a real problem without adding unnecessary ceremony.

---
