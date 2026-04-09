from typing import Protocol

from arquitectura_hexagonal.domain.entities.order import Order


class NotificationService(Protocol):
    """Port: defines the contract any notification adapter must fulfill."""

    def notify(self, order: Order) -> None:
        """Send a notification about the given order."""
        ...
