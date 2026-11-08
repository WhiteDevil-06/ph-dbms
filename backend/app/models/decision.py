"""SQLAlchemy ORM model for Decision."""

from datetime import datetime
from typing import Optional, Any
from sqlalchemy import String, DateTime, Text, JSON, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base import Base
from backend.app.models.enums import DataProvenance


class Decision(Base):
    __tablename__ = "decision"

    decision_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    session_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("session.session_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    task_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("task.task_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    decision_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    decision_type: Mapped[str] = mapped_column(String(50), nullable=False)
    selected_action: Mapped[str] = mapped_column(String(100), nullable=False)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    input_reference: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    provenance: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=DataProvenance.SIMULATED.value,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    # Relationships
    session: Mapped["Session"] = relationship("Session", back_populates="decisions")
    task: Mapped[Optional["Task"]] = relationship("Task", back_populates="decisions")
