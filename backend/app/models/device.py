"""SQLAlchemy ORM model for Device."""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, DateTime, Text, Enum as SQLEnum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base import Base
from backend.app.models.enums import DeviceStatus, DataProvenance


class Device(Base):
    __tablename__ = "device"

    device_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    device_name: Mapped[str] = mapped_column(String(100), nullable=False)
    device_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    device_status: Mapped[DeviceStatus] = mapped_column(
        SQLEnum(DeviceStatus, native_enum=False),
        nullable=False,
        default=DeviceStatus.ONLINE,
        index=True,
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
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
    operations: Mapped[List["Operation"]] = relationship(
        "Operation",
        back_populates="device",
    )
    system_events: Mapped[List["SystemEvent"]] = relationship(
        "SystemEvent",
        back_populates="device",
    )
