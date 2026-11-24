from uuid import uuid4, UUID
from datetime import datetime
from sqlalchemy import func, Numeric, ForeignKey,String, Enum as AlchemyEnum
from decimal import Decimal
from sqlalchemy import UniqueConstraint, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped
from app.helpers.db import Base
import enum 

class DeviceStatus(enum.Enum):
    running="running"
    stopped="stopped"
    created="created"


class DevicesDB(Base):
    """
    Devices Table Schema 
    """
    __tablename__ = "devices"
    __table_args__ = (
        CheckConstraint("tariff_per_kwh > 0"),
        UniqueConstraint("device_name","project_id")
    )

    device_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4
    )
    project_id: Mapped[UUID] = mapped_column(
        ForeignKey("projects.project_id", ondelete="CASCADE"),
        nullable=False
    )
    device_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    tariff_per_kwh: Mapped[Decimal] = mapped_column(
        Numeric(10,4),
        nullable=False
    )
    status: Mapped[DeviceStatus] = mapped_column(
        AlchemyEnum(DeviceStatus),
        default=DeviceStatus.created,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default = func.now(),
        nullable=False
    )

    


    