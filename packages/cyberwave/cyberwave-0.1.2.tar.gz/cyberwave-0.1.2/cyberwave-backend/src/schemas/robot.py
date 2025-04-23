from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from src.models.robot import RobotStatusEnum

# Basic Robot schema
class RobotBase(BaseModel):
    name: Optional[str] = None # Allow name update
    level_id: Optional[int] = None # Allow moving robot between levels
    robot_type: Optional[str] = None # Maybe changeable?
    serial_number: Optional[str] = None # Unlikely to change, but maybe
    status: Optional[RobotStatusEnum] = None # Status updates are common
    capabilities: Optional[List[str]] = None # Update capabilities
    initial_pos_x: Optional[float] = None # Maybe update home/initial position
    initial_pos_y: Optional[float] = None
    initial_pos_z: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None # Update metadata
    current_battery_percentage: Optional[float] = None # Battery updates

class RobotCreate(RobotBase):
    # Make fields required for creation that were optional in Base
    name: str
    # Make level_id optional for creation to allow frictionless flow
    level_id: Optional[int] = None 
    robot_type: str
    status: RobotStatusEnum = RobotStatusEnum.UNKNOWN # Default status on creation

class RobotUpdate(RobotBase):
    # All fields are optional for update, inherits from RobotBase
    pass

class RobotInDB(RobotBase):
    # Fields that are definitely present when reading from DB
    id: int
    name: str # Name is not optional in DB
    level_id: int # Level is not optional in DB
    robot_type: str # Type is not optional in DB
    status: RobotStatusEnum # Status is not optional in DB
    registration_date: datetime
    metadata_: Optional[Dict[str, Any]] = None # Alias for metadata in model

    class Config:
        from_attributes = True
        # If using metadata_ in model but metadata in schema:
        # serialization_alias = {'metadata_': 'metadata'}
        # validation_alias = {'metadata': 'metadata_'} 