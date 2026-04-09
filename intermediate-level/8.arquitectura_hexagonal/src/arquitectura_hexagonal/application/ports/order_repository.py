from typing import Optional, Protocol

from arquitectura_hexagonal.domain.entities.order import Order


class OrderRepository(Protocol):
    """Port: defines the contract any order persistence adapter must fulfill."""

    def save(self, order: Order) -> None:
        """Persist or update an order."""
        ...

    def get_by_id(self, order_id: str) -> Optional[Order]:
        """Return the order with the given id, or None if not found."""
        ...
