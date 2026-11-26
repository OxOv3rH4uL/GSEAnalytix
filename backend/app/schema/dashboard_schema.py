from pydantic import BaseModel
from app.helpers.enums import DeviceStatus
from uuid import UUID
from decimal import Decimal
from datetime import datetime

class DashboardSchema(BaseModel):

    device_id: UUID
    device_name: str
    status : DeviceStatus
    total_runtime: float
    total_energy: float
    total_cost: Decimal
    updated_at: datetime

class ProjectAnalyticsSchema(BaseModel):

    total_devices: int
    total_runtime: float
    total_energy: float
    total_cost: Decimal

class ProjectDashboardSchema(BaseModel):

    project_id: UUID
    project_name: str
    summary: ProjectAnalyticsSchema
    devices: list[DashboardSchema]