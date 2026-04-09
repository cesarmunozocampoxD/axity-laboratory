import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from solid.in_memory_repository import InMemoryUserRepository
from solid.sql_repository import SqlUserRepository
from solid.user_repository import User
from solid.user_service import UserService


def run_demo(label: str, service: UserService) -> None:
    print(f"=== {label} ===")
    service.register(User(1, "Alice", "alice@example.com"))
    service.register(User(2, "Bob", "bob@example.com"))
    print("All users :", service.list_all())
    print("Find id=1 :", service.find(1))
    service.remove(2)
    print("After del Bob:", service.list_all())
    print()


run_demo("InMemory Implementation", UserService(InMemoryUserRepository()))
run_demo("SQL Implementation", UserService(SqlUserRepository()))
