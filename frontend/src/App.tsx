import { Navigate, Outlet, Route, Routes, useLocation } from "react-router-dom";
import { LoadingState, SimulationBanner } from "./components/Primitives";
import { useAuth } from "./context/useAuth";
import { DashboardLayout } from "./layouts/DashboardLayout";
import { LoginPage } from "./pages/LoginPage";
import { OperationalPage } from "./pages/OperationalPages";
import { OverviewPage } from "./pages/OverviewPage";
import { SecurityPage } from "./pages/SecurityPage";

function ProtectedRoute() {
  const { isAuthenticated, isInitializing } = useAuth();
  const location = useLocation();

  if (isInitializing) {
    return (
      <div className="auth-shell">
        <SimulationBanner />
        <div className="auth-stage">
          <LoadingState label="Verifying JWT session…" />
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate replace state={{ from: location }} to="/login" />;
  }

  return <Outlet />;
}

function PublicOnlyRoute() {
  const { isAuthenticated, isInitializing } = useAuth();

  if (isInitializing) {
    return (
      <div className="auth-shell">
        <SimulationBanner />
        <div className="auth-stage">
          <LoadingState label="Checking active session…" />
        </div>
      </div>
    );
  }

  if (isAuthenticated) {
    return <Navigate replace to="/" />;
  }

  return <LoginPage />;
}

export default function App() {
  return (
    <Routes>
      <Route element={<PublicOnlyRoute />} path="/login" />
      <Route element={<ProtectedRoute />}>
        <Route element={<DashboardLayout />}>
          <Route element={<OverviewPage />} index />
          <Route element={<OperationalPage module="sessions" />} path="sessions" />
          <Route element={<OperationalPage module="tasks" />} path="tasks" />
          <Route element={<OperationalPage module="detections" />} path="detections" />
          <Route element={<OperationalPage module="operations" />} path="operations" />
          <Route element={<OperationalPage module="decisions" />} path="decisions" />
          <Route element={<OperationalPage module="events" />} path="events" />
          <Route element={<OperationalPage module="analytics" />} path="analytics" />
          <Route element={<OperationalPage module="registry" />} path="registry" />
          <Route element={<SecurityPage />} path="security" />
          <Route path="*" element={<Navigate replace to="/" />} />
        </Route>
      </Route>
    </Routes>
  );
}
