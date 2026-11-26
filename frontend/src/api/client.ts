import axios from "axios";
import type { APIError } from "../types/api";

export const AUTH_TOKEN_STORAGE_KEY = "ph_dbms_jwt_token";
export const SESSION_EXPIRED_EVENT = "ph-dbms:session-expired";

export function getStoredToken(): string | null {
  try {
    return window.localStorage.getItem(AUTH_TOKEN_STORAGE_KEY);
  } catch {
    return null;
  }
}

export function setStoredToken(token: string): void {
  try {
    window.localStorage.setItem(AUTH_TOKEN_STORAGE_KEY, token);
  } catch {
    // Ignore storage quota / privacy mode errors
  }
}

export function clearStoredToken(): void {
  try {
    window.localStorage.removeItem(AUTH_TOKEN_STORAGE_KEY);
  } catch {
    // Ignore storage errors
  }
}

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "",
  headers: { "Content-Type": "application/json" },
  timeout: 10000,
});

apiClient.interceptors.request.use((config) => {
  const token = getStoredToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (axios.isAxiosError(error)) {
      const status = error.response?.status;
      const url = error.config?.url ?? "";
      const isAuthEndpoint =
        url.includes("/api/v1/auth/login") || url.includes("/api/v1/auth/logout");
      if (status === 401 && !isAuthEndpoint && getStoredToken()) {
        clearStoredToken();
        window.dispatchEvent(new CustomEvent(SESSION_EXPIRED_EVENT));
      }
    }
    return Promise.reject(error);
  },
);

export function getApiErrorMessage(error: unknown): string {
  if (axios.isAxiosError<APIError>(error)) {
    const detail = error.response?.data?.detail;
    if (Array.isArray(detail) && detail.length > 0) {
      const first = detail[0] as { msg?: string };
      if (first?.msg) return first.msg;
    }
    const responseMessage =
      error.response?.data?.error?.message ??
      (typeof detail === "string" ? detail : undefined);
    if (responseMessage) return responseMessage;
    if (error.code === "ECONNABORTED") {
      return "The API request timed out. Check that the backend is available.";
    }
    if (!error.response) {
      return "Unable to reach the backend. Check the API connection and try again.";
    }
    return `The backend returned an unexpected response (${error.response.status}).`;
  }
  return "Something went wrong while communicating with the backend.";
}

export default apiClient;
