from arquitectura_limpia.application.ports import AbstractUnitOfWork
from arquitectura_limpia.application.presenters.order_presenter import OrderPresenter
from arquitectura_limpia.domain.order import Order

# ── Use Case ──────────────────────────────────────────────────────────────────
# Orchestrates the "create order" workflow:
#   1. Open a Unit of Work transaction scope.
#   2. Create the Order entity (domain event is recorded automatically).
#   3. Persist via the UoW repository.
#   4. Commit the transaction.
#   5. Dispatch collected domain events AFTER commit (safe ordering).
#   6. Return the formatted output through the Presenter.


class CreateOrderUseCase:
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        event_bus,
        presenter: OrderPresenter,
    ) -> None:
        self.uow = uow
        self.event_bus = event_bus
        self.presenter = presenter

    def execute(self, order_id: int, product: str) -> dict:
        with self.uow:
            order = Order(order_id=order_id, product=product)
            self.uow.orders.save(order)
            self.uow.commit()

        # Events are dispatched AFTER the transaction commits to avoid
        # publishing facts about changes that were never actually saved.
        for event in order.events:
            self.event_bus.publish(event)

        return self.presenter.present(order)
