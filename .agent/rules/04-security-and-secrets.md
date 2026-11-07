# Rule 04: Security, Secrets, and Safety

## Credential Protection
1. **Never Commit Secrets**: Passwords, API tokens, database URIs containing credentials, and local connection strings must never be committed to Git.
2. **Environment Configuration**: Always use environment variables loaded from `.env` (via `python-dotenv` or Pydantic `BaseSettings`). Keep `.env.example` populated with dummy placeholders only.
3. **Least Privilege**: Application database users must not use root privileges for regular backend operations. Configure separate application credentials (`post_harvest_app`) with restricted DML privileges where feasible.

## Defensive Network & Error Handling
1. **CORS Restrictions**: Configure FastAPI CORS middleware to allow only recognized local development origins (e.g., `http://localhost:5173`, `http://127.0.0.1:5173`). Never use `allow_origins=["*"]` in production-like configurations.
2. **Sanitized Error Responses**: Never leak database connection strings, stack traces, internal server file paths, or SQL syntax errors to the client in HTTP 500 responses.
3. **Data Protection**: Do not store real personal information or sensitive credentials in test/seed datasets.

