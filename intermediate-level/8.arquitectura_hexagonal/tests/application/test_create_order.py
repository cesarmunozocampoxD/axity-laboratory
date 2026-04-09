import pytest
from arquitectura_hexagonal.application.use_cases.create_order import CreateOrderUseCase
from arquitectura_hexagonal.domain.entities.order import Order
from arquitectura_hexagonal.infrastructure.persistence.in_memory_order_repository import (
    InMemoryOrderRepository,
)


class FakeNotifier:
    """Test double: records notifications so assertions can inspect them."""

    def __init__(self) -> None:
        self.notified: list[Order] = []

    def notify(self, order: Order) -> None:
        self.notified.append(order)


@pytest.fixture()
def repo():
    return InMemoryOrderRepository()


@pytest.fixture()
def notifier():
    return FakeNotifier()


@pytest.fixture()
def use_case(repo, notifier):
    return CreateOrderUseCase(repository=repo, notifier=notifier)


def test_create_order_returns_an_order(use_case):
    order = use_case.execute(product="Laptop", quantity=2, total=1500.0)

    assert order.product == "Laptop"
    assert order.quantity == 2
    assert order.total == 1500.0


def test_create_order_sets_pending_status(use_case):
    order = use_case.execute(product="Phone", quantity=1, total=300.0)

    assert order.status == "pending"


def test_create_order_persists_to_repository(use_case, repo):
    order = use_case.execute(product="Tablet", quantity=3, total=900.0)

    saved = repo.get_by_id(order.id)
    assert saved is not None
    assert saved.id == order.id
    assert saved.product == "Tablet"


def test_create_order_sends_notification(use_case, notifier):
    order = use_case.execute(product="Monitor", quantity=1, total=400.0)

    assert len(notifier.notified) == 1
    assert notifier.notified[0] == order


def test_create_order_rejects_invalid_quantity(use_case):
    with pytest.raises(ValueError, match="Quantity"):
        use_case.execute(product="Laptop", quantity=0, total=999.0)


def test_create_order_rejects_invalid_total(use_case):
    with pytest.raises(ValueError, match="Total"):
        use_case.execute(product="Laptop", quantity=1, total=-1.0)
