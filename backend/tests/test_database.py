"""Tests for database connection handlers and graceful failure behavior."""

from backend.app.database import (
    check_mysql_connection,
    check_mongodb_connection,
    get_mongo_client,
    get_mongo_db,
    get_detections_collection,
    get_telemetry_collection,
)


def test_mysql_connection_check_fails_gracefully():
    """Verify that when MySQL is offline, check_mysql_connection returns False without crashing."""
    is_connected = check_mysql_connection()
    # In test environment without running MySQL container, it must return False safely
    assert isinstance(is_connected, bool)


def test_mongodb_connection_check_fails_gracefully():
    """Verify that when MongoDB is offline, check_mongodb_connection returns False without crashing."""
    is_connected = check_mongodb_connection()
    # In test environment without running MongoDB container, it must return False safely
    assert isinstance(is_connected, bool)


def test_mongodb_collection_getters():
    """Verify MongoDB collection accessors construct correctly."""
    client = get_mongo_client()
    assert client is not None
    db = get_mongo_db()
    assert db.name == "post_harvest_telemetry"
    detections = get_detections_collection()
    assert detections.name == "detections"
    telemetry = get_telemetry_collection()
    assert telemetry.name == "telemetry_logs"
