import { useState } from "react";
import { Lock } from "lucide-react";
import { Alert, Dialog } from "./Primitives";
import { getApiErrorMessage } from "../api/client";
import { useAuth } from "../context/useAuth";
import {
  useGenerateSimulation,
  useResetSimulation,
} from "../hooks/useSystem";
import type { SimulationScale } from "../types/api";

export function SimulationControls({
  open,
  onClose,
}: {
  open: boolean;
  onClose: () => void;
}) {
  const { isAdmin } = useAuth();
  const [seed, setSeed] = useState("42");
  const [scale, setScale] = useState<SimulationScale>("demo");
  const [resetFirst, setResetFirst] = useState(false);
  const generate = useGenerateSimulation();
  const reset = useResetSimulation();
  const [resetDialogOpen, setResetDialogOpen] = useState(false);

  if (!open && !resetDialogOpen) return null;

  const closeAll = () => {
    if (generate.isPending || reset.isPending) return;
    setResetDialogOpen(false);
    onClose();
  };

  const submitGeneration = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const parsedSeed = Number(seed);
    if (!Number.isSafeInteger(parsedSeed)) return;
    generate.mutate({
      seed: parsedSeed,
      scale,
      reset_first: isAdmin ? resetFirst : false,
    });
  };

  const confirmReset = () => {
    if (!isAdmin) return;
    reset.mutate({ confirm_purge: true, purge_target: "SIMULATED_ONLY" });
  };

  return (
    <>
      {open && !resetDialogOpen ? (
        <Dialog
          description="Create a reproducible dataset using the project's simulation engine."
          onClose={closeAll}
          title="Generate simulation dataset"
        >
          <form className="dialog-form" onSubmit={submitGeneration}>
            {!isAdmin ? (
              <Alert title="Operator access scope (RBAC)" variant="info">
                Signed in as <strong>OPERATOR</strong>: non-destructive dataset generation is
                enabled. Clearing existing records (<code>reset_first</code>) and purging simulated
                data require the <strong>ADMIN</strong> role (enforced server-side with HTTP 403).
              </Alert>
            ) : null}

            <label className="field">
              <span>Random seed</span>
              <input
                max={2147483647}
                min={0}
                onChange={(event) => setSeed(event.target.value)}
                required
                step={1}
                type="number"
                value={seed}
              />
              <small>Use the same seed to reproduce a dataset.</small>
            </label>
            <label className="field">
              <span>Dataset scale</span>
              <select
                onChange={(event) =>
                  setScale(event.target.value as SimulationScale)
                }
                value={scale}
              >
                <option value="small">Small — quick checks</option>
                <option value="medium">Medium — development</option>
                <option value="demo">Demo — presentation</option>
              </select>
            </label>
            <label
              className={`checkbox-field ${!isAdmin ? "checkbox-field--locked" : ""}`}
              title={isAdmin ? undefined : "Requires ADMIN role"}
            >
              <input
                checked={isAdmin ? resetFirst : false}
                disabled={!isAdmin}
                onChange={(event) => setResetFirst(event.target.checked)}
                type="checkbox"
              />
              <span>
                Clear existing simulated records before generating
                {!isAdmin ? (
                  <span className="inline-lock-tag">
                    <Lock size={11} aria-hidden="true" /> Admin only
                  </span>
                ) : null}
              </span>
            </label>
            {generate.isError ? (
              <Alert title="Dataset generation failed">
                {getApiErrorMessage(generate.error)}
              </Alert>
            ) : null}
            {generate.isSuccess ? (
              <Alert title="Dataset generated" variant="success">
                {generate.data.message}
              </Alert>
            ) : null}
            <div className="dialog-actions">
              {generate.isSuccess ? (
                <button
                  className="button button--primary"
                  onClick={closeAll}
                  type="button"
                >
                  Done
                </button>
              ) : (
                <>
                  {isAdmin ? (
                    <button
                      className="reset-entry"
                      onClick={() => setResetDialogOpen(true)}
                      type="button"
                    >
                      Reset simulated dataset
                    </button>
                  ) : (
                    <span
                      className="reset-entry reset-entry--locked"
                      title="Purging simulated records requires the ADMIN role."
                    >
                      <Lock size={12} aria-hidden="true" /> Reset locked (Admin only)
                    </span>
                  )}
                  <button
                    className="button button--secondary"
                    onClick={closeAll}
                    type="button"
                  >
                    Cancel
                  </button>
                  <button
                    className="button button--primary"
                    disabled={generate.isPending || !Number.isSafeInteger(Number(seed))}
                    type="submit"
                  >
                    {generate.isPending ? "Generating…" : "Generate dataset"}
                  </button>
                </>
              )}
            </div>
          </form>
        </Dialog>
      ) : null}
      {resetDialogOpen && isAdmin ? (
        <Dialog
          description="This operation cannot be undone. It only targets records marked SIMULATED."
          onClose={closeAll}
          title="Reset simulated data"
        >
          <div className="dialog-form">
            <Alert title="Confirm simulated-record purge">
              Simulated sessions, tasks, operations, detections, decisions, and
              system events will be purged. No reset request is sent until you
              choose the confirmation button.
            </Alert>
            {reset.isError ? (
              <Alert title="Reset failed">
                {getApiErrorMessage(reset.error)}
              </Alert>
            ) : null}
            {reset.isSuccess ? (
              <Alert title="Simulation data reset" variant="success">
                {reset.data.message}
              </Alert>
            ) : null}
            <div className="dialog-actions">
              {reset.isSuccess ? (
                <button
                  className="button button--primary"
                  onClick={closeAll}
                  type="button"
                >
                  Done
                </button>
              ) : (
                <>
                  <button
                    className="button button--secondary"
                    onClick={closeAll}
                    type="button"
                  >
                    Cancel
                  </button>
                  <button
                    className="button button--danger"
                    disabled={reset.isPending}
                    onClick={confirmReset}
                    type="button"
                  >
                    {reset.isPending ? "Resetting…" : "Confirm reset"}
                  </button>
                </>
              )}
            </div>
          </div>
        </Dialog>
      ) : null}
    </>
  );
}
