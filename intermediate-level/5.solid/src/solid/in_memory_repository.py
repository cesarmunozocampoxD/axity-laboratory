from solid.user_repository import User


class InMemoryUserRepository:
    """In-memory implementation of UserRepository (adapter)."""

    def __init__(self) -> None:
        self._store: dict[int, User] = {}

    def save(self, user: User) -> None:
        self._store[user.id] = user

    def get(self, user_id: int) -> User | None:
        return self._store.get(user_id)

    def get_all(self) -> list[User]:
        return list(self._store.values())

    def delete(self, user_id: int) -> None:
        self._store.pop(user_id, None)
