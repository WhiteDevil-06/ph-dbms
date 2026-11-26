import { useState } from "react";
import {
  Activity,
  BarChart3,
  Boxes,
  ClipboardList,
  Cpu,
  Database,
  Eye,
  GitBranch,
  Lock,
  LogOut,
  Menu,
  Radio,
  ShieldAlert,
  ShieldCheck,
  Sprout,
  UserCog,
  X,
} from "lucide-react";
import { Link, NavLink, Outlet, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/useAuth";
import { useHealth } from "../hooks/useSystem";
import { SimulationBanner, StatusPill } from "../components/Primitives";

const navigation = [
  { label: "Overview", path: "/", icon: Activity },
  { label: "Sessions", path: "/sessions", icon: Radio },
  { label: "Tasks", path: "/tasks", icon: ClipboardList },
  { label: "Detections", path: "/detections", icon: Eye },
  { label: "Operations", path: "/operations", icon: GitBranch },
  { label: "Decisions", path: "/decisions", icon: Sprout },
  { label: "System events", path: "/events", icon: ShieldAlert },
  { label: "Analytics", path: "/analytics", icon: BarChart3 },
  { label: "Equipment & models", path: "/registry", icon: Cpu },
  { label: "Security & access", path: "/security", icon: ShieldCheck, adminBadge: true },
];

const pageTitles: Record<string, string> = {
  "/": "Overview",
  "/sessions": "Sessions",
  "/tasks": "Tasks",
  "/detections": "Detections",
  "/operations": "Operations",
  "/decisions": "Decisions",
  "/events": "System events",
  "/analytics": "Analytics",
  "/registry": "Equipment & models",
  "/security": "Security & access",
  "/simulation": "Simulation controls",
};

export function DashboardLayout() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [loggingOut, setLoggingOut] = useState(false);
  const health = useHealth();
  const { user, isAdmin, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const currentTitle = pageTitles[location.pathname] ?? "Overview";
  const healthStatus = health.data?.status;

  const initials = (user?.full_name ?? user?.username ?? "U")
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  const handleLogout = async () => {
    setLoggingOut(true);
    try {
      await logout();
      navigate("/login", { replace: true });
    } finally {
      setLoggingOut(false);
    }
  };

  return (
    <div className="app-shell">
      <aside className={`sidebar ${mobileOpen ? "sidebar--open" : ""}`}>
        <div className="brand">
          <div className="brand__mark">
            <Database size={20} aria-hidden="true" />
          </div>
          <div>
            <strong>
              PH<span>·</span>DBMS
            </strong>
            <small>Operations console</small>
          </div>
          <button
            aria-label="Close navigation"
            className="icon-button sidebar__close"
            onClick={() => setMobileOpen(false)}
            type="button"
          >
            <X size={18} />
          </button>
        </div>
        <p className="sidebar__section-label">WORKSPACE</p>
        <nav aria-label="Main navigation" className="navigation">
          {navigation.map(({ label, path, icon: Icon, adminBadge }) => (
            <NavLink
              end={path === "/"}
              key={path}
              onClick={() => setMobileOpen(false)}
              to={path}
            >
              <Icon size={17} aria-hidden="true" />
              <span>{label}</span>
              {adminBadge ? (
                <span
                  className={`nav-role-tag ${isAdmin ? "nav-role-tag--admin" : "nav-role-tag--locked"}`}
                  title={isAdmin ? "Admin governance view" : "Admin-only audit; opens RBAC notice"}
                >
                  {isAdmin ? "Admin" : <Lock size={11} aria-hidden="true" />}
                </span>
              ) : null}
            </NavLink>
          ))}
        </nav>
        <div className="sidebar__footer">
          <div className="sidebar__footer-icon">
            <Boxes size={17} aria-hidden="true" />
          </div>
          <div>
            <strong>Data environment</strong>
            <span>Deterministic simulator</span>
          </div>
          <span className="sidebar__environment-dot" aria-hidden="true" />
        </div>
      </aside>
      {mobileOpen ? (
        <button
          aria-label="Close navigation overlay"
          className="sidebar-backdrop"
          onClick={() => setMobileOpen(false)}
          type="button"
        />
      ) : null}

      <div className="main-frame">
        <SimulationBanner />
        <header className="topbar">
          <div className="topbar__left">
            <button
              aria-label="Open navigation"
              className="icon-button menu-button"
              onClick={() => setMobileOpen(true)}
              type="button"
            >
              <Menu size={20} />
            </button>
            <div className="breadcrumbs">
              <Link to="/">Workspace</Link>
              <span>/</span>
              <strong>{currentTitle}</strong>
            </div>
          </div>
          <div className="topbar__right">
            <span className="backend-label">API status</span>
            {health.isLoading ? (
              <StatusPill label="Checking" status="unknown" />
            ) : health.isError ? (
              <StatusPill label="Unavailable" status="unhealthy" />
            ) : (
              <StatusPill label={healthStatus ?? "Unknown"} status={healthStatus ?? "unknown"} />
            )}
            <span className="topbar__divider" />
            <div className="user-chip" aria-label="Signed-in account">
              <span
                className={`user-chip__avatar ${isAdmin ? "user-chip__avatar--admin" : "user-chip__avatar--operator"}`}
              >
                {initials}
              </span>
              <div className="user-chip__meta">
                <span className="user-chip__name">{user?.full_name ?? user?.username}</span>
                <span
                  className={`role-badge role-badge--${isAdmin ? "admin" : "operator"}`}
                >
                  {isAdmin ? <ShieldCheck size={11} /> : <UserCog size={11} />}
                  {user?.role}
                </span>
              </div>
            </div>
            <button
              className="button button--secondary logout-button"
              disabled={loggingOut}
              onClick={() => void handleLogout()}
              title="Sign out and revoke active JWT session"
              type="button"
            >
              <LogOut size={14} aria-hidden="true" />
              <span>{loggingOut ? "Signing out…" : "Log out"}</span>
            </button>
          </div>
        </header>
        <main className="main-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
