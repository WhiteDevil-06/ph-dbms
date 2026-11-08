"""Tests for FastAPI endpoints."""

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_check_endpoint():
    """Verify health check endpoint returns expected structure and truthful database status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "services" in data
    assert "mysql" in data["services"]
    assert "mongodb" in data["services"]
    assert data["data_source_mode"] == "SIMULATION"


def test_simulation_status_endpoint():
    """Verify simulation status endpoint returns configuration and counts."""
    response = client.get("/api/v1/simulation/status")
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "SIMULATED"
    assert "active_seed" in data
    assert "counts" in data
    assert "sessions" in data["counts"]


def test_simulation_generate_endpoint():
    """Verify simulation generation API triggers synthesis."""
    payload = {
        "seed": 42,
        "scale": "small",
        "reset_first": False,
    }
    response = client.post("/api/v1/simulation/generate", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["seed"] == 42
    assert data["scale"] == "small"
    assert data["records_created"]["sessions"] == 1
    assert data["records_created"]["tasks"] == 5


def test_simulation_reset_requires_confirmation():
    """Verify simulation reset rejects calls where confirm_purge is false."""
    payload = {
        "confirm_purge": False,
        "purge_target": "SIMULATED_ONLY",
    }
    response = client.post("/api/v1/simulation/reset", json=payload)
    assert response.status_code == 400
