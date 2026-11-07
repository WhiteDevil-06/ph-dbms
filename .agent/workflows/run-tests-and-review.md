# Workflow: Run Tests and Code Review

## Purpose
Ensure all changes satisfy testing, linting, and architectural standards prior to merging.

## Steps
1. **Static Analysis & Linting**:
   - Backend:
     ```powershell
     flake8 backend/
     black --check backend/
     ```
   - Frontend:
     ```powershell
     cd frontend
     npm run lint
     cd ..
     ```
2. **Execute Automated Test Suites**:
   - Backend tests (unit, repository, API):
     ```powershell
     pytest backend/tests -v
     ```
   - Frontend build & tests:
     ```powershell
     cd frontend
     npm run build
     cd ..
     ```
3. **Inspect Output**:
   - Confirm exit code 0 on all commands.
   - Record exact terminal outputs in the PR description.
4. **Peer Review**:
   - Reviewer checks adherence to role ownership and data boundaries.
   - Verify no secrets or `.env` files are tracked.
   - Approve PR only after all automated and manual checks pass.

