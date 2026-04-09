from arquitectura_hexagonal.infrastructure.persistence.in_memory_order_repository import (
    InMemoryOrderRepository,
)
from tests.infrastructure.contracts.order_repository_contract import (
    OrderRepositoryContract,
)


class TestInMemoryOrderRepository(OrderRepositoryContract):
    """Runs the full repository contract against the in-memory adapter."""

    def make_repository(self):
        return InMemoryOrderRepository()
