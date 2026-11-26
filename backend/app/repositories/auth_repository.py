"""Repository layer for user accounts, revoked JWT tokens, and security audit logs."""

from datetime import datetime, timezone
from typing import List, Optional
import uuid
from sqlalchemy.orm import Session

from backend.app.models.auth import AppUser, AuthAuditLog, RevokedToken
from backend.app.models.enums import AuthAuditAction, UserRole


def get_user_by_username(db: Session, username: str) -> Optional[AppUser]:
    return db.query(AppUser).filter(AppUser.username == username).first()


def get_user_by_id(db: Session, user_id: str) -> Optional[AppUser]:
    return db.query(AppUser).filter(AppUser.user_id == user_id).first()


def list_users(db: Session) -> List[AppUser]:
    return db.query(AppUser).order_by(AppUser.role.asc(), AppUser.username.asc()).all()


def create_user(
    db: Session,
    *,
    user_id: str,
    username: str,
    full_name: str,
    role: UserRole,
    password_hash: str,
    provenance: str = "SIMULATED",
) -> AppUser:
    user = AppUser(
        user_id=user_id,
        username=username,
        full_name=full_name,
        role=role,
        password_hash=password_hash,
        is_active=True,
        provenance=provenance,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def revoke_token(db: Session, *, jti: str, user_id: str, expires_at: datetime) -> RevokedToken:
    existing = db.query(RevokedToken).filter_by(jti=jti).first()
    if existing:
        return existing
    expires_naive = expires_at.astimezone(timezone.utc).replace(tzinfo=None) if expires_at.tzinfo else expires_at
    record = RevokedToken(
        jti=jti,
        user_id=user_id,
        revoked_at=datetime.now(timezone.utc).replace(tzinfo=None),
        expires_at=expires_naive,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def record_audit_event(
    db: Session,
    *,
    username: str,
    action: AuthAuditAction,
    user_id: Optional[str] = None,
    role: Optional[str] = None,
    endpoint: Optional[str] = None,
    ip_address: Optional[str] = None,
    detail: Optional[str] = None,
) -> AuthAuditLog:
    entry = AuthAuditLog(
        audit_id=str(uuid.uuid4()),
        username=username[:50],
        user_id=user_id,
        action=action,
        role=role,
        endpoint=endpoint[:150] if endpoint else None,
        ip_address=ip_address[:64] if ip_address else None,
        detail=detail[:255] if detail else None,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def list_audit_logs(db: Session, limit: int = 50) -> List[AuthAuditLog]:
    return (
        db.query(AuthAuditLog)
        .order_by(AuthAuditLog.created_at.desc())
        .limit(limit)
        .all()
    )
