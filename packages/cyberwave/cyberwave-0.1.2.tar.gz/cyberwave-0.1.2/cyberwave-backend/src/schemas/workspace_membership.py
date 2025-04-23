from pydantic import BaseModel
from datetime import datetime
from src.models.workspace_membership import RoleEnum # Import the enum

# Basic WorkspaceMembership schema
class WorkspaceMembershipBase(BaseModel):
    user_id: int
    workspace_id: int
    role: RoleEnum

class WorkspaceMembershipCreate(WorkspaceMembershipBase):
    pass

class WorkspaceMembershipInDB(WorkspaceMembershipBase):
    joined_at: datetime

    class Config:
        from_attributes = True 