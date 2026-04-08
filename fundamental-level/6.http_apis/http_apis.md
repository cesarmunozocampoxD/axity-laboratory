# Python: `requests`, `aiohttp`, and `httpx` (HTTP/2)

## 1. What Are These Libraries?

These three libraries are used to make HTTP requests from Python.

- **`requests`**: simple and very popular synchronous HTTP client
- **`aiohttp`**: asynchronous HTTP client/server built around `asyncio`
- **`httpx`**: modern HTTP client with both synchronous and asynchronous APIs, plus HTTP/2 support

They are commonly used for:
- calling APIs
- downloading data
- sending JSON
- handling authentication
- integrating external web services

---

## 2. Synchronous vs Asynchronous

Before comparing the libraries, it is important to understand this distinction.

### Synchronous
A synchronous request blocks execution until it finishes.

```python
result = do_request()
print("This runs after the request is done")
```

### Asynchronous
An asynchronous request can be awaited inside an async program, which is useful when many requests or other concurrent tasks are involved.

```python
result = await do_request()
print("This runs after the awaited request is done")
```

### Rule of thumb
- use **sync** code when the program is simple
- use **async** code when you need high concurrency or already use `asyncio`

---

## 3. `requests`

`requests` is the easiest one to start with.

It is:
- synchronous
- very readable
- excellent for scripts, tools, and simple API integrations

### Installation
```bash
pip install requests
```

### Basic GET request
```python
import requests

response = requests.get("https://httpbin.org/get")
print(response.status_code)
print(response.text)
```

---

## 4. JSON with `requests`

```python
import requests

response = requests.get("https://httpbin.org/json")
data = response.json()

print(data)
```

If the response contains valid JSON, `.json()` converts it into Python objects.

---

## 5. Sending Query Parameters with `requests`

```python
import requests

params = {"q": "python", "page": 1}
response = requests.get("https://httpbin.org/get", params=params)

print(response.url)
print(response.json())
```

This is cleaner than manually building query strings.

---

## 6. Sending JSON with `requests`

```python
import requests

payload = {
    "name": "Janette",
    "role": "developer"
}

response = requests.post("https://httpbin.org/post", json=payload)

print(response.status_code)
print(response.json())
```

Using `json=` is usually better than manually serializing JSON yourself.

---

## 7. Headers in `requests`

```python
import requests

headers = {
    "Authorization": "Bearer TOKEN",
    "Accept": "application/json"
}

response = requests.get("https://httpbin.org/headers", headers=headers)
print(response.json())
```

---

## 8. Timeouts in `requests`

Always consider using a timeout.

```python
import requests

response = requests.get("https://httpbin.org/get", timeout=10)
print(response.status_code)
```

Without a timeout, a request may hang longer than you want.

---

## 9. Error Handling in `requests`

```python
import requests

try:
    response = requests.get("https://httpbin.org/status/404", timeout=10)
    response.raise_for_status()
except requests.exceptions.RequestException as error:
    print("Request failed:", error)
```

### Why `raise_for_status()`?
It raises an exception for HTTP error responses like:
- 400
- 404
- 500

This is often useful in automation or API clients.

---

## 10. Sessions in `requests`

If you make multiple requests to the same service, use `Session`.

```python
import requests

with requests.Session() as session:
    session.headers.update({"User-Agent": "my-app"})
    
    response1 = session.get("https://httpbin.org/get")
    response2 = session.get("https://httpbin.org/headers")
    
    print(response1.status_code)
    print(response2.status_code)
```

A session helps with:
- connection reuse
- cookies
- shared configuration

---

## 11. When to Use `requests`

Use `requests` when:
- you want the simplest API
- your code is synchronous
- you do not need high async concurrency
- you want quick scripts and API integrations

It is often the best default for small and medium sync tasks.

---

## 12. `aiohttp`

`aiohttp` is an asynchronous HTTP library built for `asyncio`.

It is useful when:
- you need many concurrent requests
- you are already using `asyncio`
- you want an async HTTP client
- you may also need an async web server

### Installation
```bash
pip install aiohttp
```

---

## 13. Basic GET Request with `aiohttp`

```python
import aiohttp
import asyncio

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://httpbin.org/get") as response:
            print(response.status)
            text = await response.text()
            print(text)

asyncio.run(main())
```

### Important differences from `requests`
- functions are `async`
- you use `await`
- responses are read asynchronously

---

## 14. JSON with `aiohttp`

```python
import aiohttp
import asyncio

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://httpbin.org/json") as response:
            data = await response.json()
            print(data)

asyncio.run(main())
```

---

## 15. Sending Query Parameters with `aiohttp`

```python
import aiohttp
import asyncio

async def main():
    params = {"q": "python", "page": 1}

    async with aiohttp.ClientSession() as session:
        async with session.get("https://httpbin.org/get", params=params) as response:
            data = await response.json()
            print(data)

asyncio.run(main())
```

---

## 16. Sending JSON with `aiohttp`

```python
import aiohttp
import asyncio

async def main():
    payload = {
        "name": "Janette",
        "role": "developer"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post("https://httpbin.org/post", json=payload) as response:
            data = await response.json()
            print(data)

asyncio.run(main())
```

---

## 17. Headers in `aiohttp`

```python
import aiohttp
import asyncio

async def main():
    headers = {
        "Authorization": "Bearer TOKEN",
        "Accept": "application/json"
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get("https://httpbin.org/headers") as response:
            data = await response.json()
            print(data)

asyncio.run(main())
```

---

## 18. Timeouts in `aiohttp`

```python
import aiohttp
import asyncio

async def main():
    timeout = aiohttp.ClientTimeout(total=10)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get("https://httpbin.org/get") as response:
            print(response.status)

asyncio.run(main())
```

---

## 19. Error Handling in `aiohttp`

```python
import aiohttp
import asyncio

async def main():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://httpbin.org/status/404") as response:
                response.raise_for_status()
    except aiohttp.ClientError as error:
        print("Request failed:", error)

asyncio.run(main())
```

---

## 20. Why `ClientSession` Matters in `aiohttp`

Do not create a new session for every request unless you really need to.

Good pattern:
```python
import aiohttp
import asyncio

async def main():
    async with aiohttp.ClientSession() as session:
        for _ in range(3):
            async with session.get("https://httpbin.org/get") as response:
                print(response.status)

asyncio.run(main())
```

A session helps with:
- connection pooling
- keep-alive
- shared headers and cookies

---

## 21. Concurrent Requests with `aiohttp`

This is one reason async clients are useful.

```python
import aiohttp
import asyncio

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/uuid",
        "https://httpbin.org/ip"
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

        for item in results:
            print(item[:60])

asyncio.run(main())
```

This can be much more efficient than making the same requests one by one synchronously.

---

## 22. When to Use `aiohttp`

Use `aiohttp` when:
- you already use `asyncio`
- you need many concurrent requests
- you want an async-native HTTP client
- you may also want an async web server

---

## 23. `httpx`

`httpx` is a modern HTTP client that supports both:
- synchronous API
- asynchronous API

It is often chosen when you want:
- a modern API
- sync and async options in one library
- HTTP/2 support
- a design that feels familiar if you already know `requests`

### Installation
```bash
pip install httpx
```

---

## 24. Basic GET Request with `httpx` (Sync)

```python
import httpx

response = httpx.get("https://httpbin.org/get")
print(response.status_code)
print(response.text)
```

This looks similar to `requests`.

---

## 25. JSON with `httpx` (Sync)

```python
import httpx

response = httpx.get("https://httpbin.org/json")
data = response.json()

print(data)
```

---

## 26. Sending JSON with `httpx` (Sync)

```python
import httpx

payload = {
    "name": "Janette",
    "role": "developer"
}

response = httpx.post("https://httpbin.org/post", json=payload)
print(response.status_code)
print(response.json())
```

---

## 27. Using an `httpx.Client`

For repeated requests, use a client.

```python
import httpx

with httpx.Client(headers={"User-Agent": "my-app"}) as client:
    response1 = client.get("https://httpbin.org/get")
    response2 = client.get("https://httpbin.org/headers")

    print(response1.status_code)
    print(response2.status_code)
```

A client helps with:
- connection reuse
- shared headers
- shared configuration
- cookies

---

## 28. Async Requests with `httpx`

One big advantage of `httpx` is that it also supports async usage.

```python
import httpx
import asyncio

async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://httpbin.org/get")
        print(response.status_code)
        print(response.text)

asyncio.run(main())
```

This makes `httpx` attractive when you want one library that can handle both sync and async styles.

---

## 29. Sending JSON with `httpx.AsyncClient`

```python
import httpx
import asyncio

async def main():
    payload = {
        "name": "Janette",
        "role": "developer"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post("https://httpbin.org/post", json=payload)
        print(response.status_code)
        print(response.json())

asyncio.run(main())
```

---

## 30. Timeouts in `httpx`

```python
import httpx

response = httpx.get("https://httpbin.org/get", timeout=10.0)
print(response.status_code)
```

Or with a client:

```python
import httpx

with httpx.Client(timeout=10.0) as client:
    response = client.get("https://httpbin.org/get")
    print(response.status_code)
```

---

## 31. Error Handling in `httpx`

```python
import httpx

try:
    response = httpx.get("https://httpbin.org/status/404", timeout=10.0)
    response.raise_for_status()
except httpx.HTTPError as error:
    print("Request failed:", error)
```

---

## 32. HTTP/2 in `httpx`

One major feature of `httpx` is HTTP/2 support.

### Installation with HTTP/2 support
```bash
pip install httpx[http2]
```

### Example
```python
import httpx

with httpx.Client(http2=True) as client:
    response = client.get("https://httpbin.org/get")
    print(response.status_code)
    print(response.http_version)
```

### Important
Even if the client supports HTTP/2, the server must also support it.

If not, the request may still use HTTP/1.1.

---

## 33. Sync vs Async in `httpx`

### Sync
```python
import httpx

response = httpx.get("https://httpbin.org/get")
```

### Async
```python
import httpx
import asyncio

async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://httpbin.org/get")
        print(response.status_code)

asyncio.run(main())
```

This flexibility is one reason many developers like `httpx`.

---

## 34. `requests` vs `aiohttp` vs `httpx`

### `requests`
Best when:
- you want the simplest sync API
- you do not need async
- you want maximum simplicity for scripts

### `aiohttp`
Best when:
- your program is async
- you need high concurrency
- you want a dedicated async client
- you may also need an async server

### `httpx`
Best when:
- you want a modern API
- you may need either sync or async
- you want HTTP/2 support
- you like a `requests`-style feel with newer features

---

## 35. Common Beginner Mistakes

### Mistake 1: Forgetting timeouts
Bad:
```python
import requests

response = requests.get("https://example.com")
```

Better:
```python
import requests

response = requests.get("https://example.com", timeout=10)
```

The same idea applies to `aiohttp` and `httpx`.

---

### Mistake 2: Creating a new session/client for every request
Less ideal:
```python
import requests

for _ in range(10):
    response = requests.get("https://httpbin.org/get")
```

Better:
```python
import requests

with requests.Session() as session:
    for _ in range(10):
        response = session.get("https://httpbin.org/get")
```

The same principle applies to:
- `aiohttp.ClientSession`
- `httpx.Client`
- `httpx.AsyncClient`

---

### Mistake 3: Using async libraries without `await`
Wrong:
```python
import aiohttp

async def main():
    session = aiohttp.ClientSession()
    response = session.get("https://httpbin.org/get")
```

You need `await` and proper async context management.

---

### Mistake 4: Mixing sync and async styles incorrectly
For example, using `requests` inside a heavily async application can block the event loop.

In async programs, prefer:
- `aiohttp`
- `httpx.AsyncClient`

---

### Mistake 5: Assuming HTTP/2 is automatic everywhere
With `httpx`, enabling HTTP/2 support on the client side does not force the server to use it.
The server must support HTTP/2 too.

---

## 36. Practical Recommendations

A simple practical rule:

- choose **`requests`** for simple synchronous scripts
- choose **`aiohttp`** for heavy async concurrency and async-native projects
- choose **`httpx`** when you want a modern client with both sync and async APIs, especially if HTTP/2 matters

---

## 37. Summary

- **`requests`** is a synchronous HTTP client with a very simple API
- **`aiohttp`** is an asynchronous HTTP client/server library for `asyncio`
- **`httpx`** supports both synchronous and asynchronous HTTP clients
- **sessions/clients** are important for connection reuse and shared configuration
- use **timeouts** in all three libraries
- use `.json()` for JSON responses when appropriate
- use `raise_for_status()` when you want HTTP errors to raise exceptions
- use **`httpx`** when you need HTTP/2 support
- use **async libraries** only when your codebase benefits from async concurrency

# Python: Timeouts, Retries, and Error Handling

## 1. Why These Topics Matter

When your code interacts with:
- APIs
- databases
- files
- subprocesses
- external services

things can go wrong.

Common problems include:
- operations taking too long
- temporary network failures
- invalid input
- missing files
- service downtime
- unexpected exceptions

That is why **timeouts**, **retries**, and **error handling** are essential for reliable programs.

---

## 2. What Is a Timeout?

A **timeout** is a limit on how long an operation is allowed to take.

If the operation takes longer than that limit, the program stops waiting and raises an error or handles the situation in some other way.

### Why timeouts matter
Without timeouts, a program may:
- hang forever
- wait too long for a response
- block the rest of the system
- become hard to debug

---

## 3. Common Timeout Use Cases

Timeouts are useful in:
- HTTP requests
- database queries
- subprocesses
- sockets
- asynchronous tasks
- locks and queues

### Example idea
If an API usually responds in 1 second, you may decide to stop waiting after 10 seconds.

---

## 4. HTTP Timeout Example with `requests`

```python
import requests

response = requests.get("https://example.com", timeout=10)
print(response.status_code)
```

This means:
- wait up to 10 seconds
- if the request takes too long, raise an exception

### With error handling
```python
import requests

try:
    response = requests.get("https://example.com", timeout=10)
    print(response.status_code)
except requests.exceptions.Timeout:
    print("The request took too long")
except requests.exceptions.RequestException as error:
    print("Request failed:", error)
```

---

## 5. Timeout Example with `httpx`

```python
import httpx

try:
    response = httpx.get("https://example.com", timeout=10.0)
    print(response.status_code)
except httpx.TimeoutException:
    print("The request timed out")
except httpx.HTTPError as error:
    print("HTTP error:", error)
```

---

## 6. Timeout Example with `aiohttp`

```python
import aiohttp
import asyncio

async def main():
    timeout = aiohttp.ClientTimeout(total=10)

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get("https://example.com") as response:
                print(response.status)
    except asyncio.TimeoutError:
        print("The request timed out")
    except aiohttp.ClientError as error:
        print("Client error:", error)

asyncio.run(main())
```

---

## 7. Timeouts in `subprocess`

A subprocess can also hang.

```python
import subprocess

try:
    subprocess.run(["sleep", "10"], timeout=2)
except subprocess.TimeoutExpired:
    print("The command took too long")
```

This is useful for automation scripts and external commands.

---

## 8. Choosing a Timeout Value

A timeout should be:
- long enough for normal conditions
- short enough to avoid hanging forever

There is no universal perfect number.

### Factors to consider
- network speed
- server response times
- expected workload
- user experience
- retry strategy

### Example
- internal fast API: maybe 2–5 seconds
- external API: maybe 10–30 seconds
- long job or export: maybe much longer

---

## 9. What Are Retries?

A **retry** means trying the same operation again after it fails.

Retries are useful for **temporary** failures, such as:
- network hiccups
- timeouts
- short service interruptions
- rate limits
- transient connection resets

### Important
Retries are not for every error.

You should **not** retry blindly when:
- input is invalid
- authentication is wrong
- permission is denied
- the error is permanent

---

## 10. Simple Retry Example with a Loop

```python
def unstable_operation():
    raise ValueError("Temporary failure")

max_attempts = 3

for attempt in range(1, max_attempts + 1):
    try:
        unstable_operation()
        print("Success")
        break
    except ValueError as error:
        print(f"Attempt {attempt} failed: {error}")
        if attempt == max_attempts:
            print("All attempts failed")
```

This is the basic retry pattern.

---

## 11. Retry with Delay

Usually retries should wait a little before trying again.

```python
import time

def unstable_operation():
    raise ValueError("Temporary failure")

max_attempts = 3
delay = 2

for attempt in range(1, max_attempts + 1):
    try:
        unstable_operation()
        print("Success")
        break
    except ValueError as error:
        print(f"Attempt {attempt} failed: {error}")

        if attempt == max_attempts:
            print("All attempts failed")
        else:
            time.sleep(delay)
```

This avoids retrying too aggressively.

---

## 12. Exponential Backoff

A common retry strategy is **exponential backoff**.

That means the wait time grows after each failure.

Example:
- first retry: 1 second
- second retry: 2 seconds
- third retry: 4 seconds
- fourth retry: 8 seconds

### Example
```python
import time

def unstable_operation():
    raise ValueError("Temporary failure")

max_attempts = 4
base_delay = 1

for attempt in range(1, max_attempts + 1):
    try:
        unstable_operation()
        print("Success")
        break
    except ValueError as error:
        print(f"Attempt {attempt} failed: {error}")

        if attempt == max_attempts:
            print("All attempts failed")
        else:
            delay = base_delay * (2 ** (attempt - 1))
            print(f"Waiting {delay} seconds before retrying...")
            time.sleep(delay)
```

This is more polite to overloaded systems.

---

## 13. Retry Only for Certain Errors

A good retry strategy only retries errors that are likely temporary.

### Example
```python
import time

def unstable_operation():
    raise ConnectionError("Network problem")

max_attempts = 3

for attempt in range(1, max_attempts + 1):
    try:
        unstable_operation()
        print("Success")
        break
    except ConnectionError as error:
        print(f"Attempt {attempt} failed: {error}")

        if attempt == max_attempts:
            print("All attempts failed")
        else:
            time.sleep(2)
```

This is better than retrying every possible exception.

---

## 14. Retry Helper Function

You can wrap retry logic in a reusable function.

```python
import time

def retry(operation, max_attempts=3, delay=1):
    for attempt in range(1, max_attempts + 1):
        try:
            return operation()
        except Exception as error:
            print(f"Attempt {attempt} failed: {error}")

            if attempt == max_attempts:
                raise
            time.sleep(delay)

def unstable():
    return "done"

result = retry(unstable)
print(result)
```

This makes retry logic easier to reuse.

---

## 15. What Is Error Handling?

**Error handling** means detecting failures and responding to them safely.

In Python, the main tool is:

```python
try:
    ...
except SomeError:
    ...
```

This lets your program:
- avoid crashing unnecessarily
- log useful information
- recover from known problems
- fail in a controlled way

---

## 16. Basic `try-except`

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("You cannot divide by zero")
```

This prevents the whole program from crashing immediately.

---

## 17. Catch Specific Exceptions

It is better to catch specific exceptions than to catch everything.

Good:
```python
try:
    number = int("hello")
except ValueError:
    print("That is not a valid integer")
```

Less good:
```python
try:
    number = int("hello")
except:
    print("Something went wrong")
```

Specific exceptions make debugging easier.

---

## 18. Multiple `except` Blocks

```python
try:
    value = int(input("Enter a number: "))
    result = 10 / value
except ValueError:
    print("Invalid number")
except ZeroDivisionError:
    print("You cannot divide by zero")
```

Different errors can be handled in different ways.

---

## 19. Using `as` to Inspect the Error

```python
try:
    number = int("hello")
except ValueError as error:
    print("Error message:", error)
```

This is useful for:
- debugging
- logging
- reporting details

---

## 20. The `else` Block

`else` runs only if no exception happens.

```python
try:
    result = 10 / 2
except ZeroDivisionError:
    print("Division by zero")
else:
    print("Result:", result)
```

This helps separate:
- risky code
- success-only code

---

## 21. The `finally` Block

`finally` always runs, whether an exception happened or not.

```python
try:
    file = open("notes.txt", "r", encoding="utf-8")
    content = file.read()
except FileNotFoundError:
    print("File not found")
finally:
    print("Finished")
```

A common use is cleanup:
- closing files
- releasing resources
- ending sessions

---

## 22. Raising Exceptions

You can raise your own exception when something is wrong.

```python
age = -1

if age < 0:
    raise ValueError("Age cannot be negative")
```

This is useful when enforcing rules in your program.

---

## 23. Re-Raising Exceptions

Sometimes you want to log or inspect an error, then raise it again.

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Logging the error")
    raise
```

This preserves the original failure.

---

## 24. Timeout + Retry + Error Handling Together

A realistic pattern combines all three ideas.

```python
import time
import requests

url = "https://example.com/api"
max_attempts = 3

for attempt in range(1, max_attempts + 1):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        print("Success:", data)
        break

    except requests.exceptions.Timeout:
        print(f"Attempt {attempt}: timeout")

    except requests.exceptions.RequestException as error:
        print(f"Attempt {attempt}: request failed -> {error}")

    if attempt < max_attempts:
        time.sleep(2)
    else:
        print("All attempts failed")
```

This is a very common real-world pattern.

---

## 25. When to Retry and When Not To

### Good candidates for retry
- timeout
- temporary connection errors
- temporary server unavailability
- rate limiting with waiting
- intermittent network failures

### Bad candidates for retry
- invalid credentials
- malformed request data
- missing required parameters
- permission denied
- permanent validation errors

### Rule of thumb
Retry only errors that are likely temporary.

---

## 26. Logging Errors

Error handling is much more useful when combined with logging.

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    result = 10 / 0
except ZeroDivisionError:
    logger.exception("Calculation failed")
```

`logger.exception()` logs:
- your message
- the traceback

This is better than silently ignoring failures.

---

## 27. Summary

- A **timeout** limits how long an operation may take
- A **retry** means trying again after a temporary failure
- **Error handling** means managing failures safely with `try-except`
- Use timeouts for:
  - HTTP requests
  - subprocesses
  - external services
- Use retries for:
  - temporary connection problems
  - timeouts
  - intermittent failures
- Do **not** retry permanent errors blindly
- Catch specific exceptions when possible
- Use logging to record failures
- A reliable program often combines:
  - timeout
  - retry
  - clear error handling

  # Python: Streaming Responses and Memory-Efficient Usage

## 1. What “streaming” means

**Streaming a response** means reading data in small chunks as it arrives, instead of loading the entire response body into memory at once.

This is especially useful for:
- large downloads
- long responses
- file transfers
- line-by-line processing

---

## 2. Why streaming helps memory usage

If you read the entire response at once, your program may hold the whole body in memory.

That can be a problem for:
- large files
- many simultaneous requests
- limited-memory environments

Streaming helps because:
- memory usage stays lower
- processing can start earlier
- large responses become safer to handle

---

## 3. General rule

Use **full-body reads** only when:
- the response is small
- you truly need everything in memory

Use **streaming** when:
- the response may be large
- you want to write directly to disk
- you want to process chunks incrementally
- you want to avoid memory spikes

---

## 4. Streaming with `requests`

In `requests`, enable streaming with `stream=True`.

### Example
```python
import requests

url = "https://example.com/large-file.zip"

with requests.get(url, stream=True, timeout=30) as response:
    response.raise_for_status()

    with open("large-file.zip", "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:  # ignore keep-alive chunks
                file.write(chunk)
```

### Notes
- `stream=True` avoids downloading the whole body immediately
- `iter_content()` is the normal choice for chunked downloads
- `chunk_size` can be adjusted

---

## 5. `requests`: `iter_content()` vs `raw`

Use `iter_content()` most of the time.

```python
import requests

with requests.get("https://example.com/data.bin", stream=True, timeout=30) as response:
    response.raise_for_status()

    for chunk in response.iter_content(chunk_size=4096):
        print(len(chunk))
```

Use `raw` only when you really need lower-level undecoded bytes.

```python
import requests

with requests.get("https://example.com/data.bin", stream=True, timeout=30) as response:
    response.raise_for_status()
    raw_bytes = response.raw.read(64)
    print(raw_bytes)
```

Usually, `iter_content()` is simpler and safer.

---

## 6. Streaming with `httpx` (sync)

Use `httpx.stream(...)` for large downloads.

### Streaming bytes
```python
import httpx

with httpx.stream("GET", "https://example.com/large-file.zip", timeout=30.0) as response:
    response.raise_for_status()

    with open("large-file.zip", "wb") as file:
        for chunk in response.iter_bytes():
            file.write(chunk)
```

### Streaming text
```python
import httpx

with httpx.stream("GET", "https://example.com/log.txt", timeout=30.0) as response:
    response.raise_for_status()

    for text_chunk in response.iter_text():
        print(text_chunk)
```

### Streaming line by line
```python
import httpx

with httpx.stream("GET", "https://example.com/log.txt", timeout=30.0) as response:
    response.raise_for_status()

    for line in response.iter_lines():
        print(line)
```

### Raw bytes without decoding
```python
import httpx

with httpx.stream("GET", "https://example.com/data.bin", timeout=30.0) as response:
    response.raise_for_status()

    for chunk in response.iter_raw():
        print(chunk)
```

---

## 7. Streaming with `httpx` (async)

`httpx` also supports async streaming.

### Async bytes streaming
```python
import asyncio
import httpx

async def main():
    async with httpx.AsyncClient(timeout=30.0) as client:
        async with client.stream("GET", "https://example.com/large-file.zip") as response:
            response.raise_for_status()

            with open("large-file.zip", "wb") as file:
                async for chunk in response.aiter_bytes():
                    file.write(chunk)

asyncio.run(main())
```

### Async line streaming
```python
import asyncio
import httpx

async def main():
    async with httpx.AsyncClient(timeout=30.0) as client:
        async with client.stream("GET", "https://example.com/log.txt") as response:
            response.raise_for_status()

            async for line in response.aiter_lines():
                print(line)

asyncio.run(main())
```

---

## 8. Streaming with `aiohttp`

In `aiohttp`, stream from `resp.content`.

### Chunked download
```python
import aiohttp
import asyncio

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://example.com/large-file.zip") as resp:
            resp.raise_for_status()

            with open("large-file.zip", "wb") as file:
                async for chunk in resp.content.iter_chunked(8192):
                    file.write(chunk)

asyncio.run(main())
```

### Reading a small part from the stream
```python
import aiohttp
import asyncio

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://example.com/data.bin") as resp:
            resp.raise_for_status()
            first_bytes = await resp.content.read(32)
            print(first_bytes)

asyncio.run(main())
```

---

## 9. Write streamed data directly to disk

A very memory-efficient pattern is:

1. open the output file once
2. read network data chunk by chunk
3. write each chunk immediately
4. never keep the whole body in memory

### Generic example
```python
def save_stream_to_file(chunks, filename):
    with open(filename, "wb") as file:
        for chunk in chunks:
            file.write(chunk)
```

This is ideal for:
- ZIP files
- PDFs
- backups
- media
- large exports

---

## 10. Process data incrementally

Streaming is not only for saving files. You can also process data incrementally.

### Example: count lines without loading the full file
```python
line_count = 0

with open("huge.log", "r", encoding="utf-8") as file:
    for _ in file:
        line_count += 1

print(line_count)
```

### Example: process streamed HTTP lines
```python
import httpx

with httpx.stream("GET", "https://example.com/events.txt", timeout=30.0) as response:
    response.raise_for_status()

    for line in response.iter_lines():
        if "ERROR" in line:
            print("Found error line:", line)
```

This avoids keeping the whole response in memory.

---

## 11. Use generators for memory-efficient pipelines

Generators let you process items lazily, one at a time.

### Example
```python
def read_lines(path):
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            yield line.strip()

for line in read_lines("huge.log"):
    if "ERROR" in line:
        print(line)
```

This is more memory-efficient than:

```python
with open("huge.log", "r", encoding="utf-8") as file:
    lines = file.readlines()  # loads everything into memory
```

---

## 12. Choose the right chunk size

There is no single perfect chunk size.

Typical chunk sizes:
- `1024` bytes
- `4096` bytes
- `8192` bytes
- `65536` bytes

### Trade-off
- **smaller chunks**: lower per-chunk memory, more overhead
- **larger chunks**: fewer iterations, more memory per chunk

A common practical default is `8192` bytes.

---

## 13. Text vs binary streaming

Use **binary mode** for:
- ZIP files
- images
- videos
- PDFs
- unknown binary payloads

Use **text mode** only when you are sure the content is text and you want decoded strings.

### Binary file write
```python
with open("file.bin", "wb") as file:
    file.write(b"abc")
```

### Text file read
```python
with open("notes.txt", "r", encoding="utf-8") as file:
    text = file.read()
```

---

## 14. Explicit encodings for text files

For text files, explicitly specifying the encoding is a good habit.

### Good
```python
with open("data.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line)
```

### Riskier
```python
with open("data.txt", "r") as file:
    text = file.read()
```

Using `encoding="utf-8"` helps avoid platform-related issues.

---

## 15. Avoid loading the full response accidentally

These patterns are convenient, but not ideal for large responses.

### `requests`
```python
import requests

response = requests.get("https://example.com/large-file.zip", timeout=30)
data = response.content  # loads all bytes into memory
```

### `httpx`
```python
import httpx

response = httpx.get("https://example.com/large-file.zip", timeout=30.0)
data = response.content  # loads all bytes into memory
```

### `aiohttp`
```python
import aiohttp
import asyncio

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://example.com/large-file.zip") as resp:
            data = await resp.read()  # loads all bytes into memory

asyncio.run(main())
```

For large bodies, prefer streaming APIs.

---

## 16. Close responses and clients properly

Resource cleanup matters.

### Good patterns
- `with requests.get(..., stream=True) as response:`
- `with httpx.stream(...) as response:`
- `async with httpx.AsyncClient() as client:`
- `async with client.stream(...) as response:`
- `async with aiohttp.ClientSession() as session:`

These patterns help avoid leaked resources.

---

## 17. Practical recommendations

- Stream large downloads instead of reading full bodies at once.
- Write streamed binary data directly to disk.
- Process text incrementally when possible.
- Use generators for lazy pipelines.
- Reuse sessions/clients for repeated requests.
- Specify `encoding="utf-8"` for text files when appropriate.
- Prefer high-level streaming iterators unless you truly need lower-level access.

---

## 18. Summary

- **Streaming** means consuming data chunk by chunk instead of loading everything into memory
- In **Requests**, use `stream=True` and usually `iter_content()`
- In **HTTPX**, use `httpx.stream(...)` or `AsyncClient.stream(...)`
- In **aiohttp**, stream from `resp.content.iter_chunked(...)`
- Writing chunks directly to disk is one of the most memory-efficient patterns
- Use generators and line-by-line processing for large text data
- For text files, `encoding="utf-8"` is usually the safest default