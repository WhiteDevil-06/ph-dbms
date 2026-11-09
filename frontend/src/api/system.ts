import apiClient from "./client";
import type {
  HealthStatus,
  SimulationGenerateRequest,
  SimulationGenerateResponse,
  SimulationResetRequest,
  SimulationResetResponse,
  SimulationStatus,
} from "../types/api";

export async function getHealth(): Promise<HealthStatus> {
  const { data } = await apiClient.get<HealthStatus>("/health");
  return data;
}

export async function getSimulationStatus(): Promise<SimulationStatus> {
  const { data } =
    await apiClient.get<SimulationStatus>("/api/v1/simulation/status");
  return data;
}

export async function generateSimulation(
  payload: SimulationGenerateRequest,
): Promise<SimulationGenerateResponse> {
  const { data } = await apiClient.post<SimulationGenerateResponse>(
    "/api/v1/simulation/generate",
    payload,
  );
  return data;
}

export async function resetSimulation(
  payload: SimulationResetRequest,
): Promise<SimulationResetResponse> {
  const { data } = await apiClient.post<SimulationResetResponse>(
    "/api/v1/simulation/reset",
    payload,
  );
  return data;
}
