"""JWT authentication, PBKDF2 password hashing, RBAC guards, rate limiting, and security headers."""

from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import secrets
import time
from typing import Callable, Deque, Dict, List, Optional, Tuple
import uuid

import jwt
from jwt import InvalidTokenError
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware

from backend.app.core.config import settings
from backend.app.database.mysql import get_db
from backend.app.models.auth import AppUser, AuthAuditLog, RevokedToken
from backend.app.models.enums import AuthAuditAction, UserRole

PBKDF2_ITERATIONS = 600_000

ROLE_PERMISSIONS: Dict[UserRole, List[str]] = {
    UserRole.ADMIN: [
        "read:dashboard",
        "read:simulation",
        "write:simulation:generate",
        "write:simulation:reset",
        "read:auth:users",
        "read:auth:audit",
    ],
    UserRole.OPERATOR: [
        "read:dashboard",
        "read:simulation",
        "write:simulation:generate",
    ],
}

ROLE_PERMISSION_MATRIX = [
    {
        "capability": "View system healthcheck",
        "endpoint": "GET /health",
        "admin_allowed": True,
        "operator_allowed": True,
        "notes": "Public endpoint required for container health probes.",
    },
    {
        "capability": "View dashboard & simulation status",
        "endpoint": "GET /api/v1/simulation/status",
        "admin_allowed": True,
        "operator_allowed": True,
        "notes": "Requires valid JWT session (8-hour expiry).",
    },
    {
        "capability": "Generate simulated dataset (non-destructive)",
        "endpoint": "POST /api/v1/simulation/generate (reset_first=false)",
        "admin_allowed": True,
        "operator_allowed": True,
        "notes": "Operators can synthesize seeded simulation data.",
    },
    {
        "capability": "Clear & regenerate dataset (destructive)",
        "endpoint": "POST /api/v1/simulation/generate (reset_first=true)",
        "admin_allowed": True,
        "operator_allowed": False,
        "notes": "Restricted to ADMIN; returns HTTP 403 for OPERATOR.",
    },
    {
        "capability": "Purge simulated operational records",
        "endpoint": "POST /api/v1/simulation/reset",
        "admin_allowed": True,
        "operator_allowed": False,
        "notes": "Requires ADMIN role + explicit confirm_purge=true.",
    },
    {
        "capability": "Inspect registered accounts & security audit logs",
        "endpoint": "GET /api/v1/auth/users · /api/v1/auth/audit-logs",
        "admin_allowed": True,
        "operator_allowed": False,
        "notes": "Admin-only governance and security audit views.",
    },
]

bearer_scheme = HTTPBearer(auto_error=False, description="Paste JWT access token obtained from POST /api/v1/auth/login")


@dataclass(frozen=True)
class AuthenticatedPrincipal:
    user_id: str
    username: str
    full_name: str
    role: UserRole
    jti: str
    expires_at: datetime
    permissions: List[str]
    provenance: str
    created_at: datetime


class LoginRateLimiter:
    """In-memory sliding-window failed-login throttle to mitigate brute-force attacks."""

    def __init__(self) -> None:
        self._attempts: Dict[str, Deque[float]] = defaultdict(deque)

    def _prune(self, key: str, now: float, window: int) -> Deque[float]:
        bucket = self._attempts[key]
        cutoff = now - window
        while bucket and bucket[0] < cutoff:
            bucket.popleft()
        return bucket

    def is_limited(self, key: str) -> bool:
        now = time.monotonic()
        bucket = self._prune(key, now, settings.AUTH_RATE_LIMIT_WINDOW_SECONDS)
        return len(bucket) >= settings.AUTH_RATE_LIMIT_MAX_ATTEMPTS

    def record_failure(self, key: str) -> int:
        now = time.monotonic()
        bucket = self._prune(key, now, settings.AUTH_RATE_LIMIT_WINDOW_SECONDS)
        bucket.append(now)
        return len(bucket)

    def clear(self, key: str) -> None:
        self._attempts.pop(key, None)

    def reset_all(self) -> None:
        self._attempts.clear()


login_rate_limiter = LoginRateLimiter()


def hash_password(password: str, salt_hex: Optional[str] = None) -> str:
    """Hash a plaintext password using PBKDF2-HMAC-SHA256 with a unique random salt."""
    salt = bytes.fromhex(salt_hex) if salt_hex else secrets.token_bytes(16)
    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt.hex()}${derived.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify a password against a stored PBKDF2-HMAC-SHA256 hash using constant-time comparison."""
    try:
        scheme, iterations_str, salt_hex, expected_hex = stored_hash.split("$", 3)
        if scheme != "pbkdf2_sha256":
            return False
        iterations = int(iterations_str)
        salt = bytes.fromhex(salt_hex)
        derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
        return hmac.compare_digest(derived.hex(), expected_hex)
    except (ValueError, TypeError):
        return False


def create_access_token(
    *,
    user_id: str,
    username: str,
    role: UserRole,
    expires_minutes: Optional[int] = None,
) -> Tuple[str, str, datetime, int]:
    """Create a signed HS256 JWT access token with unique jti and expiration."""
    now = datetime.now(timezone.utc)
    ttl_minutes = expires_minutes if expires_minutes is not None else settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    expires_at = now + timedelta(minutes=ttl_minutes)
    jti = str(uuid.uuid4())
    payload = {
        "sub": user_id,
        "username": username,
        "role": role.value,
        "jti": jti,
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    expires_in = max(0, int((expires_at - now).total_seconds()))
    return token, jti, expires_at, expires_in


def decode_access_token(token: str) -> dict:
    """Decode and validate a JWT access token signature, expiry, and mandatory claims."""
    payload = jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
        options={"require": ["sub", "username", "role", "jti", "exp", "iat"]},
    )
    return payload


def extract_client_ip(request: Request) -> str:
    """Extract client IP address safely without trusting arbitrary multi-hop headers."""
    if request.client and request.client.host:
        return request.client.host[:64]
    return "unknown"


def _record_denied_audit(
    db: Session,
    *,
    principal: AuthenticatedPrincipal,
    request: Request,
    detail: str,
) -> None:
    try:
        db.add(
            AuthAuditLog(
                audit_id=str(uuid.uuid4()),
                username=principal.username,
                user_id=principal.user_id,
                action=AuthAuditAction.ACCESS_DENIED,
                role=principal.role.value,
                endpoint=f"{request.method} {request.url.path}"[:150],
                ip_address=extract_client_ip(request),
                detail=detail[:255],
            )
        )
        db.commit()
    except Exception:
        db.rollback()


def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> AuthenticatedPrincipal:
    """Validate Bearer JWT, enforce server-side revocation denylist, and resolve active user."""
    if credentials is None or credentials.scheme.lower() != "bearer" or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Provide a valid Bearer JWT.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = decode_access_token(credentials.credentials)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session token has expired. Please sign in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    jti = str(payload["jti"])
    user_id = str(payload["sub"])

    revoked = db.query(RevokedToken).filter_by(jti=jti).first()
    if revoked is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session token has been revoked. Please sign in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(AppUser).filter_by(user_id=user_id, is_active=True).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is unavailable or disabled.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    expires_at = datetime.fromtimestamp(int(payload["exp"]), tz=timezone.utc)
    return AuthenticatedPrincipal(
        user_id=user.user_id,
        username=user.username,
        full_name=user.full_name,
        role=user.role,
        jti=jti,
        expires_at=expires_at,
        permissions=list(ROLE_PERMISSIONS.get(user.role, [])),
        provenance=user.provenance,
        created_at=user.created_at,
    )


def require_roles(*allowed_roles: UserRole) -> Callable:
    """FastAPI dependency factory enforcing role-based access control (HTTP 403 on denial)."""

    def _dependency(
        request: Request,
        principal: AuthenticatedPrincipal = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> AuthenticatedPrincipal:
        if principal.role not in allowed_roles:
            allowed_names = ", ".join(r.value for r in allowed_roles)
            detail = f"Access denied: role '{principal.role.value}' cannot perform this action. Required role: {allowed_names}."
            _record_denied_audit(db, principal=principal, request=request, detail=detail)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=detail,
            )
        return principal

    return _dependency


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Attach defensive HTTP security headers to every API response."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        if request.url.path.startswith("/api/v1/auth"):
            response.headers["Cache-Control"] = "no-store"
            response.headers["Pragma"] = "no-cache"
        return response
