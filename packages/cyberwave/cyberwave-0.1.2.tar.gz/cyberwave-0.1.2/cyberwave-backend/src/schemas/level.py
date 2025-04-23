from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

# Basic Level schema
class LevelBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    primary_map_id: Optional[int] = None # Allow changing the primary map
    # project_id is typically not changed

class LevelCreate(LevelBase):
    name: str # Required
    project_id: int # Required

class LevelUpdate(LevelBase):
    # All fields from LevelBase are optional for update
    pass

class LevelInDB(LevelBase):
    id: int
    project_id: int # Required in DB
    name: str # Required in DB
    share_token: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True 