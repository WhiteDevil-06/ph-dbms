"""MySQL Database Connection and Session Management via SQLAlchemy."""

import logging
from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from backend.app.core.config import settings

logger = logging.getLogger(__name__)

# Create SQLAlchemy engine with connection pool configuration
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency yielding a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_mysql_connection() -> bool:
    """Verify active MySQL connection handshake without exposing credentials."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except (SQLAlchemyError, Exception) as exc:
        logger.warning("MySQL connection check failed: %s", type(exc).__name__)
        return False
