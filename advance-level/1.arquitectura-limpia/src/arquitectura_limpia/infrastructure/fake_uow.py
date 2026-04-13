from arquitectura_limpia.domain.order import Order

# ── In-memory repository ──────────────────────────────────────────────────────
# Implements the OrderRepository port using a plain dict.
# Used in tests and simple demos — no real DB needed.


class FakeOrderRepository:
    def __init__(self) -> None:
        self._orders: dict[int, Order] = {}

    def save(self, order: Order) -> None:
        self._orders[order.order_id] = order

    def get_by_id(self, order_id: int) -> Order | None:
        return self._orders.get(order_id)


# ── In-memory Unit of Work ─────────────────────────────────────────────────────
# Implements AbstractUnitOfWork for testing purposes.
# Tracks whether commit() was called so tests can assert it.


class FakeUnitOfWork:
    def __init__(self) -> None:
        self.orders = FakeOrderRepository()
        self.committed = False

    def __enter__(self) -> "FakeUnitOfWork":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        pass  # No real rollback needed for in-memory storage

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        pass
