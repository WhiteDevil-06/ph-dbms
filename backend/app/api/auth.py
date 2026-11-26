"""FastAPI router for JWT authentication, session revocation, RBAC info, and security audit logs."""

from typing import List
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from backend.app.core.security import (
    AuthenticatedPrincipal,
    ROLE_PERMISSION_MATRIX,
    extract_client_ip,
    get_current_user,
    require_roles,
)
from backend.app.database.mysql import get_db
from backend.app.models.enums import UserRole
from backend.app.schemas.auth import (
    AuthAuditLogItem,
    LoginRequest,
    LogoutResponse,
    RolePermissionItem,
    SessionProfileResponse,
    TokenResponse,
    UserProfile,
)
from backend.app.services import auth_service

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication & Security"])


@router.post("/login", response_model=TokenResponse)
def login(
    payload: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """Authenticate username/password and issue a signed HS256 JWT access token."""
    return auth_service.authenticate_user(
        db,
        username=payload.username,
        password=payload.password,
        client_ip=extract_client_ip(request),
    )


@router.post("/logout", response_model=LogoutResponse)
def logout(
    request: Request,
    principal: AuthenticatedPrincipal = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Revoke the active JWT session server-side so subsequent replays fail with HTTP 401."""
    return auth_service.logout_user(
        db,
        principal=principal,
        client_ip=extract_client_ip(request),
    )


@router.get("/me", response_model=SessionProfileResponse)
def get_me(principal: AuthenticatedPrincipal = Depends(get_current_user)):
    """Return the authenticated user's profile, role permissions, and token expiry."""
    return SessionProfileResponse(
        user=UserProfile(
            user_id=principal.user_id,
            username=principal.username,
            full_name=principal.full_name,
            role=principal.role,
            is_active=True,
            permissions=principal.permissions,
            provenance=principal.provenance,
            created_at=principal.created_at,
        ),
        jti=principal.jti,
        expires_at=principal.expires_at,
    )


@router.get("/permissions-matrix", response_model=List[RolePermissionItem])
def get_permissions_matrix(_principal: AuthenticatedPrincipal = Depends(get_current_user)):
    """Return the authoritative RBAC role differentiation matrix for ADMIN and OPERATOR."""
    return [RolePermissionItem(**item) for item in ROLE_PERMISSION_MATRIX]


@router.get("/users", response_model=List[UserProfile])
def list_users(
    _admin: AuthenticatedPrincipal = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    """List registered user accounts and roles (ADMIN only; password hashes are never exposed)."""
    return auth_service.list_user_profiles(db)


@router.get("/audit-logs", response_model=List[AuthAuditLogItem])
def list_audit_logs(
    limit: int = Query(default=50, ge=1, le=200),
    _admin: AuthenticatedPrincipal = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    """Return recent authentication, logout, rate-limit, and RBAC denial audit records (ADMIN only)."""
    return auth_service.list_recent_audit_logs(db, limit=limit)
