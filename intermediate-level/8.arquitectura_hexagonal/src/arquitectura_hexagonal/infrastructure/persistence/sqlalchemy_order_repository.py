from typing import Optional

from arquitectura_hexagonal.domain.entities.order import Order
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    pass


class OrderModel(Base):
    """SQLAlchemy ORM model — lives in infrastructure, not in the domain."""

    __tablename__ = "orders"

    id = Column(String, primary_key=True)
    product = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    total = Column(Float, nullable=False)
    status = Column(String, nullable=False)


def create_in_memory_engine():
    """Helper that creates a fresh SQLite in-memory engine with the schema.

    Useful for tests and local development.
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


class SqlAlchemyOrderRepository:
    """Infrastructure adapter: persists orders using SQLAlchemy.

    Works with any SQLAlchemy-supported database (SQLite, PostgreSQL, etc.).
    Satisfies the OrderRepository port.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, order: Order) -> None:
        model = OrderModel(
            id=order.id,
            product=order.product,
            quantity=order.quantity,
            total=order.total,
            status=order.status,
        )
        self._session.merge(model)
        self._session.commit()

    def get_by_id(self, order_id: str) -> Optional[Order]:
        model = self._session.get(OrderModel, order_id)
        if model is None:
            return None
        return Order(
            id=model.id,
            product=model.product,
            quantity=model.quantity,
            total=model.total,
            status=model.status,
        )
