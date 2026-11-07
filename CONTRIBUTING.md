# Contributing to Post-Harvest DBMS

Thank you for contributing to the **Intelligent Data Management and Operational Analytics for Autonomous Post-Harvest Material Handling Systems** academic project.

To maintain repository integrity, reproducibility, and prevent merge conflicts among team members, all contributors must strictly adhere to this workflow.

---

## 1. Branching Strategy

- **`main` Branch**:
  - The `main` branch represents stable, peer-reviewed, tested code.
  - **Direct pushes to `main` are strictly prohibited.**
  - Every merge to `main` must occur via a Pull Request (PR) with at least one team peer review.

- **Feature Branches**:
  - Work must be done in designated feature branches prefixed appropriately:
    - `feature/database-foundation` (Rakshith Raghavendra)
    - `feature/ramcharan-dashboard` or `feature/frontend-<component>` (Ramcharan)
    - `feature/rahul-backend` or `feature/api-<endpoint>` (Rahul)
    - `fix/<issue-description>` (Bug fixes)
    - `docs/<doc-update>` (Documentation updates)

---

## 2. Commit Discipline & Secret Prevention

- Never commit sensitive files. The `.gitignore` is configured to exclude:
  - `.env` and all credential files
  - Virtual environments (`.venv/`, `venv/`)
  - Node modules (`node_modules/`)
  - Local database volumes and dump files (`mysql_data/`, `mongo_data/`, `*.dump`)
  - Python byte-cache (`__pycache__/`) and build artifacts
- Commit messages must be clear and descriptive:
  ```text
  [MODULE] Short imperatively phrased summary

  - Detailed bullet point of architectural decision or code change
  - Reference to related issue or document
  ```

---

## 3. Pull Request Requirements

Every Pull Request must include the following information in its description:
1. **Purpose**: Clear explanation of what feature, schema, or fix is implemented.
2. **Changed Files & Scope**: Summary of modified modules (ensure no teammate's ownership was infringed).
3. **Testing Evidence**:
   - Exact command(s) executed.
   - Output/test results (e.g., pytest summary, linter output).
   - For frontend changes: screenshots or GIF of the UI and responsive layout.
4. **Documentation Updates**: Links to updated docs (API contract, decision log, architecture audit).
5. **Data Provenance Check**: Confirmation that all mock/seed data is clearly tagged as `SIMULATED`.

### Pull Request Checklist
Before requesting review, verify:
- [ ] Code follows project standards without suppressing linter errors.
- [ ] No secrets, `.env` files, or test DB dumps are included.
- [ ] New/modified endpoints are updated in `docs/api/API_CONTRACT.md`.
- [ ] All tests pass locally and commands are recorded in the PR.
- [ ] If database schemas changed, migration notes and risks are detailed.
- [ ] At least one teammate has been assigned to review.

---

## 4. Conflict Resolution & Communication

- Never overwrite a teammate's work.
- If conflicts arise between backend and frontend contracts, pause and hold a design sync.
- Log all cross-cutting agreements in `docs/decisions/DECISION_LOG.md`.

---

## 5. Local Git Initialization Note (Project Lead)

The project lead will initialize the git repository and link it to the official remote GitHub repository manually:
```bash
git init
git add .
git commit -m "chore: initialize post-harvest dbms repository scaffold and documentation"
git branch -M main
git remote add origin <GITHUB_REPO_URL>
git push -u origin main
```
Agents must never execute remote push commands autonomously.

