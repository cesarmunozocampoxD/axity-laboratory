from solid.user_repository import User, UserRepository


class UserService:
    """
    High-level service that depends on the UserRepository port (Protocol).

    It does not know or care whether storage is in-memory, SQL, or anything else.
    That is Dependency Inversion in practice.
    """

    def __init__(self, repository: UserRepository) -> None:
        self._repo = repository

    def register(self, user: User) -> None:
        self._repo.save(user)

    def find(self, user_id: int) -> User | None:
        return self._repo.get(user_id)

    def list_all(self) -> list[User]:
        return self._repo.get_all()

    def remove(self, user_id: int) -> None:
        self._repo.delete(user_id)
