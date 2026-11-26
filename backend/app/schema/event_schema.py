from pydantic import BaseModel
from typing import Literal

class Event(BaseModel):
    status: Literal["running","stopped"]
