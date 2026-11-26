import { useState, type ReactNode } from "react";
import {
  Activity,
  BarChart3,
  Boxes,
  CalendarDays,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  CircleHelp,
  ClipboardList,
  Cpu,
  Download,
  Eye,
  Filter,
  GitBranch,
  Info,
  Radio,
  RefreshCw,
  Search,
  ShieldAlert,
  SlidersHorizontal,
  Sprout,
  X,
} from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { EmptyState, PageHeader, StatusPill } from "../components/Primitives";
import { SimulationControls } from "../components/SimulationControls";

type ModuleKey =
  | "sessions"
  | "tasks"
  | "detections"
  | "operations"
  | "decisions"
  | "events"
  | "analytics"
  | "registry";

interface PageMeta {
  title: string;
  description: string;
  endpoint: string;
  icon: typeof Activity;
}

const pageMeta: Record<ModuleKey, PageMeta> = {
  sessions: {
    title: "Sessions explorer",
    description: "Inspect operational sessions, environments, and lifecycle status.",
    endpoint: "GET /api/v1/sessions",
    icon: Radio,
  },
  tasks: {
    title: "Task management",
    description: "Track task queues, priorities, and execution lifecycles.",
    endpoint: "GET /api/v1/tasks",
    icon: ClipboardList,
  },
  detections: {
    title: "Vision & detections",
    description: "Inspect spatial observations and their inference metadata.",
    endpoint: "GET /api/v1/detections",
    icon: Eye,
  },
  operations: {
    title: "Operations & actuation",
    description: "Review operation execution, outcomes, and duration analysis.",
    endpoint: "GET /api/v1/operations",
    icon: GitBranch,
  },
  decisions: {
    title: "Operational decisions",
    description: "Review action selection and the rationale behind each decision.",
    endpoint: "GET /api/v1/decisions",
    icon: Sprout,
  },
  events: {
    title: "System events & diagnostics",
    description: "Monitor event severity, device context, and resolution progress.",
    endpoint: "GET /api/v1/system-events",
    icon: ShieldAlert,
  },
  analytics: {
    title: "Analytics & reporting",
    description: "Explore simulated produce classifications and operation performance.",
    endpoint:
      "GET /api/v1/analytics/produce-classes · /operation-outcomes · /overview",
    icon: BarChart3,
  },
  registry: {
    title: "Equipment & model registry",
    description: "Inspect registered handling devices and AI model versions.",
    endpoint: "GET /api/v1/devices · GET /api/v1/models",
    icon: Cpu,
  },
};

const columns: Record<ModuleKey, string[]> = {
  sessions: [
    "Session ID",
    "Environment",
    "Start time",
    "End time",
    "Duration",
    "Status",
    "Notes",
  ],
  tasks: [
    "Task ID",
    "Type",
    "Target",
    "Priority",
    "Created",
    "Started",
    "Completed",
    "Session",
  ],
  detections: [
    "Detection ID",
    "Observed",
    "Class",
    "Confidence",
    "Bounding box",
    "Frame reference",
    "Model",
    "Device",
  ],
  operations: [
    "Operation ID",
    "Task",
    "Device",
    "Operation type",
    "Started",
    "Ended",
    "Duration",
    "Outcome",
    "Result",
  ],
  decisions: [
    "Decision ID",
    "Decision time",
    "Type",
    "Selected action",
    "Rationale",
    "Input reference",
    "Session",
    "Task",
  ],
  events: [
    "Event ID",
    "Event time",
    "Severity",
    "Description",
    "Device",
    "Operation",
    "Resolution",
    "Action",
  ],
  analytics: [],
  registry: [],
};

interface FilterOption {
  label: string;
  options: string[];
  hint?: string;
}

function UnavailableNotice({ endpoint }: { endpoint: string }) {
  return (
    <div className="api-unavailable" role="status">
      <span className="api-unavailable__icon">
        <Info size={16} aria-hidden="true" />
      </span>
      <span>
        <strong>Data endpoint not available</strong>
        <span>
          This page is ready for integration. The current backend does not
          implement <code>{endpoint}</code>; no operational records are shown.
        </span>
      </span>
      <StatusPill label="API unavailable" status="degraded" />
    </div>
  );
}

function FilterSelect({
  label,
  options,
  hint,
}: FilterOption) {
  return (
    <label className="data-filter">
      <span>{label}</span>
      <span className="data-filter__select">
        <select defaultValue="" aria-label={label} disabled>
          <option value="">All {label.toLowerCase()}</option>
          {options.map((option) => (
            <option key={option} value={option}>
              {option.replace(/_/g, " ")}
            </option>
          ))}
        </select>
        <ChevronDown size={14} aria-hidden="true" />
      </span>
      {hint ? <small>{hint}</small> : null}
    </label>
  );
}

function FilterSearch({ label = "Search records" }: { label?: string }) {
  return (
    <label className="data-filter data-filter--search">
      <span>{label}</span>
      <span className="data-filter__search">
        <Search size={15} aria-hidden="true" />
        <input aria-label={label} disabled placeholder="API unavailable" type="search" />
      </span>
    </label>
  );
}

function FilterBar({
  children,
  countLabel = "No records",
}: {
  children: ReactNode;
  countLabel?: string;
}) {
  return (
    <section className="filter-bar" aria-label="Page filters">
      <div className="filter-bar__fields">{children}</div>
      <div className="filter-bar__footer">
        <span>
          <Filter size={14} aria-hidden="true" />
          {countLabel}
        </span>
        <button className="button button--text" disabled type="button">
          Clear filters
        </button>
      </div>
    </section>
  );
}

function TableCard({
  module,
  columnLabels,
  title = "Records",
  description = "Operational records returned by the backend.",
  children,
  onRefresh,
  refreshing = false,
  emptyTitle = "No records available",
  emptyMessage = "When the API is connected, matching records will appear here.",
}: {
  module: ModuleKey;
  columnLabels?: string[];
  title?: string;
  description?: string;
  children?: ReactNode;
  onRefresh?: () => void;
  refreshing?: boolean;
  emptyTitle?: string;
  emptyMessage?: string;
}) {
  const pageColumns = columnLabels ?? columns[module];
  return (
    <section className="surface-card data-table-card">
      <div className="data-table-heading">
        <div>
          <h2>{title}</h2>
          <p>{description}</p>
        </div>
        <div className="data-table-heading__actions">
          <span className="record-count">Awaiting API</span>
          {onRefresh ? (
            <button
              aria-label="Refresh records"
              className="icon-button"
              disabled={refreshing}
              onClick={onRefresh}
              title="Refresh"
              type="button"
            >
              <RefreshCw className={refreshing ? "spin" : ""} size={16} />
            </button>
          ) : null}
        </div>
      </div>
      <div className="table-scroll">
        <table className="data-table">
          <thead>
            <tr>
              {pageColumns.map((column) => (
                <th key={column} scope="col">{column}</th>
              ))}
            </tr>
          </thead>
          <tbody>{children}</tbody>
        </table>
        <div className="table-empty">
          <EmptyState title={emptyTitle}>{emptyMessage}</EmptyState>
        </div>
      </div>
      <div className="pagination">
        <span>No records loaded</span>
        <div>
          <label>
            Rows per page
            <select aria-label="Rows per page" defaultValue="25" disabled>
              <option value="10">10</option>
              <option value="25">25</option>
              <option value="50">50</option>
            </select>
          </label>
          <button aria-label="Previous page" className="icon-button" disabled type="button">
            <ChevronLeft size={16} />
          </button>
          <span className="pagination__page">—</span>
          <button aria-label="Next page" className="icon-button" disabled type="button">
            <ChevronRight size={16} />
          </button>
        </div>
      </div>
    </section>
  );
}

function ChartPanel({
  title,
  subtitle,
  children,
  className = "",
}: {
  title: string;
  subtitle: string;
  children: ReactNode;
  className?: string;
}) {
  return (
    <section className={`surface-card chart-panel ${className}`}>
      <div className="chart-panel__heading">
        <div>
          <h2>{title}</h2>
          <p>{subtitle}</p>
        </div>
        <button
          aria-label={`About ${title}`}
          className="icon-button chart-info"
          title="Chart values will appear when the API is available."
          type="button"
        >
          <CircleHelp size={16} />
        </button>
      </div>
      <div className="chart-panel__canvas">{children}</div>
      <div className="chart-empty">
        <BarChart3 size={18} aria-hidden="true" />
        <span>Waiting for analytics API data</span>
      </div>
    </section>
  );
}

function ChartFrame({ type }: { type: "bar" | "line" | "donut" }) {
  const emptyData: Array<Record<string, string | number>> = [];
  if (type === "donut") {
    return (
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie data={emptyData} dataKey="count" nameKey="name" outerRadius="75%" />
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    );
  }
  if (type === "line") {
    return (
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={emptyData}>
          <CartesianGrid stroke="#edf1f3" strokeDasharray="3 3" />
          <XAxis dataKey="batch" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line dataKey="success_rate" name="Success rate" stroke="#0f8b83" />
        </LineChart>
      </ResponsiveContainer>
    );
  }
  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={emptyData}>
        <CartesianGrid stroke="#edf1f3" strokeDasharray="3 3" />
        <XAxis dataKey="category" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="count" name="Records" fill="#168c83" />
      </BarChart>
    </ResponsiveContainer>
  );
}

function DetailSurface({
  title,
  subtitle,
  onClose,
  children,
  mode = "drawer",
}: {
  title: string;
  subtitle: string;
  onClose: () => void;
  children: ReactNode;
  mode?: "drawer" | "modal";
}) {
  return (
    <div className={`detail-overlay detail-overlay--${mode}`} onMouseDown={onClose}>
      <section
        aria-label={title}
        aria-modal="true"
        className={`detail-surface detail-surface--${mode}`}
        onMouseDown={(event) => event.stopPropagation()}
        role="dialog"
      >
        <header className="detail-surface__header">
          <div>
            <p className="eyebrow">RECORD INSPECTOR</p>
            <h2>{title}</h2>
            <p>{subtitle}</p>
          </div>
          <button aria-label="Close details" className="icon-button" onClick={onClose} type="button">
            <X size={18} />
          </button>
        </header>
        <div className="detail-surface__body">{children}</div>
      </section>
    </div>
  );
}

function EmptyDetail({ message }: { message: string }) {
  return (
    <div className="detail-empty">
      <span><Info size={19} /></span>
      <strong>No record selected</strong>
      <p>{message}</p>
    </div>
  );
}

function ModuleHeader({
  module,
  actions,
}: {
  module: ModuleKey;
  actions?: ReactNode;
}) {
  const { title, description } = pageMeta[module];
  return <PageHeader description={description} title={title} actions={actions} />;
}

function SessionsPage() {
  const [detailOpen, setDetailOpen] = useState(false);
  return (
    <>
      <ModuleHeader
        actions={
          <>
            <button className="button button--secondary" disabled title="Session list API is not implemented." type="button">
              <RefreshCw size={15} /> Refresh
            </button>
            <button className="button button--secondary" type="button" onClick={() => setDetailOpen(true)}>
              <Radio size={16} /> Session details
            </button>
          </>
        }
        module="sessions"
      />
      <UnavailableNotice endpoint={pageMeta.sessions.endpoint} />
      <FilterBar>
        <FilterSelect label="Status" options={["INITIALIZING", "ACTIVE", "COMPLETED", "ABORTED"]} />
        <label className="data-filter">
          <span>Environment</span>
          <span className="data-filter__search"><Search size={15} /><input disabled placeholder="API unavailable" type="search" /></span>
        </label>
        <label className="data-filter">
          <span>Date from</span>
          <span className="data-filter__search"><CalendarDays size={15} /><input aria-label="Date from" disabled type="date" /></span>
          <small>Date filtering is not supported by the current list API.</small>
        </label>
        <label className="data-filter">
          <span>Date to</span>
          <span className="data-filter__search"><CalendarDays size={15} /><input aria-label="Date to" disabled type="date" /></span>
        </label>
      </FilterBar>
      <TableCard
        description="Session lifecycle records and environment details."
        emptyMessage="Session rows and detail actions will be available when the sessions API is implemented."
        module="sessions"
        title="All sessions"
      />
      {detailOpen ? (
        <DetailSurface
          onClose={() => setDetailOpen(false)}
          subtitle="Session summary, linked work, and aggregate metrics."
          title="Session details"
        >
          <UnavailableNotice endpoint="GET /api/v1/sessions/{session_id}" />
          <EmptyDetail message="Select a session from the table after session records are available." />
          <div className="detail-metric-grid">
            {["Tasks", "Operations", "Decisions"].map((item) => (
              <div key={item}><span>{item}</span><strong>—</strong></div>
            ))}
          </div>
        </DetailSurface>
      ) : null}
    </>
  );
}

function TasksPage() {
  const [view, setView] = useState<"list" | "board">("list");
  const [detailOpen, setDetailOpen] = useState(false);
  return (
    <>
      <ModuleHeader
        actions={
          <>
            <button className="button button--secondary" onClick={() => setDetailOpen(true)} type="button">
              <ClipboardList size={15} /> Task details
            </button>
            <div className="segmented-control" aria-label="Task view">
              <button aria-pressed={view === "list"} className={view === "list" ? "selected" : ""} onClick={() => setView("list")} type="button">
                <ClipboardList size={15} /> List
              </button>
              <button aria-pressed={view === "board"} className={view === "board" ? "selected" : ""} onClick={() => setView("board")} type="button">
                <Boxes size={15} /> Board
              </button>
            </div>
          </>
        }
        module="tasks"
      />
      <UnavailableNotice endpoint={pageMeta.tasks.endpoint} />
      <FilterBar>
        <FilterSelect label="Task status" options={["PENDING", "IN_PROGRESS", "COMPLETED", "FAILED"]} />
        <FilterSelect label="Priority" options={["LOW", "MEDIUM", "HIGH", "CRITICAL"]} />
        <FilterSelect label="Task type" options={["INSPECTION", "SORTING"]} />
        <FilterSearch label="Search task or session" />
      </FilterBar>
      <div className="priority-scale" aria-label="Task priority indicator key">
        <strong>Priority</strong>
        <span className="priority-pill priority-pill--low">Low</span>
        <span className="priority-pill priority-pill--medium">Medium</span>
        <span className="priority-pill priority-pill--high">High</span>
        <span className="priority-pill priority-pill--critical">Critical</span>
      </div>
      {view === "list" ? (
        <TableCard
          description="Prioritized work items with lifecycle timestamps."
          emptyMessage="Tasks will appear here when the task listing endpoint is available."
          module="tasks"
          title="Task queue"
        />
      ) : (
        <section className="task-board" aria-label="Tasks by status">
          {["PENDING", "IN_PROGRESS", "COMPLETED", "FAILED"].map((status) => (
            <div className="task-lane" key={status}>
              <header><span>{status.replace("_", " ")}</span><span className="lane-count">—</span></header>
              <div className="task-lane__empty">
                <ClipboardList size={18} />
                <span>Tasks will appear when the API is available.</span>
              </div>
            </div>
          ))}
        </section>
      )}
      <section className="surface-card timeline-card">
        <div className="data-table-heading">
          <div><h2>Task timeline</h2><p>Creation, start, and completion checkpoints.</p></div>
          <StatusPill label="Awaiting task data" status="degraded" />
        </div>
        <div className="timeline-empty">
          <span className="timeline-track" aria-hidden="true"><i /><i /><i /></span>
          <span>Task lifecycle milestones will be plotted from API timestamps.</span>
        </div>
      </section>
      {detailOpen ? (
        <DetailSurface
          onClose={() => setDetailOpen(false)}
          subtitle="Task target, priority, lifecycle, and related operation history."
          title="Task details"
        >
          <UnavailableNotice endpoint="GET /api/v1/tasks/{task_id}" />
          <EmptyDetail message="Select a task after task records become available to inspect its details." />
          <div className="audit-block">
            <span>Task lifecycle</span>
            <p>Creation, start, and end timestamps will be shown here.</p>
            <span>Related records</span>
            <p>Linked operations and decisions require the task detail response.</p>
          </div>
        </DetailSurface>
      ) : null}
    </>
  );
}

function DetectionsPage() {
  const [previewOpen, setPreviewOpen] = useState(false);
  return (
    <>
      <ModuleHeader
        actions={
          <button className="button button--secondary" onClick={() => setPreviewOpen(true)} type="button">
            <Eye size={16} /> Spatial preview
          </button>
        }
        module="detections"
      />
      <div className="tracking-notice">
        <Info size={16} aria-hidden="true" />
        Detections represent individual spatial observations. Inter-frame object tracking is not supported.
      </div>
      <UnavailableNotice endpoint={pageMeta.detections.endpoint} />
      <FilterBar>
        <FilterSelect label="Class label" options={["GRADE_A", "GRADE_B", "BLEMISHED", "FOREIGN_OBJECT"]} />
        <label className="data-filter confidence-filter">
          <span>Minimum confidence <strong>—</strong></span>
          <input aria-label="Minimum confidence" disabled max="1" min="0" step="0.05" type="range" value="0" />
          <span className="range-hints"><span>0.00</span><span>1.00</span></span>
        </label>
        <FilterSearch label="Session ID" />
      </FilterBar>
      <div className="detection-layout">
        <TableCard
          description="Confidence and normalized bounding-box values per observation."
          emptyMessage="Detection records will populate this grid when the detections API is implemented."
          module="detections"
          title="Detection observations"
        />
        <section className="surface-card spatial-card">
          <div className="data-table-heading">
            <div><h2>Spatial preview</h2><p>Normalized box coordinates</p></div>
            <span className="section-icon"><Eye size={17} /></span>
          </div>
          <div className="spatial-stage" aria-label="Empty bounding box preview">
            <div className="spatial-grid" />
            <div className="spatial-empty">
              <Eye size={20} />
              <strong>No observation selected</strong>
              <span>Bounding boxes require a detection response.</span>
            </div>
            <span className="spatial-axis spatial-axis--x">x 0—1</span>
            <span className="spatial-axis spatial-axis--y">y 0—1</span>
          </div>
          <div className="confidence-legend">
            <span><i className="legend-dot legend-dot--high" /> High ≥ 0.80</span>
            <span><i className="legend-dot legend-dot--medium" /> Medium 0.60–0.79</span>
            <span><i className="legend-dot legend-dot--low" /> Low &lt; 0.60</span>
          </div>
          <div className="confidence-meter">
            <span>Selected observation confidence</span>
            <strong>—</strong>
            <div><i /></div>
            <small>Confidence score will be shown after selecting a detection.</small>
          </div>
        </section>
      </div>
      {previewOpen ? (
        <DetailSurface mode="modal" onClose={() => setPreviewOpen(false)} subtitle="Bounding boxes are rendered only from returned normalized coordinates." title="Detection spatial preview">
          <EmptyDetail message="No detection record is available to visualize yet." />
        </DetailSurface>
      ) : null}
    </>
  );
}

function OperationsPage() {
  return (
    <>
      <ModuleHeader module="operations" />
      <UnavailableNotice endpoint={pageMeta.operations.endpoint} />
      <FilterBar>
        <FilterSelect label="Operation type" options={["GRASP", "LIFT", "TRANSPORT", "RELEASE"]} />
        <FilterSelect label="Outcome" options={["SUCCESS", "FAILURE", "TIMEOUT"]} />
        <FilterSearch label="Execution device" />
        <FilterSearch label="Task ID" />
      </FilterBar>
      <ChartPanel className="operation-chart" subtitle="Duration per operation from start and end timestamps." title="Operation duration distribution">
        <ChartFrame type="bar" />
      </ChartPanel>
      <TableCard
        description="Execution steps, device associations, elapsed time, and result."
        emptyMessage="Operation records will appear when the operations endpoint is implemented."
        module="operations"
        title="Operation records"
      />
    </>
  );
}

function DecisionsPage() {
  const [auditOpen, setAuditOpen] = useState(false);
  return (
    <>
      <ModuleHeader
        actions={
          <button className="button button--secondary" onClick={() => setAuditOpen(true)} type="button">
            <SlidersHorizontal size={16} /> Audit detail
          </button>
        }
        module="decisions"
      />
      <UnavailableNotice endpoint={pageMeta.decisions.endpoint} />
      <FilterBar>
        <FilterSelect label="Decision type" options={["GRADING", "SORT_ROUTE"]} />
        <FilterSearch label="Search selected action" />
        <FilterSearch label="Session or task ID" />
      </FilterBar>
      <TableCard
        description="Decision record, rationale, and source references."
        emptyMessage="Decision records will be available when the decisions endpoint is implemented."
        module="decisions"
        title="Decision audit log"
      />
      {auditOpen ? (
        <DetailSurface mode="modal" onClose={() => setAuditOpen(false)} subtitle="Inspect the selected action and its input context." title="Decision audit detail">
          <UnavailableNotice endpoint={pageMeta.decisions.endpoint} />
          <EmptyDetail message="Select a decision row once records are available to review its rationale and input reference." />
          <div className="audit-block">
            <span>Rationale</span><p>No decision selected.</p>
            <span>Input reference</span><p>No decision selected.</p>
          </div>
        </DetailSurface>
      ) : null}
    </>
  );
}

function EventsPage() {
  return (
    <>
      <ModuleHeader
        actions={
          <button className="button button--secondary" disabled title="Resolve action requires the system-events PATCH API." type="button">
            Resolve selected
          </button>
        }
        module="events"
      />
      <UnavailableNotice endpoint={pageMeta.events.endpoint} />
      <div className="severity-legend">
        <strong>Severity key</strong>
        <span className="severity-pill severity-pill--info"><i /> Info</span>
        <StatusPill label="Warning" status="degraded" />
        <span className="severity-pill severity-pill--error"><i /> Error</span>
        <span className="severity-pill severity-pill--critical"><i /> Critical fault</span>
      </div>
      <FilterBar>
        <FilterSelect label="Event type" options={["INFO", "WARNING", "ERROR", "CRITICAL_FAULT"]} />
        <FilterSelect label="Resolution" options={["OPEN", "ACKNOWLEDGED", "RESOLVED"]} />
        <FilterSearch label="Device ID" />
      </FilterBar>
      <TableCard
        description="Structured event history and resolution workflow."
        emptyMessage="System events will appear when the events API is implemented. Resolve actions require its PATCH endpoint."
        module="events"
        title="Event log"
      />
    </>
  );
}

function AnalyticsPage() {
  return (
    <>
      <ModuleHeader
        actions={
          <button className="button button--secondary" disabled title="CSV export is pending approval and a supporting API." type="button">
            <Download size={16} /> Export CSV · Pending approval
          </button>
        }
        module="analytics"
      />
      <UnavailableNotice endpoint={pageMeta.analytics.endpoint} />
      <div className="analytics-summary">
        <div><span>Produce classes</span><strong>—</strong><small>Waiting for classification distribution</small></div>
        <div><span>Operation success rate</span><strong>—</strong><small>Waiting for operation outcome data</small></div>
        <div><span>Average cycle time</span><strong>—</strong><small>Waiting for operation timestamps</small></div>
      </div>
      <div className="analytics-grid">
        <ChartPanel subtitle="Counts by returned produce class." title="Produce quality distribution">
          <ChartFrame type="bar" />
        </ChartPanel>
        <ChartPanel subtitle="Outcome ratios grouped by operation type." title="Operation outcome mix">
          <ChartFrame type="donut" />
        </ChartPanel>
        <ChartPanel className="analytics-grid__wide" subtitle="Success ratio by available simulation batch." title="Operation success rate">
          <ChartFrame type="line" />
        </ChartPanel>
        <ChartPanel subtitle="Elapsed operation time by category." title="Cycle time analysis">
          <ChartFrame type="bar" />
        </ChartPanel>
      </div>
      <div className="export-note"><Info size={15} /> CSV export remains disabled pending project approval.</div>
    </>
  );
}

function RegistryPage() {
  return (
    <>
      <ModuleHeader module="registry" />
      <UnavailableNotice endpoint={pageMeta.registry.endpoint} />
      <FilterBar>
        <FilterSelect label="Device type" options={[]} />
        <FilterSelect label="Device status" options={["ONLINE", "OFFLINE", "CALIBRATING", "FAULT"]} />
        <FilterSearch label="Search devices or models" />
      </FilterBar>
      <div className="registry-grid">
        <TableCard
          description="Registered handling devices and cameras."
          emptyMessage="Device inventory will load from GET /api/v1/devices when implemented."
          module="registry"
          columnLabels={["Device ID", "Name", "Type", "Status", "Description"]}
          title="Device inventory"
        />
        <TableCard
          description="Registered model versions and configuration."
          emptyMessage="AI models will load from GET /api/v1/models when implemented."
          module="registry"
          columnLabels={["Model ID", "Name", "Version", "Configuration", "Created"]}
          title="AI model catalog"
        />
      </div>
    </>
  );
}

export function OperationalPage({ module }: { module: ModuleKey }) {
  const [controlsOpen, setControlsOpen] = useState(false);
  let page: ReactNode = null;

  switch (module) {
    case "sessions":
      page = <SessionsPage />;
      break;
    case "tasks":
      page = <TasksPage />;
      break;
    case "detections":
      page = <DetectionsPage />;
      break;
    case "operations":
      page = <OperationsPage />;
      break;
    case "decisions":
      page = <DecisionsPage />;
      break;
    case "events":
      page = <EventsPage />;
      break;
    case "analytics":
      page = <AnalyticsPage />;
      break;
    case "registry":
      page = <RegistryPage />;
      break;
  }

  return (
    <div className="operational-page">
      <div className="page-controls">
        {page}
        <button
          aria-label="Open simulation controls"
          className="simulation-fab"
          onClick={() => setControlsOpen(true)}
          title="Simulation controls"
          type="button"
        >
          <Activity size={17} />
        </button>
      </div>
      <SimulationControls onClose={() => setControlsOpen(false)} open={controlsOpen} />
    </div>
  );
}
