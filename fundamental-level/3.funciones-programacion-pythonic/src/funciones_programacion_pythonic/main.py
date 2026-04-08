"""
Lab exercises:
  - Decorador de reintentos con backoff
  - Generador por lotes y context manager de temporización
"""

from __future__ import annotations

import time
from contextlib import contextmanager
from functools import wraps

# ──────────────────────────────────────────────────────────────────────────────
# LAB — Decorador de reintentos con backoff
# ──────────────────────────────────────────────────────────────────────────────


def retry(max_attempts: int = 3, initial_delay: float = 0.5, backoff: float = 2.0):
    """
    Decorator that retries a function up to *max_attempts* times.
    Waits *initial_delay* seconds before the first retry and multiplies
    the wait time by *backoff* on each subsequent attempt.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    if attempt < max_attempts:
                        print(
                            f"  [{func.__name__}] attempt {attempt} failed: "
                            f"{exc!r} — retrying in {delay:.2f}s…"
                        )
                        time.sleep(delay)
                        delay *= backoff
                    else:
                        print(
                            f"  [{func.__name__}] attempt {attempt} failed: "
                            f"{exc!r} — no more retries."
                        )
                        raise

        return wrapper

    return decorator


def demo_lab_retry() -> None:
    print("--- LAB: Retry decorator with exponential backoff ---")

    call_count = 0

    @retry(max_attempts=4, initial_delay=0.1, backoff=2.0)
    def flaky_service(succeed_on: int) -> str:
        nonlocal call_count
        call_count += 1
        if call_count < succeed_on:
            raise ConnectionError(f"Service unavailable (attempt {call_count})")
        return f"Success on attempt {call_count}!"

    # Succeeds on the 3rd attempt
    call_count = 0
    result = flaky_service(succeed_on=3)
    print(f"  Result: {result}")

    # Exhausts all retries
    call_count = 0
    try:
        flaky_service(succeed_on=99)
    except ConnectionError as exc:
        print(f"  Final exception caught: {exc}")

    print()


# ──────────────────────────────────────────────────────────────────────────────
# LAB — Generador por lotes y context manager de temporización
# ──────────────────────────────────────────────────────────────────────────────


def batch_generator(iterable, batch_size: int):
    """
    Generator that yields successive slices of *iterable* as lists,
    each of length *batch_size* (the last batch may be shorter).
    """
    batch: list = []
    for item in iterable:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


@contextmanager
def timer(label: str = "Block"):
    """Context manager that measures and prints the elapsed time of a block."""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"  [{label}] elapsed: {elapsed:.4f}s")


def demo_lab_batch_and_timer() -> None:
    print("--- LAB: Batch generator + timing context manager ---")

    data = list(range(1, 18))
    print(f"  Data ({len(data)} items): {data}")

    print("  Processing in batches of 5:")
    with timer("batch processing"):
        for batch in batch_generator(data, batch_size=5):
            # simulate some work per batch
            time.sleep(0.02)
            total = sum(batch)
            print(f"    batch {batch} → sum={total}")

    print()

    print("  Timing a heavy computation:")
    with timer("sum(range(5_000_000))"):
        result = sum(range(5_000_000))
    print(f"  result = {result}")

    print()


def main() -> None:
    demo_lab_retry()
    demo_lab_batch_and_timer()


if __name__ == "__main__":
    main()
