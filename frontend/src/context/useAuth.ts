import { createContext, useContext } from "react";
import type { LoginRequest, UserProfile } from "../types/auth";

export interface AuthContextValue {
  user: UserProfile | null;
  token: string | null;
  jti: string | null;
  expiresAt: string | null;
  isAuthenticated: boolean;
  isInitializing: boolean;
  isAdmin: boolean;
  isOperator: boolean;
  sessionNotice: string | null;
  clearSessionNotice: () => void;
  login: (payload: LoginRequest) => Promise<UserProfile>;
  logout: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextValue | null>(null);

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used inside an AuthProvider");
  }
  return ctx;
}
