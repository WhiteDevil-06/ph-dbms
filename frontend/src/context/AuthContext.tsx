import {
  useCallback,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { useQueryClient } from "@tanstack/react-query";
import { getCurrentSession, loginRequest, logoutRequest } from "../api/auth";
import {
  clearStoredToken,
  getStoredToken,
  SESSION_EXPIRED_EVENT,
  setStoredToken,
} from "../api/client";
import type { LoginRequest, UserProfile } from "../types/auth";
import { AuthContext, type AuthContextValue } from "./useAuth";

export function AuthProvider({ children }: { children: ReactNode }) {
  const queryClient = useQueryClient();
  const [token, setToken] = useState<string | null>(() => getStoredToken());
  const [user, setUser] = useState<UserProfile | null>(null);
  const [jti, setJti] = useState<string | null>(null);
  const [expiresAt, setExpiresAt] = useState<string | null>(null);
  const [isInitializing, setIsInitializing] = useState<boolean>(() => Boolean(getStoredToken()));
  const [sessionNotice, setSessionNotice] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    const initialToken = getStoredToken();
    if (!initialToken) {
      setIsInitializing(false);
      return;
    }
    getCurrentSession()
      .then((session) => {
        if (!active) return;
        setToken(initialToken);
        setUser(session.user);
        setJti(session.jti);
        setExpiresAt(session.expires_at);
      })
      .catch(() => {
        if (!active) return;
        clearStoredToken();
        setToken(null);
        setUser(null);
        setJti(null);
        setExpiresAt(null);
        setSessionNotice("Your previous session expired or was revoked. Please sign in again.");
      })
      .finally(() => {
        if (active) setIsInitializing(false);
      });

    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    const handleExpired = () => {
      clearStoredToken();
      setToken(null);
      setUser(null);
      setJti(null);
      setExpiresAt(null);
      queryClient.clear();
      setSessionNotice("Your JWT session expired or was revoked. Please sign in again.");
    };
    window.addEventListener(SESSION_EXPIRED_EVENT, handleExpired);
    return () => window.removeEventListener(SESSION_EXPIRED_EVENT, handleExpired);
  }, [queryClient]);

  const login = useCallback(
    async (payload: LoginRequest) => {
      const response = await loginRequest(payload);
      setStoredToken(response.access_token);
      setToken(response.access_token);
      setUser(response.user);
      setExpiresAt(response.expires_at);
      setSessionNotice(null);
      queryClient.clear();

      try {
        const session = await getCurrentSession();
        setJti(session.jti);
        setExpiresAt(session.expires_at);
      } catch {
        setJti(null);
      }

      return response.user;
    },
    [queryClient],
  );

  const logout = useCallback(async () => {
    try {
      if (getStoredToken()) {
        await logoutRequest();
      }
    } catch {
      // Clear local session even if server is unreachable
    } finally {
      clearStoredToken();
      setToken(null);
      setUser(null);
      setJti(null);
      setExpiresAt(null);
      queryClient.clear();
      setSessionNotice("Signed out cleanly. Your JWT session token was revoked on the server.");
    }
  }, [queryClient]);

  const clearSessionNotice = useCallback(() => setSessionNotice(null), []);

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      token,
      jti,
      expiresAt,
      isAuthenticated: Boolean(token && user),
      isInitializing,
      isAdmin: user?.role === "ADMIN",
      isOperator: user?.role === "OPERATOR",
      sessionNotice,
      clearSessionNotice,
      login,
      logout,
    }),
    [user, token, jti, expiresAt, isInitializing, sessionNotice, clearSessionNotice, login, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
