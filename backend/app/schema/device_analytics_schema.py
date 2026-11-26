from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal
from datetime import datetime


class DeviceAnalyticsSchema(BaseModel):
    device_id : UUID
    total_runtime: float = Field(
        gt=0,
        allow_inf_nan=False
    )
    total_kwh : float = Field(
        gt=0,
        allow_inf_nan=False
    )
    total_cost: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2
    )

class DeviceAnalyticsUpdateSchema(BaseModel):
    device_id: UUID
    total_runtime: float = Field(
        gt=0,
        allow_inf_nan=False
    )
    total_kwh : float = Field(
        gt=0,
        allow_inf_nan=False
    )
    total_cost: Decimal = Field(
        gt=0,
        allow_inf_nan=False
    )
    


class DeviceAnalyticsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    device_id: UUID
    total_runtime: float
    total_kwh: float
    total_cost: Decimal
    updated_at: datetime

