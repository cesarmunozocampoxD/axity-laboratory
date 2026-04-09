import sqlite3

from solid.user_repository import User


class SqlUserRepository:
    """SQLite implementation of UserRepository (adapter)."""

    def __init__(self, connection: sqlite3.Connection | None = None) -> None:
        self._conn = connection or sqlite3.connect(":memory:")
        self._create_table()

    def _create_table(self) -> None:
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id    INTEGER PRIMARY KEY,
                name  TEXT NOT NULL,
                email TEXT NOT NULL
            )
            """)
        self._conn.commit()

    def save(self, user: User) -> None:
        self._conn.execute(
            "INSERT OR REPLACE INTO users (id, name, email) VALUES (?, ?, ?)",
            (user.id, user.name, user.email),
        )
        self._conn.commit()

    def get(self, user_id: int) -> User | None:
        cursor = self._conn.execute(
            "SELECT id, name, email FROM users WHERE id = ?", (user_id,)
        )
        row = cursor.fetchone()
        return User(id=row[0], name=row[1], email=row[2]) if row else None

    def get_all(self) -> list[User]:
        cursor = self._conn.execute("SELECT id, name, email FROM users")
        return [User(id=row[0], name=row[1], email=row[2]) for row in cursor.fetchall()]

    def delete(self, user_id: int) -> None:
        self._conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self._conn.commit()
