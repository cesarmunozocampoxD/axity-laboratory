"""
Lab – Concurrent Fetcher and CPU-bound Parallelism
===================================================
Demonstrates three ideas from the WIKI:

 1. httpx.AsyncClient + asyncio.Semaphore → concurrent I/O-bound fetching
    (WIKI §§ 7, 18-19: async is effective for I/O because the event loop keeps
    running while each coroutine awaits the network response)

 2. Sequential sync vs concurrent async timing comparison
    (WIKI § 30: "waiting work → async")

 3. ProcessPoolExecutor for CPU-bound work
    (WIKI §§ 14-16, 29: separate processes bypass the GIL and use multiple cores;
    WIKI § 30: "heavy computation → processes")
"""

import asyncio
import time
from concurrent.futures import ProcessPoolExecutor

import httpx

# Public demo API – returns simple JSON objects
DEMO_URLS = [f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, 11)]


# ─── 1. Synchronous (sequential) fetcher ─────────────────────────────────────


def fetch_one_sync(url: str) -> dict:
    """Fetch *url* and return parsed JSON. Creates a new client per call."""
    with httpx.Client(timeout=10) as client:
        r = client.get(url)
        r.raise_for_status()
        return r.json()


def run_sync(urls: list[str]) -> list[dict]:
    """Fetch every URL in *urls* one-by-one (blocking, sequential)."""
    return [fetch_one_sync(url) for url in urls]


# ─── 2. Async concurrent fetcher with semaphore ───────────────────────────────
#
# asyncio.Semaphore(n) ensures at most *n* coroutines hold the lock at once.
# Without a semaphore you could accidentally open hundreds of connections
# simultaneously and overwhelm the server.


async def _fetch_one_async(
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
    url: str,
) -> dict:
    """Acquire one semaphore slot, fetch *url*, release slot, return JSON."""
    async with semaphore:  # blocks here if n slots are taken
        r = await client.get(url)  # yields control while waiting
        r.raise_for_status()
        return r.json()


async def run_async(urls: list[str], max_concurrent: int = 5) -> list[dict]:
    """Fetch all *urls* concurrently, capped at *max_concurrent* simultaneous
    in-flight requests via a semaphore.

    A single AsyncClient is reused across all requests (efficient connection
    pooling) while asyncio.gather dispatches all coroutines at once.
    """
    semaphore = asyncio.Semaphore(max_concurrent)
    async with httpx.AsyncClient(timeout=10) as client:
        tasks = [_fetch_one_async(client, semaphore, url) for url in urls]
        return list(await asyncio.gather(*tasks))


# ─── 3. CPU-bound: prime counting with ProcessPoolExecutor ───────────────────
#
# Using threads for this would still be limited by the GIL (WIKI § 9).
# Separate processes have separate GILs, so they truly run in parallel.


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def count_primes_in_range(start: int, end: int) -> int:
    """Count primes in [start, end].

    Defined at module level so ProcessPoolExecutor can pickle (serialize) it
    and send it to worker processes.
    """
    return sum(1 for n in range(start, end + 1) if _is_prime(n))


def _make_ranges(limit: int, workers: int) -> list[tuple[int, int]]:
    """Split [2, limit] into *workers* non-overlapping, contiguous sub-ranges."""
    width = max(1, (limit - 1) // workers)
    result: list[tuple[int, int]] = []
    s = 2
    for _ in range(workers - 1):
        e = s + width - 1
        if e >= limit:
            result.append((s, limit))
            return result
        result.append((s, e))
        s = e + 1
    result.append((s, limit))
    return result


def count_primes_sequential(limit: int) -> int:
    """Count all primes up to *limit* in the calling process (single-core)."""
    return count_primes_in_range(2, limit)


def count_primes_parallel(limit: int, workers: int = 4) -> int:
    """Count all primes up to *limit* using *workers* OS processes.

    Each worker receives one sub-range and returns the count; the main process
    sums the partial results.  Because each worker is a separate CPython
    process it has its own GIL, enabling true multi-core parallelism.
    """
    ranges = _make_ranges(limit, workers)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(count_primes_in_range, s, e) for s, e in ranges]
        return sum(f.result() for f in futures)


# ─── Demo: timing comparisons ─────────────────────────────────────────────────


def compare_fetchers(urls: list[str] | None = None) -> None:
    """Compare sequential-sync vs concurrent-async HTTP fetching and print results."""
    if urls is None:
        urls = DEMO_URLS

    print(f"\n{'─' * 52}")
    print("HTTP Fetcher Comparison")
    print(f"  {len(urls)} URLs  ·  max_concurrent (async) = 5")
    print(f"{'─' * 52}")

    t0 = time.perf_counter()
    sync_results = run_sync(urls)
    sync_time = time.perf_counter() - t0
    print(f"  Sync  (sequential):    {sync_time:.2f}s  → {len(sync_results)} responses")

    t0 = time.perf_counter()
    async_results = asyncio.run(run_async(urls, max_concurrent=5))
    async_time = time.perf_counter() - t0
    print(
        f"  Async (semaphore=5):   {async_time:.2f}s  → {len(async_results)} responses"
    )

    speedup = sync_time / async_time if async_time > 0 else float("inf")
    print(f"  Speedup: {speedup:.1f}×")


def compare_prime_computation(limit: int = 500_000, workers: int = 4) -> None:
    """Compare sequential vs parallel prime counting and print results."""
    print(f"\n{'─' * 52}")
    print("CPU-bound: Prime Counting")
    print(f"  Limit: {limit:,}  ·  Workers: {workers}")
    print(f"{'─' * 52}")

    t0 = time.perf_counter()
    seq_count = count_primes_sequential(limit)
    seq_time = time.perf_counter() - t0
    print(f"  Sequential:              {seq_time:.2f}s  → {seq_count:,} primes")

    t0 = time.perf_counter()
    par_count = count_primes_parallel(limit, workers=workers)
    par_time = time.perf_counter() - t0
    print(f"  Parallel ({workers} workers):    {par_time:.2f}s  → {par_count:,} primes")

    speedup = seq_time / par_time if par_time > 0 else float("inf")
    print(f"  Speedup: {speedup:.1f}×")


# Required on Windows so spawned worker processes don't re-run the demo
if __name__ == "__main__":
    compare_fetchers()
    compare_prime_computation()
