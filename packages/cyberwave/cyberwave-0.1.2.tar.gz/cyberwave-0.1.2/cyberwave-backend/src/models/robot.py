import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON, Enum as SQLEnum, func, ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Dict, Any, Optional
import enum

from src.db.base_class import Base

# Define RobotStatus enum
class RobotStatusEnum(str, enum.Enum):
    IDLE = "idle"
    CHARGING = "charging"
    MOVING = "moving"
    WORKING = "working"
    ERROR = "error"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"
    UNKNOWN = "unknown"

class Robot(Base):
    __tablename__ = "robots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    robot_type: Mapped[str] = mapped_column(String, index=True, nullable=False) # e.g., "agv/model-x"
    serial_number: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=True)
    status: Mapped[RobotStatusEnum] = mapped_column(SQLEnum(RobotStatusEnum), nullable=False, default=RobotStatusEnum.UNKNOWN)
    # Changed capabilities from ARRAY(String) to JSON for SQLite compatibility
    capabilities: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    # Store initial pose as separate columns
    initial_pos_x: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    initial_pos_y: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    initial_pos_z: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    metadata_: Mapped[Optional[Dict[str, Any]]] = mapped_column("metadata", JSON, nullable=True)
    current_battery_percentage: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    registration_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Foreign Keys
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id"), nullable=False)

    # Relationships
    level: Mapped["Level"] = relationship("Level", back_populates="robots") 