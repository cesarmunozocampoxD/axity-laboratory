from dataclasses import dataclass

# ── Domain Event ─────────────────────────────────────────────────────────────
# Represents a meaningful business fact: "an order was created."
# Named in past tense, immutable, no framework dependencies.


@dataclass(frozen=True)
class OrderCreated:
    order_id: int
    product: str


# ── Entity ────────────────────────────────────────────────────────────────────
# Holds identity, state, and business rules.
# Records domain events when significant state changes happen.


class Order:
    def __init__(self, order_id: int, product: str) -> None:
        self.order_id = order_id
        self.product = product
        self.status = "created"
        self.events: list = []

        # The entity itself records the event — no framework, no DB, no HTTP.
        self.events.append(OrderCreated(order_id=self.order_id, product=self.product))
