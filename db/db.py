import os
import logging

from sqlalchemy import create_engine
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
