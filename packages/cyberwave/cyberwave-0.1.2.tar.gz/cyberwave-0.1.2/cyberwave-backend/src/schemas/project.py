from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Basic Project schema
class ProjectBase(BaseModel):
    name: Optional[str] = None # Allow name update
    # workspace_id is usually not updated directly, maybe via a different endpoint

class ProjectCreate(ProjectBase):
    name: str # Name required for creation
    workspace_id: int # Workspace ID required for creation

class ProjectUpdate(ProjectBase):
    # Only name is updatable in this basic setup
    pass

class ProjectInDB(ProjectBase):
    id: int
    workspace_id: int # Required in DB
    name: str # Required in DB
    created_at: datetime

    class Config:
        from_attributes = True 