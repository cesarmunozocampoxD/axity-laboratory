"""
Strategy Pattern – Pricing

Problem: a product can be priced in different ways depending on the
context (regular, member discount, seasonal sale).  We want to be able
to swap the pricing algorithm at runtime without touching the
PriceCalculator.

Pattern: each pricing rule is encapsulated in its own class that shares
the same interface.  PriceCalculator is initialised with a strategy and
simply delegates the calculation to it.
"""


class RegularPricing:
    """Full price – no discount."""

    def calculate(self, base_price: float) -> float:
        return base_price


class MemberPricing:
    """10 % discount for registered members."""

    def calculate(self, base_price: float) -> float:
        return round(base_price * 0.90, 2)


class SalePricing:
    """30 % discount during a seasonal sale."""

    def calculate(self, base_price: float) -> float:
        return round(base_price * 0.70, 2)


class PriceCalculator:
    """Context that uses a pricing strategy to compute the final price."""

    def __init__(self, strategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy) -> None:
        """Swap the strategy at runtime."""
        self._strategy = strategy

    def get_price(self, base_price: float) -> float:
        return self._strategy.calculate(base_price)
