"""
Tests for fetcher_lab.py
========================
All HTTP calls are intercepted by respx – no real network access required.

Test groups:
 1. Sync fetcher correctness
 2. Async fetcher correctness
 3. Semaphore concurrency cap
 4. Range-splitting helper
 5. CPU-bound prime counting (sequential vs parallel)
"""

import asyncio

import pytest  # type: ignore
import respx  # type: ignore
from concurrencia_rendimiento.fetcher_lab import (
    _make_ranges,
    count_primes_in_range,
    count_primes_parallel,
    count_primes_sequential,
    run_async,
    run_sync,
)
from httpx import Response

URLS = [f"https://fake.test/posts/{i}" for i in range(1, 6)]
PAYLOAD = {"id": 1, "title": "hello", "body": "world"}


# ─── 1. Sync fetcher ──────────────────────────────────────────────────────────


@respx.mock
def test_run_sync_returns_one_result_per_url():
    """run_sync must return exactly one JSON result per URL, in order."""
    for url in URLS:
        respx.get(url).mock(return_value=Response(200, json=PAYLOAD))

    results = run_sync(URLS)

    assert len(results) == len(URLS)
    assert all(r == PAYLOAD for r in results)


@respx.mock
def test_run_sync_raises_on_http_error():
    """run_sync must propagate HTTP errors raised by raise_for_status()."""
    respx.get(URLS[0]).mock(return_value=Response(500))

    with pytest.raises(Exception):
        run_sync([URLS[0]])


# ─── 2. Async fetcher ────────────────────────────────────────────────────────


@respx.mock
async def test_run_async_returns_one_result_per_url():
    """run_async must return the same number of results as input URLs."""
    for url in URLS:
        respx.get(url).mock(return_value=Response(200, json=PAYLOAD))

    results = await run_async(URLS, max_concurrent=3)

    assert len(results) == len(URLS)
    assert all(r == PAYLOAD for r in results)


@respx.mock
async def test_run_async_raises_on_http_error():
    """run_async must propagate HTTP errors raised by raise_for_status()."""
    respx.get(URLS[0]).mock(return_value=Response(404))

    with pytest.raises(Exception):
        await run_async([URLS[0]])


# ─── 3. Semaphore caps concurrency ───────────────────────────────────────────


@respx.mock
async def test_semaphore_caps_concurrency():
    """Peak simultaneous in-flight requests must not exceed max_concurrent.

    Each fake response waits 20 ms; we track the high-water mark of
    concurrently active requests and verify it never exceeds the cap.
    """
    MAX = 2
    active = 0
    peak = 0

    async def delayed_response(request):
        nonlocal active, peak
        active += 1
        peak = max(peak, active)
        await asyncio.sleep(0.02)
        active -= 1
        return Response(200, json=PAYLOAD)

    for url in URLS:
        respx.get(url).mock(side_effect=delayed_response)

    await run_async(URLS, max_concurrent=MAX)

    assert peak <= MAX, f"peak={peak} exceeded max_concurrent={MAX}"


@respx.mock
async def test_semaphore_allows_full_concurrency_when_limit_is_high():
    """When max_concurrent >= len(urls) all requests start concurrently."""
    started: list[int] = []

    async def track(request):
        started.append(1)
        return Response(200, json=PAYLOAD)

    for url in URLS:
        respx.get(url).mock(side_effect=track)

    await run_async(URLS, max_concurrent=len(URLS))

    assert len(started) == len(URLS)


# ─── 4. Range-splitting helper ───────────────────────────────────────────────


def test_make_ranges_covers_full_interval():
    """All integers from 2 to limit must appear in exactly one range."""
    limit = 100
    ranges = _make_ranges(limit, workers=4)

    covered: set[int] = set()
    for s, e in ranges:
        covered.update(range(s, e + 1))

    assert covered == set(range(2, limit + 1))


def test_make_ranges_no_overlap():
    """No integer must appear in more than one range."""
    ranges = _make_ranges(50, workers=3)
    all_nums: list[int] = []
    for s, e in ranges:
        all_nums.extend(range(s, e + 1))

    assert len(all_nums) == len(set(all_nums)), "ranges overlap"


def test_make_ranges_produces_at_most_workers_ranges():
    ranges = _make_ranges(10, workers=4)
    assert len(ranges) <= 4


def test_make_ranges_single_worker():
    """With one worker the single range must cover [2, limit]."""
    ranges = _make_ranges(20, workers=1)
    assert ranges == [(2, 20)]


# ─── 5. CPU-bound prime counting ─────────────────────────────────────────────


def test_count_primes_in_range_small_known_values():
    # Primes ≤ 10: 2 3 5 7 → 4
    assert count_primes_in_range(2, 10) == 4
    # Primes in [11, 20]: 11 13 17 19 → 4
    assert count_primes_in_range(11, 20) == 4
    # Single non-prime
    assert count_primes_in_range(4, 4) == 0
    # Single prime
    assert count_primes_in_range(7, 7) == 1


def test_count_primes_sequential_pi_100():
    """There are exactly 25 primes below 100 (prime-counting function π(100)=25)."""
    assert count_primes_sequential(100) == 25


def test_count_primes_parallel_matches_sequential():
    """ProcessPoolExecutor result must equal the single-process reference."""
    limit = 1_000  # fast enough for CI, but exercises the executor
    seq = count_primes_sequential(limit)
    par = count_primes_parallel(limit, workers=2)
    assert par == seq


def test_count_primes_parallel_different_worker_counts():
    """Result must be independent of how many workers are used."""
    limit = 500
    reference = count_primes_sequential(limit)
    for w in (1, 2, 3):
        assert (
            count_primes_parallel(limit, workers=w) == reference
        ), f"failed with workers={w}"
