"""Tests for FastAPI endpoints (healthcheck and JWT-protected simulation routes)."""

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest

from backend.app.core.config import settings
from backend.app.core.security import login_rate_limiter
from backend.app.database.base import Base
from backend.app.database.mysql import get_db
from backend.app.main import app
from backend.app.services.auth_service import ensure_auth_tables_and_seed_users


@pytest.fixture()
def api_client():
    """Provide a TestClient backed by an isolated in-memory SQLite DB with seeded auth users."""
    login_rate_limiter.reset_all()
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=test_engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    seed_db = TestingSessionLocal()
    ensure_auth_tables_and_seed_users(db_session=seed_db)
    seed_db.close()

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()
        login_rate_limiter.reset_all()


def _login_headers(client: TestClient, username: str, password: str) -> dict:
    resp = client.post("/api/v1/auth/login", json={"username": username, "password": password})
    assert resp.status_code == 200, resp.text
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_health_check_endpoint(api_client: TestClient):
    """Verify health check endpoint stays public and returns truthful database status."""
    response = api_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "services" in data
    assert "mysql" in data["services"]
    assert "mongodb" in data["services"]
    assert data["data_source_mode"] == "SIMULATION"


def test_simulation_status_endpoint(api_client: TestClient):
    """Verify simulation status endpoint returns configuration and counts when authenticated."""
    headers = _login_headers(api_client, "admin", settings.DEFAULT_ADMIN_PASSWORD)
    response = api_client.get("/api/v1/simulation/status", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "SIMULATED"
    assert "active_seed" in data
    assert "counts" in data
    assert "sessions" in data["counts"]


def test_simulation_generate_endpoint(api_client: TestClient):
    """Verify simulation generation API triggers synthesis when authenticated."""
    headers = _login_headers(api_client, "operator", settings.DEFAULT_OPERATOR_PASSWORD)
    payload = {
        "seed": 42,
        "scale": "small",
        "reset_first": False,
    }
    response = api_client.post("/api/v1/simulation/generate", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["seed"] == 42
    assert data["scale"] == "small"
    assert data["triggered_by"] == {"username": "operator", "role": "OPERATOR"}
    assert data["records_created"]["sessions"] == 1
    assert data["records_created"]["tasks"] == 5


def test_simulation_reset_requires_confirmation(api_client: TestClient):
    """Verify simulation reset rejects calls where confirm_purge is false (for ADMIN)."""
    headers = _login_headers(api_client, "admin", settings.DEFAULT_ADMIN_PASSWORD)
    payload = {
        "confirm_purge": False,
        "purge_target": "SIMULATED_ONLY",
    }
    response = api_client.post("/api/v1/simulation/reset", json=payload, headers=headers)
    assert response.status_code == 400
