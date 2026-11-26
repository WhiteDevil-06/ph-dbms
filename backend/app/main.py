"""FastAPI Application Entrypoint — Post-Harvest DBMS Layer.

Intelligent Data Management and Operational Analytics for Autonomous Post-Harvest Material Handling Systems.
"""

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Literal
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from backend.app.api.auth import router as auth_router
from backend.app.core.config import settings
from backend.app.core.security import (
    AuthenticatedPrincipal,
    SecurityHeadersMiddleware,
    extract_client_ip,
    get_current_user,
    require_roles,
)
from backend.app.database.mysql import check_mysql_connection, get_db, SessionLocal
from backend.app.database.mongodb import check_mongodb_connection, get_mongo_db
from backend.app.models import (
    AuthAuditAction,
    Session as SessionModel,
    Task as TaskModel,
    Operation as OperationModel,
    Decision as DecisionModel,
    SystemEvent as SystemEventModel,
    UserRole,
)
from backend.app.repositories import auth_repository
from backend.app.services.auth_service import ensure_auth_tables_and_seed_users
from simulator.generators.data_generator import SimulationGenerator
from simulator.generators.database_loader import (
    insert_dataset_into_databases,
    reset_simulated_data,
)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Bootstrap auth tables and seeded demo accounts idempotently on startup."""
    ensure_auth_tables_and_seed_users()
    yield


# Initialize FastAPI application
app = FastAPI(
    title="Post-Harvest Material Handling DBMS API",
    description="Operational persistence, detection indexing, JWT RBAC security, and analytics layer for autonomous post-harvest robotics.",
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Defensive Security Response Headers
app.add_middleware(SecurityHeadersMiddleware)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else [settings.CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Auth & RBAC Router
app.include_router(auth_router)


# --- Pydantic Schemas for Simulation ---
class SimulationGenerateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    seed: int = Field(default=42, ge=0, le=2147483647, description="Pseudorandom seed for generation")
    scale: Literal["small", "medium", "demo"] = Field(
        default="demo",
        description="Scale profile: small, medium, or demo",
    )
    reset_first: bool = Field(
        default=False,
        description="Whether to reset existing simulated data first (ADMIN role required)",
    )


class SimulationResetRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    confirm_purge: bool = Field(..., description="Explicit confirmation required to reset data")
    purge_target: Literal["SIMULATED_ONLY"] = Field(
        default="SIMULATED_ONLY",
        description="Target of purge operation",
    )


# --- System Endpoints ---
@app.get("/health", tags=["System"])
def health_check():
    """Reports real-time connectivity status of backend services and databases."""
    mysql_connected = check_mysql_connection()
    mongo_connected = check_mongodb_connection()

    overall_status = (
        "healthy"
        if (mysql_connected and mongo_connected)
        else "degraded"
        if (mysql_connected or mongo_connected)
        else "unhealthy"
    )

    return {
        "status": overall_status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.1.0",
        "data_source_mode": settings.DATA_SOURCE_MODE,
        "services": {
            "mysql": "connected" if mysql_connected else "disconnected",
            "mongodb": "connected" if mongo_connected else "disconnected",
        },
    }


# --- Simulation Endpoints (Protected by JWT + RBAC) ---
@app.get("/api/v1/simulation/status", tags=["Simulation"])
def simulation_status(_principal: AuthenticatedPrincipal = Depends(get_current_user)):
    """Returns the current simulation engine configuration and record counts (ADMIN & OPERATOR)."""
    counts = {
        "sessions": 0,
        "tasks": 0,
        "operations": 0,
        "detections": 0,
        "decisions": 0,
        "system_events": 0,
    }

    if check_mysql_connection():
        db = SessionLocal()
        try:
            counts["sessions"] = db.query(SessionModel).filter_by(provenance="SIMULATED").count()
            counts["tasks"] = db.query(TaskModel).filter_by(provenance="SIMULATED").count()
            counts["operations"] = db.query(OperationModel).filter_by(provenance="SIMULATED").count()
            counts["decisions"] = db.query(DecisionModel).filter_by(provenance="SIMULATED").count()
            counts["system_events"] = db.query(SystemEventModel).filter_by(provenance="SIMULATED").count()
        finally:
            db.close()

    if check_mongodb_connection():
        mongo_db = get_mongo_db()
        counts["detections"] = mongo_db["detections"].count_documents({"provenance": "SIMULATED"})

    return {
        "mode": "SIMULATED",
        "active_seed": settings.SIMULATION_DEFAULT_SEED,
        "counts": counts,
    }


@app.post("/api/v1/simulation/generate", status_code=status.HTTP_201_CREATED, tags=["Simulation"])
def generate_simulation_data(
    payload: SimulationGenerateRequest,
    request: Request,
    principal: AuthenticatedPrincipal = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Trigger seeded deterministic record generation (ADMIN full; OPERATOR non-destructive only)."""
    if payload.reset_first and principal.role != UserRole.ADMIN:
        detail = "Access denied: clearing existing simulated data (reset_first=true) requires ADMIN role."
        auth_repository.record_audit_event(
            db,
            username=principal.username,
            user_id=principal.user_id,
            action=AuthAuditAction.ACCESS_DENIED,
            role=principal.role.value,
            endpoint="POST /api/v1/simulation/generate",
            ip_address=extract_client_ip(request),
            detail=detail,
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )

    if payload.reset_first:
        try:
            reset_simulated_data(confirm=True)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to reset data prior to generation: {type(exc).__name__}",
            )

    generator = SimulationGenerator(seed=payload.seed, scale=payload.scale)
    dataset = generator.generate()

    inserted_records = insert_dataset_into_databases(dataset)

    return {
        "message": "Simulation data generated successfully.",
        "seed": payload.seed,
        "scale": payload.scale,
        "triggered_by": {
            "username": principal.username,
            "role": principal.role.value,
        },
        "records_created": {
            "sessions": len(dataset.sessions),
            "tasks": len(dataset.tasks),
            "operations": len(dataset.operations),
            "detections": len(dataset.detections),
            "decisions": len(dataset.decisions),
            "system_events": len(dataset.system_events),
        },
        "database_ingested": inserted_records,
    }


@app.post("/api/v1/simulation/reset", tags=["Simulation"])
def reset_simulation(
    payload: SimulationResetRequest,
    _admin: AuthenticatedPrincipal = Depends(require_roles(UserRole.ADMIN)),
):
    """Safely purges simulated records from MySQL and MongoDB (ADMIN role required)."""
    if not payload.confirm_purge:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="confirm_purge must be true to execute reset.",
        )

    try:
        purged = reset_simulated_data(confirm=True)
        return {
            "message": "Simulated operational records safely purged.",
            "records_purged": purged,
        }
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Reset operation failed: {type(exc).__name__}",
        )
