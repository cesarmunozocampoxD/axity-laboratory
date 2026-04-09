"""
Decorator Pattern – Cache

Problem: computing the final price for a product may call an external
service or a heavy calculation.  We do not want to repeat the same
computation for the same base price.

Pattern: CachedPriceCalculator wraps any object that exposes
get_price(base_price) and transparently stores results in a dictionary.
Callers can use it exactly like the original calculator.
"""

from patrones.pricing import PriceCalculator


class CachedPriceCalculator:
    """Adds an in-memory cache layer on top of any PriceCalculator."""

    def __init__(self, calculator: PriceCalculator) -> None:
        self._calculator = calculator
        self._cache: dict[float, float] = {}

    def get_price(self, base_price: float) -> float:
        if base_price not in self._cache:
            self._cache[base_price] = self._calculator.get_price(base_price)
        return self._cache[base_price]

    @property
    def cache_size(self) -> int:
        """Number of entries currently stored in the cache."""
        return len(self._cache)

    def clear_cache(self) -> None:
        """Invalidate all cached results (e.g. after a strategy change)."""
        self._cache.clear()
