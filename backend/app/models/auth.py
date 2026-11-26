"""SQLAlchemy ORM models for JWT authentication, RBAC, token revocation, and security audit logs."""

from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Boolean, DateTime, Enum as SAEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.base import Base
from backend.app.models.enums import AuthAuditAction, UserRole


def _utcnow_naive() -> datetime:
    """Return current UTC timestamp as naive datetime compatible with MySQL DATETIME."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class AppUser(Base):
    """Registered dashboard user account with role-based permissions."""

    __tablename__ = "app_user"

    user_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole), nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    provenance: Mapped[str] = mapped_column(String(20), nullable=False, default="SIMULATED")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=_utcnow_naive)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=_utcnow_naive,
        onupdate=_utcnow_naive,
    )


class RevokedToken(Base):
    """Server-side JWT denylist enabling true revocation on logout."""

    __tablename__ = "revoked_token"

    jti: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("app_user.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    revoked_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=_utcnow_naive)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)


class AuthAuditLog(Base):
    """Security audit trail recording authentication, logout, rate-limit, and RBAC denial events."""

    __tablename__ = "auth_audit_log"

    audit_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    user_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("app_user.user_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    action: Mapped[AuthAuditAction] = mapped_column(SAEnum(AuthAuditAction), nullable=False, index=True)
    role: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    endpoint: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    detail: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=_utcnow_naive, index=True)
