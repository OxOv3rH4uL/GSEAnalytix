from uuid import uuid4, UUID
from datetime import datetime
from sqlalchemy import func, Float, ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import CheckConstraint
from app.helpers.db import Base

class DeviceReadings(Base):
    """
    Device Readings Table Schema
    """
    __tablename__ = "device_readings"
    __table_args__ = (
        CheckConstraint("power_kw > 0"),
        CheckConstraint("duration > 0")
    )

    reading_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4
    )

    device_id: Mapped[UUID] = mapped_column(
        ForeignKey("devices.device_id", ondelete="CASCADE"),
        nullable=False
    )
    power_kw: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    duration: Mapped[float] = mapped_column(
        Float,
        nullable=False   
    )
    measured_at: Mapped[datetime] = mapped_column(
        server_default= func.now(),
        nullable=False
    )
