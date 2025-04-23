from src.repository.base import CRUDBase
from src.models.fixed_asset import FixedAsset
from src.schemas.fixed_asset import FixedAssetCreate, FixedAssetInDB # Placeholder Update

class FixedAssetRepository(CRUDBase[FixedAsset, FixedAssetCreate, FixedAssetInDB]): # Replace InDB with Update
    pass

fixed_asset_repo = FixedAssetRepository(FixedAsset) 