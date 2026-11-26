export type Provenance = "SIMULATED" | "MANUAL_TEST";
export type SimulationScale = "small" | "medium" | "demo";

export interface HealthStatus {
  status: "healthy" | "degraded" | "unhealthy" | string;
  timestamp: string;
  version: string;
  data_source_mode: string;
  services: {
    mysql: string;
    mongodb: string;
  };
}

export interface SimulationCounts {
  sessions: number;
  tasks: number;
  operations: number;
  detections: number;
  decisions: number;
  system_events: number;
}

export interface SimulationStatus {
  mode: "SIMULATED" | string;
  active_seed: number;
  counts: SimulationCounts;
}

export interface SimulationGenerateRequest {
  seed: number;
  scale: SimulationScale;
  reset_first: boolean;
}

export interface SimulationGenerateResponse {
  message: string;
  seed: number;
  scale: SimulationScale;
  records_created: SimulationCounts;
  database_ingested?: Record<string, number>;
}

export interface SimulationResetRequest {
  confirm_purge: true;
  purge_target: "SIMULATED_ONLY";
}

export interface SimulationResetResponse {
  message: string;
  records_purged: Record<string, number>;
}

export interface APIError {
  error?: {
    code?: string;
    message?: string;
    details?: unknown;
    timestamp?: string;
  };
  detail?: string;
}
