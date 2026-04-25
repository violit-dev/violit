"""
violit/db.py
============
Violit ORM Integration - SQLModel + Alembic 기반.

사용법:
    from sqlmodel import SQLModel, Field, Relationship
    from typing import Optional

    class Task(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        title: str
        done: bool = False

    app = vl.App(title="My App", db="./app.db")
    # migrate 기본값 = "auto"

    task = Task(title="할 일")
    app.db.add(task)
    tasks = app.db.all(Task)
"""

from __future__ import annotations

import logging
import sys
from typing import Any, List, Optional, Type, TypeVar, Union

logger = logging.getLogger("violit.db")

# SQLModel / SQLAlchemy는 lazy import (미설치 시 오류 방지)
try:
    from sqlmodel import SQLModel, Session, select
    from sqlalchemy import create_engine, inspect, text, func
    from sqlalchemy.engine import Engine
    _SQLMODEL_AVAILABLE = True
except ImportError:
    _SQLMODEL_AVAILABLE = False

T = TypeVar("T")

# ─────────────────────────────────────────────────────────────────────────────
# migrate 모드 상수
# ─────────────────────────────────────────────────────────────────────────────
MIGRATE_AUTO   = "auto"    # 기본값: 테이블 생성 + 컬럼 추가 자동 (삭제/변경은 경고)
MIGRATE_FORCE  = "force"   # 컬럼 삭제·변경 포함 전부 자동
MIGRATE_FILES  = "files"   # Alembic 파일 기반 마이그레이션
MIGRATE_OFF    = False     # 완전 비활성화


def _check_sqlmodel():
    if not _SQLMODEL_AVAILABLE:
        raise ImportError(
            "[violit] db 기능을 사용하려면 sqlmodel 패키지가 필요합니다.\n"
            "  pip install sqlmodel aiosqlite"
        )


class ViolItDB:
    """
    Violit DB 헬퍼 클래스. app.db 로 접근.

    Parameters
    ----------
    db_url : str
        SQLAlchemy DB URL.
        - SQLite  : 'sqlite:///./app.db'  (또는 './app.db' → 자동 변환)
        - PostgreSQL: 'postgresql+psycopg2://user:pass@host/db'
    migrate : str | bool
        - "auto"  (기본) : 테이블 자동 생성 + 누락 컬럼 자동 추가
        - "force" : auto + 컬럼 삭제·타입 변경 자동 적용
        - "files" : Alembic 마이그레이션 파일 기반 (make_migration / apply / rollback)
        - False   : 마이그레이션 없음 (DB 직접 관리)
    """

    def __init__(self, db_url: str, migrate: Union[str, bool] = MIGRATE_AUTO):
        _check_sqlmodel()

        self._url = db_url
        self._migrate_mode = migrate
        self._is_sqlite = db_url.startswith("sqlite")

        self._engine: Engine = create_engine(
            db_url,
            echo=False,
            # SQLite: 멀티스레드 허용 (violit 핸들러는 스레드풀에서 동작)
            connect_args={"check_same_thread": False} if self._is_sqlite else {},
        )

    # ─────────────────────────────────────────────────────────────────────
    # 내부: 시작 시 마이그레이션 실행 (App.run()에서 호출)
    # ─────────────────────────────────────────────────────────────────────

    def _run_startup_migration(self) -> None:
        """App.run() 직전에 호출. migrate 모드에 따라 동작."""
        if self._migrate_mode is False:
            return

        # 공통: 정의된 모든 테이블을 아직 없으면 생성
        SQLModel.metadata.create_all(self._engine)

        if self._migrate_mode in (MIGRATE_AUTO, MIGRATE_FORCE):
            self._smart_sync(force=(self._migrate_mode == MIGRATE_FORCE))

        # "files" 모드: CLI 인자 또는 수동 호출로만 동작, 여기서 자동 실행 안 함

    def _smart_sync(self, force: bool = False) -> None:
        """
        현재 DB 스키마 ↔ SQLModel 모델 정의를 비교해서 동기화.

        force=False (auto):
            - 컬럼 추가만 자동 적용
            - 컬럼 삭제·타입 변경은 경고 출력 후 건너뜀
        force=True (force):
            - 컬럼 추가 + 삭제 자동 적용
            - 타입 변경은 SQLite 제약으로 인해 경고 후 건너뜀 (Alembic 배치 필요)
        """
        try:
            inspector = inspect(self._engine)
        except Exception as e:
            logger.warning(f"[violit:db] 스키마 검사 실패: {e}")
            return

        existing_tables = set(inspector.get_table_names())

        for table_name, table in SQLModel.metadata.tables.items():
            # 새 테이블 → create_all 이 이미 생성했으므로 건너뜀
            if table_name not in existing_tables:
                logger.info(f"[violit:db] ✅ 신규 테이블 생성: {table_name}")
                continue

            existing_cols: dict[str, dict] = {
                col["name"]: col
                for col in inspector.get_columns(table_name)
            }
            model_col_names = {col.name for col in table.columns}

            try:
                with self._engine.begin() as conn:
                    # ── 누락 컬럼 추가 ──────────────────────────────────
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
                                f"컬럼 추가 → {col.name} ({col_type_str})"
                            )

                    # ── 여분 컬럼 삭제 (force 모드만) ───────────────────
                    if force:
                        for col_name in list(existing_cols.keys()):
                            if col_name not in model_col_names:
                                if self._is_sqlite:
                                    # SQLite 3.35.0+ 에서 DROP COLUMN 지원
                                    import sqlite3
                                    if sqlite3.sqlite_version_info >= (3, 35, 0):
                                        sql = (
                                            f'ALTER TABLE "{table_name}" '
                                            f'DROP COLUMN "{col_name}"'
                                        )
                                        conn.execute(text(sql))
                                        logger.warning(
                                            f"[violit:db] 🗑️  {table_name}: "
                                            f"컬럼 삭제 → {col_name}"
                                        )
                                    else:
                                        logger.warning(
                                            f"[violit:db] ⚠️  {table_name}: "
                                            f"'{col_name}' 컬럼 삭제 실패 "
                                            f"(SQLite {sqlite3.sqlite_version} 에서는 "
                                            f"DROP COLUMN 미지원, 3.35.0+ 필요)"
                                        )
                                else:
                                    sql = (
                                        f'ALTER TABLE "{table_name}" '
                                        f'DROP COLUMN "{col_name}"'
                                    )
                                    conn.execute(text(sql))
                                    logger.warning(
                                        f"[violit:db] 🗑️  {table_name}: "
                                        f"컬럼 삭제 → {col_name}"
                                    )
                    else:
                        # auto 모드: 여분 컬럼은 경고만
                        for col_name in existing_cols:
                            if col_name not in model_col_names:
                                logger.warning(
                                    f"[violit:db] ⚠️  {table_name}: "
                                    f"모델에 없는 컬럼 '{col_name}' 발견 "
                                    f"(삭제하려면 migrate='force' 사용)"
                                )

            except Exception as e:
                logger.error(
                    f"[violit:db] ❌ {table_name} 마이그레이션 오류: {e}"
                )

    @staticmethod
    def _build_default_clause(col) -> str:
        """컬럼의 DEFAULT 절 SQL 문자열 생성."""
        if col.default is not None:
            val = col.default.arg
            if callable(val):
                return ""  # 함수형 default (now() 등)는 SQL에 삽입 불가
            if isinstance(val, str):
                escaped = val.replace("'", "''")
                return f" DEFAULT '{escaped}'"
            if val is not None:
                return f" DEFAULT {val}"
        if col.nullable is not False:
            return " DEFAULT NULL"
        return ""

    # ─────────────────────────────────────────────────────────────────────
    # 공개 CRUD API
    # ─────────────────────────────────────────────────────────────────────

    def session(self) -> Session:
        """
        raw SQLModel 세션 반환. 복잡한 쿼리에 사용.

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
        객체를 DB에 추가(INSERT)하고 commit 후 refresh.

        Example::

            task = Task(title="새 할일")
            task = app.db.add(task)   # id가 채워진 task 반환
        """
        _check_sqlmodel()
        with Session(self._engine) as session:
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def save(self, obj: T) -> T:
        """
        기존 객체를 UPDATE하고 commit 후 refresh.
        내부적으로 add()와 동일하지만 의미적으로 구분.

        Example::

            task.done = True
            app.db.save(task)
        """
        return self.add(obj)

    def get(self, model: Type[T], pk: Any) -> Optional[T]:
        """
        Primary Key로 단건 조회. 없으면 None.

        Example::

            task = app.db.get(Task, 1)
        """
        _check_sqlmodel()
        with Session(self._engine) as session:
            return session.get(model, pk)

    def first(self, model: Type[T], *conditions) -> Optional[T]:
        """
        조건에 맞는 첫 번째 레코드 반환. 없으면 None.

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
        모든 레코드 반환.

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
        조건 기반 다건 조회.

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
        객체를 DB에서 삭제.

        Example::

            app.db.delete(task)
        """
        _check_sqlmodel()
        with Session(self._engine) as session:
            # 다른 세션에서 가져온 객체도 안전하게 삭제하기 위해 merge 사용
            managed = session.merge(obj)
            session.delete(managed)
            session.commit()

    def delete_by(self, model: Type[T], *conditions) -> int:
        """
        조건에 맞는 레코드 일괄 삭제. 삭제된 행 수 반환.

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
        레코드 수 반환.

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
        조건에 맞는 레코드가 존재하는지 확인.

        Example::

            if app.db.exists(User, User.email == "a@b.com"):
                app.toast("이미 가입된 이메일입니다.", "danger")
        """
        return self.count(model, *conditions) > 0

    # ─────────────────────────────────────────────────────────────────────
    # 파일 기반 마이그레이션 (migrate="files" 모드)
    # ─────────────────────────────────────────────────────────────────────

    def make_migration(self, message: str = "auto") -> None:
        """
        현재 모델 변경사항으로 Alembic 마이그레이션 파일 자동 생성.
        migrate="files" 모드에서 사용.

        Example::

            app.db.make_migration("priority 컬럼 추가")
            # → migrations/versions/YYYYMMDD_HHMMSS_priority_컬럼_추가.py
        """
        self._ensure_alembic_initialized()
        try:
            from alembic.config import Config
            from alembic import command
        except ImportError:
            raise ImportError(
                "[violit] 파일 기반 마이그레이션에는 alembic 패키지가 필요합니다.\n"
                "  pip install alembic"
            )

        cfg = Config("alembic.ini")
        cfg.attributes["target_metadata"] = SQLModel.metadata
        command.revision(cfg, message=message, autogenerate=True)
        print(f"[violit:db] ✅ migrations/versions/ 에 마이그레이션 파일 생성됨")

    def apply(self) -> None:
        """
        미적용 마이그레이션 파일을 순서대로 전부 적용 (alembic upgrade head).

        Example::

            app.db.apply()
        """
        self._ensure_alembic_initialized()
        try:
            from alembic.config import Config
            from alembic import command
        except ImportError:
            raise ImportError("[violit] alembic 패키지가 필요합니다: pip install alembic")

        cfg = Config("alembic.ini")
        command.upgrade(cfg, "head")
        print("[violit:db] ✅ 마이그레이션 적용 완료 (head)")

    def rollback(self, steps: int = 1) -> None:
        """
        마이그레이션을 N단계 되돌리기 (alembic downgrade -N).

        Example::

            app.db.rollback()       # 1단계
            app.db.rollback(steps=3)  # 3단계
        """
        self._ensure_alembic_initialized()
        try:
            from alembic.config import Config
            from alembic import command
        except ImportError:
            raise ImportError("[violit] alembic 패키지가 필요합니다: pip install alembic")

        cfg = Config("alembic.ini")
        command.downgrade(cfg, f"-{steps}")
        print(f"[violit:db] ✅ {steps}단계 롤백 완료")

    def migration_status(self) -> None:
        """현재 적용된 마이그레이션 버전 출력."""
        self._ensure_alembic_initialized()
        try:
            from alembic.config import Config
            from alembic import command
        except ImportError:
            raise ImportError("[violit] alembic 패키지가 필요합니다: pip install alembic")

        cfg = Config("alembic.ini")
        command.current(cfg, verbose=True)

    # ─────────────────────────────────────────────────────────────────────
    # Alembic 초기화 헬퍼
    # ─────────────────────────────────────────────────────────────────────

    def _ensure_alembic_initialized(self) -> None:
        """alembic.ini + migrations/ 폴더가 없으면 자동 생성."""
        from pathlib import Path

        if not Path("alembic.ini").exists():
            _write_alembic_ini(self._url)
            print("[violit:db] alembic.ini 생성됨")

        if not Path("migrations").exists():
            try:
                from alembic.config import Config
                from alembic import command
            except ImportError:
                raise ImportError(
                    "[violit] alembic 패키지가 필요합니다: pip install alembic"
                )
            cfg = Config("alembic.ini")
            command.init(cfg, "migrations")
            _write_env_py()  # violit 커스텀 env.py로 덮어쓰기
            print("[violit:db] migrations/ 폴더 초기화됨")


# ─────────────────────────────────────────────────────────────────────────────
# Alembic 설정 파일 템플릿
# ─────────────────────────────────────────────────────────────────────────────

def _write_alembic_ini(db_url: str) -> None:
    """violit 기본 alembic.ini 생성."""
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
    Alembic 기본 env.py를 violit 커스텀 버전으로 교체.
    - SQLModel.metadata 자동 사용
    - SQLite: render_as_batch=True (ALTER TABLE 제약 우회)
    - config.attributes["target_metadata"] 로 외부 주입 지원
    """
    from pathlib import Path

    env_content = '''"""
migrations/env.py
Violit 자동 생성 - SQLModel + SQLite batch 모드 지원
"""
from logging.config import fileConfig
from alembic import context
from sqlmodel import SQLModel

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# config.attributes 에서 metadata를 받거나 SQLModel.metadata 사용
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
# URL 정규화 유틸
# ─────────────────────────────────────────────────────────────────────────────

def normalize_db_url(db: str) -> str:
    """
    사용자가 전달한 db 문자열을 SQLAlchemy URL 형식으로 정규화.

    Examples
    --------
    "./app.db"            → "sqlite:///./app.db"
    "app.db"              → "sqlite:///app.db"
    "/data/app.db"        → "sqlite:////data/app.db"
    "sqlite:///./app.db"  → "sqlite:///./app.db"  (그대로)
    "postgresql://..."    → "postgresql://..."     (그대로)
    """
    if "://" in db:
        return db
    # 경로만 주어진 경우 → sqlite URL로 변환
    import os
    if os.path.isabs(db):
        # 절대경로: sqlite:////absolute/path.db
        return f"sqlite:///{db}"
    else:
        # 상대경로: sqlite:///./relative/path.db
        if not db.startswith("./") and not db.startswith(".\\"):
            db = f"./{db}"
        return f"sqlite:///{db}"
