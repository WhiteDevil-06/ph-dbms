"""Database modules and connection dependencies."""

from backend.app.database.base import Base
from backend.app.database.mysql import engine, SessionLocal, get_db, check_mysql_connection
from backend.app.database.mongodb import (
    get_mongo_client,
    get_mongo_db,
    get_detections_collection,
    get_telemetry_collection,
    check_mongodb_connection,
    close_mongo_connection,
)

__all__ = [
    "Base",
    "engine",
    "SessionLocal",
    "get_db",
    "check_mysql_connection",
    "get_mongo_client",
    "get_mongo_db",
    "get_detections_collection",
    "get_telemetry_collection",
    "check_mongodb_connection",
    "close_mongo_connection",
]
