from .base import Base
from .session import engine


def create_tables() -> None:
    # Import all models here so SQLAlchemy registers them before creating tables
    from apis_fastapi.app.models import order  # noqa: F401

    Base.metadata.create_all(bind=engine)
