"""SQLAlchemy ORM model for Task."""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, DateTime, Text, Enum as SQLEnum, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base import Base
from backend.app.models.enums import TaskPriority, TaskStatus, DataProvenance


class Task(Base):
    __tablename__ = "task"

    task_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    session_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("session.session_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    task_type: Mapped[str] = mapped_column(String(50), nullable=False)
    target_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    priority: Mapped[TaskPriority] = mapped_column(
        SQLEnum(TaskPriority, native_enum=False),
        nullable=False,
        default=TaskPriority.MEDIUM,
        index=True,
    )
    creation_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    start_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    task_status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus, native_enum=False),
        nullable=False,
        default=TaskStatus.PENDING,
        index=True,
    )
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
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    session: Mapped["Session"] = relationship("Session", back_populates="tasks")
    operations: Mapped[List["Operation"]] = relationship(
        "Operation",
        back_populates="task",
        cascade="all, delete-orphan",
    )
    decisions: Mapped[List["Decision"]] = relationship(
        "Decision",
        back_populates="task",
    )

    __table_args__ = (
        CheckConstraint(
            "(start_time IS NULL OR start_time >= creation_time) AND "
            "(end_time IS NULL OR (start_time IS NOT NULL AND end_time >= start_time))",
            name="chk_task_times",
        ),
    )
