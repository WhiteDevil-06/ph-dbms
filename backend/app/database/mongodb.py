"""MongoDB Connection and Collection Management via PyMongo."""

import logging
from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError

from backend.app.core.config import settings

logger = logging.getLogger(__name__)

_mongo_client: Optional[MongoClient] = None


def get_mongo_client() -> MongoClient:
    """Lazily initialize and return the global PyMongo client instance."""
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = MongoClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=2000,
            connectTimeoutMS=2000,
        )
    return _mongo_client


def get_mongo_db() -> Database:
    """Return the post_harvest_telemetry MongoDB database."""
    client = get_mongo_client()
    return client[settings.MONGODB_DATABASE]


def get_detections_collection() -> Collection:
    """Return the detections collection in MongoDB."""
    return get_mongo_db()["detections"]


def get_telemetry_collection() -> Collection:
    """Return the telemetry_logs collection in MongoDB."""
    return get_mongo_db()["telemetry_logs"]


def check_mongodb_connection() -> bool:
    """Verify active MongoDB handshake ping without exposing credentials."""
    try:
        client = get_mongo_client()
        client.admin.command("ping")
        return True
    except (ServerSelectionTimeoutError, PyMongoError, Exception) as exc:
        logger.warning("MongoDB connection check failed: %s", type(exc).__name__)
        return False


def close_mongo_connection() -> None:
    """Close MongoDB client connection on shutdown."""
    global _mongo_client
    if _mongo_client is not None:
        _mongo_client.close()
        _mongo_client = None
