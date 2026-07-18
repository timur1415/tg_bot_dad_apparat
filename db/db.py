import os
import logging

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker


logger = logging.getLogger(__name__)

DB_PATH = os.getenv("DB_PATH", "requests.db")
_raw_database_url = (os.getenv("DATABASE_URL", "") or "").strip()

# Current project uses sync SQLAlchemy sessions. Async DB URLs (e.g. asyncpg)
# will fail with MissingGreenlet in sync context, so we fallback to sqlite.
if _raw_database_url.startswith("postgresql+asyncpg://"):
    logger.warning(
        "DATABASE_URL uses asyncpg, but sync engine is configured. Falling back to sqlite DB_PATH=%s",
        DB_PATH,
    )
    DATABASE_URL = f"sqlite:///{DB_PATH}"
else:
    DATABASE_URL = _raw_database_url or f"sqlite:///{DB_PATH}"


class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    import db.models as models  # noqa: F401 - Import ensures model metadata is registered.

    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    if "requests" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("requests")}
    with engine.begin() as connection:
        if "status" not in columns:
            connection.execute(
                text("ALTER TABLE requests ADD COLUMN status VARCHAR NOT NULL DEFAULT 'new'")
            )
        if "photo_file_id" not in columns:
            connection.execute(
                text("ALTER TABLE requests ADD COLUMN photo_file_id VARCHAR")
            )
