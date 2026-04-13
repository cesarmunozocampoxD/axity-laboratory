from typing import Protocol

from arquitectura_limpia.domain.order import Order

# ── Repository gateway (outbound port) ───────────────────────────────────────
# The application layer defines what it *needs* from persistence.
# Infrastructure will implement it — the use case never knows the details.


class OrderRepository(Protocol):
    def save(self, order: Order) -> None: ...

    def get_by_id(self, order_id: int) -> Order | None: ...


# ── Unit of Work (abstract) ───────────────────────────────────────────────────
# Groups related repository operations into a single transaction boundary.
# Usage:
#   with uow:
#       uow.orders.save(order)
#       uow.commit()
#
# On any unhandled exception __exit__ calls rollback automatically.


class AbstractUnitOfWork:
    orders: OrderRepository

    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.rollback()

    def commit(self) -> None:
        raise NotImplementedError

    def rollback(self) -> None:
        raise NotImplementedError
