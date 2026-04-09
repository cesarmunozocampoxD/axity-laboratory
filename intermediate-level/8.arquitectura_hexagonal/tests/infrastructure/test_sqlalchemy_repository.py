from arquitectura_hexagonal.infrastructure.persistence.sqlalchemy_order_repository import (
    SqlAlchemyOrderRepository,
    create_in_memory_engine,
)
from sqlalchemy.orm import Session
from tests.infrastructure.contracts.order_repository_contract import (
    OrderRepositoryContract,
)


class TestSqlAlchemyOrderRepository(OrderRepositoryContract):
    """Runs the full repository contract against the SQLAlchemy adapter.

    Uses an SQLite in-memory database so tests stay fast and isolated.
    Each test gets a fresh engine via `make_repository`.
    """

    def make_repository(self):
        engine = create_in_memory_engine()
        session = Session(engine)
        return SqlAlchemyOrderRepository(session)
