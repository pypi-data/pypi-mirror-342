from pydantic import BaseModel
from typing import Optional, Dict, Any
from src.models.map_feature import FeatureTypeEnum

# Basic MapFeature schema
class MapFeatureBase(BaseModel):
    name: str
    map_id: int
    feature_type: FeatureTypeEnum
    geometry: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

class MapFeatureCreate(MapFeatureBase):
    pass

class MapFeatureInDB(MapFeatureBase):
    id: int
    metadata_: Optional[Dict[str, Any]] = None # Alias for metadata in model

    class Config:
        from_attributes = True
        # If using metadata_ in model but metadata in schema:
        # serialization_alias = {'metadata_': 'metadata'}
        # validation_alias = {'metadata': 'metadata_'} 