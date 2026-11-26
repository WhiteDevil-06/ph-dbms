"""Pydantic v2 request and response schemas for authentication, RBAC, and audit logs."""

from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field

from backend.app.models.enums import AuthAuditAction, UserRole


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_.-]+$",
        description="Account username (alphanumeric, dot, underscore, hyphen).",
    )
    password: str = Field(
        ...,
        min_length=6,
        max_length=128,
        description="Account password.",
    )


class UserProfile(BaseModel):
    user_id: str
    username: str
    full_name: str
    role: UserRole
    is_active: bool = True
    permissions: List[str]
    provenance: str
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    expires_in: int
    expires_at: datetime
    user: UserProfile


class SessionProfileResponse(BaseModel):
    user: UserProfile
    jti: str
    expires_at: datetime


class LogoutResponse(BaseModel):
    message: str
    jti: str
    revoked_at: datetime


class AuthAuditLogItem(BaseModel):
    audit_id: str
    username: str
    user_id: Optional[str] = None
    action: AuthAuditAction
    role: Optional[str] = None
    endpoint: Optional[str] = None
    ip_address: Optional[str] = None
    detail: Optional[str] = None
    created_at: datetime


class RolePermissionItem(BaseModel):
    capability: str
    endpoint: str
    admin_allowed: bool
    operator_allowed: bool
    notes: str
