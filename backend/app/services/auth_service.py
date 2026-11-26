"""Business service layer for JWT authentication, session revocation, and demo user seeding."""

from datetime import datetime, timezone
import logging
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.security import (
    AuthenticatedPrincipal,
    ROLE_PERMISSIONS,
    create_access_token,
    hash_password,
    login_rate_limiter,
    verify_password,
)
from backend.app.database.base import Base
from backend.app.database.mysql import SessionLocal, check_mysql_connection, engine
from backend.app.models.auth import AppUser, AuthAuditLog, RevokedToken
from backend.app.models.enums import AuthAuditAction, UserRole
from backend.app.repositories import auth_repository
from backend.app.schemas.auth import (
    AuthAuditLogItem,
    LogoutResponse,
    TokenResponse,
    UserProfile,
)

logger = logging.getLogger(__name__)


def _to_user_profile(user: AppUser) -> UserProfile:
    return UserProfile(
        user_id=user.user_id,
        username=user.username,
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active,
        permissions=list(ROLE_PERMISSIONS.get(user.role, [])),
        provenance=user.provenance,
        created_at=user.created_at,
    )


def ensure_auth_tables_and_seed_users(db_session: Session | None = None) -> bool:
    """Idempotently ensure auth tables exist and seed the ADMIN and OPERATOR demo accounts."""
    if db_session is None:
        if not check_mysql_connection():
            logger.warning("MySQL unavailable during auth bootstrap; skipping table/user seed.")
            return False
        Base.metadata.create_all(
            bind=engine,
            tables=[AppUser.__table__, RevokedToken.__table__, AuthAuditLog.__table__],
        )

    close_session = False
    if db_session is None:
        db_session = SessionLocal()
        close_session = True

    try:
        seed_specs = [
            {
                "user_id": "usr-admin-001",
                "username": "admin",
                "full_name": "Packhouse System Admin",
                "role": UserRole.ADMIN,
                "password": settings.DEFAULT_ADMIN_PASSWORD,
            },
            {
                "user_id": "usr-operator-001",
                "username": "operator",
                "full_name": "Robotics Line Operator",
                "role": UserRole.OPERATOR,
                "password": settings.DEFAULT_OPERATOR_PASSWORD,
            },
        ]
        for spec in seed_specs:
            existing = auth_repository.get_user_by_username(db_session, spec["username"])
            if existing is None:
                auth_repository.create_user(
                    db_session,
                    user_id=spec["user_id"],
                    username=spec["username"],
                    full_name=spec["full_name"],
                    role=spec["role"],
                    password_hash=hash_password(spec["password"]),
                    provenance="SIMULATED",
                )
        return True
    except Exception as exc:
        logger.warning("Auth bootstrap encountered an error: %s", type(exc).__name__)
        db_session.rollback()
        return False
    finally:
        if close_session:
            db_session.close()


def authenticate_user(
    db: Session,
    *,
    username: str,
    password: str,
    client_ip: str,
) -> TokenResponse:
    """Authenticate credentials, enforce brute-force rate limit, issue JWT, and log audit event."""
    normalized_username = username.strip()
    rate_key = f"{client_ip}:{normalized_username.lower()}"

    if login_rate_limiter.is_limited(rate_key):
        auth_repository.record_audit_event(
            db,
            username=normalized_username,
            action=AuthAuditAction.RATE_LIMITED,
            endpoint="POST /api/v1/auth/login",
            ip_address=client_ip,
            detail="Too many failed login attempts within rate-limit window.",
        )
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many failed login attempts. Please wait a few minutes and try again.",
        )

    user = auth_repository.get_user_by_username(db, normalized_username)
    if user is None or not user.is_active or not verify_password(password, user.password_hash):
        login_rate_limiter.record_failure(rate_key)
        auth_repository.record_audit_event(
            db,
            username=normalized_username,
            user_id=user.user_id if user else None,
            action=AuthAuditAction.LOGIN_FAILED,
            role=user.role.value if user else None,
            endpoint="POST /api/v1/auth/login",
            ip_address=client_ip,
            detail="Invalid credentials or inactive account.",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    login_rate_limiter.clear(rate_key)
    access_token, jti, expires_at, expires_in = create_access_token(
        user_id=user.user_id,
        username=user.username,
        role=user.role,
    )

    auth_repository.record_audit_event(
        db,
        username=user.username,
        user_id=user.user_id,
        action=AuthAuditAction.LOGIN_SUCCESS,
        role=user.role.value,
        endpoint="POST /api/v1/auth/login",
        ip_address=client_ip,
        detail=f"Issued JWT session (jti={jti[:8]}..., ttl={settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES}m).",
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=expires_in,
        expires_at=expires_at,
        user=_to_user_profile(user),
    )


def logout_user(
    db: Session,
    *,
    principal: AuthenticatedPrincipal,
    client_ip: str,
) -> LogoutResponse:
    """Revoke the current JWT server-side and log the logout event."""
    record = auth_repository.revoke_token(
        db,
        jti=principal.jti,
        user_id=principal.user_id,
        expires_at=principal.expires_at,
    )
    auth_repository.record_audit_event(
        db,
        username=principal.username,
        user_id=principal.user_id,
        action=AuthAuditAction.LOGOUT,
        role=principal.role.value,
        endpoint="POST /api/v1/auth/logout",
        ip_address=client_ip,
        detail=f"Revoked JWT session (jti={principal.jti[:8]}...).",
    )
    revoked_at_utc = record.revoked_at.replace(tzinfo=timezone.utc)
    return LogoutResponse(
        message="Session ended and JWT token revoked server-side.",
        jti=principal.jti,
        revoked_at=revoked_at_utc,
    )


def list_user_profiles(db: Session) -> List[UserProfile]:
    users = auth_repository.list_users(db)
    return [_to_user_profile(u) for u in users]


def list_recent_audit_logs(db: Session, limit: int = 50) -> List[AuthAuditLogItem]:
    rows = auth_repository.list_audit_logs(db, limit=limit)
    return [
        AuthAuditLogItem(
            audit_id=row.audit_id,
            username=row.username,
            user_id=row.user_id,
            action=row.action,
            role=row.role,
            endpoint=row.endpoint,
            ip_address=row.ip_address,
            detail=row.detail,
            created_at=row.created_at.replace(tzinfo=timezone.utc)
            if row.created_at.tzinfo is None
            else row.created_at,
        )
        for row in rows
    ]
