# Python: `sqlite3` and Drivers for PostgreSQL / SQL Server

## 1. Overview

In Python, database access usually follows the same general pattern:

1. open a connection
2. create a cursor or use a connection method
3. execute SQL
4. fetch results when needed
5. commit or roll back the transaction
6. close resources

For SQLite, Python includes the built-in `sqlite3` module.

For PostgreSQL, common choices include:
- `psycopg`
- `asyncpg`

For SQL Server, common choices include:
- `pyodbc`
- `mssql-python`

---

## 2. `sqlite3`

`sqlite3` is part of Python’s standard library.

It is a DB-API 2.0 interface for SQLite, which is:
- lightweight
- file-based
- serverless

It is a good option for:
- local apps
- prototypes
- tests
- small tools

### Basic connection

```python
import sqlite3

conn = sqlite3.connect("app.db")
cursor = conn.cursor()
```

### Create a table

```python
import sqlite3

conn = sqlite3.connect("app.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
)
""")

conn.commit()
conn.close()
```

### Insert data

`sqlite3` commonly uses `?` placeholders.

```python
import sqlite3

conn = sqlite3.connect("app.db")
cursor = conn.cursor()

cursor.execute(
    "INSERT INTO users (name, age) VALUES (?, ?)",
    ("Janette", 24)
)

conn.commit()
conn.close()
```

### Query data

```python
import sqlite3

conn = sqlite3.connect("app.db")
cursor = conn.cursor()

cursor.execute("SELECT id, name, age FROM users")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
```

### Fetch one row

```python
import sqlite3

conn = sqlite3.connect("app.db")
cursor = conn.cursor()

cursor.execute("SELECT id, name, age FROM users WHERE name = ?", ("Janette",))
row = cursor.fetchone()

print(row)

conn.close()
```

### Row factory for dictionary-like access

```python
import sqlite3

conn = sqlite3.connect("app.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT id, name, age FROM users")
row = cursor.fetchone()

print(row["name"])
print(dict(row))

conn.close()
```

### In-memory database

```python
import sqlite3

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("CREATE TABLE demo (id INTEGER)")
cursor.execute("INSERT INTO demo (id) VALUES (?)", (1,))
cursor.execute("SELECT * FROM demo")

print(cursor.fetchall())

conn.close()
```

### When to use `sqlite3`

Use `sqlite3` when:
- you want zero server setup
- the database is local to the app
- you are prototyping
- you are writing small desktop or CLI tools
- you want simple automated tests

---

## 3. PostgreSQL drivers

Two important options are:

- **`psycopg`**: the main modern PostgreSQL adapter, with DB-API-style usage and async support
- **`asyncpg`**: an async-native PostgreSQL driver built for `asyncio`

---

## 4. `psycopg` (Psycopg 3)

`psycopg` is the main modern PostgreSQL adapter.

It is a strong default when you want:
- PostgreSQL support
- DB-API-style code
- sync or async access

### Install

```bash
pip install "psycopg[binary]"
```

### Basic connection

```python
import psycopg

with psycopg.connect("dbname=test user=postgres password=secret host=localhost") as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT version()")
        print(cur.fetchone())
```

### Create a table

```python
import psycopg

with psycopg.connect("dbname=test user=postgres password=secret host=localhost") as conn:
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        """)
    conn.commit()
```

### Insert data

`psycopg` uses `%s` placeholders.

```python
import psycopg

with psycopg.connect("dbname=test user=postgres password=secret host=localhost") as conn:
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO users (name, age) VALUES (%s, %s)",
            ("Janette", 24)
        )
    conn.commit()
```

### Query data

```python
import psycopg

with psycopg.connect("dbname=test user=postgres password=secret host=localhost") as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, age FROM users ORDER BY id")
        rows = cur.fetchall()

        for row in rows:
            print(row)
```

### Async connection in Psycopg 3

```python
import asyncio
import psycopg

async def main():
    conn = await psycopg.AsyncConnection.connect(
        "dbname=test user=postgres password=secret host=localhost"
    )

    async with conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT version()")
            row = await cur.fetchone()
            print(row)

asyncio.run(main())
```

### When to use `psycopg`

Use `psycopg` when:
- you want the standard PostgreSQL choice
- you want DB-API-style code
- you may need sync or async usage
- you want a solid default for PostgreSQL apps

---

## 5. `asyncpg`

`asyncpg` is an async-native PostgreSQL driver.

It is useful when:
- your app already uses `asyncio`
- you want high async performance
- you do not need DB-API compatibility

### Install

```bash
pip install asyncpg
```

### Basic connection

```python
import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect(
        user="postgres",
        password="secret",
        database="test",
        host="localhost"
    )

    row = await conn.fetchrow("SELECT version()")
    print(row)

    await conn.close()

asyncio.run(main())
```

### Create a table

```python
import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect(
        user="postgres",
        password="secret",
        database="test",
        host="localhost"
    )

    await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)

    await conn.close()

asyncio.run(main())
```

### Insert data

`asyncpg` uses `$1`, `$2`, and so on.

```python
import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect(
        user="postgres",
        password="secret",
        database="test",
        host="localhost"
    )

    await conn.execute(
        "INSERT INTO users (name, age) VALUES ($1, $2)",
        "Janette",
        24
    )

    await conn.close()

asyncio.run(main())
```

### Query data

```python
import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect(
        user="postgres",
        password="secret",
        database="test",
        host="localhost"
    )

    rows = await conn.fetch("SELECT id, name, age FROM users ORDER BY id")

    for row in rows:
        print(dict(row))

    await conn.close()

asyncio.run(main())
```

### When to use `asyncpg`

Use `asyncpg` when:
- your project is already async
- you want PostgreSQL-specific async performance
- you do not need DB-API compatibility
- you want a fully async-native API

---

## 6. SQL Server drivers

For SQL Server in Python, two important options are:

- **`pyodbc`**
- **`mssql-python`**

---

## 7. `pyodbc`

`pyodbc` is a DB-API 2.0 ODBC bridge.

It is commonly used for SQL Server, especially when:
- your environment already uses ODBC
- you want a mature and widely used option
- you are comfortable with ODBC drivers

### Install

```bash
pip install pyodbc
```

### Basic connection

```python
import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=testdb;"
    "UID=sa;"
    "PWD=YourPassword123;"
    "TrustServerCertificate=yes;"
)

cursor = conn.cursor()
cursor.execute("SELECT @@VERSION")
print(cursor.fetchone())

conn.close()
```

### Create a table

```python
import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=testdb;"
    "UID=sa;"
    "PWD=YourPassword123;"
    "TrustServerCertificate=yes;"
)

cursor = conn.cursor()

cursor.execute("""
IF OBJECT_ID('users', 'U') IS NULL
BEGIN
    CREATE TABLE users (
        id INT IDENTITY(1,1) PRIMARY KEY,
        name NVARCHAR(100) NOT NULL,
        age INT NOT NULL
    )
END
""")

conn.commit()
conn.close()
```

### Insert data

`pyodbc` commonly uses `?` placeholders.

```python
import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=testdb;"
    "UID=sa;"
    "PWD=YourPassword123;"
    "TrustServerCertificate=yes;"
)

cursor = conn.cursor()

cursor.execute(
    "INSERT INTO users (name, age) VALUES (?, ?)",
    ("Janette", 24)
)

conn.commit()
conn.close()
```

### Query data

```python
import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=testdb;"
    "UID=sa;"
    "PWD=YourPassword123;"
    "TrustServerCertificate=yes;"
)

cursor = conn.cursor()
cursor.execute("SELECT id, name, age FROM users ORDER BY id")

for row in cursor.fetchall():
    print(row)

conn.close()
```

### When to use `pyodbc`

Use `pyodbc` when:
- you already work with ODBC
- you need broad compatibility
- your environment already has ODBC drivers installed
- you want a mature DB-API option for SQL Server

---

## 8. `mssql-python`

`mssql-python` is Microsoft’s newer Python driver for SQL Server.

It is useful when:
- you want Microsoft’s newer dedicated driver
- you want DB-API-style code
- you want to follow Microsoft’s current Python SQL Server approach

### Install

```bash
pip install mssql-python
```

### Basic connection

```python
from mssql_python import connect

conn = connect(
    "Server=localhost;"
    "Database=testdb;"
    "User Id=sa;"
    "Password=YourPassword123;"
    "Encrypt=no;"
)

cursor = conn.cursor()
cursor.execute("SELECT @@VERSION")

for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
```

### Insert data

`mssql-python` also uses `?` placeholders.

```python
from mssql_python import connect

conn = connect(
    "Server=localhost;"
    "Database=testdb;"
    "User Id=sa;"
    "Password=YourPassword123;"
    "Encrypt=no;"
)

cursor = conn.cursor()

cursor.execute(
    "INSERT INTO users (name, age) VALUES (?, ?)",
    ("Janette", 24)
)

conn.commit()
cursor.close()
conn.close()
```

### Query data

```python
from mssql_python import connect

conn = connect(
    "Server=localhost;"
    "Database=testdb;"
    "User Id=sa;"
    "Password=YourPassword123;"
    "Encrypt=no;"
)

cursor = conn.cursor()
cursor.execute("SELECT id, name, age FROM users ORDER BY id")

for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
```

### When to use `mssql-python`

Use `mssql-python` when:
- you want Microsoft’s newer dedicated Python driver for SQL Server
- you want DB-API-style code
- you prefer Microsoft’s current documented path

---

## 9. Placeholder differences to remember

One of the easiest mistakes when switching drivers is parameter syntax.

### `sqlite3`

```python
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Janette", 24))
```

### `psycopg`

```python
cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", ("Janette", 24))
```

### `asyncpg`

```python
await conn.execute("INSERT INTO users (name, age) VALUES ($1, $2)", "Janette", 24)
```

### `pyodbc` / `mssql-python`

```python
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Janette", 24))
```

Do not build SQL by concatenating user input into the query string.

---

## 10. Transactions

The normal pattern is:

1. open connection
2. execute SQL
3. `commit()` if successful
4. `rollback()` if something fails
5. close cursor and connection

### Example

```python
import sqlite3

conn = sqlite3.connect("app.db")

try:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Ana", 30))
    conn.commit()
except Exception:
    conn.rollback()
    raise
finally:
    conn.close()
```

The same general idea applies to PostgreSQL and SQL Server drivers too.

---

## 11. Good practices

### Use parameterized queries

This helps avoid:
- SQL injection
- broken quoting
- formatting mistakes

### Close resources properly

Use:
- context managers when supported
- or explicit `close()`

### Pick the driver based on your database and app style

- local/simple: `sqlite3`
- PostgreSQL sync/default: `psycopg`
- PostgreSQL async-native: `asyncpg`
- SQL Server via ODBC: `pyodbc`
- SQL Server with Microsoft’s newer driver: `mssql-python`

### Remember SQL dialect differences

Even if the Python pattern looks similar, SQL syntax can differ between:
- SQLite
- PostgreSQL
- SQL Server

---

## 12. Quick comparison

### `sqlite3`
- built into Python
- no server needed
- best for local and small apps

### `psycopg`
- main PostgreSQL adapter
- DB-API style
- supports async too

### `asyncpg`
- PostgreSQL only
- async-native
- not DB-API compatible

### `pyodbc`
- DB-API ODBC bridge
- common for SQL Server
- often requires Microsoft ODBC Driver installation

### `mssql-python`
- newer Microsoft driver for SQL Server
- DB-API style
- dedicated to Microsoft SQL-family databases

---

## 13. Summary

- `sqlite3` is Python’s built-in interface for SQLite
- `sqlite3` is great for local, lightweight, serverless databases
- `psycopg` is the main modern PostgreSQL adapter
- `asyncpg` is a strong async-native PostgreSQL option
- `pyodbc` is a common SQL Server option through ODBC
- `mssql-python` is Microsoft’s newer Python driver for SQL Server
- the overall Python database workflow is usually:
  - connect
  - execute
  - fetch
  - commit or rollback
  - close
- one of the biggest differences between drivers is the parameter placeholder style

# Python: SQLAlchemy Core and ORM; Relationships and Queries

SQLAlchemy’s documentation presents **Core** as the SQL Expression Language and schema toolkit, and **ORM** as the higher-level object-relational mapper built on top of it. In SQLAlchemy 2.x, the ORM uses **2.0-style querying** based on `select()`, and the old `Query` API is considered legacy.

## 1. What is SQLAlchemy?

SQLAlchemy has two main layers:

- **Core**: build SQL statements and table metadata directly
- **ORM**: map Python classes to database tables and work with objects instead of raw rows

A simple rule:

- use **Core** when you want explicit SQL-style control
- use **ORM** when you want object-oriented data access

SQLAlchemy’s unified tutorial explains that Core and ORM are integrated, and in 2.0 style the ORM uses Core-style `select()` statements.

---

## 2. Installing SQLAlchemy

```bash
pip install SQLAlchemy
```

If you want PostgreSQL support too, you typically install SQLAlchemy plus a PostgreSQL driver such as `psycopg`. SQLAlchemy itself is the toolkit/ORM layer, while the actual DB connection is handled by a driver.

---

## 3. SQLAlchemy Core

### 3.1 Core idea

In **Core**, you define tables and build SQL expressions with Python objects.

You work with things like:
- `Engine`
- `Connection`
- `MetaData`
- `Table`
- `Column`
- `select()`
- `insert()`
- `update()`
- `delete()`

The SQLAlchemy docs describe the SQL Expression Language as a toolkit for constructing SQL expressions represented by composable Python objects.

### 3.2 Creating an engine

```python
from sqlalchemy import create_engine

engine = create_engine("sqlite:///app.db", echo=True)
```

`create_engine()` builds the database engine. The engine is the central source of connections and database interaction in Core.

### 3.3 Defining tables

```python
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    ForeignKey
)

engine = create_engine("sqlite:///app.db", echo=True)
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
)

addresses = Table(
    "addresses",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(255), nullable=False),
    Column("user_id", ForeignKey("users.id"), nullable=False),
)

metadata.create_all(engine)
```

`MetaData` stores table definitions, and `create_all()` creates them in the database. Foreign keys are what Core and ORM commonly use to determine joins automatically.

### 3.4 Insert with Core

```python
from sqlalchemy import insert

with engine.begin() as conn:
    conn.execute(insert(users), [
        {"name": "Janette"},
        {"name": "Ana"},
    ])
```

SQLAlchemy documents `insert(table)` as the Core constructor for building INSERT statements. `engine.begin()` is a convenient transaction block.

### 3.5 Select with Core

```python
from sqlalchemy import select

with engine.connect() as conn:
    stmt = select(users)
    result = conn.execute(stmt)

    for row in result:
        print(row)
```

`select()` is the standard way to build SELECT statements in Core. The unified tutorial and select documentation use `select()` as the main query-building primitive.

### 3.6 Filtering and joins in Core

```python
from sqlalchemy import select

stmt = (
    select(users.c.name, addresses.c.email)
    .join(addresses, users.c.id == addresses.c.user_id)
    .where(users.c.name == "Janette")
)
```

Core `select()` supports filtering with `where()` and joins with `join()`. SQLAlchemy can often infer the `ON` clause automatically when foreign keys are present.

### 3.7 Update and delete in Core

```python
from sqlalchemy import update, delete

with engine.begin() as conn:
    conn.execute(
        update(users)
        .where(users.c.name == "Ana")
        .values(name="Ana Maria")
    )

    conn.execute(
        delete(users)
        .where(users.c.name == "Janette")
    )
```

SQLAlchemy documents `update(table)` and `delete(table)` as the Core constructors for UPDATE and DELETE statements.

---

## 4. SQLAlchemy ORM

### 4.1 ORM idea

In the ORM, you map Python classes to database tables. Then you work with Python objects instead of manually handling row tuples all the time. SQLAlchemy’s ORM docs describe this layer as the higher-level system that automates persistence and querying of mapped classes.

### 4.2 Declarative mapping

In modern SQLAlchemy 2.x, a common pattern is to use `DeclarativeBase`, `Mapped`, and `mapped_column()`. The relationships docs also illustrate mappings using the `Mapped` annotation style.

```python
from __future__ import annotations

from sqlalchemy import String, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

engine = create_engine("sqlite:///app.db", echo=True)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    addresses: Mapped[list["Address"]] = relationship(back_populates="user")


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="addresses")


Base.metadata.create_all(engine)
```

---

## 5. Session

The **Session** is the main ORM unit for persistence and ORM querying. SQLAlchemy’s session docs say transaction control for ORM use happens through `Session`, and querying commonly uses `select()` executed via methods like `Session.execute()` and `Session.scalars()`.

### Basic session usage

```python
from sqlalchemy.orm import Session

with Session(engine) as session:
    user = User(name="Janette")
    session.add(user)
    session.commit()
```

### Add multiple objects

```python
from sqlalchemy.orm import Session

with Session(engine) as session:
    session.add_all([
        User(name="Janette"),
        User(name="Ana"),
    ])
    session.commit()
```

---

## 6. Basic ORM queries

### 6.1 Select objects

SQLAlchemy 2.x recommends ORM queries built with `select()`. The session docs show `Session.scalars(select(User))` as a common way to get ORM objects.

```python
from sqlalchemy import select
from sqlalchemy.orm import Session

with Session(engine) as session:
    statement = select(User)
    users_list = session.scalars(statement).all()

    for user in users_list:
        print(user.id, user.name)
```

### 6.2 Filter objects

```python
from sqlalchemy import select
from sqlalchemy.orm import Session

with Session(engine) as session:
    statement = select(User).where(User.name == "Janette")
    user = session.scalars(statement).first()

    print(user)
```

### 6.3 Select specific columns

```python
from sqlalchemy import select
from sqlalchemy.orm import Session

with Session(engine) as session:
    statement = select(User.id, User.name)
    rows = session.execute(statement).all()

    for row in rows:
        print(row)
```

The ORM querying guide states that `select()` can accept mapped classes and class-level mapped attributes.

---

## 7. Relationships

The SQLAlchemy relationships docs describe `relationship()` as the ORM tool for connecting mapped classes, and the basic relationship patterns docs walk through one-to-many, many-to-one, one-to-one, and many-to-many patterns.

### 7.1 One-to-many / many-to-one

This is the `User` ↔ `Address` example shown earlier:

- one user can have many addresses
- each address belongs to one user

```python
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    addresses: Mapped[list["Address"]] = relationship(back_populates="user")


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="addresses")
```

`relationship()` usually figures out how to join classes by inspecting the foreign key relationship between the tables.

### 7.2 Create related objects

```python
from sqlalchemy.orm import Session

with Session(engine) as session:
    user = User(
        name="Janette",
        addresses=[
            Address(email="janette@example.com"),
            Address(email="jc@example.com"),
        ],
    )

    session.add(user)
    session.commit()
```

This is a major ORM benefit: related objects can be persisted through Python object graphs instead of writing every insert manually.

### 7.3 Access related objects

```python
from sqlalchemy import select
from sqlalchemy.orm import Session

with Session(engine) as session:
    user = session.scalars(
        select(User).where(User.name == "Janette")
    ).first()

    for address in user.addresses:
        print(address.email)
```

---

## 8. Querying across relationships

### 8.1 Join related tables

```python
from sqlalchemy import select
from sqlalchemy.orm import Session

with Session(engine) as session:
    statement = (
        select(User, Address)
        .join(User.addresses)
        .where(User.name == "Janette")
    )

    rows = session.execute(statement).all()

    for user, address in rows:
        print(user.name, address.email)
```

The ORM querying guide is built around 2.0-style `select()` usage, including joins between mapped entities.

### 8.2 Filter by related rows

```python
from sqlalchemy import select
from sqlalchemy.orm import Session

with Session(engine) as session:
    statement = (
        select(User)
        .join(User.addresses)
        .where(Address.email.like("%@example.com"))
    )

    users_list = session.scalars(statement).all()

    for user in users_list:
        print(user.name)
```

---

## 9. Loading strategies for relationships

When working with relationships, you need to think about **how related rows are loaded**. SQLAlchemy supports multiple loading strategies, and relationship configuration/loading is a major ORM topic in the docs.

### Example with `selectinload`

```python
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

with Session(engine) as session:
    statement = select(User).options(selectinload(User.addresses))
    users_list = session.scalars(statement).all()

    for user in users_list:
        print(user.name, [a.email for a in user.addresses])
```

This pattern is commonly used to avoid N+1-style query problems when loading collections.

---

## 10. Many-to-many relationships

SQLAlchemy’s relationship docs also cover many-to-many via an association table.

### Example

```python
from __future__ import annotations

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

user_groups = Table(
    "user_groups",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    groups: Mapped[list["Group"]] = relationship(
        secondary=user_groups,
        back_populates="users"
    )


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    users: Mapped[list["User"]] = relationship(
        secondary=user_groups,
        back_populates="groups"
    )
```

### Insert and query many-to-many

```python
from sqlalchemy.orm import Session
from sqlalchemy import select

with Session(engine) as session:
    admin = Group(name="admin")
    editor = Group(name="editor")

    user = User(name="Janette", groups=[admin, editor])

    session.add(user)
    session.commit()

with Session(engine) as session:
    statement = select(User).where(User.name == "Janette")
    user = session.scalars(statement).first()

    for group in user.groups:
        print(group.name)
```

---

## 11. Updating and deleting in the ORM

### 11.1 Update via objects

A common ORM pattern is:
1. load an object
2. change attributes
3. commit

```python
from sqlalchemy import select
from sqlalchemy.orm import Session

with Session(engine) as session:
    user = session.scalars(
        select(User).where(User.name == "Ana")
    ).first()

    user.name = "Ana Maria"
    session.commit()
```

### 11.2 Delete via objects

```python
from sqlalchemy import select
from sqlalchemy.orm import Session

with Session(engine) as session:
    user = session.scalars(
        select(User).where(User.name == "Ana Maria")
    ).first()

    session.delete(user)
    session.commit()
```

SQLAlchemy also documents ORM-enabled bulk INSERT/UPDATE/DELETE statements built on the same Core DML constructs, but object-based persistence is the most common conceptual starting point.

---

## 12. Core vs ORM: when to use each

### Use Core when:
- you want very explicit SQL control
- you work heavily with SQL expressions
- you need lightweight data access without mapped classes
- you are writing generic SQL tooling

### Use ORM when:
- your data model maps naturally to Python classes
- you want relationships as objects
- you want unit-of-work behavior through `Session`
- you want more object-oriented app code

SQLAlchemy’s docs present Core and ORM as integrated layers, not mutually exclusive choices. Many real apps use both.

---

## 13. Common beginner mistakes

### 13.1 Using old `Query` style everywhere

In SQLAlchemy 2.x, the old `Query` API is legacy. Prefer `select()` with `Session.execute()` or `Session.scalars()`.

### 13.2 Forgetting relationships need foreign keys

`relationship()` usually relies on foreign keys to determine joins automatically. If relationships are ambiguous or unusual, you may need custom join configuration.

### 13.3 Loading related objects inefficiently

If you access related collections one by one without planning loading strategy, you can create too many SQL queries. SQLAlchemy’s relationship loading tools exist to address that.

### 13.4 Mixing Core and ORM concepts without understanding transaction flow

When using the ORM, transaction control is centered on `Session`. When using Core directly, you work through `Engine` and `Connection`.

---

## 14. Summary

- **SQLAlchemy Core** is the lower-level SQL Expression Language and schema toolkit.
- **SQLAlchemy ORM** maps Python classes to tables and is built on top of Core.
- In **SQLAlchemy 2.x**, ORM querying is based on `select()`, and `Query` is legacy.
- **Core** commonly uses:
  - `create_engine()`
  - `MetaData`
  - `Table`
  - `Column`
  - `select()`
  - `insert()`
  - `update()`
  - `delete()`
- **ORM** commonly uses:
  - `DeclarativeBase`
  - `Mapped`
  - `mapped_column()`
  - `relationship()`
  - `Session`
  - `select()` + `Session.scalars()` / `Session.execute()`
- Relationships commonly include:
  - one-to-many
  - many-to-one
  - many-to-many
- SQLAlchemy often infers joins from foreign keys, but more advanced relationship join configuration is also supported.


# Python: Migrations with Alembic

## 1. What Is Alembic?

**Alembic** is a lightweight database migration tool commonly used with SQLAlchemy.

It helps you:
- track schema changes over time
- generate migration scripts
- apply upgrades
- roll back changes when needed
- keep database structure synchronized across environments

Alembic is especially useful when your project evolves and the database schema changes frequently.

---

## 2. Why Migrations Matter

Without migrations, database changes become difficult to manage.

For example:
- one developer adds a column
- another renames a table
- production still uses the old schema
- testing and staging drift away from development

Migrations solve this by making schema changes:
- explicit
- versioned
- repeatable
- reviewable

---

## 3. Installing Alembic

```bash
pip install alembic
```

Alembic is usually installed alongside SQLAlchemy.

---

## 4. Initializing an Alembic Environment

To start using Alembic in a project:

```bash
alembic init alembic
```

This creates a migration environment, usually including:
- an `alembic/` directory
- a `versions/` directory inside it
- an `alembic.ini` file
- an `env.py` file

These files control how Alembic discovers and applies migrations.

---

## 5. Important Files

### `alembic.ini`
This is the main configuration file.

It commonly contains:
- script location
- database URL
- logging configuration

### `alembic/env.py`
This is one of the most important files.

It defines how Alembic connects to the database and where it should find your SQLAlchemy metadata.

### `alembic/versions/`
This folder stores revision files.

Each migration usually lives in its own Python file.

---

## 6. Configuring the Database URL

In `alembic.ini`, you will often see something like:

```ini
sqlalchemy.url = sqlite:///app.db
```

You can replace it with your actual database URL.

Examples:

### SQLite
```ini
sqlalchemy.url = sqlite:///app.db
```

### PostgreSQL
```ini
sqlalchemy.url = postgresql+psycopg://user:password@localhost/dbname
```

### SQL Server
```ini
sqlalchemy.url = mssql+pyodbc://user:password@server/dbname?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes
```

In real projects, many teams avoid hardcoding credentials here and instead load the URL dynamically in `env.py`.

---

## 7. Connecting Alembic to SQLAlchemy Models

For autogeneration to work, Alembic needs access to your SQLAlchemy metadata.

Inside `env.py`, you typically set:

```python
target_metadata = Base.metadata
```

A common pattern is:

```python
from myapp.models import Base
target_metadata = Base.metadata
```

If this is missing or wrong, Alembic cannot compare your models against the current database schema for autogeneration.

---

## 8. Creating a Revision

To create a new migration revision manually:

```bash
alembic revision -m "create users table"
```

This creates a new revision file inside `alembic/versions/`.

A migration file usually contains:

- revision identifiers
- an `upgrade()` function
- a `downgrade()` function

Example structure:

```python
def upgrade():
    pass

def downgrade():
    pass
```

You then fill those functions with schema operations.

---

## 9. Autogenerating Migrations

A very common Alembic workflow is autogeneration.

```bash
alembic revision --autogenerate -m "add users table"
```

This tells Alembic to compare:
- your SQLAlchemy metadata
- the current database schema

Then it generates migration operations based on the differences.

### Important
Autogenerate is helpful, but it is not magic.

You should always review generated migrations before applying them.

---

## 10. What Autogenerate Usually Detects

Autogenerate is commonly useful for detecting things like:
- new tables
- removed tables
- added columns
- removed columns
- some type changes
- some constraint and index changes

### Important
Not every schema change is detected perfectly.

You should still inspect the generated migration manually.

---

## 11. Running Migrations

To upgrade to the latest revision:

```bash
alembic upgrade head
```

This applies all pending migrations up to the current head revision.

### Other examples

Upgrade to a specific revision:
```bash
alembic upgrade <revision_id>
```

Upgrade one step forward:
```bash
alembic upgrade +1
```

---

## 12. Downgrading Migrations

To roll back one migration:

```bash
alembic downgrade -1
```

To roll back to a specific revision:

```bash
alembic downgrade <revision_id>
```

To downgrade all the way back to the base state:

```bash
alembic downgrade base
```

Downgrades are important when:
- a migration was wrong
- deployment needs rollback
- testing requires moving backward and forward

---

## 13. Viewing Migration History

Alembic provides commands to inspect revision history.

### Show history
```bash
alembic history
```

### Show current revision in the database
```bash
alembic current
```

### Show heads
```bash
alembic heads
```

These commands help you understand:
- where the database is now
- what revisions exist
- whether multiple heads exist

---

## 14. Migration File Structure

A migration file typically looks like this:

```python
from alembic import op
import sqlalchemy as sa

revision = "123456789abc"
down_revision = "abcdef123456"
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
    )

def downgrade():
    op.drop_table("users")
```

### Key parts
- `revision` → current migration ID
- `down_revision` → previous migration ID
- `upgrade()` → apply the change
- `downgrade()` → reverse the change

---

## 15. Common `op` Operations

Alembic migration files often use the `op` object from `alembic.op`.

Examples:

### Create table
```python
op.create_table(...)
```

### Drop table
```python
op.drop_table("users")
```

### Add column
```python
op.add_column("users", sa.Column("email", sa.String(length=255)))
```

### Drop column
```python
op.drop_column("users", "email")
```

### Alter column
```python
op.alter_column("users", "name", nullable=False)
```

### Create index
```python
op.create_index("ix_users_email", "users", ["email"])
```

### Drop index
```python
op.drop_index("ix_users_email", table_name="users")
```

These operations are part of Alembic’s migration API.

---

## 16. Example: Add a Column

Suppose you already have a `users` table and want to add an `email` column.

Autogenerated or manual migration might look like:

```python
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column("users", sa.Column("email", sa.String(length=255), nullable=True))

def downgrade():
    op.drop_column("users", "email")
```

This is a very typical Alembic change.

---

## 17. Example: Rename-like Changes

Alembic can handle many structural operations, but some changes need extra care.

For example, renaming a column may not always be safely inferred as a rename during autogeneration.

Sometimes Alembic may see it as:
- drop old column
- add new column

That is why reviewing migrations manually is important.

---

## 18. Offline Mode

Alembic supports an **offline mode** for generating SQL scripts instead of directly executing migrations against a live database.

This is useful when:
- DBAs need to review SQL first
- deployment uses SQL scripts
- direct database access is not allowed in the migration step

Example conceptually:

```bash
alembic upgrade head --sql
```

This generates SQL output rather than applying changes immediately.

---

## 19. Using `pyproject.toml`

Alembic also supports using `pyproject.toml` for configuration in addition to the classic `.ini` setup.

This can fit better in modern Python projects that centralize tool configuration in `pyproject.toml`.

---

## 20. Branches and Multiple Heads

Sometimes two migration branches are created in parallel.

For example:
- developer A creates migration A
- developer B creates migration B
- both are based on the same earlier revision

Now Alembic may report multiple heads.

You can inspect this with:

```bash
alembic heads
```

To merge them:

```bash
alembic merge -m "merge heads" <head1> <head2>
```

This creates a merge revision that resolves the branch structure.

---

## 21. Batch Migrations for SQLite

SQLite has some schema alteration limitations compared to databases like PostgreSQL.

Because of that, Alembic documents **batch mode** for certain schema changes, especially with SQLite.

Example pattern:

```python
with op.batch_alter_table("users") as batch_op:
    batch_op.add_column(sa.Column("email", sa.String(length=255)))
```

Batch mode is especially relevant for SQLite migrations involving operations that SQLite does not support directly in simple `ALTER TABLE` form.

---

## 22. Naming Constraints Matters

Constraint naming is important in Alembic migrations.

Examples:
- primary keys
- foreign keys
- unique constraints
- check constraints
- indexes

If constraints are unnamed or inconsistently named, migrations and autogeneration can become harder to manage.

A good practice is to use a naming convention in SQLAlchemy metadata.

---

## 23. Alembic with SQLAlchemy Models

A common real-world workflow looks like this:

1. update SQLAlchemy models
2. run:
   ```bash
   alembic revision --autogenerate -m "describe change"
   ```
3. review the generated migration
4. apply it:
   ```bash
   alembic upgrade head
   ```

This is one of the most common Alembic usage patterns.

---

## 24. Data Migrations vs Schema Migrations

Alembic is mainly used for **schema migrations**:
- create table
- drop column
- alter constraint
- add index

It can also perform **data migrations**, but this should be done carefully.

Examples:
- backfilling a new column
- transforming existing values
- copying data between structures

Small data migrations may be fine inside Alembic revisions, but large or risky data moves often need a separate strategy.

---

## 25. Common Beginner Mistakes

### Mistake 1: Not setting `target_metadata`
If `env.py` does not point to the correct SQLAlchemy metadata, autogenerate will not work correctly.

### Mistake 2: Trusting autogenerate blindly
Autogenerate is helpful, but it must still be reviewed manually.

### Mistake 3: Writing no `downgrade()`
A downgrade path is often important, especially in staging and production rollback scenarios.

### Mistake 4: Forgetting to commit model changes before generating migrations
If the Python models are not updated first, Alembic cannot generate the intended schema changes.

### Mistake 5: Ignoring multiple heads
Branch conflicts in migration history should be resolved intentionally with merge revisions when appropriate.

### Mistake 6: Doing SQLite schema changes without understanding batch mode
SQLite needs special handling for some table alteration workflows.

---

## 26. Practical Recommendations

A good practical workflow is:

- define SQLAlchemy models clearly
- set `target_metadata` correctly in `env.py`
- use `--autogenerate` when appropriate
- always review generated migrations
- keep revision messages descriptive
- test both upgrade and downgrade paths
- handle branch conflicts early
- be extra careful with SQLite-specific migration behavior

---

## 27. Useful Alembic Commands

### Initialize environment
```bash
alembic init alembic
```

### Create revision
```bash
alembic revision -m "message"
```

### Autogenerate revision
```bash
alembic revision --autogenerate -m "message"
```

### Upgrade to latest
```bash
alembic upgrade head
```

### Downgrade one revision
```bash
alembic downgrade -1
```

### Show current revision
```bash
alembic current
```

### Show history
```bash
alembic history
```

### Show heads
```bash
alembic heads
```

### Merge branches
```bash
alembic merge -m "merge heads" <head1> <head2>
```

### Generate SQL offline
```bash
alembic upgrade head --sql
```

---

## 28. Summary

- **Alembic** is a migration tool commonly used with SQLAlchemy
- it helps manage schema evolution through versioned migration scripts
- `alembic init` creates the migration environment
- `env.py` is critical because it connects Alembic to your metadata
- `revision` creates migration files
- `revision --autogenerate` compares models and schema
- `upgrade` applies migrations
- `downgrade` rolls them back
- `history`, `current`, and `heads` help inspect migration state
- SQLite may require **batch mode** for some schema changes
- always review autogenerated migrations before applying them


# Python: Introduction to MongoDB (Motor)

## 1. What Is MongoDB?

**MongoDB** is a NoSQL document database.

Instead of storing data in tables and rows like a relational database, MongoDB stores data in **collections** and **documents**.

### Main ideas
- **database** → contains collections
- **collection** → similar to a table
- **document** → similar to a row, but stored as a flexible JSON-like structure

### Example document
```json
{
  "name": "Janette",
  "age": 24,
  "skills": ["Python", "SQL", "React"]
}
```

MongoDB stores documents in a BSON format, which is similar to JSON but supports more data types.

---

## 2. What Is Motor?

**Motor** is the official asynchronous Python driver for MongoDB.

It is designed for:
- `asyncio`
- async web frameworks
- high-concurrency applications
- non-blocking database access

A common use case is using Motor with frameworks such as:
- FastAPI
- aiohttp
- Tornado

---

## 3. Important Current Note About Motor

Motor has been **deprecated** in favor of the **PyMongo Async API**.

That means:
- new development should strongly consider using PyMongo Async
- Motor is still usable for existing projects
- support is limited during the deprecation period

### Practical meaning
If you are learning Motor for an existing codebase, it is still useful.

If you are starting a brand-new async MongoDB project, you should also evaluate the **PyMongo Async API**.

---

## 4. Installing Motor

```bash
pip install motor
```

Motor depends on PyMongo internally.

---

## 5. Basic Import

```python
import motor.motor_asyncio
```

A very common entry point is:

```python
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
```

---

## 6. Connecting to MongoDB

### Example
```python
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
```

### MongoDB Atlas example
```python
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://<user>:<password>@<cluster-url>/")
```

You usually create one client and reuse it.

---

## 7. Getting a Database and Collection

With MongoDB, you usually do:

```python
db = client.my_database
collection = db.users
```

### Full example
```python
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")

db = client.my_database
collection = db.users
```

This means:
- `my_database` is the database
- `users` is the collection

---

## 8. Why Motor Is Async

Motor is built for asynchronous Python programs.

That means many operations are used with `await`.

### Example
```python
import asyncio
import motor.motor_asyncio

async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.my_database
    collection = db.users

    document = await collection.find_one({"name": "Janette"})
    print(document)

asyncio.run(main())
```

### Important
If you forget `await`, the operation will not behave as expected.

---

## 9. Inserting One Document

Use `insert_one()`.

```python
import asyncio
import motor.motor_asyncio

async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    collection = client.my_database.users

    result = await collection.insert_one({
        "name": "Janette",
        "age": 24,
        "skills": ["Python", "SQL", "React"]
    })

    print("Inserted ID:", result.inserted_id)

asyncio.run(main())
```

### Result
`insert_one()` returns an object with details such as:
- `inserted_id`

---

## 10. Inserting Many Documents

Use `insert_many()`.

```python
import asyncio
import motor.motor_asyncio

async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    collection = client.my_database.users

    result = await collection.insert_many([
        {"name": "Ana", "age": 30},
        {"name": "Luis", "age": 28},
        {"name": "Mia", "age": 22}
    ])

    print("Inserted IDs:", result.inserted_ids)

asyncio.run(main())
```

---

## 11. Finding One Document

Use `find_one()`.

```python
import asyncio
import motor.motor_asyncio

async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    collection = client.my_database.users

    document = await collection.find_one({"name": "Janette"})
    print(document)

asyncio.run(main())
```

If a document matches, MongoDB returns it as a dictionary-like object.

If nothing matches, it returns `None`.

---

## 12. Finding Multiple Documents

Use `find()`.

### Important
`find()` does not directly return a list.
It returns a cursor.

```python
import asyncio
import motor.motor_asyncio

async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    collection = client.my_database.users

    cursor = collection.find({"age": {"$gte": 25}})

    async for document in cursor:
        print(document)

asyncio.run(main())
```

---

## 13. Converting Cursor Results to a List

Motor supports turning a cursor into a list.

```python
import asyncio
import motor.motor_asyncio

async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    collection = client.my_database.users

    cursor = collection.find({})
    documents = await cursor.to_list(length=100)

    print(documents)

asyncio.run(main())
```

### Important
Use `to_list()` carefully with large result sets, because it loads matching documents into memory.

---

## 14. Query Operators

MongoDB queries use operators such as:

- `$eq` → equals
- `$gt` → greater than
- `$gte` → greater than or equal
- `$lt` → less than
- `$lte` → less than or equal
- `$in` → value is in a list
- `$ne` → not equal

### Example
```python
{"age": {"$gte": 18}}
```

This means:
- age greater than or equal to 18

### Example with Motor
```python
import asyncio
import motor.motor_asyncio

async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    collection = client.my_database.users

    async for document in collection.find({"age": {"$gte": 25}}):
        print(document)

asyncio.run(main())
```

---

## 15. Projections

A projection chooses which fields to return.

### Example
```python
document = await collection.find_one(
    {"name": "Janette"},
    {"_id": 0, "name": 1, "age": 1}
)
```

This means:
- include `name`
- include `age`
- exclude `_id`

### Full example
```python
import asyncio
import motor.motor_asyncio

async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    collection = client.my_database.users

    document = await collection.find_one(
        {"name": "Janette"},
        {"_id": 0, "name": 1, "age": 1}
    )

    print(document)

asyncio.run(main())
```

---

## 16. Updating One Document

Use `update_one()`.

```python
import asyncio
import motor.motor_asyncio

async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    collection = client.my_database.users

    result = await collection.update_one(
        {"name": "Janette"},
        {"$set": {"age": 25}}
    )

    print("Matched:", result.matched_count)
    print("Modified:", result.modified_count)

asyncio.run(main())
```

### Important
MongoDB updates usually use operators such as:
- `$set`
- `$inc`
- `$unset`
- `$push`

---

## 17. Updating Many Documents

Use `update_many()`.

```python
import asyncio
import motor.motor_asyncio

async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    collection = client.my_database.users

    result = await collection.update_many(
        {"age": {"$lt": 18}},
        {"$set": {"minor": True}}
    )

    print("Matched:", result.matched_count)
    print("Modified:", result.modified_count)

asyncio.run(main())
```

---

## 18. Replacing a Document

Use `replace_one()` when you want to replace the whole document body.

```python
import asyncio
import motor.motor_asyncio

async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    collection = client.my_database.users

    result = await collection.replace_one(
        {"name": "Janette"},
        {"name": "Janette", "age": 26, "city": "Mexico City"}
    )

    print("Matched:", result.matched_count)
    print("Modified:", result.modified_count)

asyncio.run(main())
```

### Important
`replace_one()` replaces the full document except for `_id`.

---

## 19. Deleting One Document

Use `delete_one()`.

```python
import asyncio
import motor.motor_asyncio

async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    collection = client.my_database.users

    result = await collection.delete_one({"name": "Janette"})
    print("Deleted:", result.deleted_count)

asyncio.run(main())
```

---

## 20. Deleting Many Documents

Use `delete_many()`.

```python
import asyncio
import motor.motor_asyncio

async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    collection = client.my_database.users

    result = await collection.delete_many({"minor": True})
    print("Deleted:", result.deleted_count)

asyncio.run(main())
```

---

## 21. Sorting Results

Use `sort()` on a cursor.

```python
import asyncio
import motor.motor_asyncio

async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    collection = client.my_database.users

    cursor = collection.find({}).sort("age", 1)

    async for document in cursor:
        print(document)

asyncio.run(main())
```

### Sort directions
- `1` → ascending
- `-1` → descending

---

## 22. Limiting Results

Use `limit()`.

```python
import asyncio
import motor.motor_asyncio

async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    collection = client.my_database.users

    cursor = collection.find({}).limit(5)

    async for document in cursor:
        print(document)

asyncio.run(main())
```

---

## 23. Counting Documents

Use `count_documents()`.

```python
import asyncio
import motor.motor_asyncio

async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    collection = client.my_database.users

    count = await collection.count_documents({"age": {"$gte": 18}})
    print(count)

asyncio.run(main())
```

---

## 24. MongoDB `_id`

Every MongoDB document has an `_id` field.

If you do not provide one, MongoDB creates it automatically.

Example returned document:
```python
{
    "_id": ObjectId("..."),
    "name": "Janette",
    "age": 24
}
```

This `_id` is commonly an `ObjectId`.

---

## 25. Querying by `_id`

To query by `_id`, you often need `ObjectId`.

```python
from bson import ObjectId
import asyncio
import motor.motor_asyncio

async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    collection = client.my_database.users

    document = await collection.find_one({"_id": ObjectId("64f123456789abcdef123456")})
    print(document)

asyncio.run(main())
```

---

## 26. Creating an Index

Indexes improve query performance.

Example:
```python
import asyncio
import motor.motor_asyncio

async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    collection = client.my_database.users

    index_name = await collection.create_index("email")
    print(index_name)

asyncio.run(main())
```

Indexes are especially important for:
- frequent queries
- sorting
- unique lookups

---

## 27. Unique Index Example

```python
import asyncio
import motor.motor_asyncio

async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    collection = client.my_database.users

    index_name = await collection.create_index("email", unique=True)
    print(index_name)

asyncio.run(main())
```

This prevents duplicate values in the indexed field.

---

## 28. Using Motor with FastAPI

Motor is commonly used with async frameworks such as FastAPI.

A common pattern is:
- create one shared client
- reuse it across requests
- close it when the app shuts down if needed

### Simple example idea
```python
import motor.motor_asyncio
from fastapi import FastAPI

app = FastAPI()

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client.my_database

@app.get("/users")
async def get_users():
    users = await db.users.find({}).to_list(length=100)
    return users
```

---

## 29. Good Practices

### Reuse one client
Create the client once and reuse it.

Bad:
```python
# creating a new client inside every request
```

Better:
```python
client = motor.motor_asyncio.AsyncIOMotorClient(...)
```

### Use indexes
Without indexes, queries can become slow as data grows.

### Be careful with `to_list()`
It can load many documents into memory.

### Validate data at the application level
MongoDB is flexible, but your app still needs consistent data rules.

### Think about schema design
Even in a flexible document database, structure matters.

---

## 30. Common Beginner Mistakes

### Mistake 1: Forgetting `await`
Wrong:
```python
document = collection.find_one({"name": "Janette"})
```

Correct:
```python
document = await collection.find_one({"name": "Janette"})
```

### Mistake 2: Thinking `find()` returns a list
`find()` returns a cursor, not a list.

### Mistake 3: Creating a new client for every operation
This is inefficient.

### Mistake 4: Using `to_list()` for huge datasets
This can use too much memory.

### Mistake 5: Ignoring the Motor deprecation note
For new projects, you should also evaluate PyMongo Async.

---

## 31. Motor vs PyMongo Async

### Motor
- async MongoDB driver
- widely used in existing async Python projects
- now deprecated

### PyMongo Async
- newer async API in PyMongo
- recommended migration direction
- better choice to evaluate for new projects

### Practical advice
- existing Motor project → learning Motor still makes sense
- brand-new project → strongly consider PyMongo Async

---

## 32. Summary

- **MongoDB** stores data as documents in collections
- **Motor** is the async MongoDB driver for Python
- it works well with `asyncio` and async web frameworks
- common objects are:
  - `AsyncIOMotorClient`
  - database
  - collection
- common operations include:
  - `insert_one()`
  - `insert_many()`
  - `find_one()`
  - `find()`
  - `update_one()`
  - `update_many()`
  - `replace_one()`
  - `delete_one()`
  - `delete_many()`
- `find()` returns a cursor
- indexes are important for performance
- Motor is deprecated, so new projects should also evaluate the **PyMongo Async API**
