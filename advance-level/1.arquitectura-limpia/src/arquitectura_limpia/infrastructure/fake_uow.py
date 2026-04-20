from arquitectura_limpia.application.ports import AbstractUnitOfWork, OrderRepository
from arquitectura_limpia.domain.order import Order

# ── In-memory repository ──────────────────────────────────────────────────────
# Implements the OrderRepository port using a plain dict.
# Used in tests and simple demos — no real DB needed.


class FakeOrderRepository(OrderRepository):
    def __init__(self) -> None:
        self._orders: dict[int, Order] = {}

    def save(self, order: Order) -> None:
        self._orders[order.order_id] = order

    def get_by_id(self, order_id: int) -> Order | None:
        return self._orders.get(order_id)


# ── In-memory Unit of Work ─────────────────────────────────────────────────────
# Implements AbstractUnitOfWork for testing purposes.
# Tracks whether commit() was called so tests can assert it.


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self) -> None:
        self.orders = FakeOrderRepository()
        self.committed = False

    def __enter__(self) -> "FakeUnitOfWork":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        pass  # No real rollback needed for in-memory storage

    def commit(self) -> None:
        # Typical production commit flow (DB-backed UoW):
        # 1) Flush/execute pending inserts, updates, and deletes.
        # 2) Validate DB constraints and finalize transaction atomically.
        # 3) Persist outbox records/events in the same transaction.
        # 4) Release locks and mark transaction as completed.
        self.committed = True

    def rollback(self) -> None:
        pass
