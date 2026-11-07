# Workflow: Implement Backend Feature

## Owner
Rahul (Backend and Database Integration Developer)

## Steps
1. **Sync on Interface**:
   - Verify requirement against `docs/api/API_CONTRACT.md`.
   - If contract changes are required, notify Ramcharan and update documentation before coding.
2. **Define Pydantic Schemas**:
   - Create request and response validation models in `backend/app/schemas/`.
   - Ensure provenance fields default to `"SIMULATED"` where appropriate.
3. **Implement Repository Layer**:
   - Write parameterized database access methods in `backend/app/repositories/`.
   - Ensure connection handling and errors are properly encapsulated.
4. **Implement Service Logic**:
   - Add business validation and orchestrate transactions in `backend/app/services/`.
5. **Implement API Route**:
   - Add endpoint in `backend/app/api/` and attach to FastAPI router.
   - Use correct HTTP status codes (200, 201, 400, 404, 422, 500).
6. **Write Automated Tests**:
   - Add unit/integration tests in `backend/tests/`.
   - Run tests: `pytest backend/tests/`.
7. **Document Endpoint**:
   - Verify FastAPI OpenAPI documentation (`/docs`) reflects accurate request/response models.

