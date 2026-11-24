from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime

class ProjectCreateRequest(BaseModel):
    project_name: str = Field(min_length=1, max_length=100)


class ProjectUpdateRequest(BaseModel):
    project_name: str = Field(min_length=1, max_length=100)


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    project_id: UUID
    project_name: str
    created_at: datetime