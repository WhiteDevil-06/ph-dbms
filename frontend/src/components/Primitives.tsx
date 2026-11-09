import { useEffect, useRef, type KeyboardEvent, type ReactNode } from "react";
import { AlertCircle, CheckCircle2, LoaderCircle, X } from "lucide-react";
import clsx from "clsx";

interface PageHeaderProps {
  eyebrow?: string;
  title: string;
  description: string;
  actions?: ReactNode;
}

export function PageHeader({
  eyebrow = "POST-HARVEST OPERATIONS",
  title,
  description,
  actions,
}: PageHeaderProps) {
  return (
    <div className="page-heading flex items-end justify-between">
      <div>
        <p className="eyebrow">{eyebrow}</p>
        <h1>{title}</h1>
        <p className="page-description">{description}</p>
      </div>
      {actions ? <div className="page-actions">{actions}</div> : null}
    </div>
  );
}

export function SimulationBanner() {
  return (
    <div className="simulation-banner" role="status">
      <span className="simulation-banner__label">
        <span className="banner-dot" aria-hidden="true" />
        SIMULATION DATA ACTIVE
      </span>
      <span>
        All telemetry, tasks, and detections are generated from simulated
        models.
      </span>
    </div>
  );
}

export function Alert({
  title,
  children,
  variant = "error",
}: {
  title: string;
  children: ReactNode;
  variant?: "error" | "success" | "info";
}) {
  const Icon =
    variant === "success"
      ? CheckCircle2
      : variant === "info"
        ? AlertCircle
        : AlertCircle;
  return (
    <div className={`alert alert--${variant}`} role="status">
      <Icon size={18} aria-hidden="true" />
      <div>
        <strong>{title}</strong>
        <div>{children}</div>
      </div>
    </div>
  );
}

export function LoadingState({ label = "Loading data" }: { label?: string }) {
  return (
    <div className="loading-state" role="status" aria-live="polite">
      <LoaderCircle className="spin" size={20} aria-hidden="true" />
      <span>{label}</span>
    </div>
  );
}

export function EmptyState({
  title,
  children,
}: {
  title: string;
  children: ReactNode;
}) {
  return (
    <div className="empty-state">
      <span className="empty-state__mark" aria-hidden="true">
        —
      </span>
      <strong>{title}</strong>
      <p>{children}</p>
    </div>
  );
}

export function MetricCard({
  label,
  value,
  footnote,
  icon,
  tone = "teal",
}: {
  label: string;
  value: string | number;
  footnote: string;
  icon: ReactNode;
  tone?: "teal" | "blue" | "amber" | "violet";
}) {
  return (
    <article className="metric-card">
      <div className="metric-card__top">
        <span>{label}</span>
        <span className={clsx("metric-card__icon", `tone-${tone}`)}>{icon}</span>
      </div>
      <strong className="metric-card__value">{value}</strong>
      <span className="metric-card__footnote">{footnote}</span>
    </article>
  );
}

export function Dialog({
  title,
  description,
  onClose,
  children,
  size = "regular",
}: {
  title: string;
  description: string;
  onClose: () => void;
  children: ReactNode;
  size?: "regular" | "wide";
}) {
  const dialogRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const firstFocusable = dialogRef.current?.querySelector<HTMLElement>(
      'button:not([disabled]), input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])',
    );
    firstFocusable?.focus();
  }, []);

  const handleKeyDown = (event: KeyboardEvent<HTMLElement>) => {
    if (event.key === "Escape") {
      onClose();
      return;
    }
    if (event.key !== "Tab") return;

    const focusable = dialogRef.current?.querySelectorAll<HTMLElement>(
      'button:not([disabled]), input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])',
    );
    if (!focusable?.length) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  };

  return (
    <div className="dialog-backdrop" onMouseDown={onClose}>
      <section
        aria-describedby="dialog-description"
        aria-labelledby="dialog-title"
        aria-modal="true"
        className={clsx("dialog", size === "wide" && "dialog--wide")}
        onKeyDown={handleKeyDown}
        onMouseDown={(event) => event.stopPropagation()}
        ref={dialogRef}
        role="dialog"
      >
        <div className="dialog__heading">
          <div>
            <h2 id="dialog-title">{title}</h2>
            <p id="dialog-description">{description}</p>
          </div>
          <button
            aria-label="Close dialog"
            className="icon-button"
            onClick={onClose}
            type="button"
          >
            <X size={18} />
          </button>
        </div>
        {children}
      </section>
    </div>
  );
}

export function StatusPill({
  status,
  label,
}: {
  status: string;
  label?: string;
}) {
  const normalized = status.toLowerCase();
  const tone =
    normalized === "healthy" || normalized === "connected"
      ? "good"
      : normalized === "degraded"
        ? "warning"
        : normalized === "unhealthy" || normalized === "disconnected"
          ? "bad"
          : "neutral";
  return (
    <span className={`status-pill status-pill--${tone}`}>
      <span className="status-pill__dot" aria-hidden="true" />
      {label ?? status}
    </span>
  );
}
