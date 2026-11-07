# Workflow: Prepare Pull Request

## Purpose
Standardized procedure for preparing and opening pull requests into the `main` branch.

## Steps
1. **Status and Diff Check**:
   - Run `git status` to verify no unintended or untracked files (e.g. `.env`, `node_modules`, `__pycache__`) exist.
   - Run `git diff` to perform a self-review of changes.
2. **Execute Full Test Suite**:
   - Run the workflow `run-tests-and-review.md`.
   - Copy the execution commands and terminal outputs.
3. **Commit and Push Feature Branch**:
   ```powershell
   git add <modified_files>
   git commit -m "[MODULE] Descriptive summary of changes"
   git push origin <feature-branch-name>
   ```
4. **Draft PR Description**:
   - Fill out the PR template from `CONTRIBUTING.md`.
   - Attach test execution logs and frontend UI screenshots.
   - Tag the appropriate teammate for peer review:
     - Backend PRs -> Reviewed by Rakshith Raghavendra or Ramcharan.
     - Frontend PRs -> Reviewed by Rahul or Rakshith Raghavendra.
     - Database/Architecture PRs -> Reviewed by Rahul and Ramcharan.
5. **Await Review & Merge**:
   - Merge only when review approval is received and all CI/test checks pass.

