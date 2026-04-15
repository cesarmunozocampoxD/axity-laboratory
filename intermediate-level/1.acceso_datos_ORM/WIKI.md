# Python Databases and Migrations — Clear Summary

## 1. Goal

This document gives a clear summary of these practical Python data-access topics:

- `sqlite3` and drivers for PostgreSQL / SQL Server
- SQLAlchemy Core and ORM, including relationships and queries
- migrations with Alembic
- an introduction to MongoDB with Motor

The purpose is to connect relational access, ORM usage, migrations, and introductory async MongoDB access into one practical mental model.

---

## 2. `sqlite3` and Drivers for PostgreSQL / SQL Server

### `sqlite3`
`sqlite3` is Python’s built-in database interface for SQLite.

It is useful because:
- it ships with Python
- it requires no separate database server
- it is excellent for local apps, prototypes, tests, and lightweight persistence

A good fit for `sqlite3` is:
- small tools
- local persistence
- demos and prototypes
- simple apps
- tests

### PostgreSQL drivers
For PostgreSQL, a very common modern choice is **Psycopg 3**.

It is useful because:
- it is a serious PostgreSQL adapter for Python
- it supports modern PostgreSQL and Python features
- it supports both sync and async usage patterns

A good fit for Psycopg is:
- production PostgreSQL applications
- SQLAlchemy backends
- direct PostgreSQL access
- async PostgreSQL workflows

### SQL Server drivers
For SQL Server, common Python access is built around SQLAlchemy dialects and supported DBAPI drivers such as:
- `pyodbc`
- `mssql-python`

A practical way to think about SQL Server access is:
- the **driver** handles low-level DB connectivity
- SQLAlchemy can sit on top to provide Core or ORM abstractions

### Practical shortcut
A useful summary is:

- **`sqlite3`** → built-in SQLite access for lightweight or local use
- **Psycopg** → strong PostgreSQL driver choice
- **SQL Server drivers** → usually driver + SQLAlchemy dialect combination

### Main idea
Start by choosing:
- the database engine
- the driver/DBAPI
- then decide whether you want raw SQL access or a higher-level abstraction like SQLAlchemy

---

## 3. SQLAlchemy Core and ORM; Relationships and Queries

### SQLAlchemy Core
SQLAlchemy Core is the lower-level SQL expression and schema layer.

It is useful when:
- you want explicit SQL-oriented control
- you want schema-centric access
- you prefer query construction closer to SQL thinking
- you do not necessarily want full ORM objects

A good fit for Core is:
- explicit SQL building
- reporting queries
- lower-level data-access layers
- systems where ORM automation is unnecessary

### SQLAlchemy ORM
SQLAlchemy ORM builds on top of Core and maps Python objects to database tables.

It is useful when:
- you want domain-oriented object persistence
- you want mapped classes
- you want relationships between models
- you want unit-of-work style persistence behavior

A good fit for ORM is:
- business applications
- CRUD-heavy apps
- apps where object relationships matter
- applications using repository or domain-style patterns

### Relationships
In ORM usage, relationships express links between mapped objects, such as:
- one-to-many
- many-to-one
- many-to-many

Examples of relationship ideas:
- a user has many posts
- an order has many items
- a post belongs to one author

### Queries
With SQLAlchemy, queries can be built in:
- Core style
- ORM style

The exact syntax differs, but the main idea is:
- Core is more SQL-expression-centric
- ORM is more object/mapping-centric

### Practical shortcut
A useful summary is:

- **Core** → explicit SQL-building layer
- **ORM** → object mapping and persistence layer

### Main idea
SQLAlchemy gives you both a lower-level SQL toolkit and a higher-level ORM model, and the right choice depends on how object-oriented or SQL-oriented your data-access layer should be.

---

## 4. Migrations with Alembic

### What Alembic is
Alembic is a migration tool designed to work with SQLAlchemy.

It is used to manage schema evolution over time.

### Why migrations matter
Database schemas change:
- new columns appear
- tables are renamed
- indexes are added
- constraints change

Without migrations, schema changes become:
- manual
- inconsistent
- risky
- harder to reproduce across environments

### What Alembic does
Alembic helps you:
- create migration scripts
- version schema changes
- apply upgrades
- apply downgrades
- keep environments aligned

### Why this is useful
It makes schema change management:
- explicit
- reviewable
- repeatable
- automatable in CI/CD and deployments

### Autogeneration
A very important Alembic feature is migration autogeneration.

This is useful when SQLAlchemy metadata changes and you want Alembic to propose migration code automatically.

### Practical note
Autogeneration is helpful, but migrations should still be reviewed carefully before applying them.

### Main idea
Alembic is the standard migration layer for SQLAlchemy-based relational projects.

---

## 5. Introduction to MongoDB with Motor

### What MongoDB is
MongoDB is a document-oriented database.

Instead of tables and rows, it works with:
- collections
- documents

This makes it a very different model from relational systems such as PostgreSQL or SQL Server.

### What Motor is
Motor is the async MongoDB driver for Python applications.

It is useful because:
- it supports asynchronous MongoDB access
- it fits naturally into `asyncio` applications
- it is commonly used in async Python services

### Good fit for Motor
Use Motor when:
- the app is async
- MongoDB is the chosen database
- non-blocking I/O matters
- document-database access is part of the architecture

### Important modeling idea
With MongoDB, the mental model is not:
- SQL joins
- tables
- row mapping

Instead, it is more like:
- documents
- nested data
- collection operations
- query filters over document fields

### Practical note
Motor is about async MongoDB access, not ORM-style relational mapping.

### Main idea
Motor is a good intro path when you want async Python access to MongoDB’s document model.

---

## 6. How These Topics Connect

These topics are different parts of one data-access picture:

- **drivers** connect Python to the database
- **SQLAlchemy Core/ORM** add relational abstractions on top of drivers
- **Alembic** manages relational schema changes over time
- **Motor** introduces async access to MongoDB’s document model

A practical workflow is often:

1. choose the database type
2. choose the driver
3. choose the abstraction level
4. manage schema evolution if relational
5. keep the access layer aligned with the application style (sync or async)

---

## 7. Practical Selection Guide

### Choose `sqlite3` when:
- you need lightweight built-in relational storage
- the app is small or local
- the environment is simple

### Choose PostgreSQL + Psycopg when:
- you want a strong relational database
- PostgreSQL is the target platform
- production-grade relational features matter

### Choose SQL Server drivers when:
- SQL Server is your platform
- enterprise or Microsoft ecosystem integration matters
- SQLAlchemy dialect support will be used on top

### Choose SQLAlchemy Core when:
- you want explicit SQL-oriented control

### Choose SQLAlchemy ORM when:
- you want object mapping and relationship handling

### Choose Alembic when:
- your relational schema must evolve safely over time

### Choose Motor when:
- the app is async
- MongoDB is the selected datastore
- document-oriented access is the right model

---

## 8. Final Takeaway

If you only keep the essentials:

1. `sqlite3` is the built-in lightweight relational option.
2. Psycopg is a strong PostgreSQL driver choice.
3. SQL Server access usually combines a driver with SQLAlchemy dialect support.
4. SQLAlchemy Core is SQL-oriented; SQLAlchemy ORM is object-oriented.
5. Alembic manages schema migrations for SQLAlchemy-based relational projects.
6. Motor is the async path for MongoDB access in Python.

---
