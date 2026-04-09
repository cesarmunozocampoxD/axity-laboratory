"""Contract tests for the OrderRepository port.

Any class that satisfies the OrderRepository port must pass all tests defined
here.  Concrete test classes simply inherit this base and implement
`make_repository()` to inject the adapter under test.
"""

from arquitectura_hexagonal.domain.entities.order import Order


class OrderRepositoryContract:
    """Base class: defines the expected behaviour of any OrderRepository adapter."""

    def make_repository(self):
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Contract tests
    # ------------------------------------------------------------------

    def test_save_and_retrieve_order(self):
        repo = self.make_repository()
        order = Order(id="contract-1", product="Laptop", quantity=1, total=999.0)

        repo.save(order)
        result = repo.get_by_id("contract-1")

        assert result is not None
        assert result.id == "contract-1"
        assert result.product == "Laptop"
        assert result.quantity == 1
        assert result.total == 999.0
        assert result.status == "pending"

    def test_get_nonexistent_order_returns_none(self):
        repo = self.make_repository()

        result = repo.get_by_id("does-not-exist")

        assert result is None

    def test_save_updates_existing_order(self):
        repo = self.make_repository()
        order = Order(id="contract-2", product="Tablet", quantity=1, total=300.0)
        repo.save(order)

        # mutate and persist again
        order.status = "confirmed"
        repo.save(order)

        result = repo.get_by_id("contract-2")
        assert result is not None
        assert result.status == "confirmed"

    def test_multiple_orders_are_stored_independently(self):
        repo = self.make_repository()
        order_a = Order(id="contract-3", product="Phone", quantity=2, total=600.0)
        order_b = Order(id="contract-4", product="Watch", quantity=1, total=200.0)

        repo.save(order_a)
        repo.save(order_b)

        assert repo.get_by_id("contract-3") is not None
        assert repo.get_by_id("contract-4") is not None
        assert repo.get_by_id("contract-3").product == "Phone"
        assert repo.get_by_id("contract-4").product == "Watch"
