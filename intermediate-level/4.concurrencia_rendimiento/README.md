# Lab 4 – Concurrencia y Rendimiento

Practical lab demonstrating Python concurrency patterns tied to the GIL concepts in `WIKI.md`.

---

## Requirements

- Python >= 3.12
- [Poetry](https://python-poetry.org/) >= 2.0

---

## Setup

```bash
# Install runtime + dev dependencies
poetry install --with dev
```

---

## Run the demo

Fetches 10 URLs sequentially then concurrently, and counts primes up to 500 000
sequentially then in parallel across 4 worker processes. Prints elapsed time and speedup for both.

```bash
poetry run python -m concurrencia_rendimiento.fetcher_lab
```

Expected output (times vary by machine/network):

```
────────────────────────────────────────────────────
HTTP Fetcher Comparison
  10 URLs  ·  max_concurrent (async) = 5
────────────────────────────────────────────────────
  Sync  (sequential):    4.85s  → 10 responses
  Async (semaphore=5):   0.53s  → 10 responses
  Speedup: 9.1×

────────────────────────────────────────────────────
CPU-bound: Prime Counting
  Limit: 500,000  ·  Workers: 4
────────────────────────────────────────────────────
  Sequential:              1.06s  → 41,538 primes
  Parallel (4 workers):    0.61s  → 41,538 primes
  Speedup: 1.7×
```

---

## Run the tests

```bash
poetry run pytest tests/ -v
```

All HTTP calls are intercepted by `respx` — no real network access required.

| Test group | What it checks |
|---|---|
| Sync fetcher | Returns one JSON result per URL; propagates HTTP errors |
| Async fetcher | Results match input length; propagates HTTP errors |
| Semaphore | Peak concurrent requests never exceeds `max_concurrent` |
| Range splitting | `_make_ranges` covers interval fully, no overlaps |
| Prime counting | Sequential and parallel results match known values |

---

## Project structure

```
src/
  concurrencia_rendimiento/
    __init__.py
    fetcher_lab.py   ← main module
tests/
  test_fetcher_lab.py
pyproject.toml
WIKI.md              ← theory: GIL, I/O-bound vs CPU-bound, async, multiprocessing
```

---