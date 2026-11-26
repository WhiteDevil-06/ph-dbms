import { useQuery } from "@tanstack/react-query";
import {
  CheckCircle2,
  Clock,
  KeyRound,
  Lock,
  LogOut,
  RefreshCw,
  ShieldAlert,
  ShieldCheck,
  Users,
  XCircle,
} from "lucide-react";
import { getAuditLogs, getPermissionsMatrix, getUsers } from "../api/auth";
import { getApiErrorMessage } from "../api/client";
import { Alert, LoadingState, PageHeader, StatusPill } from "../components/Primitives";
import { useAuth } from "../context/useAuth";

function formatTimestamp(iso: string | null): string {
  if (!iso) return "—";
  try {
    return new Date(iso).toLocaleString();
  } catch {
    return iso;
  }
}

function AuditActionBadge({ action }: { action: string }) {
  const tone =
    action === "LOGIN_SUCCESS"
      ? "good"
      : action === "LOGOUT"
        ? "neutral"
        : action === "ACCESS_DENIED" || action === "RATE_LIMITED"
          ? "bad"
          : "warning";
  return <StatusPill label={action.replace(/_/g, " ")} status={tone === "good" ? "healthy" : tone === "bad" ? "unhealthy" : tone === "warning" ? "degraded" : "unknown"} />;
}

export function SecurityPage() {
  const { user, jti, expiresAt, isAdmin, logout } = useAuth();

  const matrixQuery = useQuery({
    queryKey: ["auth", "permissions-matrix"],
    queryFn: getPermissionsMatrix,
  });

  const usersQuery = useQuery({
    queryKey: ["auth", "users"],
    queryFn: getUsers,
    enabled: isAdmin,
  });

  const auditQuery = useQuery({
    queryKey: ["auth", "audit-logs"],
    queryFn: () => getAuditLogs(50),
    enabled: isAdmin,
  });

  const refreshAll = () => {
    void matrixQuery.refetch();
    if (isAdmin) {
      void usersQuery.refetch();
      void auditQuery.refetch();
    }
  };

  return (
    <>
      <PageHeader
        eyebrow="SECURITY, JWT SESSIONS & RBAC"
        title="Access control & audit trail"
        description="Inspect active JWT session validity, role permission boundaries, and security audit events."
        actions={
          <>
            <button
              className="button button--secondary"
              disabled={matrixQuery.isFetching || usersQuery.isFetching || auditQuery.isFetching}
              onClick={refreshAll}
              type="button"
            >
              <RefreshCw
                size={15}
                className={auditQuery.isFetching || usersQuery.isFetching ? "spin" : ""}
              />
              Refresh
            </button>
            <button
              className="button button--secondary"
              onClick={() => void logout()}
              type="button"
            >
              <LogOut size={15} />
              Sign out &amp; revoke JWT
            </button>
          </>
        }
      />

      <section className="surface-card security-session-card">
        <div className="section-heading">
          <div>
            <p className="eyebrow">ACTIVE JWT SESSION</p>
            <h2>Authenticated principal</h2>
          </div>
          <span className="section-icon">
            <KeyRound size={18} />
          </span>
        </div>
        <div className="security-session-grid">
          <div>
            <span className="data-label">Signed-in user</span>
            <strong className="data-value">
              {user?.full_name} (<code>{user?.username}</code>)
            </strong>
          </div>
          <div>
            <span className="data-label">Assigned role</span>
            <span
              className={`role-badge role-badge--${user?.role === "ADMIN" ? "admin" : "operator"}`}
            >
              {user?.role === "ADMIN" ? <ShieldCheck size={12} /> : <Lock size={12} />}
              {user?.role}
            </span>
          </div>
          <div>
            <span className="data-label">JWT token ID (jti)</span>
            <code className="data-code">{jti ? `${jti.slice(0, 18)}…` : "Verified"}</code>
          </div>
          <div>
            <span className="data-label">Session expires (8h TTL)</span>
            <strong className="data-value security-expiry">
              <Clock size={13} aria-hidden="true" /> {formatTimestamp(expiresAt)}
            </strong>
          </div>
        </div>
      </section>

      {!isAdmin ? (
        <section className="surface-card access-denied-card" role="alert">
          <div className="access-denied-card__icon">
            <ShieldAlert size={28} />
          </div>
          <div>
            <p className="eyebrow">HTTP 403 · RBAC ENFORCEMENT</p>
            <h2>Access Restricted — Administrator Role Required</h2>
            <p>
              You are currently signed in as <strong>{user?.username}</strong> with the{" "}
              <span className="role-badge role-badge--operator">OPERATOR</span> role. User account
              administration (<code>GET /api/v1/auth/users</code>), security audit logs (
              <code>GET /api/v1/auth/audit-logs</code>), and destructive dataset purge operations (
              <code>POST /api/v1/simulation/reset</code>) are restricted to{" "}
              <strong>ADMIN</strong> accounts and enforced server-side.
            </p>
          </div>
        </section>
      ) : null}

      <section className="surface-card security-section">
        <div className="section-heading">
          <div>
            <p className="eyebrow">ROLE DIFFERENTIATION</p>
            <h2>RBAC permission matrix (ADMIN vs OPERATOR)</h2>
          </div>
          <span className="section-icon section-icon--blue">
            <ShieldCheck size={18} />
          </span>
        </div>
        {matrixQuery.isLoading ? (
          <LoadingState label="Loading role permission matrix" />
        ) : matrixQuery.isError ? (
          <Alert title="Permission matrix unavailable">
            {getApiErrorMessage(matrixQuery.error)}
          </Alert>
        ) : (
          <div className="table-scroll">
            <table className="data-table">
              <thead>
                <tr>
                  <th scope="col">Capability</th>
                  <th scope="col">API Endpoint</th>
                  <th scope="col">ADMIN</th>
                  <th scope="col">OPERATOR</th>
                  <th scope="col">Enforcement Notes</th>
                </tr>
              </thead>
              <tbody>
                {matrixQuery.data?.map((row) => (
                  <tr key={row.capability}>
                    <td>
                      <strong>{row.capability}</strong>
                    </td>
                    <td>
                      <code>{row.endpoint}</code>
                    </td>
                    <td>
                      {row.admin_allowed ? (
                        <span className="perm-pill perm-pill--allow">
                          <CheckCircle2 size={13} /> Allowed
                        </span>
                      ) : (
                        <span className="perm-pill perm-pill--deny">
                          <XCircle size={13} /> 403 Denied
                        </span>
                      )}
                    </td>
                    <td>
                      {row.operator_allowed ? (
                        <span className="perm-pill perm-pill--allow">
                          <CheckCircle2 size={13} /> Allowed
                        </span>
                      ) : (
                        <span className="perm-pill perm-pill--deny">
                          <XCircle size={13} /> 403 Denied
                        </span>
                      )}
                    </td>
                    <td>{row.notes}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      {isAdmin ? (
        <div className="security-admin-grid">
          <section className="surface-card security-section">
            <div className="section-heading">
              <div>
                <p className="eyebrow">ADMIN ONLY · GET /API/V1/AUTH/USERS</p>
                <h2>Registered accounts</h2>
              </div>
              <span className="section-icon">
                <Users size={18} />
              </span>
            </div>
            {usersQuery.isLoading ? (
              <LoadingState label="Loading registered users" />
            ) : usersQuery.isError ? (
              <Alert title="Unable to load users">{getApiErrorMessage(usersQuery.error)}</Alert>
            ) : (
              <div className="table-scroll">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th scope="col">User ID</th>
                      <th scope="col">Username</th>
                      <th scope="col">Full name</th>
                      <th scope="col">Role</th>
                      <th scope="col">Permissions</th>
                      <th scope="col">Provenance</th>
                    </tr>
                  </thead>
                  <tbody>
                    {usersQuery.data?.map((account) => (
                      <tr key={account.user_id}>
                        <td>
                          <code>{account.user_id}</code>
                        </td>
                        <td>
                          <strong>{account.username}</strong>
                        </td>
                        <td>{account.full_name}</td>
                        <td>
                          <span
                            className={`role-badge role-badge--${account.role === "ADMIN" ? "admin" : "operator"}`}
                          >
                            {account.role}
                          </span>
                        </td>
                        <td>{account.permissions.length} scopes</td>
                        <td>
                          <code>{account.provenance}</code>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
            <p className="updated-note">
              Passwords are stored as salted PBKDF2-HMAC-SHA256 digests in MySQL and are strictly
              excluded from all API responses.
            </p>
          </section>

          <section className="surface-card security-section">
            <div className="section-heading">
              <div>
                <p className="eyebrow">ADMIN ONLY · GET /API/V1/AUTH/AUDIT-LOGS</p>
                <h2>Security &amp; auth audit log</h2>
              </div>
              <span className="section-icon section-icon--blue">
                <ShieldAlert size={18} />
              </span>
            </div>
            {auditQuery.isLoading ? (
              <LoadingState label="Loading security audit trail" />
            ) : auditQuery.isError ? (
              <Alert title="Unable to load audit log">{getApiErrorMessage(auditQuery.error)}</Alert>
            ) : (
              <div className="table-scroll">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th scope="col">Timestamp</th>
                      <th scope="col">Event</th>
                      <th scope="col">User</th>
                      <th scope="col">Role</th>
                      <th scope="col">Endpoint</th>
                      <th scope="col">Detail</th>
                    </tr>
                  </thead>
                  <tbody>
                    {auditQuery.data?.map((entry) => (
                      <tr key={entry.audit_id}>
                        <td>{formatTimestamp(entry.created_at)}</td>
                        <td>
                          <AuditActionBadge action={entry.action} />
                        </td>
                        <td>
                          <code>{entry.username}</code>
                        </td>
                        <td>{entry.role ?? "—"}</td>
                        <td>
                          <code>{entry.endpoint ?? "—"}</code>
                        </td>
                        <td>{entry.detail ?? "—"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>
        </div>
      ) : null}
    </>
  );
}
