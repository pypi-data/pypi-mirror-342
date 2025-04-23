from src.repository.base import CRUDBase
from src.models.map import Map
from src.schemas.map import MapCreate, MapInDB # Placeholder Update

class MapRepository(CRUDBase[Map, MapCreate, MapInDB]): # Replace InDB with Update
    pass

map_repo = MapRepository(Map) 