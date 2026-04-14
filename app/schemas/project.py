from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Base schema — shared fields between create and update
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

# Schema for CREATING a project — what the client sends us
class ProjectCreate(ProjectBase):
    pass  # Only needs name and description

# Schema for UPDATING a project — all fields optional
class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

# Schema for READING a project — what we send back to client
class ProjectResponse(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        # Tells Pydantic to read data from SQLAlchemy objects
        from_attributes = True