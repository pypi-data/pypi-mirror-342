from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Basic Workspace schema
class WorkspaceBase(BaseModel):
    name: str

class WorkspaceCreate(WorkspaceBase):
    pass

# --- Add Update Schema --- 
class WorkspaceUpdate(BaseModel):
    name: Optional[str] = None # Allow updating name, make it optional
# --- End Add --- 

class WorkspaceInDB(WorkspaceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 