from uuid import UUID
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from app.helpers.enums import DeviceStatus


class DeviceCreateRequest(BaseModel):
    project_id: UUID
    device_name: str = Field(min_length=1, max_length=100)
    tariff_per_kwh: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=4
    )

class DeviceUpdateRequest(BaseModel):
    device_name: str = Field(min_length=1, max_length=100)
    tariff_per_kwh: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=4
    )

class DeviceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    device_id: UUID
    project_id: UUID
    device_name: str
    tariff_per_kwh: Decimal
    status: DeviceStatus
    created_at: datetime


