from src.repository.base import CRUDBase
from src.models.robot import Robot
from src.schemas.robot import RobotCreate, RobotUpdate

class RobotRepository(CRUDBase[Robot, RobotCreate, RobotUpdate]):
    # Add specific query methods if needed, e.g.:
    # async def get_by_serial_number(self, db: AsyncSession, *, serial_number: str) -> Optional[Robot]:
    #     result = await db.execute(select(self.model).filter(self.model.serial_number == serial_number))
    #     return result.scalars().first()
    pass

robot_repo = RobotRepository(Robot) 