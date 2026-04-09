from typing import Optional

from arquitectura_hexagonal.domain.entities.order import Order


class InMemoryOrderRepository:
    """Infrastructure adapter: stores orders in a plain Python dict.

    Useful for unit tests and local development without a real database.
    Satisfies the OrderRepository port.
    """

    def __init__(self) -> None:
        self._store: dict[str, Order] = {}

    def save(self, order: Order) -> None:
        self._store[order.id] = order

    def get_by_id(self, order_id: str) -> Optional[Order]:
        return self._store.get(order_id)
