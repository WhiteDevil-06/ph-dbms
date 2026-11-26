import { Navigate, Route, Routes } from "react-router-dom";
import { DashboardLayout } from "./layouts/DashboardLayout";
import { OverviewPage } from "./pages/OverviewPage";
import { OperationalPage } from "./pages/OperationalPages";

export default function App() {
  return (
    <Routes>
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
        <Route path="*" element={<Navigate replace to="/" />} />
      </Route>
    </Routes>
  );
}
