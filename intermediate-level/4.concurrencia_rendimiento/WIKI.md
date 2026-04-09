# Python GIL and Its Implications

## 1. Goal

This guide explains the **GIL** in Python and its practical implications.

It focuses on:

- what the GIL is
- why it exists
- how it affects threads
- CPU-bound vs I/O-bound workloads
- multiprocessing
- async programming
- common misunderstandings
- practical recommendations

The goal is to give you a clear mental model of when the GIL matters and when it does not.

---

## 2. What is the GIL?

**GIL** stands for **Global Interpreter Lock**.

In the standard **CPython** implementation of Python, the GIL is a mechanism that allows only **one thread at a time** to execute Python bytecode within a single process.

This is one of the most discussed characteristics of Python concurrency.

### Simple idea
Even if your program creates multiple threads, only one of those threads can execute Python code at a given instant inside the same CPython process.

---

## 3. Why the GIL exists

The GIL exists mainly to simplify memory management and internal interpreter safety in CPython.

Python objects are shared heavily inside the interpreter, and CPython uses **reference counting** as a core memory management technique.

Without a mechanism like the GIL, operations that update internal object state would require much more complex synchronization.

### In practice
The GIL makes CPython’s implementation:
- simpler
- safer internally
- easier to maintain in some areas

But it also creates trade-offs, especially for CPU-heavy multithreaded code.

---

## 4. Important scope: CPython

When people talk about “Python has a GIL,” they usually mean **CPython**, which is the most common Python implementation.

That statement is not universally true for every Python implementation.

### Why this matters
The GIL is primarily a CPython runtime characteristic, not a universal law of the Python language itself.

In most real-world backend development, though, CPython is what people are using, so the distinction is still practical.

---

## 5. Basic consequence of the GIL

The most important consequence is:

> Multiple threads in one CPython process do not execute Python bytecode in true parallel for CPU-bound work.

This means that if you have several threads all doing heavy computation in Python, they will compete for the GIL instead of fully using multiple CPU cores in parallel.

---

## 6. Does that mean threads are useless?

No.

This is one of the biggest misunderstandings.

Threads are still useful in Python, especially for:
- I/O-bound work
- waiting on files
- waiting on network requests
- waiting on databases
- waiting on external systems

### Why?
Because while one thread is waiting for I/O, the interpreter can switch to another thread.

So even with the GIL, threads can improve responsiveness and throughput for many real workloads.

---

## 7. CPU-bound vs I/O-bound workloads

This distinction is essential.

### CPU-bound
A task is CPU-bound when performance depends mostly on raw computation.

Examples:
- image processing in pure Python
- large mathematical loops
- heavy parsing
- transformations over huge datasets
- compression in Python code

### I/O-bound
A task is I/O-bound when it spends much of its time waiting.

Examples:
- HTTP requests
- reading files
- database queries
- calling external APIs
- waiting for sockets

### Why the distinction matters
The GIL is usually a bigger problem for CPU-bound threaded programs than for I/O-bound threaded programs.

---

## 8. Example mental model

Imagine two threads in one process.

### Case 1: both threads are CPU-bound
They both want to execute Python code intensely.  
They must take turns holding the GIL.

Result:
- no true Python-level parallel execution of bytecode
- limited scaling across cores

### Case 2: both threads are I/O-bound
One thread sends a request and waits.  
During that wait, another thread can run.

Result:
- threads can still be very effective
- the GIL is much less of a bottleneck

---

## 9. Example: CPU-bound threads

```python
import threading


def count():
    total = 0
    for i in range(10_000_000):
        total += i


threads = [threading.Thread(target=count) for _ in range(2)]

for t in threads:
    t.start()

for t in threads:
    t.join()
```

### What to expect
This usually does **not** give the kind of speedup people expect from multithreading on multiple CPU cores.

Why?
Because both threads are doing Python-level computation and competing for the GIL.

---

## 10. Example: I/O-bound threads

```python
import threading
import time


def task():
    time.sleep(2)


threads = [threading.Thread(target=task) for _ in range(5)]

for t in threads:
    t.start()

for t in threads:
    t.join()
```

### Why this can still help
The threads spend most of their time waiting, so the GIL is not the main bottleneck here.

This is why threading can work well for concurrent waiting tasks.

---

## 11. How thread switching works

CPython does not let one thread keep the GIL forever.  
The interpreter periodically gives other threads a chance to run.

This improves fairness, but it does not change the core limitation:
only one thread executes Python bytecode at a time within the same process.

---

## 12. Does the GIL block everything?

Not exactly.

The GIL controls execution of Python bytecode in CPython, but some operations may release the GIL internally.

This can happen in:
- blocking I/O operations
- some C extensions
- some numerical libraries
- some system calls

### Why this matters
A library written in C may release the GIL while doing heavy native work, which allows other threads to run.

This is one reason why some numeric or scientific workloads can still scale well despite the GIL.

---

## 13. Native extensions and the GIL

Many high-performance libraries avoid part of the GIL problem by doing heavy work in optimized native code.

Examples often include libraries that:
- release the GIL during internal C-level computation
- perform vectorized operations outside regular Python loops
- move work to compiled code

### Practical implication
A Python program that uses such libraries may benefit from concurrency more than pure-Python CPU loops would suggest.

This is an important nuance.

---

## 14. Multiprocessing as a workaround

When you need true CPU parallelism in Python, a common solution is **multiprocessing**.

Why?
Because separate processes have separate Python interpreters and separate GILs.

### Result
Multiple processes can run on multiple CPU cores at the same time.

---

## 15. Example with multiprocessing

```python
from multiprocessing import Process


def count():
    total = 0
    for i in range(10_000_000):
        total += i


processes = [Process(target=count) for _ in range(2)]

for p in processes:
    p.start()

for p in processes:
    p.join()
```

### Why this is different
Each process has its own interpreter state, so CPU-bound work can run truly in parallel across cores.

---

## 16. Trade-offs of multiprocessing

Multiprocessing avoids the GIL bottleneck for CPU-bound work, but it has costs.

Common trade-offs:
- more memory usage
- process startup overhead
- more complex inter-process communication
- serialization costs
- harder shared-state coordination

### Practical point
Multiprocessing is powerful, but not free.

---

## 17. Threading vs multiprocessing

### Use threading when:
- tasks are mostly waiting on I/O
- you need lightweight concurrency
- shared memory inside one process is useful
- responsiveness matters more than CPU scaling

### Use multiprocessing when:
- tasks are CPU-bound
- you need real parallelism across cores
- the overhead is acceptable

This is one of the most common practical rules in Python concurrency.

---

## 18. GIL and async programming

`asyncio` is often discussed together with the GIL, but they solve different problems.

### Important distinction
- **GIL** is about thread execution in CPython
- **asyncio** is about cooperative concurrency in a single thread

Async programming does **not** remove the GIL.

However, async code can still be extremely effective for I/O-bound systems because it avoids blocking while waiting.

---

## 19. Async is not parallel CPU execution

Consider a web server handling thousands of network connections.

Async can work very well because most of the time is spent waiting for:
- sockets
- databases
- external APIs

This is concurrency, not CPU parallelism.

### Key idea
Async helps you manage many waiting operations efficiently.  
It does not make CPU-heavy Python code run in parallel across cores by itself.

---

## 20. GIL and web backends

In web development, the GIL is often less catastrophic than beginners fear.

Why?
Because many backend workloads are heavily I/O-bound:
- HTTP handling
- database access
- cache calls
- messaging systems
- file/network waits

That is why threaded or async web servers can still perform well in practice.

### But
If a web request triggers heavy CPU work in pure Python, the GIL can become a real bottleneck.

---

## 21. GIL and data processing

The GIL becomes more visible in workloads like:
- CPU-heavy loops in pure Python
- text processing at scale
- custom parsers
- large transformation pipelines written in Python loops
- algorithm-heavy code

In these cases, simply adding threads often does not solve the performance problem.

Better options may be:
- multiprocessing
- vectorized libraries
- compiled extensions
- algorithmic improvements
- moving critical code to faster native implementations

---

## 22. Common misunderstandings

### Misunderstanding 1: “Python cannot do concurrency”
False.

Python can absolutely do concurrency:
- threads
- async I/O
- multiprocessing
- subprocess orchestration
- distributed systems

The GIL affects one specific area: CPU-bound multithreaded execution in CPython.

### Misunderstanding 2: “Threads never help in Python”
False.

Threads can help a lot for I/O-bound workloads.

### Misunderstanding 3: “Async solves the GIL”
False.

Async is a different concurrency model.  
It helps with I/O efficiency, not CPU parallelism by itself.

### Misunderstanding 4: “The GIL means Python is always slow”
False.

Performance depends heavily on workload, libraries, architecture, and where the real bottlenecks are.

---

## 23. Example decision guide

Suppose you have one of these tasks.

### Many HTTP requests to external APIs
Prefer:
- threads
- async I/O

### Heavy numerical computation in pure Python
Prefer:
- multiprocessing
- native/compiled libraries
- vectorization

### A web app with database queries and API calls
Prefer:
- async or threads, depending on stack
- multiple worker processes for scaling

### Image or data processing pipeline
Consider:
- multiprocessing
- NumPy or other optimized libraries
- offloading critical work

---

## 24. GIL and multiple processes in production

Many production Python systems scale using multiple worker processes.

Examples:
- web servers with multiple workers
- background job workers
- task queues
- process-based execution pools

This is one of the reasons Python remains practical at scale despite the GIL.

The GIL limits one process.  
It does not prevent horizontal scaling or multi-process scaling.

---

## 25. When the GIL matters most

The GIL matters most when all of these are true:
- you are using CPython
- you are using threads
- the workload is CPU-bound
- the heavy work is happening in Python bytecode
- you expect multi-core speedup from threads

That combination is where the disappointment usually happens.

---

## 26. When the GIL matters less

The GIL matters less when:
- the workload is I/O-bound
- the program spends much time waiting
- heavy work is done in native extensions that release the GIL
- you use multiple processes
- you use async for high-concurrency I/O

This is why many Python systems function very well in production.

---

## 27. Performance thinking beyond the GIL

It is easy to blame the GIL too quickly.

In practice, performance problems may come from:
- poor algorithms
- unnecessary I/O
- slow database queries
- too much serialization
- inefficient network design
- excessive memory use
- poor batching

### Practical lesson
Do not assume the GIL is the bottleneck until you measure.

Profiling matters.

---

## 28. Measuring before optimizing

Before redesigning around the GIL, ask:
- Is the workload CPU-bound or I/O-bound?
- Where is time actually being spent?
- Are threads really the issue?
- Would batching, caching, or algorithm changes help more?
- Would a native library solve the hotspot?

The best optimization choice depends on evidence, not only theory.

---

## 29. Practical recommendations

### For I/O-bound tasks
Use:
- `threading`
- `concurrent.futures.ThreadPoolExecutor`
- `asyncio`, when appropriate

### For CPU-bound tasks
Use:
- `multiprocessing`
- `concurrent.futures.ProcessPoolExecutor`
- optimized native libraries
- vectorized approaches when available

### For web apps
Use:
- async or threads for I/O concurrency
- multiple worker processes for scaling
- offload CPU-heavy jobs when needed

---

## 30. Simple rule of thumb

A practical shortcut is:

- **waiting work** → threads or async
- **heavy computation** → processes or native code

This is not perfect in every case, but it is a very strong default mental model.

---

## 31. The future and GIL discussions

The GIL is a long-running topic in the Python ecosystem, and there have been ongoing efforts and discussions around improving or changing this area.

However, regardless of interpreter evolution, the important practical skill is understanding:
- what your workload looks like
- which concurrency model fits it
- how to choose the right tool

That understanding matters more than memorizing slogans about the GIL.

---

## 32. Best practices

### 1. Understand the workload first
Always distinguish CPU-bound from I/O-bound tasks.

### 2. Do not expect thread-based CPU scaling in CPython
That assumption often leads to disappointment.

### 3. Measure performance
Use profiling and benchmarking before making architectural changes.

### 4. Use the right concurrency model
Threads, async, and multiprocessing solve different problems.

### 5. Offload hotspots when needed
Sometimes the best fix is moving critical work to optimized libraries or separate workers.

---

## 33. Common mistakes

### 1. Using threads for pure Python CPU-heavy loops and expecting multi-core speedup
This is one of the most common GIL-related mistakes.

### 2. Blaming the GIL without measuring
Sometimes the real bottleneck is elsewhere.

### 3. Thinking async removes the GIL
It does not.

### 4. Ignoring process-based scaling
Multiprocessing is a standard and practical solution.

### 5. Overcomplicating architecture too early
Sometimes the workload does not actually justify a more complex concurrency model.

---

## 34. Practical mental model

A useful mental model is:

- the GIL limits **Python bytecode execution by threads inside one CPython process**
- it hurts most for **CPU-bound threaded work**
- it matters much less for **I/O-bound concurrency**
- true multi-core CPU parallelism usually means **multiple processes** or **native code**

That mental model is enough for many real engineering decisions.

---

## 35. Final recommendation

When thinking about the GIL, do not reduce the conversation to “Python threads are bad.”

A better conclusion is:

- threads are good for waiting-heavy tasks
- async is good for managing many I/O operations efficiently
- processes are good for CPU parallelism
- profiling should guide the decision

That is the most practical way to think about the GIL in real systems.

---

## 36. Quick summary

If you only keep the essentials:

1. The GIL is a CPython mechanism that allows only one thread at a time to execute Python bytecode in a process.
2. It mainly limits CPU-bound multithreaded Python code.
3. Threads still work well for I/O-bound tasks.
4. Async does not remove the GIL, but it helps with high-concurrency I/O.
5. Multiprocessing is a common way to achieve real CPU parallelism in Python.

---

# Python: `threading` and `concurrent.futures`

## 1. Goal

This guide explains two important Python tools for concurrency:

- **`threading`**
- **`concurrent.futures`**

It focuses on:

- what each module is for
- when to use each one
- threads and task execution
- `ThreadPoolExecutor`
- `ProcessPoolExecutor`
- futures
- result handling
- common patterns
- practical recommendations

The goal is to give you a clear mental model for choosing between low-level thread management and higher-level executor-based concurrency.

---

## 2. What is `threading`?

`threading` is Python’s standard library module for working directly with threads.

It gives you lower-level control over:
- creating threads
- starting threads
- joining threads
- synchronization primitives
- locks
- events
- conditions
- semaphores

### In simple terms
`threading` is useful when you want explicit control over how threads are created and coordinated.

---

## 3. What is `concurrent.futures`?

`concurrent.futures` is a higher-level standard library API for asynchronous task execution.

It provides executors such as:
- `ThreadPoolExecutor`
- `ProcessPoolExecutor`

It also provides **Future** objects to represent work that may finish later.

### In simple terms
`concurrent.futures` lets you think more in terms of:
- submitting tasks
- getting results
- managing pools of workers

instead of manually managing individual threads or processes.

---

## 4. Relationship between them

These modules are related, but they work at different abstraction levels.

### `threading`
Lower-level and more manual.

### `concurrent.futures`
Higher-level and more task-oriented.

A practical way to think about it is:

- use `threading` when you need fine-grained thread control
- use `concurrent.futures` when you mainly want to run tasks concurrently and collect results

---

## 5. When concurrency helps

Concurrency is often useful when:
- tasks wait on I/O
- you want multiple tasks progressing at once
- you need background work
- you need to process multiple independent jobs

Examples:
- downloading multiple URLs
- processing many files
- calling several APIs
- background monitoring
- parallelizing independent tasks

---

## 6. Reminder about the GIL

In CPython, threads do not provide true parallel execution of Python bytecode for CPU-bound tasks inside one process.

### Practical implication
- threads are often great for **I/O-bound** tasks
- processes are usually better for **CPU-bound** tasks

This is why `concurrent.futures` includes both:
- thread pools
- process pools

---

## 7. Basic `threading` example

```python
import threading


def task():
    print("Task is running")


thread = threading.Thread(target=task)
thread.start()
thread.join()
```

### What happens here
- a new thread is created
- `task()` runs in that thread
- `join()` waits until the thread finishes

---

## 8. Why `join()` matters

Without `join()`, the main thread may continue before the worker thread finishes.

Example:

```python
import threading
import time


def task():
    time.sleep(2)
    print("Done")


thread = threading.Thread(target=task)
thread.start()
thread.join()

print("Main finished")
```

### Meaning
`join()` ensures that the main flow waits for the thread’s completion when needed.

---

## 9. Multiple threads with `threading`

```python
import threading
import time


def task(name):
    print(f"Starting {name}")
    time.sleep(1)
    print(f"Finished {name}")


threads = []

for i in range(3):
    thread = threading.Thread(target=task, args=(f"task-{i}",))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
```

### What this shows
- manual creation of several threads
- manual start
- manual tracking in a list
- manual join of each thread

This works, but it can become verbose in larger programs.

---

## 10. Common use cases for `threading`

`threading` is useful when you need:
- long-running background threads
- explicit thread lifecycle control
- thread synchronization primitives
- worker loops
- producer-consumer coordination
- daemon threads
- events and custom coordination logic

If your need is mostly “run many independent tasks and get results,” `concurrent.futures` is often simpler.

---

## 11. Daemon threads

A daemon thread runs in the background and does not keep the program alive by itself.

```python
import threading
import time


def background_task():
    while True:
        print("Monitoring...")
        time.sleep(1)


thread = threading.Thread(target=background_task, daemon=True)
thread.start()

time.sleep(3)
print("Main exiting")
```

### Why useful
Daemon threads are often used for:
- monitoring
- background housekeeping
- lightweight background helpers

### Important
Daemon threads may stop abruptly when the main program exits.

---

## 12. Synchronization basics

When multiple threads share mutable state, synchronization matters.

Without protection, race conditions can happen.

Example shared state problem:

```python
import threading

counter = 0


def increment():
    global counter
    for _ in range(100000):
        counter += 1
```

If multiple threads modify shared data without coordination, results can become inconsistent.

---

## 13. Locks with `threading.Lock`

A lock protects critical sections.

```python
import threading

counter = 0
lock = threading.Lock()


def increment():
    global counter
    for _ in range(100000):
        with lock:
            counter += 1
```

### Why useful
The lock ensures only one thread at a time enters the protected block.

### Important
Locks improve correctness, but excessive locking can reduce concurrency and increase complexity.

---

## 14. Other synchronization primitives

`threading` also provides:
- `RLock`
- `Event`
- `Condition`
- `Semaphore`
- `Barrier`

### Quick intuition
- `Lock` → mutual exclusion
- `Event` → signal that something happened
- `Condition` → wait for a state change
- `Semaphore` → limit concurrent access count
- `Barrier` → wait until a group reaches the same point

These are useful for more advanced coordination patterns.

---

## 15. `Event` example

```python
import threading
import time

event = threading.Event()


def worker():
    print("Worker waiting")
    event.wait()
    print("Worker resumed")


thread = threading.Thread(target=worker)
thread.start()

time.sleep(2)
event.set()
thread.join()
```

### What this shows
The worker blocks until another part of the program signals the event.

---

## 16. Limitations of manual `threading`

Direct `threading` gives power, but also responsibility.

Common drawbacks:
- more boilerplate
- manual lifecycle management
- manual result collection
- harder error handling
- more coordination complexity

This is where `concurrent.futures` often becomes a better choice for task-oriented workloads.

---

## 17. `concurrent.futures` overview

The main executors are:

- `ThreadPoolExecutor`
- `ProcessPoolExecutor`

They let you:
- submit tasks
- run multiple tasks through a worker pool
- get results via Future objects
- avoid manually creating each worker

---

## 18. What is a `Future`?

A **Future** represents work that may complete later.

A Future can hold:
- a result
- an exception
- a completion state

You can ask a Future:
- is it done?
- what was the result?
- did it raise an error?

This makes async task handling much cleaner.

---

## 19. Basic `ThreadPoolExecutor` example

```python
from concurrent.futures import ThreadPoolExecutor


def square(x):
    return x * x


with ThreadPoolExecutor(max_workers=3) as executor:
    future = executor.submit(square, 4)
    result = future.result()

print(result)
```

### What happens here
- a task is submitted to the thread pool
- `future` represents the pending computation
- `future.result()` waits and returns the result

---

## 20. Why executors are convenient

Compared with manual threading, executors give you:
- automatic worker pool management
- simpler task submission
- cleaner result retrieval
- easier scaling for many independent jobs

This is often the most convenient way to do concurrent task execution in Python.

---

## 21. Submitting multiple tasks

```python
from concurrent.futures import ThreadPoolExecutor


def square(x):
    return x * x


with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(square, i) for i in range(5)]

    results = [future.result() for future in futures]

print(results)
```

### Result
This collects results from multiple submitted tasks.

---

## 22. Using `map()`

Executors also support `map()`.

```python
from concurrent.futures import ThreadPoolExecutor


def square(x):
    return x * x


with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(square, [1, 2, 3, 4, 5]))

print(results)
```

### Why useful
`map()` is concise when:
- the same function is applied to many inputs
- you want results in input order

---

## 23. `submit()` vs `map()`

### `submit()`
Better when:
- inputs are irregular
- you want per-task control
- you want to inspect each Future
- you want custom completion handling

### `map()`
Better when:
- one function applies to many inputs
- you want a simpler style
- ordered results are acceptable

This distinction is practical and common.

---

## 24. Handling task completion with `as_completed`

Sometimes you want results as soon as each task finishes, not in submission order.

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


def task(x):
    time.sleep(1 / (x + 1))
    return x


with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(task, i) for i in range(5)]

    for future in as_completed(futures):
        print(future.result())
```

### Why useful
This lets you process fast-completing tasks immediately.

---

## 25. Exception handling with futures

If a submitted task raises an exception, the Future stores it.

```python
from concurrent.futures import ThreadPoolExecutor


def divide(x):
    return 10 / x


with ThreadPoolExecutor(max_workers=2) as executor:
    future = executor.submit(divide, 0)

    try:
        result = future.result()
    except ZeroDivisionError:
        print("Task failed")
```

### Important
Exceptions do not disappear.  
They are re-raised when you access `future.result()`.

---

## 26. `ThreadPoolExecutor`

`ThreadPoolExecutor` uses threads.

### Best for
- I/O-bound work
- network calls
- file operations
- database waits
- lightweight background tasks

### Less ideal for
- CPU-heavy pure Python work

This is where the GIL matters.

---

## 27. `ProcessPoolExecutor`

`ProcessPoolExecutor` uses separate processes.

### Best for
- CPU-bound work
- heavy computation
- tasks that benefit from multiple CPU cores

### Trade-offs
- more overhead
- more memory usage
- serialization requirements
- slower startup than threads

---

## 28. Basic `ProcessPoolExecutor` example

```python
from concurrent.futures import ProcessPoolExecutor


def square(x):
    return x * x


with ProcessPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(square, [1, 2, 3, 4, 5]))

print(results)
```

### Why this matters
For CPU-bound workloads, this can give real parallelism across cores.

---

## 29. Choosing between thread pool and process pool

### Prefer `ThreadPoolExecutor` when:
- work is mostly waiting on I/O
- tasks are lightweight
- you need shared memory in one process
- startup overhead should stay low

### Prefer `ProcessPoolExecutor` when:
- work is CPU-bound
- true parallelism matters
- process overhead is acceptable

This is one of the most important decisions in practical Python concurrency.

---

## 30. Practical comparison

### Manual `threading`
Good when:
- you need direct thread control
- the thread is long-lived
- you need synchronization primitives
- the design is thread-centric rather than task-centric

### `ThreadPoolExecutor`
Good when:
- you have many similar jobs
- you want simpler code
- you want to submit work and get results easily

### `ProcessPoolExecutor`
Good when:
- the work is CPU-heavy
- scaling across cores matters more than overhead

---

## 31. Common pattern: concurrent I/O tasks

Example idea:
- download multiple pages
- query multiple APIs
- read many files

This is a very common use case for `ThreadPoolExecutor`.

```python
from concurrent.futures import ThreadPoolExecutor
import time


def fetch(item):
    time.sleep(1)
    return f"done: {item}"


with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(fetch, ["a", "b", "c", "d"]))

print(results)
```

---

## 32. Common pattern: CPU task batch

This is a common use case for `ProcessPoolExecutor`.

```python
from concurrent.futures import ProcessPoolExecutor


def compute(n):
    total = 0
    for i in range(n):
        total += i
    return total


with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(compute, [1000000, 2000000, 3000000]))
```

### Why useful
Each task can run in a separate process and better use multiple CPU cores.

---

## 33. Cancellation and state

Futures support some state inspection and cancellation behavior.

Common methods:
- `future.done()`
- `future.running()`
- `future.cancel()`
- `future.cancelled()`
- `future.result()`
- `future.exception()`

### Important
A task cannot always be cancelled if it has already started running.

---

## 34. Timeouts

You can wait for results with time limits.

```python
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import time


def slow_task():
    time.sleep(5)
    return "done"


with ThreadPoolExecutor(max_workers=1) as executor:
    future = executor.submit(slow_task)

    try:
        result = future.result(timeout=1)
    except TimeoutError:
        print("Timed out")
```

### Why useful
Timeouts help avoid waiting forever for slow or stuck tasks.

---

## 35. Common mistakes

### 1. Using threads for CPU-bound pure Python work and expecting core scaling
This often disappoints because of the GIL.

### 2. Using manual threads when an executor would be simpler
Sometimes lower-level control adds unnecessary complexity.

### 3. Ignoring shared-state risks
Threads sharing mutable data need synchronization.

### 4. Calling `future.result()` immediately after every submit
That can reduce concurrency and make code behave more sequentially than expected.

### 5. Using process pools for tiny tasks
The overhead may be larger than the benefit.

---

## 36. Best practices

### 1. Match the concurrency tool to the workload
- I/O-bound → thread pool or async
- CPU-bound → process pool

### 2. Prefer higher-level APIs when possible
`concurrent.futures` is often easier to maintain than manual thread management.

### 3. Keep shared mutable state to a minimum
This reduces bugs and synchronization needs.

### 4. Handle exceptions from futures explicitly
Do not ignore task failures.

### 5. Use timeouts where appropriate
This improves robustness.

### 6. Profile before optimizing
The best concurrency approach depends on real workload behavior.

---

## 37. Practical mental model

A useful mental model is:

- **`threading`** = manual control over thread lifecycle and coordination
- **`ThreadPoolExecutor`** = easy concurrent task execution with threads
- **`ProcessPoolExecutor`** = easy concurrent task execution with processes for CPU-heavy work
- **Future** = handle to a result that may be ready later

This mental model helps you choose the right abstraction level.

---

## 38. Final recommendation

In many Python projects:

- use `threading` when you need explicit thread coordination or background worker patterns
- use `ThreadPoolExecutor` for most simple I/O-bound concurrent task execution
- use `ProcessPoolExecutor` for CPU-bound batch workloads

If you mainly want “run these jobs and collect results,” `concurrent.futures` is usually the better starting point.

---

## 39. Quick summary

If you only keep the essentials:

1. `threading` gives low-level control over threads and synchronization.
2. `concurrent.futures` gives a higher-level API for task execution.
3. `ThreadPoolExecutor` is usually best for I/O-bound work.
4. `ProcessPoolExecutor` is usually best for CPU-bound work.
5. Futures make result handling, exceptions, and timeouts much easier to manage.

---

# Python `asyncio`: Event Loop and `async`/`await`

## 1. Goal

This guide explains the core ideas behind Python’s asynchronous programming model using **`asyncio`**.

It focuses on:

- what `asyncio` is
- what the event loop does
- how `async` and `await` work
- coroutines
- tasks
- concurrency vs parallelism
- common patterns
- common mistakes
- practical recommendations

The goal is to build a clear mental model of how asynchronous code works in Python.

---

## 2. What is `asyncio`?

`asyncio` is Python’s standard library framework for **asynchronous I/O** and **cooperative concurrency**.

It is designed for programs that spend a lot of time waiting on things like:

- network requests
- sockets
- databases
- file-like I/O operations
- timers
- external services

### In simple terms
`asyncio` helps one thread manage many waiting operations efficiently without blocking on each one in sequence.

---

## 3. Why `asyncio` exists

Imagine a program that needs to:
- call multiple APIs
- wait for database responses
- handle many client connections
- coordinate many I/O-heavy tasks

If each operation blocks normally, the program spends a lot of time idle while waiting.

`asyncio` allows the program to switch to other work while one operation is waiting.

### Result
You can handle many I/O-bound operations efficiently with fewer threads and less blocking.

---

## 4. `asyncio` is about concurrency, not automatic parallelism

This distinction is critical.

### Concurrency
Many tasks can make progress over time by taking turns.

### Parallelism
Multiple tasks literally run at the same instant on different CPU cores.

`asyncio` is mainly about **concurrency**, not CPU parallelism.

### Practical meaning
`asyncio` is excellent for coordinating many waiting tasks, but it does not automatically make CPU-heavy Python code run in parallel across cores.

---

## 5. The event loop

The **event loop** is the core engine of `asyncio`.

It is responsible for:
- running asynchronous tasks
- pausing tasks when they need to wait
- resuming tasks when they are ready
- scheduling callbacks
- coordinating the whole async workflow

### Simple mental model
The event loop is like a traffic controller for asynchronous operations.

It decides:
- what can run now
- what must wait
- what should resume next

---

## 6. Why the event loop matters

Without the event loop, `async` functions would not actually be coordinated.

The event loop is what makes it possible for one thread to:
- start many tasks
- suspend them while they wait
- resume them later
- keep the application responsive

This is the central idea behind `asyncio`.

---

## 7. What is a coroutine?

A **coroutine** is a special kind of function declared with `async def`.

Example:

```python
async def greet():
    return "hello"
```

This function does not behave like a normal function.

Calling it does **not** immediately run its body to completion.

Instead, it returns a **coroutine object** that must be awaited or scheduled.

---

## 8. `async def`

Functions declared with `async def` are asynchronous functions.

Example:

```python
async def fetch_data():
    return {"status": "ok"}
```

When you call:

```python
fetch_data()
```

you do not get the final result directly.  
You get a coroutine object.

To actually execute it, you usually need:
- `await`
- `asyncio.run(...)`
- task scheduling through the event loop

---

## 9. `await`

`await` is used inside async functions to pause until another awaitable completes.

Example:

```python
import asyncio


async def main():
    await asyncio.sleep(1)
    print("done")
```

### What `await` means
It tells the event loop:

> “This operation is waiting. Let other work run until it is ready.”

This is one of the most important ideas in async programming.

---

## 10. Basic example with `asyncio.run`

```python
import asyncio


async def main():
    print("start")
    await asyncio.sleep(1)
    print("end")


asyncio.run(main())
```

### What happens here
- `main()` returns a coroutine object
- `asyncio.run(...)` creates and runs the event loop
- the coroutine is executed
- `asyncio.sleep(1)` pauses without blocking the whole program
- after the pause, execution resumes

---

## 11. Why `asyncio.sleep()` is special

`asyncio.sleep()` is not like `time.sleep()`.

### `time.sleep()`
Blocks the current thread completely.

### `asyncio.sleep()`
Pauses the coroutine and gives control back to the event loop.

This means other async tasks can run while one task is waiting.

That difference is fundamental.

---

## 12. Example: blocking vs non-blocking wait

### Blocking version

```python
import time

def task():
    time.sleep(2)
    print("done")
```

### Async version

```python
import asyncio

async def task():
    await asyncio.sleep(2)
    print("done")
```

The async version lets the event loop run something else during the wait.

---

## 13. Running multiple coroutines concurrently

One of the biggest benefits of `asyncio` is running several waiting tasks concurrently.

Example:

```python
import asyncio


async def task(name, delay):
    print(f"start {name}")
    await asyncio.sleep(delay)
    print(f"end {name}")


async def main():
    await asyncio.gather(
        task("A", 2),
        task("B", 1),
        task("C", 3),
    )


asyncio.run(main())
```

### What this shows
The tasks overlap in time.  
They are not executed in strict sequential blocking style.

---

## 14. `asyncio.gather`

`asyncio.gather(...)` is a common way to run multiple awaitables together.

It:
- schedules them concurrently
- waits until all are finished
- returns their results in input order

Example:

```python
import asyncio


async def square(x):
    await asyncio.sleep(1)
    return x * x


async def main():
    results = await asyncio.gather(
        square(2),
        square(3),
        square(4),
    )
    print(results)


asyncio.run(main())
```

### Result
```python
[4, 9, 16]
```

---

## 15. Tasks

A **Task** is a scheduled coroutine managed by the event loop.

Tasks let a coroutine run independently in the background of the event loop.

Example:

```python
import asyncio


async def worker():
    await asyncio.sleep(1)
    print("worker done")


async def main():
    task = asyncio.create_task(worker())
    print("task created")
    await task


asyncio.run(main())
```

### Why tasks matter
They let you explicitly schedule coroutines instead of only awaiting them immediately.

---

## 16. `asyncio.create_task`

`asyncio.create_task(...)` tells the event loop to start managing a coroutine as a Task.

This is useful when:
- you want work to begin now
- you want multiple things progressing at once
- you want to await the result later

Example:

```python
import asyncio


async def task1():
    await asyncio.sleep(2)
    return "A"


async def task2():
    await asyncio.sleep(1)
    return "B"


async def main():
    t1 = asyncio.create_task(task1())
    t2 = asyncio.create_task(task2())

    result1 = await t1
    result2 = await t2

    print(result1, result2)


asyncio.run(main())
```

---

## 17. Awaiting sequentially vs scheduling concurrently

This difference is very important.

### Sequential style

```python
async def main():
    result1 = await task1()
    result2 = await task2()
```

Here, `task2()` only begins after `task1()` finishes.

### Concurrent style

```python
async def main():
    t1 = asyncio.create_task(task1())
    t2 = asyncio.create_task(task2())

    result1 = await t1
    result2 = await t2
```

Here, both tasks can progress concurrently.

This difference is often the whole reason async code performs better for I/O-heavy workflows.

---

## 18. Awaitables

In async code, an **awaitable** is something you can use with `await`.

Common awaitables include:
- coroutines
- tasks
- futures

You do not need to memorize the theory perfectly at the beginning.  
The practical idea is that `await` works on async-compatible units of work.

---

## 19. Example mental model

Imagine three API calls:
- each takes 2 seconds of waiting time

### Sequential blocking style
Total time is about 6 seconds.

### Async concurrent style
Total time can be about 2 seconds plus overhead.

Why?
Because the waiting overlaps.

This is why async is so valuable for I/O-heavy workflows.

---

## 20. `asyncio` is best for I/O-bound workloads

Typical good use cases:
- HTTP clients
- web servers
- database drivers with async support
- websocket systems
- bots
- crawlers
- event-driven systems

### Less ideal use case
Heavy CPU-bound computation in pure Python.

For CPU-heavy work, async alone is usually not the right solution.

---

## 21. Async does not magically make sync code non-blocking

This is one of the most important warnings.

If you write:

```python
import time

async def bad_task():
    time.sleep(2)
```

the `time.sleep(2)` blocks the thread and blocks the event loop.

### Meaning
Even though the function is declared with `async def`, it still contains blocking code.

This is a very common beginner mistake.

---

## 22. Example of bad async code

```python
import asyncio
import time


async def bad_task():
    print("start")
    time.sleep(2)
    print("end")
```

### Problem
The event loop cannot do other work during `time.sleep(2)`.

### Better version

```python
import asyncio


async def good_task():
    print("start")
    await asyncio.sleep(2)
    print("end")
```

---

## 23. Async and the GIL

`asyncio` does not remove the GIL.

It works within the Python runtime and usually within one thread, but it avoids wasting time on blocking waits by switching between coroutines efficiently.

### Practical implication
Async helps you handle many waiting operations, but it is not a substitute for multiprocessing when you need CPU-bound parallelism.

---

## 24. Exception handling in async code

Exceptions inside awaited coroutines behave much like normal exceptions.

```python
import asyncio


async def broken():
    raise ValueError("Something failed")


async def main():
    try:
        await broken()
    except ValueError as exc:
        print(exc)


asyncio.run(main())
```

### Important
Async code still needs proper error handling.

---

## 25. Exceptions with `gather`

By default, if one coroutine in `asyncio.gather(...)` fails, that exception propagates.

```python
import asyncio


async def ok():
    return "ok"


async def broken():
    raise RuntimeError("fail")


async def main():
    try:
        await asyncio.gather(ok(), broken())
    except RuntimeError as exc:
        print(exc)


asyncio.run(main())
```

You can also use:

```python
return_exceptions=True
```

if you want to collect exceptions as results instead of immediately propagating them.

---

## 26. Timeouts

Async workflows often need timeouts.

Example:

```python
import asyncio


async def slow_task():
    await asyncio.sleep(5)


async def main():
    try:
        await asyncio.wait_for(slow_task(), timeout=1)
    except asyncio.TimeoutError:
        print("Timed out")


asyncio.run(main())
```

### Why useful
Timeouts prevent the program from waiting forever on slow operations.

---

## 27. Cancellation

Tasks can be cancelled.

```python
import asyncio


async def worker():
    try:
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        print("worker cancelled")
        raise


async def main():
    task = asyncio.create_task(worker())
    await asyncio.sleep(1)
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        print("main noticed cancellation")


asyncio.run(main())
```

### Why important
Cancellation is a normal part of async systems, especially in:
- servers
- timeouts
- shutdown flows
- task orchestration

---

## 28. Async context managers

Async code can also use special context managers.

```python
class AsyncResource:
    async def __aenter__(self):
        print("enter")
        return self

    async def __aexit__(self, exc_type, exc, tb):
        print("exit")
```

Usage:

```python
async def main():
    async with AsyncResource():
        print("using resource")
```

This pattern is common in async database sessions, clients, and connections.

---

## 29. Async iterators

There are also async iterators.

```python
class AsyncCounter:
    def __init__(self):
        self.current = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.current >= 3:
            raise StopAsyncIteration
        value = self.current
        self.current += 1
        return value
```

Usage:

```python
async def main():
    async for item in AsyncCounter():
        print(item)
```

This is useful for async streams and event-driven consumption.

---

## 30. Common use pattern in real applications

A typical async application may:
- accept many connections
- schedule async tasks
- await network/database operations
- coordinate timeouts and cancellation
- keep everything moving through the event loop

This is why async is so common in:
- web frameworks
- API clients
- message consumers
- bots
- streaming systems

---

## 31. Common mistakes

### 1. Calling async functions without awaiting or scheduling them
This creates coroutine objects that never actually run.

### 2. Using blocking code inside async functions
This blocks the event loop.

### 3. Thinking async means CPU parallelism
It usually does not.

### 4. Awaiting tasks sequentially when concurrency was intended
This can accidentally remove the benefit of async.

### 5. Ignoring cancellation and timeouts
These are normal parts of async systems.

---

## 32. Best practices

### 1. Use async for I/O-heavy workflows
That is where it shines most.

### 2. Avoid blocking calls inside async functions
Prefer async-compatible libraries and APIs.

### 3. Use `create_task()` or `gather()` intentionally
Understand when work is sequential vs concurrent.

### 4. Handle exceptions, cancellation, and timeouts
Production async code needs them.

### 5. Keep a clear mental model
The event loop schedules coroutines that cooperate by yielding control at `await` points.

---

## 33. Practical mental model

A useful mental model is:

- `async def` creates coroutines
- `await` pauses a coroutine without blocking the whole event loop
- the **event loop** switches between tasks while they wait
- `create_task()` schedules work to run concurrently
- `gather()` waits for multiple tasks together

So async code works because tasks **cooperate** by giving control back when they need to wait.

That is the core idea.

---

## 34. Final recommendation

When learning `asyncio`, focus first on these ideas:

- coroutine = async unit of work
- `await` = pause here and let other work continue
- event loop = scheduler of async work
- async is best for I/O-bound concurrency
- blocking code inside async functions defeats the model

Once those ideas are clear, most of the rest becomes much easier to understand.

---

## 35. Quick summary

If you only keep the essentials:

1. `asyncio` is Python’s framework for asynchronous I/O and cooperative concurrency.
2. The event loop schedules and resumes async tasks.
3. `async def` defines a coroutine.
4. `await` pauses a coroutine without blocking the whole program.
5. Async is especially useful for I/O-bound workloads, not CPU-heavy parallelism.

---

# Python `multiprocessing` for CPU-Bound Workloads

## 1. Goal

This guide explains how to use Python’s **`multiprocessing`** module for **CPU-bound** workloads.

It focuses on:

- why `multiprocessing` matters
- what CPU-bound means
- why threads are often not enough in CPython
- processes vs threads
- `Process`
- `Pool`
- inter-process communication
- shared state considerations
- common patterns
- practical recommendations

The goal is to build a clear mental model for using multiple processes to speed up computation-heavy Python code.

---

## 2. What is a CPU-bound task?

A task is **CPU-bound** when its performance depends mainly on computation rather than waiting.

Examples:
- large numerical loops
- image transformation
- parsing huge datasets
- custom algorithms
- simulations
- heavy text processing
- pure Python data transformations

### Key idea
The CPU is the bottleneck.

The program is spending most of its time calculating, not waiting for network, files, or a database.

---

## 3. Why `multiprocessing` matters in Python

In CPython, threads do not usually give true multi-core speedup for **CPU-bound Python bytecode** because of the **GIL**.

That means:
- threads can be very useful for I/O-bound tasks
- threads are often disappointing for CPU-bound pure Python work

`multiprocessing` solves this by using **separate processes** instead of threads.

### Why that helps
Each process has:
- its own Python interpreter
- its own memory space
- its own GIL

So multiple CPU-heavy tasks can run truly in parallel across multiple CPU cores.

---

## 4. Process vs thread

### Thread
- lighter weight
- shares memory with the same process
- useful for I/O-bound concurrency
- limited by the GIL for CPU-bound Python work

### Process
- heavier than a thread
- separate memory space
- good for CPU-bound parallelism
- can fully use multiple CPU cores

### Practical rule
For **CPU-bound** tasks in Python, processes are often the right default choice.

---

## 5. Simple mental model

A useful mental model is:

- **threads** = multiple workers sharing one interpreter process
- **processes** = multiple independent Python runtimes working in parallel

For heavy computation, the second model is often much more effective.

---

## 6. Basic `multiprocessing` example

```python
from multiprocessing import Process


def compute():
    total = 0
    for i in range(10_000_000):
        total += i
    print(total)


if __name__ == "__main__":
    p = Process(target=compute)
    p.start()
    p.join()
```

### What happens here
- a new process is created
- `compute()` runs in that process
- `join()` waits for it to finish

This is the basic unit of process-based parallelism.

---

## 7. Why `if __name__ == "__main__"` matters

This guard is very important in `multiprocessing`, especially on Windows and macOS spawn-based environments.

```python
if __name__ == "__main__":
    ...
```

### Why?
Because process creation may import the main module again.

Without this guard, code may:
- run multiple times unintentionally
- spawn processes recursively
- behave incorrectly

### Rule
When using `multiprocessing`, always protect the process-starting entry point with:

```python
if __name__ == "__main__":
```

---

## 8. Running multiple processes

```python
from multiprocessing import Process


def worker(n):
    total = 0
    for i in range(n):
        total += i
    print(f"Done: {n}")


if __name__ == "__main__":
    processes = []

    for n in [1_000_000, 2_000_000, 3_000_000]:
        p = Process(target=worker, args=(n,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
```

### What this shows
- multiple independent processes
- each does CPU-heavy work
- the operating system can schedule them across different cores

---

## 9. When `Process` is useful

Using `Process` directly is useful when:
- you want explicit control over each process
- the workload is custom
- you are building a more manual architecture
- you need a few dedicated worker processes

However, for many repeated jobs, `Pool` is often more convenient.

---

## 10. `Pool`

`multiprocessing.Pool` is a higher-level interface for distributing work across worker processes.

It is useful when:
- the same function must be applied to many inputs
- you want a worker pool
- you want easier result collection

### In simple terms
`Pool` is to processes what a thread pool is to threads.

---

## 11. Basic `Pool.map()` example

```python
from multiprocessing import Pool


def square(x):
    return x * x


if __name__ == "__main__":
    with Pool(processes=4) as pool:
        results = pool.map(square, [1, 2, 3, 4, 5])

    print(results)
```

### Result
```python
[1, 4, 9, 16, 25]
```

### Why useful
This is one of the simplest and most common ways to parallelize CPU-heavy independent tasks.

---

## 12. Why `map()` is convenient

`pool.map(function, iterable)` is useful when:
- the same function applies to many inputs
- the inputs are independent
- you want results in the same order as the input

This is a very common pattern in data processing workloads.

---

## 13. `starmap()` for multiple arguments

If the worker function needs multiple arguments, `starmap()` is useful.

```python
from multiprocessing import Pool


def add(a, b):
    return a + b


if __name__ == "__main__":
    with Pool(processes=4) as pool:
        results = pool.starmap(add, [(1, 2), (3, 4), (5, 6)])

    print(results)
```

### Result
```python
[3, 7, 11]
```

---

## 14. `apply()` and `apply_async()`

### `apply()`
Runs one function call in the pool and waits for it.

### `apply_async()`
Runs one function call asynchronously and returns an async result handle.

Example:

```python
from multiprocessing import Pool


def square(x):
    return x * x


if __name__ == "__main__":
    with Pool(processes=2) as pool:
        async_result = pool.apply_async(square, (5,))
        result = async_result.get()

    print(result)
```

### Why useful
`apply_async()` gives you more flexibility when you do not want to block immediately.

---

## 15. Comparing `map()` and `apply_async()`

### Use `map()`
when:
- one function applies to many items
- you want simple code
- ordered results are fine

### Use `apply_async()`
when:
- you want more control
- jobs are submitted dynamically
- you want results later
- you want flexible orchestration

---

## 16. CPU-bound example pattern

Suppose you have a heavy function:

```python
def compute(n):
    total = 0
    for i in range(n):
        total += i * i
    return total
```

Using `Pool.map()`:

```python
from multiprocessing import Pool


def compute(n):
    total = 0
    for i in range(n):
        total += i * i
    return total


if __name__ == "__main__":
    inputs = [5_000_000, 6_000_000, 7_000_000, 8_000_000]

    with Pool(processes=4) as pool:
        results = pool.map(compute, inputs)

    print(results)
```

### Why this works well
Each input is independent and computation-heavy, which is exactly the kind of workload process-based parallelism is good for.

---

## 17. Data must be serializable

When sending work to another process, Python usually needs to **serialize** the function arguments and results.

In practice, this often means objects must be **picklable**.

### Why this matters
Some objects are difficult or impossible to send cleanly between processes, such as:
- open file handles
- live socket connections
- some locks
- certain local or nested objects
- lambdas in some contexts

### Practical lesson
Design process work around:
- simple data
- top-level functions
- serializable inputs and outputs

---

## 18. Top-level functions are usually safest

Worker functions used by `multiprocessing` are safest when defined at module level.

Good:

```python
def compute(x):
    return x * x
```

Less safe in many cases:

```python
def main():
    def compute(x):
        return x * x
```

### Why?
Nested functions are often harder to serialize across process boundaries.

---

## 19. Process startup overhead

Processes are more expensive than threads.

Common costs include:
- starting the process
- copying or initializing interpreter state
- serializing inputs
- collecting outputs

### Practical implication
`multiprocessing` works best when each job is large enough to justify the overhead.

If the tasks are tiny, the process overhead may cancel out the benefit.

---

## 20. Good task granularity matters

A very important performance principle is **task granularity**.

### Too small
Too many tiny tasks create excessive overhead.

### Too large
Too few giant tasks may underuse available cores.

### Practical goal
Choose task sizes that:
- are large enough to justify process cost
- are balanced enough to distribute well

This often requires measurement and experimentation.

---

## 21. Shared memory is not automatic

Unlike threads, processes do **not** share normal Python memory automatically.

If one process changes a variable, another process does not see that change unless you use a dedicated communication or shared-memory mechanism.

### Why this matters
Process-based parallelism avoids many shared-state bugs, but it also makes data sharing more explicit and more expensive.

---

## 22. Inter-process communication

Processes often communicate using:
- `Queue`
- `Pipe`
- shared values/arrays
- managers
- files
- databases
- external brokers

The right choice depends on the workload and architecture.

---

## 23. `Queue` example

A `Queue` is a common way to send data between processes.

```python
from multiprocessing import Process, Queue


def worker(queue):
    result = sum(i * i for i in range(1000))
    queue.put(result)


if __name__ == "__main__":
    queue = Queue()
    p = Process(target=worker, args=(queue,))
    p.start()
    p.join()

    print(queue.get())
```

### Why useful
It provides a simple message-passing model between processes.

---

## 24. `Pipe` example

A `Pipe` is another communication primitive.

```python
from multiprocessing import Process, Pipe


def worker(conn):
    conn.send("done")
    conn.close()


if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    p = Process(target=worker, args=(child_conn,))
    p.start()

    print(parent_conn.recv())
    p.join()
```

### Why useful
It is often good for simple one-to-one process communication.

---

## 25. Shared values and arrays

If you need a small amount of shared state, `multiprocessing` provides shared memory helpers like:
- `Value`
- `Array`

Example:

```python
from multiprocessing import Process, Value


def increment(shared_value):
    for _ in range(1000):
        with shared_value.get_lock():
            shared_value.value += 1


if __name__ == "__main__":
    shared_value = Value("i", 0)

    processes = [Process(target=increment, args=(shared_value,)) for _ in range(4)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    print(shared_value.value)
```

### Important
Shared state across processes is possible, but it introduces coordination complexity, so it should be used carefully.

---

## 26. Managers

`multiprocessing.Manager()` can create shared managed objects like:
- lists
- dicts
- namespaces

Example:

```python
from multiprocessing import Process, Manager


def worker(shared_list, value):
    shared_list.append(value)


if __name__ == "__main__":
    with Manager() as manager:
        shared_list = manager.list()

        processes = [Process(target=worker, args=(shared_list, i)) for i in range(3)]

        for p in processes:
            p.start()

        for p in processes:
            p.join()

        print(list(shared_list))
```

### Trade-off
Managers are convenient, but they are usually slower than simpler message-passing designs.

---

## 27. Prefer message passing over shared mutable state

A strong design rule for `multiprocessing` is:

> Prefer sending inputs and outputs between processes instead of sharing mutable state directly.

### Why?
It usually leads to:
- simpler reasoning
- fewer synchronization bugs
- clearer process boundaries
- better maintainability

This is often one of the biggest conceptual benefits of process-based design.

---

## 28. Error handling in pools

Worker exceptions do not disappear.

For example:

```python
from multiprocessing import Pool


def divide(x):
    return 10 / x


if __name__ == "__main__":
    with Pool(processes=2) as pool:
        try:
            results = pool.map(divide, [2, 1, 0])
        except ZeroDivisionError:
            print("Worker failed")
```

### Why important
You still need proper error handling around parallel jobs.

---

## 29. How many processes should you use?

A common starting point is near the number of CPU cores.

Why?
Because CPU-bound work usually benefits from distributing computation across available cores.

### But
The best number depends on:
- workload size
- memory pressure
- scheduling overhead
- other system activity
- external constraints

### Practical rule
Start around the CPU core count, then benchmark.

---

## 30. `cpu_count()`

Python can help estimate available CPUs.

```python
from multiprocessing import cpu_count

print(cpu_count())
```

### Important
This gives a starting point, not always the perfect number for every workload.

---

## 31. Common use cases

`multiprocessing` is often useful for:
- image processing
- batch data transformation
- scientific computation
- feature extraction
- text analysis
- parallel simulations
- CPU-heavy ETL stages
- custom algorithm execution

It is especially strong when tasks are:
- independent
- computation-heavy
- serializable

---

## 32. When not to use `multiprocessing`

`multiprocessing` may be a poor fit when:
- tasks are mostly I/O-bound
- tasks are too small
- communication cost dominates
- the architecture needs very frequent shared-state updates
- memory overhead is too high

In such cases, better choices may be:
- threads
- async I/O
- vectorized libraries
- single-process optimization
- external distributed systems

---

## 33. `multiprocessing` vs `concurrent.futures.ProcessPoolExecutor`

Both solve similar CPU-bound problems.

### `multiprocessing`
- older, more direct module
- more primitives and explicit process tools
- lower-level flexibility

### `ProcessPoolExecutor`
- higher-level interface
- simpler task-submission model
- future-based result handling

### Practical advice
If you mainly want:
- “run these CPU-heavy tasks in parallel and get results”

then `ProcessPoolExecutor` is often simpler.

If you need:
- lower-level process primitives
- queues, pipes, manual process coordination

then `multiprocessing` is often more appropriate.

---

## 34. Common mistakes

### 1. Forgetting `if __name__ == "__main__"`
This is one of the most common errors.

### 2. Using tiny tasks
The overhead can make performance worse.

### 3. Sending non-picklable objects
This often causes failures or confusing behavior.

### 4. Overusing shared mutable state
This increases complexity and reduces clarity.

### 5. Assuming more processes always means faster
Too many processes can cause overhead, memory pressure, and scheduling inefficiency.

### 6. Ignoring serialization cost
Large data transfer between processes can be expensive.

---

## 35. Best practices

### 1. Use `multiprocessing` mainly for CPU-bound workloads
That is where it usually provides the most value.

### 2. Keep worker functions top-level and simple
This improves compatibility and clarity.

### 3. Design tasks to be independent
Independent tasks parallelize best.

### 4. Benchmark task size and process count
Real performance depends on workload shape.

### 5. Prefer message passing over shared state
This reduces complexity.

### 6. Be careful with large data movement
Sometimes data transfer costs dominate runtime.

### 7. Use higher-level APIs when enough
`Pool` or `ProcessPoolExecutor` is often easier than manual process orchestration.

---

## 36. Practical mental model

A useful mental model is:

- **CPU-bound work** needs real parallelism
- in CPython, **processes** provide that parallelism more reliably than threads
- each process is an isolated worker with its own interpreter and GIL
- the best multiprocessing workloads are **large, independent, serializable tasks**

That mental model is enough to guide many practical design decisions.

---

## 37. Final recommendation

When you have a Python workload that is genuinely CPU-bound:

- first confirm the bottleneck with measurement
- then consider `multiprocessing` if the tasks are large and independent
- start with `Pool.map()` for simple parallel work
- use lower-level primitives only when necessary
- avoid unnecessary shared state and unnecessary process communication

That is usually the most effective way to use `multiprocessing` in real projects.

---

## 38. Quick summary

If you only keep the essentials:

1. `multiprocessing` is a strong option for CPU-bound workloads in Python.
2. It avoids the thread-based GIL limitation by using separate processes.
3. `Pool.map()` is one of the simplest ways to parallelize repeated heavy work.
4. Tasks should be large enough and serializable enough to justify process overhead.
5. Prefer independent tasks and message passing over shared mutable state.

---
# Performance Measurement with `timeit` and `cProfile`

## 1. Goal

This guide explains two essential Python tools for performance measurement:

- **`timeit`**
- **`cProfile`**

It focuses on:

- what each tool is for
- when to use each one
- microbenchmarking vs profiling
- measuring small code snippets
- measuring full program behavior
- reading profiling output
- practical workflows
- common mistakes
- best practices

The goal is to help you measure Python performance more correctly and make better optimization decisions.

---

## 2. Why performance measurement matters

When code feels slow, it is tempting to guess the cause.

That often leads to:
- optimizing the wrong thing
- wasting time
- making code more complex without real benefit
- missing the actual bottleneck

Performance tools help replace guessing with evidence.

### Practical rule
Measure first, optimize second.

---

## 3. Two different questions

`timeit` and `cProfile` answer different kinds of questions.

### `timeit`
Answers:

> “How long does this small operation take?”

### `cProfile`
Answers:

> “Where is my program spending time overall?”

This distinction is very important.

---

## 4. What is `timeit`?

`timeit` is a Python tool for timing **small code snippets** and **micro-operations**.

It is especially useful when you want to compare:
- two implementations
- small functions
- expression-level performance
- repeated operations

### In simple terms
Use `timeit` when you want a controlled benchmark of a specific piece of code.

---

## 5. What is `cProfile`?

`cProfile` is Python’s built-in **profiler**.

It measures:
- which functions were called
- how many times they were called
- how much time was spent in them
- how much cumulative time was spent through them

### In simple terms
Use `cProfile` when you want to understand where time goes across a larger execution flow.

---

## 6. Microbenchmarking vs profiling

### Microbenchmarking
Measures a small isolated piece of code very precisely.

Example:
- list comprehension vs loop
- string concatenation styles
- dictionary lookup patterns

This is where `timeit` is useful.

### Profiling
Measures runtime behavior of a full script or workflow.

Example:
- request handling flow
- data pipeline
- parsing process
- report generation

This is where `cProfile` is useful.

---

## 7. When to use `timeit`

Use `timeit` when:
- the code snippet is small
- you want to compare alternatives
- you want repeated timing
- you want to reduce noise from one-off execution

Typical examples:
- checking whether one expression is faster than another
- comparing list vs tuple construction
- timing string operations
- testing small helper functions

---

## 8. When to use `cProfile`

Use `cProfile` when:
- the program has many functions
- you do not know the bottleneck yet
- you need a global performance view
- a real workflow is slow
- you need call-count and cumulative timing information

Typical examples:
- profiling an API handler
- profiling a CLI command
- profiling a data transformation pipeline
- profiling a batch job

---

## 9. Basic `timeit` from Python code

Example:

```python
import timeit

result = timeit.timeit("sum(range(100))", number=10000)
print(result)
```

### What this does
- runs the code snippet many times
- measures total elapsed time
- returns a float in seconds

### Why repeated execution matters
A single run is often too noisy to trust.  
`timeit` reduces that problem by repeating the code many times.

---

## 10. The `number` parameter

`number` controls how many times the statement runs.

```python
import timeit

result = timeit.timeit("x = 1 + 1", number=1000000)
print(result)
```

### Meaning
If the operation is very fast, timing it once is not useful.  
Repeating it many times makes the measurement more stable.

---

## 11. Timing a function call

```python
import timeit


def square(x):
    return x * x


result = timeit.timeit(lambda: square(10), number=1000000)
print(result)
```

### Why this style is useful
It is often cleaner than building a long timing string, especially when timing existing Python functions directly.

---

## 12. `timeit.repeat`

Sometimes you want multiple benchmark runs.

```python
import timeit

results = timeit.repeat("sum(range(100))", repeat=5, number=10000)
print(results)
```

### What this does
- performs the timing multiple times
- returns a list of timings

### Why useful
It helps you see measurement variation across runs.

A common practical approach is to look at the **minimum** or compare the distribution rather than trusting one random run.

---

## 13. Why the minimum can matter

If several timing runs differ, the minimum often reflects the run with the least interference from external noise.

That is why many microbenchmarking workflows pay special attention to:
- the best run
- the most stable runs
- repeated measurements

### Important
This does not mean “always trust the minimum blindly,” but it is often more meaningful than the average when the environment is noisy.

---

## 14. Setup code in `timeit`

Sometimes the code being timed depends on imports or initialized data.

Example:

```python
import timeit

result = timeit.timeit(
    stmt="math.sqrt(12345)",
    setup="import math",
    number=1000000
)

print(result)
```

### Why `setup` exists
It lets you prepare the environment without including setup cost in every repeated timing iteration.

---

## 15. Avoid mixing setup cost with measured cost

This is an important principle.

Bad measurement:

```python
import timeit

result = timeit.timeit(
    stmt="""
data = list(range(1000))
sum(data)
""",
    number=10000
)
```

This includes both:
- building the list
- summing the list

If you only wanted to measure `sum(data)`, the setup should be separated.

Better:

```python
import timeit

result = timeit.timeit(
    stmt="sum(data)",
    setup="data = list(range(1000))",
    number=10000
)
```

---

## 16. Comparing two implementations with `timeit`

Suppose you want to compare:

```python
def square_loop(values):
    result = []
    for x in values:
        result.append(x * x)
    return result


def square_comp(values):
    return [x * x for x in values]
```

Timing them:

```python
import timeit

setup = """
values = list(range(1000))

def square_loop(values):
    result = []
    for x in values:
        result.append(x * x)
    return result

def square_comp(values):
    return [x * x for x in values]
"""

loop_time = timeit.timeit("square_loop(values)", setup=setup, number=10000)
comp_time = timeit.timeit("square_comp(values)", setup=setup, number=10000)

print(loop_time, comp_time)
```

### Why useful
This is a classic microbenchmarking use case.

---

## 17. Command-line use of `timeit`

You can also use `timeit` from the command line.

Example:

```bash
python -m timeit "sum(range(100))"
```

With setup:

```bash
python -m timeit -s "import math" "math.sqrt(12345)"
```

### Why useful
This is convenient for quick experiments without creating a script.

---

## 18. Be careful with unrealistic microbenchmarks

A code snippet may benchmark well in isolation but not matter much in the real application.

Example:
- saving a few microseconds in a helper function
- while the real bottleneck is a database query or file I/O

### Practical lesson
`timeit` is powerful, but only for the specific thing being measured.

Always ask:
- does this operation matter in the real workload?
- how often is it called?
- is this the real bottleneck?

---

## 19. What `timeit` is best at

`timeit` is best at:
- comparing small alternatives
- benchmarking expressions and functions
- measuring tiny repeated operations
- reducing one-run timing noise

It is **not** the best tool for understanding the structure of a large slowdown across a whole program.

That is where profiling matters.

---

## 20. Basic `cProfile` usage in code

Example:

```python
import cProfile


def compute():
    total = 0
    for i in range(100000):
        total += i * i
    return total


cProfile.run("compute()")
```

### What this does
It profiles the execution of `compute()` and prints a summary report.

---

## 21. Basic `cProfile` from the command line

You can also profile a script directly:

```bash
python -m cProfile my_script.py
```

### Why useful
This is one of the easiest ways to profile a real program or script without modifying the code much.

---

## 22. Example profiling output

A typical output includes columns like:

- `ncalls`
- `tottime`
- `percall`
- `cumtime`
- `filename:lineno(function)`

### Quick meaning

#### `ncalls`
Number of calls.

#### `tottime`
Time spent in the function itself, excluding time in subcalls.

#### `cumtime`
Cumulative time, including subcalls.

### Why this matters
`tottime` and `cumtime` answer different performance questions.

---

## 23. `tottime` vs `cumtime`

This distinction is essential.

### `tottime`
Time spent directly inside a function’s own body.

### `cumtime`
Time spent in the function plus everything it calls.

### Example interpretation
If a function mainly delegates work to other functions:
- `tottime` may be small
- `cumtime` may be large

That often means the function is a major entry point to expensive work even if its own body is small.

---

## 24. Profiling a function with `Profile`

For more control, use `cProfile.Profile`.

```python
import cProfile
import pstats


def compute():
    total = 0
    for i in range(100000):
        total += i * i
    return total


profiler = cProfile.Profile()
profiler.enable()

compute()

profiler.disable()

stats = pstats.Stats(profiler)
stats.sort_stats("cumtime").print_stats(10)
```

### Why useful
This allows you to:
- profile only a specific section
- sort output
- limit how many lines are printed

---

## 25. Sorting profiling output

With `pstats`, you can sort results in useful ways.

Common choices:
- `"tottime"`
- `"cumtime"`
- `"ncalls"`

Example:

```python
stats.sort_stats("tottime").print_stats(10)
```

### Practical guidance
- sort by `cumtime` when looking for high-level bottlenecks
- sort by `tottime` when looking for functions doing expensive direct work

---

## 26. Saving profiling results to a file

You can save profile data for later analysis.

```python
import cProfile


def compute():
    total = 0
    for i in range(100000):
        total += i * i
    return total


cProfile.run("compute()", "profile_output.prof")
```

Later:

```python
import pstats

stats = pstats.Stats("profile_output.prof")
stats.sort_stats("cumtime").print_stats(10)
```

### Why useful
This is practical when you want to analyze profile results separately from the run itself.

---

## 27. What `cProfile` is best at

`cProfile` is best at:
- finding hot functions
- locating broad bottlenecks
- understanding call structure
- deciding where optimization effort should go

It is usually the better starting point when you do **not yet know** what is slow.

---

## 28. Typical workflow: `cProfile` first, `timeit` second

A strong performance workflow is often:

1. use `cProfile` to find where the program spends time
2. identify one or two suspicious hotspots
3. isolate those hotspots
4. use `timeit` to compare alternative implementations

### Why this works well
It combines:
- broad bottleneck discovery
- focused implementation benchmarking

This is often much better than using only one tool.

---

## 29. Example mental model

Suppose a report-generation script is slow.

### Step 1: `cProfile`
You discover:
- 60% of time is in parsing
- 25% is in formatting
- 10% is in file output

### Step 2: `timeit`
You isolate the parser’s inner transformation and compare:
- current version
- optimized version
- alternative data structure approach

This is a practical and realistic use of both tools together.

---

## 30. Common mistakes with `timeit`

### 1. Timing code only once
One run is too noisy to trust.

### 2. Measuring unrealistic snippets
A tiny benchmark may not matter in the real program.

### 3. Including setup cost accidentally
This can distort the result.

### 4. Optimizing what is measurable instead of what matters
Easy-to-benchmark code is not always the real bottleneck.

### 5. Comparing code with different semantics
The two implementations must do the same work.

---

## 31. Common mistakes with `cProfile`

### 1. Profiling toy code instead of the real workload
Results may not reflect production behavior.

### 2. Misreading `tottime` and `cumtime`
These values answer different questions.

### 3. Optimizing a function with many calls but little total cost
High call count alone does not always mean important.

### 4. Ignoring I/O or environment effects
Profiling reflects the observed run, which depends on the workload and context.

### 5. Failing to narrow the optimization target
A profile report is useful only if you turn it into a decision.

---

## 32. Best practices

### 1. Measure before optimizing
Never optimize only from intuition.

### 2. Use `cProfile` to find major hotspots
Especially in large workflows.

### 3. Use `timeit` for isolated comparisons
Especially when comparing implementation alternatives.

### 4. Keep workloads realistic
Benchmark representative data and execution paths.

### 5. Interpret results carefully
Look at both total cost and real impact.

### 6. Optimize the biggest bottleneck first
That is usually where effort pays off best.

### 7. Re-measure after changes
Performance work should be verified, not assumed.

---

## 33. `timeit` and `cProfile` are complementary

A useful summary is:

- `timeit` is for **small, focused timing**
- `cProfile` is for **whole-flow bottleneck discovery**

They are not competitors.  
They solve different performance questions.

The best performance workflow often uses both.

---

## 34. Practical decision guide

### Use `timeit` when:
- comparing two functions
- checking micro-optimizations
- measuring small repeated logic
- validating a local implementation idea

### Use `cProfile` when:
- a script is slow and you do not know why
- a workflow has many functions
- you need cumulative timing information
- you need a big-picture performance view

---

## 35. Practical mental model

A useful mental model is:

- `timeit` tells you **how fast this small thing is**
- `cProfile` tells you **where the full program spends time**

That distinction alone prevents many bad optimization decisions.

---

## 36. Final recommendation

When working on Python performance:

- start with `cProfile` if the bottleneck is unknown
- isolate hot functions or code paths
- use `timeit` to compare candidate improvements
- keep benchmarks realistic
- optimize only after evidence shows where the real cost is

This is one of the most reliable ways to improve performance without wasting effort.

---

## 37. Quick summary

If you only keep the essentials:

1. `timeit` is for microbenchmarking small code snippets.
2. `cProfile` is for profiling full execution flows and function-level hotspots.
3. `timeit` helps compare implementations.
4. `cProfile` helps find where optimization matters.
5. A strong workflow is often: profile first, benchmark second.

---
