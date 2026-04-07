import pytest
from acceso_datos_orm.crud import (
    create_order,
    create_order_item,
    create_user,
    delete_order,
    delete_order_item,
    delete_user,
    get_order,
    get_order_item,
    get_user,
    get_user_by_email,
    list_order_items,
    list_orders,
    list_orders_by_user,
    list_users,
    update_order_item,
    update_order_status,
    update_user,
)
from acceso_datos_orm.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    s = Session()
    yield s
    s.close()
    Base.metadata.drop_all(engine)


# ---------------------------------------------------------------------------
# User tests
# ---------------------------------------------------------------------------


def test_create_user(session):
    user = create_user(session, "Janette", "janette@example.com")

    assert user.id is not None
    assert user.name == "Janette"
    assert user.email == "janette@example.com"


def test_get_user(session):
    user = create_user(session, "Janette", "janette@example.com")

    found = get_user(session, user.id)

    assert found is not None
    assert found.id == user.id
    assert found.name == "Janette"


def test_get_user_not_found(session):
    assert get_user(session, 999) is None


def test_get_user_by_email(session):
    create_user(session, "Janette", "janette@example.com")

    found = get_user_by_email(session, "janette@example.com")

    assert found is not None
    assert found.name == "Janette"


def test_get_user_by_email_not_found(session):
    assert get_user_by_email(session, "missing@example.com") is None


def test_list_users(session):
    create_user(session, "Janette", "janette@example.com")
    create_user(session, "Ana", "ana@example.com")

    users = list_users(session)

    assert len(users) == 2


def test_update_user_name(session):
    user = create_user(session, "Janette", "janette@example.com")

    updated = update_user(session, user.id, name="Janette Updated")

    assert updated is not None
    assert updated.name == "Janette Updated"
    assert updated.email == "janette@example.com"


def test_update_user_email(session):
    user = create_user(session, "Janette", "janette@example.com")

    updated = update_user(session, user.id, email="new@example.com")

    assert updated is not None
    assert updated.email == "new@example.com"


def test_update_user_not_found(session):
    assert update_user(session, 999, name="Ghost") is None


def test_delete_user(session):
    user = create_user(session, "Janette", "janette@example.com")

    result = delete_user(session, user.id)

    assert result is True
    assert get_user(session, user.id) is None


def test_delete_user_not_found(session):
    assert delete_user(session, 999) is False


# ---------------------------------------------------------------------------
# Order tests
# ---------------------------------------------------------------------------


def test_create_order(session):
    user = create_user(session, "Janette", "janette@example.com")

    order = create_order(session, user.id)

    assert order.id is not None
    assert order.user_id == user.id
    assert order.status == "pending"
    assert order.created_at is not None


def test_create_order_custom_status(session):
    user = create_user(session, "Janette", "janette@example.com")

    order = create_order(session, user.id, status="confirmed")

    assert order.status == "confirmed"


def test_get_order(session):
    user = create_user(session, "Janette", "janette@example.com")
    order = create_order(session, user.id)

    found = get_order(session, order.id)

    assert found is not None
    assert found.id == order.id


def test_get_order_not_found(session):
    assert get_order(session, 999) is None


def test_list_orders(session):
    user = create_user(session, "Janette", "janette@example.com")
    create_order(session, user.id)
    create_order(session, user.id)

    orders = list_orders(session)

    assert len(orders) == 2


def test_list_orders_by_user(session):
    user_a = create_user(session, "Janette", "janette@example.com")
    user_b = create_user(session, "Ana", "ana@example.com")
    create_order(session, user_a.id)
    create_order(session, user_a.id)
    create_order(session, user_b.id)

    orders = list_orders_by_user(session, user_a.id)

    assert len(orders) == 2
    assert all(o.user_id == user_a.id for o in orders)


def test_update_order_status(session):
    user = create_user(session, "Janette", "janette@example.com")
    order = create_order(session, user.id)

    updated = update_order_status(session, order.id, "shipped")

    assert updated is not None
    assert updated.status == "shipped"


def test_update_order_status_not_found(session):
    assert update_order_status(session, 999, "shipped") is None


def test_delete_order(session):
    user = create_user(session, "Janette", "janette@example.com")
    order = create_order(session, user.id)

    result = delete_order(session, order.id)

    assert result is True
    assert get_order(session, order.id) is None


def test_delete_order_not_found(session):
    assert delete_order(session, 999) is False


# ---------------------------------------------------------------------------
# OrderItem tests
# ---------------------------------------------------------------------------


def test_create_order_item(session):
    user = create_user(session, "Janette", "janette@example.com")
    order = create_order(session, user.id)

    item = create_order_item(session, order.id, "Widget", 2, 9.99)

    assert item.id is not None
    assert item.order_id == order.id
    assert item.product_name == "Widget"
    assert item.quantity == 2


def test_get_order_item(session):
    user = create_user(session, "Janette", "janette@example.com")
    order = create_order(session, user.id)
    item = create_order_item(session, order.id, "Widget", 2, 9.99)

    found = get_order_item(session, item.id)

    assert found is not None
    assert found.id == item.id


def test_get_order_item_not_found(session):
    assert get_order_item(session, 999) is None


def test_list_order_items(session):
    user = create_user(session, "Janette", "janette@example.com")
    order = create_order(session, user.id)
    create_order_item(session, order.id, "Widget", 2, 9.99)
    create_order_item(session, order.id, "Gadget", 1, 24.50)

    items = list_order_items(session, order.id)

    assert len(items) == 2


def test_update_order_item(session):
    user = create_user(session, "Janette", "janette@example.com")
    order = create_order(session, user.id)
    item = create_order_item(session, order.id, "Widget", 2, 9.99)

    updated = update_order_item(session, item.id, quantity=5, unit_price=8.00)

    assert updated is not None
    assert updated.quantity == 5


def test_update_order_item_not_found(session):
    assert update_order_item(session, 999, product_name="Ghost") is None


def test_delete_order_item(session):
    user = create_user(session, "Janette", "janette@example.com")
    order = create_order(session, user.id)
    item = create_order_item(session, order.id, "Widget", 2, 9.99)

    result = delete_order_item(session, item.id)

    assert result is True
    assert get_order_item(session, item.id) is None


def test_delete_order_item_not_found(session):
    assert delete_order_item(session, 999) is False


# ---------------------------------------------------------------------------
# Cascade tests
# ---------------------------------------------------------------------------


def test_delete_user_cascades_to_orders_and_items(session):
    user = create_user(session, "Janette", "janette@example.com")
    order = create_order(session, user.id)
    item = create_order_item(session, order.id, "Widget", 2, 9.99)

    delete_user(session, user.id)

    assert get_order(session, order.id) is None
    assert get_order_item(session, item.id) is None


def test_delete_order_cascades_to_items(session):
    user = create_user(session, "Janette", "janette@example.com")
    order = create_order(session, user.id)
    item = create_order_item(session, order.id, "Widget", 2, 9.99)

    delete_order(session, order.id)

    assert get_order_item(session, item.id) is None
    assert get_user(session, user.id) is not None
