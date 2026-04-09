import pytest
from arquitectura_hexagonal.domain.entities.order import Order


def test_order_is_created_with_pending_status():
    order = Order(product="Laptop", quantity=2, total=1500.0)

    assert order.product == "Laptop"
    assert order.quantity == 2
    assert order.total == 1500.0
    assert order.status == "pending"


def test_order_gets_a_unique_id():
    order_a = Order(product="Laptop", quantity=1, total=999.0)
    order_b = Order(product="Laptop", quantity=1, total=999.0)

    assert order_a.id != order_b.id


def test_order_accepts_explicit_id():
    order = Order(id="fixed-id", product="Phone", quantity=1, total=300.0)

    assert order.id == "fixed-id"


def test_order_raises_when_quantity_is_zero():
    with pytest.raises(ValueError, match="Quantity"):
        Order(product="Laptop", quantity=0, total=999.0)


def test_order_raises_when_quantity_is_negative():
    with pytest.raises(ValueError, match="Quantity"):
        Order(product="Laptop", quantity=-1, total=999.0)


def test_order_raises_when_total_is_zero():
    with pytest.raises(ValueError, match="Total"):
        Order(product="Laptop", quantity=1, total=0.0)


def test_order_raises_when_total_is_negative():
    with pytest.raises(ValueError, match="Total"):
        Order(product="Laptop", quantity=1, total=-10.0)
