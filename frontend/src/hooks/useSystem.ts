import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
import {
  generateSimulation,
  getHealth,
  getSimulationStatus,
  resetSimulation,
} from "../api/system";
import type {
  SimulationGenerateRequest,
  SimulationResetRequest,
} from "../types/api";

export const systemKeys = {
  health: ["system", "health"] as const,
  simulation: ["simulation", "status"] as const,
};

export function useHealth() {
  return useQuery({
    queryKey: systemKeys.health,
    queryFn: getHealth,
    refetchInterval: 30_000,
    retry: 1,
  });
}

export function useSimulationStatus() {
  return useQuery({
    queryKey: systemKeys.simulation,
    queryFn: getSimulationStatus,
    refetchInterval: 30_000,
    retry: 1,
  });
}

function useRefreshSystemData() {
  const queryClient = useQueryClient();
  return async () => {
    await Promise.all([
      queryClient.invalidateQueries({ queryKey: systemKeys.simulation }),
      queryClient.invalidateQueries({ queryKey: systemKeys.health }),
    ]);
  };
}

export function useGenerateSimulation() {
  const refresh = useRefreshSystemData();
  return useMutation({
    mutationFn: (payload: SimulationGenerateRequest) =>
      generateSimulation(payload),
    onSuccess: refresh,
  });
}

export function useResetSimulation() {
  const refresh = useRefreshSystemData();
  return useMutation({
    mutationFn: (payload: SimulationResetRequest) =>
      resetSimulation(payload),
    onSuccess: refresh,
  });
}
