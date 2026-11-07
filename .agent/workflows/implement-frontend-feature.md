# Workflow: Implement Frontend Feature

## Owner
Ramcharan (Frontend and Dashboard Developer)

## Steps
1. **Review Page Specification**:
   - Consult `docs/project/DASHBOARD_SPECIFICATION.md` for layout, filters, metrics, and chart expectations.
   - Cross-check available endpoints with `docs/api/API_CONTRACT.md`.
2. **Define TypeScript Types**:
   - Add/update interface models in `frontend/src/types/` corresponding directly to backend schemas.
3. **Implement API Client / Hook**:
   - Add data fetching methods in `frontend/src/api/` using `axios` or `fetch`.
   - Wrap with TanStack Query hooks in `frontend/src/hooks/` for caching, pagination, and refresh.
4. **Build Component / Page**:
   - Create UI in `frontend/src/components/` and `frontend/src/pages/`.
   - Ensure explicit handling of:
     - Loading state (skeleton or loader).
     - Empty state (clean zero-data placeholder).
     - Error state (informative error banner).
     - Simulation indicator banner on top of page.
5. **Responsive and Accessibility Verification**:
   - Check layout on desktop and tablet viewport widths.
   - Verify keyboard navigability and accessible contrast.
6. **Local Verification**:
   - Test UI with live backend or mock server.
   - Run typecheck and linter: `npm run lint` and `npm run build`.

