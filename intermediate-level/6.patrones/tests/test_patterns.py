"""
Tests – Strategy, Decorator, Adapter lab

Run:
    poetry run pytest tests/ -v
"""

from patrones.cache import CachedPriceCalculator
from patrones.pricing import (
    MemberPricing,
    PriceCalculator,
    RegularPricing,
    SalePricing,
)
from patrones.provider import ExternalPricingAdapter, ExternalPricingService

# ===========================================================================
# Strategy – PriceCalculator
# ===========================================================================


class TestRegularPricing:
    def test_returns_base_price_unchanged(self):
        calc = PriceCalculator(RegularPricing())
        assert calc.get_price(100.0) == 100.0

    def test_works_with_decimal_price(self):
        calc = PriceCalculator(RegularPricing())
        assert calc.get_price(49.99) == 49.99


class TestMemberPricing:
    def test_applies_10_percent_discount(self):
        calc = PriceCalculator(MemberPricing())
        assert calc.get_price(100.0) == 90.0

    def test_rounds_to_two_decimals(self):
        calc = PriceCalculator(MemberPricing())
        # 33.33 * 0.90 = 29.997 → rounded to 2 decimals = 30.0
        assert calc.get_price(33.33) == 30.0


class TestSalePricing:
    def test_applies_30_percent_discount(self):
        calc = PriceCalculator(SalePricing())
        assert calc.get_price(100.0) == 70.0

    def test_rounds_to_two_decimals(self):
        calc = PriceCalculator(SalePricing())
        assert calc.get_price(33.33) == 23.33


class TestStrategySwap:
    def test_can_change_strategy_at_runtime(self):
        calc = PriceCalculator(RegularPricing())
        assert calc.get_price(100.0) == 100.0

        calc.set_strategy(MemberPricing())
        assert calc.get_price(100.0) == 90.0

        calc.set_strategy(SalePricing())
        assert calc.get_price(100.0) == 70.0


# ===========================================================================
# Decorator – CachedPriceCalculator
# ===========================================================================


class TestCachedPriceCalculator:
    def test_returns_correct_price(self):
        calc = PriceCalculator(RegularPricing())
        cached = CachedPriceCalculator(calc)
        assert cached.get_price(100.0) == 100.0

    def test_cache_is_empty_initially(self):
        calc = PriceCalculator(RegularPricing())
        cached = CachedPriceCalculator(calc)
        assert cached.cache_size == 0

    def test_cache_grows_after_first_call(self):
        calc = PriceCalculator(RegularPricing())
        cached = CachedPriceCalculator(calc)
        cached.get_price(100.0)
        assert cached.cache_size == 1

    def test_same_price_uses_cache(self):
        """Second call must not increase cache size."""
        calc = PriceCalculator(RegularPricing())
        cached = CachedPriceCalculator(calc)
        cached.get_price(100.0)
        cached.get_price(100.0)
        assert cached.cache_size == 1

    def test_different_prices_create_separate_entries(self):
        calc = PriceCalculator(RegularPricing())
        cached = CachedPriceCalculator(calc)
        cached.get_price(100.0)
        cached.get_price(200.0)
        assert cached.cache_size == 2

    def test_clear_cache_resets_size(self):
        calc = PriceCalculator(MemberPricing())
        cached = CachedPriceCalculator(calc)
        cached.get_price(100.0)
        cached.clear_cache()
        assert cached.cache_size == 0

    def test_cached_result_matches_direct_result(self):
        """Value from cache must equal value from the wrapped calculator."""
        strategy = SalePricing()
        calc = PriceCalculator(strategy)
        cached = CachedPriceCalculator(calc)

        direct = calc.get_price(80.0)
        via_cache = cached.get_price(80.0)

        assert via_cache == direct


# ===========================================================================
# Adapter – ExternalPricingAdapter
# ===========================================================================


class TestExternalPricingService:
    """Verify the raw external service so we understand what we're adapting."""

    def test_returns_dict_with_final_price(self):
        service = ExternalPricingService()
        result = service.fetch_price("PROD-1", 100.0)
        assert "final_price" in result

    def test_applies_15_percent_reduction(self):
        service = ExternalPricingService()
        result = service.fetch_price("PROD-1", 100.0)
        assert result["final_price"] == 85.0


class TestExternalPricingAdapter:
    def test_exposes_get_price_interface(self):
        service = ExternalPricingService()
        adapter = ExternalPricingAdapter(service, "PROD-1")
        # Must have a get_price method (same interface as PriceCalculator)
        assert hasattr(adapter, "get_price")

    def test_returns_correct_discounted_price(self):
        service = ExternalPricingService()
        adapter = ExternalPricingAdapter(service, "PROD-1")
        assert adapter.get_price(100.0) == 85.0

    def test_adapter_hides_provider_interface(self):
        """
        The adapter should NOT expose fetch_price –
        callers must not depend on the external shape.
        """
        service = ExternalPricingService()
        adapter = ExternalPricingAdapter(service, "PROD-1")
        assert not hasattr(adapter, "fetch_price")

    def test_works_with_cached_decorator(self):
        """Adapter is compatible with the cache decorator."""
        service = ExternalPricingService()
        adapter = ExternalPricingAdapter(service, "PROD-42")
        cached = CachedPriceCalculator(adapter)  # type: ignore

        price = cached.get_price(200.0)
        assert price == 170.0
        assert cached.cache_size == 1

    def test_different_product_ids_independent_adapters(self):
        service = ExternalPricingService()
        adapter_a = ExternalPricingAdapter(service, "PROD-A")
        adapter_b = ExternalPricingAdapter(service, "PROD-B")

        # Both apply the same logic but are independently configured
        assert adapter_a.get_price(100.0) == adapter_b.get_price(100.0)
