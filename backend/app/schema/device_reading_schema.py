# {
#     "device_id" : device_id,
#     "power_kw" : round(random.uniform(1,10),3),
#     "duration" : round(random.uniform(0.5,5),2)
# }

from uuid import UUID
from pydantic import BaseModel, Field

class DeviceReadingSchema(BaseModel):
    device_id : UUID
    power_kw : float = Field(
        gt = 0,
        allow_inf_nan=False
    )   

    duration: float = Field(
        gt = 0,
        allow_inf_nan=False
    )


