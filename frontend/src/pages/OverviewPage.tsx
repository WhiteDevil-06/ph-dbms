import {
  Activity,
  ArrowUpRight,
  Boxes,
  ClipboardList,
  Database,
  Eye,
  RefreshCw,
  ShieldAlert,
  SlidersHorizontal,
  CircleHelp,
} from "lucide-react";
import { Link } from "react-router-dom";
import {
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import {
  Alert,
  EmptyState,
  LoadingState,
  MetricCard,
  PageHeader,
  StatusPill,
} from "../components/Primitives";
import { SimulationControls } from "../components/SimulationControls";
import { getApiErrorMessage } from "../api/client";
import { useHealth, useSimulationStatus } from "../hooks/useSystem";
import { useState } from "react";

const metrics = [
  { label: "Total sessions", key: "sessions", icon: <Activity size={18} />, tone: "teal" as const },
  { label: "Active tasks", key: null, icon: <ClipboardList size={18} />, tone: "blue" as const },
  { label: "Completed operations", key: null, icon: <Boxes size={18} />, tone: "violet" as const },
  { label: "Open system events", key: null, icon: <ShieldAlert size={18} />, tone: "amber" as const },
  { label: "Avg. detection confidence", key: null, icon: <Eye size={18} />, tone: "blue" as const },
];

export function OverviewPage() {
  const [controlsOpen, setControlsOpen] = useState(false);
  const status = useSimulationStatus();
  const health = useHealth();
  const counts = status.data?.counts;

  return (
    <>
      <PageHeader
        description="A clear view of the current simulation dataset and backend availability."
        title="Operations overview"
        actions={
          <>
            <button
              className="button button--secondary"
              disabled={status.isFetching || health.isFetching}
              onClick={() => {
                void status.refetch();
                void health.refetch();
              }}
              type="button"
            >
              <RefreshCw size={16} className={status.isFetching ? "spin" : ""} />
              Refresh
            </button>
            <button
              className="button button--primary"
              onClick={() => setControlsOpen(true)}
              type="button"
            >
              <SlidersHorizontal size={16} />
              Simulation controls
            </button>
          </>
        }
      />

      {status.isError ? (
        <Alert title="Simulation status unavailable">
          {getApiErrorMessage(status.error)}
        </Alert>
      ) : null}

      <section aria-label="Simulation dataset metrics" className="metrics-grid">
        {metrics.map((metric) => (
          <MetricCard
            footnote={
              metric.key
                ? "Count reported by simulation status"
                : "Requires a backend analytics/read endpoint"
            }
            icon={metric.icon}
            key={metric.label}
            label={metric.label}
            tone={metric.tone}
            value={
              status.isLoading
                ? "—"
                : metric.key
                  ? (counts?.[metric.key as keyof typeof counts] ?? "—")
                  : "—"
            }
          />
        ))}
      </section>

      <div className="overview-grid">
        <section className="surface-card dataset-card">
          <div className="section-heading">
            <div>
              <p className="eyebrow">CURRENT ENVIRONMENT</p>
              <h2>Simulation status</h2>
            </div>
            <span className="section-icon">
              <Database size={18} />
            </span>
          </div>
          {status.isLoading ? (
            <LoadingState label="Reading simulation status" />
          ) : status.isError ? (
            <EmptyState title="Status could not be loaded">
              Check the backend connection and refresh this view.
            </EmptyState>
          ) : status.data ? (
            <>
              <div className="status-summary">
                <div>
                  <span className="data-label">Simulation mode</span>
                  <StatusPill label={status.data.mode} status="healthy" />
                </div>
                <div>
                  <span className="data-label">Active seed</span>
                  <strong className="data-value">{status.data.active_seed}</strong>
                </div>
                <div>
                  <span className="data-label">Backend</span>
                  {health.isLoading ? (
                    <StatusPill label="Checking" status="unknown" />
                  ) : health.isError ? (
                    <StatusPill label="Unavailable" status="unhealthy" />
                  ) : (
                    <StatusPill
                      label={health.data?.status ?? "Unknown"}
                      status={health.data?.status ?? "unknown"}
                    />
                  )}
                </div>
              </div>
              <div className="record-breakdown">
                {Object.entries(status.data.counts).map(([label, value]) => (
                  <div className="record-breakdown__row" key={label}>
                    <span>{label.replace("_", " ")}</span>
                    <strong>{value.toLocaleString()}</strong>
                  </div>
                ))}
              </div>
              <p className="updated-note">
                Status refreshed{" "}
                {status.dataUpdatedAt
                  ? new Date(status.dataUpdatedAt).toLocaleTimeString()
                  : "—"}
              </p>
            </>
          ) : (
            <EmptyState title="No simulation status">
              The backend has not returned a status record.
            </EmptyState>
          )}
        </section>

        <section className="surface-card insight-card">
          <div className="section-heading">
            <div>
              <p className="eyebrow">OPERATIONAL REPORTING</p>
              <h2>Outcomes & recent activity</h2>
            </div>
            <span className="section-icon section-icon--blue">
              <Activity size={18} />
            </span>
          </div>
          <div className="overview-lower-grid">
            <section className="overview-widget">
              <div className="overview-widget__heading">
                <div>
                  <h3>Operation outcomes</h3>
                  <p>Success, failure, and timeout distribution</p>
                </div>
                <CircleHelp size={15} aria-label="Requires operation analytics API" />
              </div>
              <div className="overview-chart">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={[]}
                      dataKey="count"
                      nameKey="name"
                      outerRadius="72%"
                    >
                      <Cell fill="#14877d" />
                      <Cell fill="#d77d55" />
                      <Cell fill="#d7a940" />
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
                <div className="overview-chart__empty">
                  Operation outcomes endpoint unavailable
                </div>
              </div>
              <div className="chart-legend">
                <span><i className="legend-dot legend-dot--success" /> Success</span>
                <span><i className="legend-dot legend-dot--failure" /> Failure</span>
                <span><i className="legend-dot legend-dot--timeout" /> Timeout</span>
              </div>
            </section>
            <section className="overview-widget">
              <div className="overview-widget__heading">
                <div>
                  <h3>Recent activity</h3>
                  <p>Latest tasks and system events</p>
                </div>
                <span className="record-count">Awaiting API</span>
              </div>
              <div className="activity-empty">
                <Activity size={19} />
                <strong>Activity feed unavailable</strong>
                <span>Task and system-event read endpoints are not implemented.</span>
              </div>
              <Link className="text-link" to="/events">
                Open system events <ArrowUpRight size={15} />
              </Link>
            </section>
          </div>
        </section>
      </div>
      <SimulationControls
        onClose={() => setControlsOpen(false)}
        open={controlsOpen}
      />
    </>
  );
}
