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
  Menu,
  Radio,
  ShieldAlert,
  Sprout,
  X,
} from "lucide-react";
import { Link, NavLink, Outlet, useLocation } from "react-router-dom";
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
  "/simulation": "Simulation controls",
};

export function DashboardLayout() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const health = useHealth();
  const location = useLocation();
  const currentTitle = pageTitles[location.pathname] ?? "Overview";
  const healthStatus = health.data?.status;

  return (
    <div className="app-shell">
      <aside className={`sidebar ${mobileOpen ? "sidebar--open" : ""}`}>
        <div className="brand">
          <div className="brand__mark">
            <Database size={20} aria-hidden="true" />
          </div>
          <div>
            <strong>PH<span>·</span>DBMS</strong>
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
          {navigation.map(({ label, path, icon: Icon }) => (
            <NavLink
              end={path === "/"}
              key={path}
              onClick={() => setMobileOpen(false)}
              to={path}
            >
              <Icon size={17} aria-hidden="true" />
              <span>{label}</span>
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
            <div className="user-chip" aria-label="Developer workspace">
              <span className="user-chip__avatar">R</span>
              <span className="user-chip__name">Research team</span>
            </div>
          </div>
        </header>
        <main className="main-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
