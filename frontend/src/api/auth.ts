import apiClient from "./client";
import type {
  AuthAuditLogItem,
  LoginRequest,
  LogoutResponse,
  RolePermissionItem,
  SessionProfileResponse,
  TokenResponse,
  UserProfile,
} from "../types/auth";

export async function loginRequest(payload: LoginRequest): Promise<TokenResponse> {
  const { data } = await apiClient.post<TokenResponse>("/api/v1/auth/login", payload);
  return data;
}

export async function logoutRequest(): Promise<LogoutResponse> {
  const { data } = await apiClient.post<LogoutResponse>("/api/v1/auth/logout");
  return data;
}

export async function getCurrentSession(): Promise<SessionProfileResponse> {
  const { data } = await apiClient.get<SessionProfileResponse>("/api/v1/auth/me");
  return data;
}

export async function getPermissionsMatrix(): Promise<RolePermissionItem[]> {
  const { data } = await apiClient.get<RolePermissionItem[]>("/api/v1/auth/permissions-matrix");
  return data;
}

export async function getUsers(): Promise<UserProfile[]> {
  const { data } = await apiClient.get<UserProfile[]>("/api/v1/auth/users");
  return data;
}

export async function getAuditLogs(limit = 50): Promise<AuthAuditLogItem[]> {
  const { data } = await apiClient.get<AuthAuditLogItem[]>("/api/v1/auth/audit-logs", {
    params: { limit },
  });
  return data;
}
