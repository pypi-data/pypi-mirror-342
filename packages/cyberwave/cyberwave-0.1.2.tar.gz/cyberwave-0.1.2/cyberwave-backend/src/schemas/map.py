from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from src.models.map import MapTypeEnum

# Basic Map schema
class MapBase(BaseModel):
    name: str
    project_id: int
    map_type: MapTypeEnum
    map_data_uri: Optional[str] = None
    origin_pose: Optional[Dict[str, Any]] = None
    resolution: Optional[float] = None

class MapCreate(MapBase):
    pass

class MapInDB(MapBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 