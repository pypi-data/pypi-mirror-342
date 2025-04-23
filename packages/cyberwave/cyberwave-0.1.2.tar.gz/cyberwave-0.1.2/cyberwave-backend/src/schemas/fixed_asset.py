from pydantic import BaseModel
from typing import Optional, Dict, Any
from src.models.fixed_asset import AssetTypeEnum, AssetStatusEnum

# Basic FixedAsset schema
class FixedAssetBase(BaseModel):
    name: str
    level_id: int
    asset_type: AssetTypeEnum
    status: AssetStatusEnum
    location: Dict[str, Any]
    properties: Optional[Dict[str, Any]] = None

class FixedAssetCreate(FixedAssetBase):
    pass

class FixedAssetInDB(FixedAssetBase):
    id: int

    class Config:
        from_attributes = True 