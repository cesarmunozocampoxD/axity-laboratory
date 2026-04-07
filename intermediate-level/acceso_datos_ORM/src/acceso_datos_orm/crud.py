import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Order, OrderItem, User

# ---------------------------------------------------------------------------
# User CRUD
# ---------------------------------------------------------------------------


def create_user(session: Session, name: str, email: str) -> User:
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)


def get_user_by_email(session: Session, email: str) -> User | None:
    return session.scalars(select(User).where(User.email == email)).first()


def list_users(session: Session) -> list[User]:
    return list(session.scalars(select(User)).all())


def update_user(
    session: Session,
    user_id: int,
    name: str | None = None,
    email: str | None = None,
) -> User | None:
    user = session.get(User, user_id)
    if user is None:
        return None
    if name is not None:
        user.name = name
    if email is not None:
        user.email = email
    session.commit()
    session.refresh(user)
    return user


def delete_user(session: Session, user_id: int) -> bool:
    user = session.get(User, user_id)
    if user is None:
        return False
    session.delete(user)
    session.commit()
    return True


# ---------------------------------------------------------------------------
# Order CRUD
# ---------------------------------------------------------------------------


def create_order(session: Session, user_id: int, status: str = "pending") -> Order:
    order = Order(
        user_id=user_id,
        status=status,
        created_at=datetime.datetime.now(datetime.UTC),
    )
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


def get_order(session: Session, order_id: int) -> Order | None:
    return session.get(Order, order_id)


def list_orders(session: Session) -> list[Order]:
    return list(session.scalars(select(Order)).all())


def list_orders_by_user(session: Session, user_id: int) -> list[Order]:
    return list(session.scalars(select(Order).where(Order.user_id == user_id)).all())


def update_order_status(session: Session, order_id: int, status: str) -> Order | None:
    order = session.get(Order, order_id)
    if order is None:
        return None
    order.status = status
    session.commit()
    session.refresh(order)
    return order


def delete_order(session: Session, order_id: int) -> bool:
    order = session.get(Order, order_id)
    if order is None:
        return False
    session.delete(order)
    session.commit()
    return True


# ---------------------------------------------------------------------------
# OrderItem CRUD
# ---------------------------------------------------------------------------


def create_order_item(
    session: Session,
    order_id: int,
    product_name: str,
    quantity: int,
    unit_price: float,
) -> OrderItem:
    item = OrderItem(
        order_id=order_id,
        product_name=product_name,
        quantity=quantity,
        unit_price=unit_price,
    )
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def get_order_item(session: Session, item_id: int) -> OrderItem | None:
    return session.get(OrderItem, item_id)


def list_order_items(session: Session, order_id: int) -> list[OrderItem]:
    return list(
        session.scalars(select(OrderItem).where(OrderItem.order_id == order_id)).all()
    )


def update_order_item(
    session: Session,
    item_id: int,
    product_name: str | None = None,
    quantity: int | None = None,
    unit_price: float | None = None,
) -> OrderItem | None:
    item = session.get(OrderItem, item_id)
    if item is None:
        return None
    if product_name is not None:
        item.product_name = product_name
    if quantity is not None:
        item.quantity = quantity
    if unit_price is not None:
        item.unit_price = unit_price
    session.commit()
    session.refresh(item)
    return item


def delete_order_item(session: Session, item_id: int) -> bool:
    item = session.get(OrderItem, item_id)
    if item is None:
        return False
    session.delete(item)
    session.commit()
    return True
