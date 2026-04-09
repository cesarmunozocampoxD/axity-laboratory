from arquitectura_hexagonal.application.ports.notification_service import (
    NotificationService,
)
from arquitectura_hexagonal.application.ports.order_repository import OrderRepository
from arquitectura_hexagonal.domain.entities.order import Order


class CreateOrderUseCase:
    """Application use case: creates a new order.

    Orchestrates:
    1. Build the Order domain entity (invariants are checked inside it).
    2. Persist it through the repository port.
    3. Notify through the notification port.
    """

    def __init__(
        self,
        repository: OrderRepository,
        notifier: NotificationService,
    ) -> None:
        self.repository = repository
        self.notifier = notifier

    def execute(self, product: str, quantity: int, total: float) -> Order:
        order = Order(product=product, quantity=quantity, total=total)
        self.repository.save(order)
        self.notifier.notify(order)
        return order
