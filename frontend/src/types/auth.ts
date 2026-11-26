export type UserRole = "ADMIN" | "OPERATOR";

export type AuthAuditAction =
  | "LOGIN_SUCCESS"
  | "LOGIN_FAILED"
  | "LOGOUT"
  | "ACCESS_DENIED"
  | "RATE_LIMITED";

export interface UserProfile {
  user_id: string;
  username: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  permissions: string[];
  provenance: string;
  created_at: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: "bearer";
  expires_in: number;
  expires_at: string;
  user: UserProfile;
}

export interface SessionProfileResponse {
  user: UserProfile;
  jti: string;
  expires_at: string;
}

export interface LogoutResponse {
  message: string;
  jti: string;
  revoked_at: string;
}

export interface AuthAuditLogItem {
  audit_id: string;
  username: string;
  user_id: string | null;
  action: AuthAuditAction;
  role: string | null;
  endpoint: string | null;
  ip_address: string | null;
  detail: string | null;
  created_at: string;
}

export interface RolePermissionItem {
  capability: string;
  endpoint: string;
  admin_allowed: boolean;
  operator_allowed: boolean;
  notes: string;
}
