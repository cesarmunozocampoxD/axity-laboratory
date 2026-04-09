from dataclasses import dataclass
from typing import Protocol


@dataclass
class User:
    id: int
    name: str
    email: str


class UserRepository(Protocol):
    """Port: contract that any storage implementation must fulfill."""

    def save(self, user: User) -> None: ...

    def get(self, user_id: int) -> User | None: ...

    def get_all(self) -> list[User]: ...

    def delete(self, user_id: int) -> None: ...
