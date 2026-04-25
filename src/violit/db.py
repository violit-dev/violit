"""
violit/db.py
============
Violit ORM Integration - SQLModel + Alembic based.

Usage:
    from sqlmodel import SQLModel, Field, Relationship
    from typing import Optional

    class Task(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        title: str
        done: bool = False

    app = vl.App(title="My App", db="./app.db")
    # migrate default = "auto"

    task = Task(title="To Do")
    app.db.add(task)
    tasks = app.db.all(Task)
"""

from __future__ import annotations

import logging
import sys
from typing import Any, List, Optional, Type, TypeVar, Union

logger = logging.getLogger("violit.db")

# SQLModel / SQLAlchemy lazy import (prevents errors if not installed)
try:
    from sqlmodel import SQLModel, Session, select
    from sqlalchemy import create_engine, inspect, text, func
    from sqlalchemy.engine import Engine
    _SQLMODEL_AVAILABLE = True
except ImportError:
    _SQLMODEL_AVAILABLE = False

T = TypeVar("T")

# ─────────────────────────────────────────────────────────────────────────────
# Migrate mode constants
# ─────────────────────────────────────────────────────────────────────────────
MIGRATE_AUTO   = "auto"    # Default: auto create tables + add missing columns (warns on delete/modify)
MIGRATE_FORCE  = "force"   # Fully automatic including column drop/modify
MIGRATE_FILES  = "files"   # Alembic file-based migration
MIGRATE_OFF    = False     # Fully disabled


def _check_sqlmodel():
    if not _SQLMODEL_AVAILABLE:
        raise ImportError(
            "[violit] sqlmodel package is required to use db features.\n"
            "  pip install sqlmodel aiosqlite"
        )


class ViolItDB:
    """
    Violit DB helper class. Accessed via app.db.

    Parameters
    ----------
    db_url : str
        SQLAlchemy DB URL.
        - SQLite  : 'sqlite:///./app.db' (or './app.db' -> auto conversion)
        - PostgreSQL: 'postgresql+psycopg2://user:pass@host/db'
    migrate : str | bool
        - "auto"  (default) : auto create tables + add missing columns
        - "force" : auto + auto apply column drops and type changes
        - "files" : Alembic file-based migration (make_migration / apply / rollback)
        - False   : no migration (manage DB directly)
    """

    def __init__(self, db_url: str, migrate: Union[str, bool] = MIGRATE_AUTO):
        _check_sqlmodel()

        self._url = db_url
        self._migrate_mode = migrate
        self._is_sqlite = db_url.startswith("sqlite")

        self._engine: Engine = create_engine(
            db_url,
            echo=False,
            # SQLite: allow multithreading (violit handlers run in a thread pool)
            connect_args={"check_same_thread": False} if self._is_sqlite else {},
        )

    # ─────────────────────────────────────────────────────────────────────
    # Internal: execute startup migration (called from App.run())
    # ─────────────────────────────────────────────────────────────────────

    def _run_startup_migration(self) -> None:
        """Called right before App.run(). Behavior depends on migrate mode."""
        if self._migrate_mode is False:
            return

        # Common: create all defined tables if they do not exist yet
        SQLModel.metadata.create_all(self._engine)

        if self._migrate_mode in (MIGRATE_AUTO, MIGRATE_FORCE):
            self._smart_sync(force=(self._migrate_mode == MIGRATE_FORCE))

        # "files" mode: operates only via CLI args or manual call, no auto run here

    def _smart_sync(self, force: bool = False) -> None:
        """
        Synchronize current DB schema ↔ SQLModel definitions.

        force=False (auto):
            - Auto apply column additions only
            - Warn and skip column drops / type changes
        force=True (force):
            - Auto apply column additions + drops
            - Warn and skip type changes due to SQLite limitations (requires Alembic batch)
        """
        try:
            inspector = inspect(self._engine)
        except Exception as e:
            logger.warning(f"[violit:db] Schema inspection failed: {e}")
            return

        existing_tables = set(inspector.get_table_names())

        for table_name, table in SQLModel.metadata.tables.items():
            # New table -> already created by create_all, so skip
            if table_name not in existing_tables:
                logger.info(f"[violit:db] ✅ New table created: {table_name}")
                continue

            existing_cols: dict[str, dict] = {
                col["name"]: col
                for col in inspector.get_columns(table_name)
            }
            model_col_names = {col.name for col in table.columns}

            try:
                with self._engine.begin() as conn:
                    # ── Add missing columns ──────────────────────────────────
                    for col in table.columns:
                        if col.name not in existing_cols:
                            col_type_str = col.type.compile(
                                dialect=self._engine.dialect
                            )
                            default_clause = self._build_default_clause(col)
                            sql = (
                                f'ALTER TABLE "{table_name}" '
                                f'ADD COLUMN "{col.name}" {col_type_str}{default_clause}'
                            )
                            conn.execute(text(sql))
                            logger.info(
                                f"[violit:db] ✅ {table_name}: "
                                f"Added column -> {col.name} ({col_type_str})"
                            )

                    # ── Drop extra columns (force mode only) ───────────────────
                    if force:
                        for col_name in list(existing_cols.keys()):
                            if col_name not in model_col_names:
                                if self._is_sqlite:
                                    # SQLite 3.35.0+ supports DROP COLUMN
                                    import sqlite3
                                    if sqlite3.sqlite_version_info >= (3, 35, 0):
                                        sql = (
                                            f'ALTER TABLE "{table_name}" '
                                            f'DROP COLUMN "{col_name}"'
                                        )
                                        conn.execute(text(sql))
                                        logger.warning(
                                            f"[violit:db] 🗑️  {table_name}: "
                                            f"Dropped column -> {col_name}"
                                        )
                                    else:
                                        logger.warning(
                                            f"[violit:db] ⚠️  {table_name}: "
                                            f"Failed to drop '{col_name}' column "
                                            f"(SQLite {sqlite3.sqlite_version} does not "
                                            f"support DROP COLUMN, requires 3.35.0+)"
                                        )
                                else:
                                    sql = (
                                        f'ALTER TABLE "{table_name}" '
                                        f'DROP COLUMN "{col_name}"'
                                    )
                                    conn.execute(text(sql))
                                    logger.warning(
                                        f"[violit:db] 🗑️  {table_name}: "
                                        f"Dropped column -> {col_name}"
                                    )
                    else:
                        # auto mode: warn on extra columns only
                        for col_name in existing_cols:
                            if col_name not in model_col_names:
                                logger.warning(
                                    f"[violit:db] ⚠️  {table_name}: "
                                    f"Found column '{col_name}' not in model "
                                    f"(use migrate='force' to delete)"
                                )

            except Exception as e:
                logger.error(
                    f"[violit:db] ❌ {table_name} migration error: {e}"
                )

    @staticmethod
    def _build_default_clause(col) -> str:
        """Generate DEFAULT clause SQL string for a column."""
        if col.default is not None:
            val = col.default.arg
            if callable(val):
                return ""  # functional defaults (like now()) cannot be inserted into SQL directly
            if isinstance(val, str):
                escaped = val.replace("'", "''")
                return f" DEFAULT '{escaped}'"
            if val is not None:
                return f" DEFAULT {val}"
        if col.nullable is not False:
            return " DEFAULT NULL"
        return ""

    # ─────────────────────────────────────────────────────────────────────
    # Public CRUD API
    # ─────────────────────────────────────────────────────────────────────

    def session(self) -> Session:
        """
        Return a raw SQLModel session. Used for complex queries.

        Example::

            from sqlmodel import select
            with app.db.session() as s:
                results = s.exec(
                    select(Task).where(Task.done == False).limit(10)
                ).all()
        """
        _check_sqlmodel()
        return Session(self._engine)

    def add(self, obj: T) -> T:
        """
        Add (INSERT) object to DB, commit, and refresh.

        Example::

            task = Task(title="New task")
            task = app.db.add(task)   # Returns task with populated id
        """
        _check_sqlmodel()
        with Session(self._engine) as session:
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def save(self, obj: T) -> T:
        """
        Update (UPDATE) existing object, commit, and refresh.
        Internally identical to add(), but conceptually distinct.

        Example::

            task.done = True
            app.db.save(task)
        """
        return self.add(obj)

    def get(self, model: Type[T], pk: Any) -> Optional[T]:
        """
        Fetch a single record by Primary Key. Returns None if not found.

        Example::

            task = app.db.get(Task, 1)
        """
        _check_sqlmodel()
        with Session(self._engine) as session:
            return session.get(model, pk)

    def first(self, model: Type[T], *conditions) -> Optional[T]:
        """
        Return the first matching record. Returns None if not found.

        Example::

            user = app.db.first(User, User.email == "a@b.com")
        """
        _check_sqlmodel()
        with Session(self._engine) as session:
            stmt = select(model)
            for cond in conditions:
                stmt = stmt.where(cond)
            return session.exec(stmt).first()

    def all(self, model: Type[T]) -> List[T]:
        """
        Return all records.

        Example::

            tasks = app.db.all(Task)
        """
        _check_sqlmodel()
        with Session(self._engine) as session:
            return list(session.exec(select(model)).all())

    def filter(
        self,
        model: Type[T],
        *conditions,
        order_by=None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[T]:
        """
        Fetch multiple records based on conditions.

        Example::

            tasks = app.db.filter(
                Task,
                Task.done == False,
                order_by=Task.id.desc(),
                limit=20,
            )
        """
        _check_sqlmodel()
        with Session(self._engine) as session:
            stmt = select(model)
            for cond in conditions:
                stmt = stmt.where(cond)
            if order_by is not None:
                stmt = stmt.order_by(order_by)
            if offset:
                stmt = stmt.offset(offset)
            if limit:
                stmt = stmt.limit(limit)
            return list(session.exec(stmt).all())

    def delete(self, obj: T) -> None:
        """
        Delete object from DB.

        Example::

            app.db.delete(task)
        """
        _check_sqlmodel()
        with Session(self._engine) as session:
            # use merge to safely delete objects fetched from other sessions
            managed = session.merge(obj)
            session.delete(managed)
            session.commit()

    def delete_by(self, model: Type[T], *conditions) -> int:
        """
        Bulk delete records matching conditions. Returns the number of deleted rows.

        Example::

            count = app.db.delete_by(Task, Task.done == True)
        """
        _check_sqlmodel()
        rows = self.filter(model, *conditions)
        with Session(self._engine) as session:
            for row in rows:
                managed = session.merge(row)
                session.delete(managed)
            session.commit()
        return len(rows)

    def count(self, model: Type[T], *conditions) -> int:
        """
        Return record count.

        Example::

            total = app.db.count(Task)
            done_count = app.db.count(Task, Task.done == True)
        """
        _check_sqlmodel()
        with Session(self._engine) as session:
            stmt = select(func.count()).select_from(model)
            for cond in conditions:
                stmt = stmt.where(cond)
            return session.exec(stmt).one()

    def exists(self, model: Type[T], *conditions) -> bool:
        """
        Check if any record matching conditions exists.

        Example::

            if app.db.exists(User, User.email == "a@b.com"):
                app.toast("Email already registered.", "danger")
        """
        return self.count(model, *conditions) > 0

    # ─────────────────────────────────────────────────────────────────────
    # File-based migration (migrate="files" mode)
    # ─────────────────────────────────────────────────────────────────────

    def make_migration(self, message: str = "auto") -> None:
        """
        Auto-generate Alembic migration file for current model changes.
        Used in migrate="files" mode.

        Example::

            app.db.make_migration("add priority column")
            # -> migrations/versions/YYYYMMDD_HHMMSS_add_priority_column.py
        """
        self._ensure_alembic_initialized()
        try:
            from alembic.config import Config
            from alembic import command
        except ImportError:
            raise ImportError(
                "[violit] alembic package is required for file-based migrations.\n"
                "  pip install alembic"
            )

        cfg = Config("alembic.ini")
        cfg.attributes["target_metadata"] = SQLModel.metadata
        command.revision(cfg, message=message, autogenerate=True)
        print(f"[violit:db] ✅ Migration file generated in migrations/versions/")

    def apply(self) -> None:
        """
        Apply all pending migration files in order (alembic upgrade head).

        Example::

            app.db.apply()
        """
        self._ensure_alembic_initialized()
        try:
            from alembic.config import Config
            from alembic import command
        except ImportError:
            raise ImportError("[violit] alembic package is required: pip install alembic")

        cfg = Config("alembic.ini")
        command.upgrade(cfg, "head")
        print("[violit:db] ✅ Migration apply completed (head)")

    def rollback(self, steps: int = 1) -> None:
        """
        Rollback N migration steps (alembic downgrade -N).

        Example::

            app.db.rollback()         # 1 step
            app.db.rollback(steps=3)  # 3 steps
        """
        self._ensure_alembic_initialized()
        try:
            from alembic.config import Config
            from alembic import command
        except ImportError:
            raise ImportError("[violit] alembic package is required: pip install alembic")

        cfg = Config("alembic.ini")
        command.downgrade(cfg, f"-{steps}")
        print(f"[violit:db] ✅ Rolled back {steps} steps")

    def migration_status(self) -> None:
        """Print current applied migration version."""
        self._ensure_alembic_initialized()
        try:
            from alembic.config import Config
            from alembic import command
        except ImportError:
            raise ImportError("[violit] alembic package is required: pip install alembic")

        cfg = Config("alembic.ini")
        command.current(cfg, verbose=True)

    # ─────────────────────────────────────────────────────────────────────
    # Alembic initialization helper
    # ─────────────────────────────────────────────────────────────────────

    def _ensure_alembic_initialized(self) -> None:
        """Auto generate alembic.ini + migrations/ folder if not present."""
        from pathlib import Path

        if not Path("alembic.ini").exists():
            _write_alembic_ini(self._url)
            print("[violit:db] alembic.ini created")

        if not Path("migrations").exists():
            try:
                from alembic.config import Config
                from alembic import command
            except ImportError:
                raise ImportError(
                    "[violit] alembic package is required: pip install alembic"
                )
            cfg = Config("alembic.ini")
            command.init(cfg, "migrations")
            _write_env_py()  # Override with violit custom env.py
            print("[violit:db] migrations/ folder initialized")


# ─────────────────────────────────────────────────────────────────────────────
# Alembic config file templates
# ─────────────────────────────────────────────────────────────────────────────

def _write_alembic_ini(db_url: str) -> None:
    """Generate violit default alembic.ini."""
    content = f"""[alembic]
script_location = migrations
sqlalchemy.url = {db_url}

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
"""
    with open("alembic.ini", "w", encoding="utf-8") as f:
        f.write(content)


def _write_env_py() -> None:
    """
    Replace Alembic default env.py with violit custom version.
    - Uses SQLModel.metadata automatically
    - SQLite: render_as_batch=True (to bypass ALTER TABLE constraints)
    - Supports external injection via config.attributes["target_metadata"]
    """
    from pathlib import Path

    env_content = '''"""
migrations/env.py
Violit auto-generated - SQLModel + SQLite batch mode support
"""
from logging.config import fileConfig
from alembic import context
from sqlmodel import SQLModel

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Get metadata from config.attributes or fallback to SQLModel.metadata
target_metadata = config.attributes.get("target_metadata", SQLModel.metadata)

_db_url = config.get_main_option("sqlalchemy.url", "")
_is_sqlite = "sqlite" in _db_url


def run_migrations_offline() -> None:
    context.configure(
        url=_db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=_is_sqlite,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    from sqlalchemy import engine_from_config, pool

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=_is_sqlite,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
'''
    env_path = Path("migrations") / "env.py"
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(env_content)


# ─────────────────────────────────────────────────────────────────────────────
# URL normalization utility
# ─────────────────────────────────────────────────────────────────────────────

def normalize_db_url(db: str) -> str:
    """
    Normalize user-provided db string into a SQLAlchemy URL format.

    Examples
    --------
    "./app.db"            -> "sqlite:///./app.db"
    "app.db"              -> "sqlite:///app.db"
    "/data/app.db"        -> "sqlite:////data/app.db"
    "sqlite:///./app.db"  -> "sqlite:///./app.db"  (unchanged)
    "postgresql://..."    -> "postgresql://..."     (unchanged)
    """
    if "://" in db:
        return db
    # If only path is provided -> convert to sqlite URL
    import os
    if os.path.isabs(db):
        # Absolute path: sqlite:////absolute/path.db
        return f"sqlite:///{db}"
    else:
        # Relative path: sqlite:///./relative/path.db
        if not db.startswith("./") and not db.startswith(".\\\\"):
            db = f"./{db}"
        return f"sqlite:///{db}"
