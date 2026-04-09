"""
Adapter Pattern – External Pricing Provider

Problem: an external pricing service returns prices through its own
interface (fetch_price) and its own response shape.  Our application
expects a uniform get_price(base_price) interface.

Pattern: ExternalPricingAdapter wraps the external service and translates
its interface into the one our application already knows.  The rest of the
codebase never needs to know about the external shape of the API.
"""

# ---------------------------------------------------------------------------
# Simulated external service (third-party, we cannot modify it)
# ---------------------------------------------------------------------------


class ExternalPricingService:
    """
    Pretends to be a third-party pricing API.
    Its interface is completely different from what our app expects.
    """

    def fetch_price(self, product_id: str, amount: float) -> dict:
        """Returns a dict with vendor-specific keys."""
        discount = 0.15  # vendor always applies a 15 % platform fee reduction
        return {
            "product": product_id,
            "original": amount,
            "final_price": round(amount * (1 - discount), 2),
        }


# ---------------------------------------------------------------------------
# Adapter – makes ExternalPricingService look like our PriceCalculator
# ---------------------------------------------------------------------------


class ExternalPricingAdapter:
    """
    Exposes get_price(base_price) so the rest of the application can use
    ExternalPricingService without knowing its real interface.
    """

    def __init__(self, service: ExternalPricingService, product_id: str) -> None:
        self._service = service
        self._product_id = product_id

    def get_price(self, base_price: float) -> float:
        result = self._service.fetch_price(self._product_id, base_price)
        return result["final_price"]
