"""
LSP verification tests.

Both InMemoryUserRepository and SqlUserRepository are tested with the
identical test logic via pytest parametrize.

If both pass, they are behaviorally substitutable → LSP holds.
"""

import pytest
from solid.in_memory_repository import InMemoryUserRepository
from solid.sql_repository import SqlUserRepository
from solid.user_repository import User, UserRepository
from solid.user_service import UserService

# ---------------------------------------------------------------------------
# Fixture: one fixture, two concrete implementations
# ---------------------------------------------------------------------------


@pytest.fixture(
    params=["memory", "sql"],
    ids=["InMemoryUserRepository", "SqlUserRepository"],
)
def repo(request) -> UserRepository:
    if request.param == "memory":
        return InMemoryUserRepository()
    return SqlUserRepository()


@pytest.fixture
def service(repo: UserRepository) -> UserService:
    return UserService(repo)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

ALICE = User(id=1, name="Alice", email="alice@example.com")
BOB = User(id=2, name="Bob", email="bob@example.com")


# ---------------------------------------------------------------------------
# Tests — same expectations, two adapters
# ---------------------------------------------------------------------------


def test_save_and_get(service: UserService) -> None:
    """Saved user can be retrieved by id."""
    service.register(ALICE)

    result = service.find(ALICE.id)

    assert result == ALICE


def test_get_missing_returns_none(service: UserService) -> None:
    """Looking up a non-existent id returns None."""
    result = service.find(999)

    assert result is None


def test_list_all_returns_all_users(service: UserService) -> None:
    """All registered users appear in list_all."""
    service.register(ALICE)
    service.register(BOB)

    all_users = service.list_all()

    assert len(all_users) == 2
    assert ALICE in all_users
    assert BOB in all_users


def test_delete_removes_user(service: UserService) -> None:
    """Deleting a user means it is no longer findable."""
    service.register(ALICE)
    service.remove(ALICE.id)

    assert service.find(ALICE.id) is None


def test_list_all_empty_at_start(service: UserService) -> None:
    """A fresh repository has no users."""
    assert service.list_all() == []


def test_save_overwrites_existing(service: UserService) -> None:
    """Saving with the same id updates the record."""
    service.register(ALICE)

    updated = User(id=ALICE.id, name="Alice Updated", email="new@example.com")
    service.register(updated)

    result = service.find(ALICE.id)
    assert result == updated
