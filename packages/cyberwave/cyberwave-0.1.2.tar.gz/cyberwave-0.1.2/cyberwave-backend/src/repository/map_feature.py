from src.repository.base import CRUDBase
from src.models.map_feature import MapFeature
from src.schemas.map_feature import MapFeatureCreate, MapFeatureInDB # Placeholder Update

class MapFeatureRepository(CRUDBase[MapFeature, MapFeatureCreate, MapFeatureInDB]): # Replace InDB with Update
    pass

map_feature_repo = MapFeatureRepository(MapFeature) 