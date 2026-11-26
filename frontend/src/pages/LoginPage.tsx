import { useState, type FormEvent } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {
  CheckCircle2,
  Clock,
  Database,
  Eye,
  EyeOff,
  KeyRound,
  Lock,
  ShieldCheck,
  UserCog,
} from "lucide-react";
import { Alert, SimulationBanner, StatusPill } from "../components/Primitives";
import { getApiErrorMessage } from "../api/client";
import { useAuth } from "../context/useAuth";
import { useHealth } from "../hooks/useSystem";

export function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, sessionNotice, clearSessionNotice } = useAuth();
  const health = useHealth();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const redirectTo =
    (location.state as { from?: { pathname?: string } } | null)?.from?.pathname || "/";

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setErrorMessage(null);
    clearSessionNotice();

    const trimmedUser = username.trim();
    if (trimmedUser.length < 3) {
      setErrorMessage("Username must be at least 3 characters.");
      return;
    }
    if (password.length < 6) {
      setErrorMessage("Password must be at least 6 characters.");
      return;
    }

    setSubmitting(true);
    try {
      await login({ username: trimmedUser, password });
      navigate(redirectTo, { replace: true });
    } catch (err) {
      setErrorMessage(getApiErrorMessage(err));
    } finally {
      setSubmitting(false);
    }
  };

  const fillDemoAccount = (demoUser: string, demoPass: string) => {
    setUsername(demoUser);
    setPassword(demoPass);
    setErrorMessage(null);
  };

  return (
    <div className="auth-shell">
      <SimulationBanner />
      <div className="auth-stage">
        <div className="auth-grid">
          <section className="auth-card surface-card" aria-label="JWT Sign In">
            <div className="auth-card__brand">
              <div className="auth-brand-mark">
                <Database size={22} aria-hidden="true" />
              </div>
              <div>
                <p className="eyebrow">POST-HARVEST DBMS · SECURE ACCESS</p>
                <h1>Sign in to Operations Console</h1>
              </div>
            </div>

            <p className="auth-card__subtitle">
              Authenticate with your assigned role account to obtain a signed HS256 JWT session
              (8-hour shift validity with server-side logout revocation).
            </p>

            <div className="auth-health-bar">
              <span>Backend gateway</span>
              {health.isLoading ? (
                <StatusPill label="Checking" status="unknown" />
              ) : health.isError ? (
                <StatusPill label="Unavailable" status="unhealthy" />
              ) : (
                <StatusPill
                  label={`${health.data?.status ?? "Unknown"} · MySQL & MongoDB`}
                  status={health.data?.status ?? "unknown"}
                />
              )}
            </div>

            {sessionNotice ? (
              <div className="auth-alert-wrap">
                <Alert title="Session status" variant="info">
                  {sessionNotice}
                </Alert>
              </div>
            ) : null}

            {errorMessage ? (
              <div className="auth-alert-wrap">
                <Alert title="Authentication failed" variant="error">
                  {errorMessage}
                </Alert>
              </div>
            ) : null}

            <form className="auth-form" onSubmit={handleSubmit} noValidate>
              <label className="field">
                <span>Username</span>
                <input
                  autoComplete="username"
                  autoFocus
                  id="login-username"
                  name="username"
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="Enter username (e.g. admin or operator)"
                  required
                  type="text"
                  value={username}
                />
              </label>

              <label className="field">
                <span>Password</span>
                <div className="password-input-wrap">
                  <input
                    autoComplete="current-password"
                    id="login-password"
                    name="password"
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter password"
                    required
                    type={showPassword ? "text" : "password"}
                    value={password}
                  />
                  <button
                    aria-label={showPassword ? "Hide password" : "Show password"}
                    className="icon-button password-toggle"
                    onClick={() => setShowPassword((prev) => !prev)}
                    type="button"
                  >
                    {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                </div>
              </label>

              <button
                className="button button--primary auth-submit"
                disabled={submitting}
                type="submit"
              >
                <KeyRound size={16} />
                {submitting ? "Signing in…" : "Sign in with JWT"}
              </button>
            </form>

            <div className="auth-security-meta">
              <span>
                <Clock size={13} aria-hidden="true" /> 8-hour JWT TTL
              </span>
              <span>
                <Lock size={13} aria-hidden="true" /> PBKDF2-SHA256
              </span>
              <span>
                <ShieldCheck size={13} aria-hidden="true" /> Server-side logout revocation
              </span>
            </div>
          </section>

          <aside className="auth-roles-card surface-card" aria-label="Role differentiation accounts">
            <p className="eyebrow">SIMULATED RBAC DEMO ACCOUNTS</p>
            <h2>Role Differentiation Guide</h2>
            <p className="auth-roles-card__intro">
              Select a role below to test server-enforced RBAC across the dashboard and FastAPI
              endpoints. All actions are recorded in the security audit log.
            </p>

            <div className="demo-role-list">
              <article className="demo-role-box demo-role-box--admin">
                <div className="demo-role-box__header">
                  <div>
                    <span className="role-badge role-badge--admin">
                      <ShieldCheck size={12} /> ADMIN
                    </span>
                    <h3>Packhouse System Admin</h3>
                  </div>
                  <button
                    className="button button--secondary demo-fill-btn"
                    onClick={() => fillDemoAccount("admin", "Admin@1234")}
                    type="button"
                  >
                    Fill Admin
                  </button>
                </div>
                <p className="demo-role-creds">
                  Username: <code>admin</code> · Password: <code>Admin@1234</code>
                </p>
                <ul className="demo-role-perms">
                  <li>
                    <CheckCircle2 size={13} /> Full Overview &amp; operational monitoring
                  </li>
                  <li>
                    <CheckCircle2 size={13} /> Generate, clear-before-generate &amp; purge datasets
                  </li>
                  <li>
                    <CheckCircle2 size={13} /> Access Security &amp; Audit Logs (<code>/security</code>)
                  </li>
                </ul>
              </article>

              <article className="demo-role-box demo-role-box--operator">
                <div className="demo-role-box__header">
                  <div>
                    <span className="role-badge role-badge--operator">
                      <UserCog size={12} /> OPERATOR
                    </span>
                    <h3>Robotics Line Operator</h3>
                  </div>
                  <button
                    className="button button--secondary demo-fill-btn"
                    onClick={() => fillDemoAccount("operator", "Operator@1234")}
                    type="button"
                  >
                    Fill Operator
                  </button>
                </div>
                <p className="demo-role-creds">
                  Username: <code>operator</code> · Password: <code>Operator@1234</code>
                </p>
                <ul className="demo-role-perms">
                  <li>
                    <CheckCircle2 size={13} /> View Overview &amp; operational monitoring
                  </li>
                  <li>
                    <CheckCircle2 size={13} /> Trigger non-destructive dataset generation
                  </li>
                  <li className="demo-role-perms--restricted">
                    <Lock size={13} /> Restricted (HTTP 403): Data purge/reset &amp; Admin audit logs
                  </li>
                </ul>
              </article>
            </div>
          </aside>
        </div>
      </div>
    </div>
  );
}
