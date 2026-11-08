"""SQLAlchemy ORM model for AIModel."""

from datetime import datetime
from typing import Optional, Any
from sqlalchemy import String, DateTime, JSON, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.base import Base
from backend.app.models.enums import DataProvenance


class AIModel(Base):
    __tablename__ = "ai_model"

    model_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    model_version: Mapped[str] = mapped_column(String(50), nullable=False)
    configuration: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    provenance: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=DataProvenance.SIMULATED.value,
    )

    __table_args__ = (
        UniqueConstraint("model_name", "model_version", name="uq_model_name_version"),
    )
