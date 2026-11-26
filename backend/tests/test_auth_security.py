"""Comprehensive security, JWT session, RBAC (ADMIN vs OPERATOR), and input validation tests."""

from datetime import datetime, timedelta, timezone
import jwt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.core.config import settings
from backend.app.core.security import hash_password, login_rate_limiter, verify_password
from backend.app.database.base import Base
from backend.app.database.mysql import get_db
from backend.app.main import app
from backend.app.services.auth_service import ensure_auth_tables_and_seed_users


@pytest.fixture()
def auth_client():
    """Isolated in-memory SQLite database with seeded ADMIN and OPERATOR accounts."""
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


def _login(client: TestClient, username: str, password: str):
    return client.post("/api/v1/auth/login", json={"username": username, "password": password})


def test_password_hashing_uses_unique_salts_and_verifies():
    """Verify PBKDF2-HMAC-SHA256 produces distinct salted hashes and verifies accurately."""
    h1 = hash_password("StrongPass!2026")
    h2 = hash_password("StrongPass!2026")
    assert h1 != h2
    assert h1.startswith("pbkdf2_sha256$600000$")
    assert verify_password("StrongPass!2026", h1) is True
    assert verify_password("WrongPass!2026", h1) is False


def test_admin_and_operator_login_issue_valid_8h_jwt(auth_client: TestClient):
    """Verify ADMIN and OPERATOR logins return signed JWTs with 8-hour TTL and no password leak."""
    for username, password, expected_role in [
        ("admin", settings.DEFAULT_ADMIN_PASSWORD, "ADMIN"),
        ("operator", settings.DEFAULT_OPERATOR_PASSWORD, "OPERATOR"),
    ]:
        res = _login(auth_client, username, password)
        assert res.status_code == 200
        body = res.json()
        assert body["token_type"] == "bearer"
        assert body["user"]["username"] == username
        assert body["user"]["role"] == expected_role
        assert "password_hash" not in body["user"]
        # 8 hours = 28800 seconds (allow small delta for execution time)
        assert 28750 <= body["expires_in"] <= 28800

        # /me returns matching profile and jti
        me_res = auth_client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {body['access_token']}"},
        )
        assert me_res.status_code == 200
        assert me_res.json()["user"]["role"] == expected_role


def test_invalid_credentials_do_not_enumerate_usernames(auth_client: TestClient):
    """Wrong password and unknown user must return identical generic 401 responses."""
    wrong_pw = _login(auth_client, "admin", "WrongPassword123")
    unknown_user = _login(auth_client, "nonexistent_user", "WrongPassword123")
    assert wrong_pw.status_code == 401
    assert unknown_user.status_code == 401
    assert wrong_pw.json()["detail"] == unknown_user.json()["detail"] == "Invalid username or password."


def test_sql_injection_payload_safely_rejected(auth_client: TestClient):
    """SQL injection attempts in username are rejected cleanly by Pydantic regex validation."""
    res = _login(auth_client, "admin' OR '1'='1", "anything123")
    assert res.status_code == 422


def test_unauthenticated_and_tampered_and_expired_tokens_rejected(auth_client: TestClient):
    """Protected endpoints must return 401 for missing, tampered, or expired JWTs."""
    # Missing token
    assert auth_client.get("/api/v1/simulation/status").status_code == 401
    assert auth_client.get("/api/v1/auth/me").status_code == 401

    # Tampered signature
    valid_token = _login(auth_client, "admin", settings.DEFAULT_ADMIN_PASSWORD).json()["access_token"]
    tampered = valid_token[:-4] + ("AAAA" if not valid_token.endswith("AAAA") else "BBBB")
    assert auth_client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {tampered}"}).status_code == 401

    # Expired token
    expired_payload = {
        "sub": "usr-admin-001",
        "username": "admin",
        "role": "ADMIN",
        "jti": "expired-jti-001",
        "iat": int((datetime.now(timezone.utc) - timedelta(hours=10)).timestamp()),
        "exp": int((datetime.now(timezone.utc) - timedelta(hours=1)).timestamp()),
    }
    expired_token = jwt.encode(expired_payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    exp_res = auth_client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {expired_token}"})
    assert exp_res.status_code == 401
    assert "expired" in exp_res.json()["detail"].lower()


def test_logout_revokes_jwt_server_side(auth_client: TestClient):
    """After POST /api/v1/auth/logout, replaying the same JWT must immediately return 401."""
    token = _login(auth_client, "operator", settings.DEFAULT_OPERATOR_PASSWORD).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Valid before logout
    assert auth_client.get("/api/v1/auth/me", headers=headers).status_code == 200

    # Logout revokes token
    logout_res = auth_client.post("/api/v1/auth/logout", headers=headers)
    assert logout_res.status_code == 200
    assert "revoked" in logout_res.json()["message"].lower()

    # Replaying revoked token fails with 401
    replay_me = auth_client.get("/api/v1/auth/me", headers=headers)
    assert replay_me.status_code == 401
    assert "revoked" in replay_me.json()["detail"].lower()

    replay_sim = auth_client.get("/api/v1/simulation/status", headers=headers)
    assert replay_sim.status_code == 401


def test_rbac_role_differentiation_admin_vs_operator(auth_client: TestClient):
    """Verify OPERATOR is blocked (403) from destructive/admin actions while ADMIN succeeds."""
    admin_headers = {
        "Authorization": f"Bearer {_login(auth_client, 'admin', settings.DEFAULT_ADMIN_PASSWORD).json()['access_token']}"
    }
    op_headers = {
        "Authorization": f"Bearer {_login(auth_client, 'operator', settings.DEFAULT_OPERATOR_PASSWORD).json()['access_token']}"
    }

    # Both roles can read simulation status and permissions matrix
    assert auth_client.get("/api/v1/simulation/status", headers=op_headers).status_code == 200
    assert auth_client.get("/api/v1/auth/permissions-matrix", headers=op_headers).status_code == 200

    # OPERATOR can run non-destructive generate (reset_first=False)
    gen_ok = auth_client.post(
        "/api/v1/simulation/generate",
        json={"seed": 42, "scale": "small", "reset_first": False},
        headers=op_headers,
    )
    assert gen_ok.status_code == 201

    # OPERATOR is DENIED (403) on destructive reset_first=True
    gen_denied = auth_client.post(
        "/api/v1/simulation/generate",
        json={"seed": 42, "scale": "small", "reset_first": True},
        headers=op_headers,
    )
    assert gen_denied.status_code == 403

    # OPERATOR is DENIED (403) on simulation reset
    reset_denied = auth_client.post(
        "/api/v1/simulation/reset",
        json={"confirm_purge": True, "purge_target": "SIMULATED_ONLY"},
        headers=op_headers,
    )
    assert reset_denied.status_code == 403

    # OPERATOR is DENIED (403) on admin-only user list and audit logs
    assert auth_client.get("/api/v1/auth/users", headers=op_headers).status_code == 403
    assert auth_client.get("/api/v1/auth/audit-logs", headers=op_headers).status_code == 403

    # ADMIN succeeds on users list (no password_hash exposed) and audit logs (records 403 denials!)
    users_res = auth_client.get("/api/v1/auth/users", headers=admin_headers)
    assert users_res.status_code == 200
    users = users_res.json()
    assert {u["role"] for u in users} == {"ADMIN", "OPERATOR"}
    for u in users:
        assert "password_hash" not in u

    audit_res = auth_client.get("/api/v1/auth/audit-logs", headers=admin_headers)
    assert audit_res.status_code == 200
    actions = {entry["action"] for entry in audit_res.json()}
    assert "LOGIN_SUCCESS" in actions
    assert "ACCESS_DENIED" in actions


def test_strict_input_validation_on_auth_and_simulation(auth_client: TestClient):
    """Verify strict Pydantic validation rejects invalid fields, scales, seeds, and extra keys."""
    admin_headers = {
        "Authorization": f"Bearer {_login(auth_client, 'admin', settings.DEFAULT_ADMIN_PASSWORD).json()['access_token']}"
    }

    # Extra unknown field in login rejected
    res_extra = auth_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": settings.DEFAULT_ADMIN_PASSWORD, "role": "ADMIN"},
    )
    assert res_extra.status_code == 422

    # Invalid scale rejected
    res_scale = auth_client.post(
        "/api/v1/simulation/generate",
        json={"seed": 42, "scale": "huge", "reset_first": False},
        headers=admin_headers,
    )
    assert res_scale.status_code == 422

    # Negative seed rejected
    res_seed = auth_client.post(
        "/api/v1/simulation/generate",
        json={"seed": -5, "scale": "small", "reset_first": False},
        headers=admin_headers,
    )
    assert res_seed.status_code == 422


def test_brute_force_rate_limit_triggers_429(auth_client: TestClient):
    """After 5 consecutive failed logins, the 6th attempt must be throttled with HTTP 429."""
    for _ in range(settings.AUTH_RATE_LIMIT_MAX_ATTEMPTS):
        res = _login(auth_client, "operator", "WrongPass999")
        assert res.status_code == 401

    throttled = _login(auth_client, "operator", "WrongPass999")
    assert throttled.status_code == 429
    assert "too many failed login attempts" in throttled.json()["detail"].lower()


def test_security_headers_attached(auth_client: TestClient):
    """Verify defensive security headers are present on responses, with no-store on auth routes."""
    health_res = auth_client.get("/health")
    assert health_res.headers.get("X-Content-Type-Options") == "nosniff"
    assert health_res.headers.get("X-Frame-Options") == "DENY"
    assert health_res.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"

    login_res = _login(auth_client, "admin", settings.DEFAULT_ADMIN_PASSWORD)
    assert login_res.headers.get("Cache-Control") == "no-store"
