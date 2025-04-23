from src.repository.base import CRUDBase
from src.models.level import Level
from src.schemas.level import LevelCreate, LevelUpdate

class LevelRepository(CRUDBase[Level, LevelCreate, LevelUpdate]):
    # Add custom methods if needed
    pass

level_repo = LevelRepository(Level) 