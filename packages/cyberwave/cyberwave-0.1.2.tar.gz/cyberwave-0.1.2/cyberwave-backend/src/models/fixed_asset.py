from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Dict, Any
import enum

from src.db.base_class import Base

# Define AssetType enum
class AssetTypeEnum(str, enum.Enum):
    CHARGER = "CHARGER"
    INPUT_CONVEYOR = "INPUT_CONVEYOR"
    OUTPUT_CONVEYOR = "OUTPUT_CONVEYOR"
    WORKSTATION = "WORKSTATION"
    STORAGE_RACK = "STORAGE_RACK"
    OTHER = "OTHER"

# Define AssetStatus enum
class AssetStatusEnum(str, enum.Enum):
    AVAILABLE = "available"
    IN_USE = "in_use"
    MAINTENANCE = "maintenance"
    ERROR = "error"
    UNKNOWN = "unknown"
    IDLE = "idle" # Added from seed data

class FixedAsset(Base):
    __tablename__ = "fixed_assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    asset_type: Mapped[AssetTypeEnum] = mapped_column(SQLEnum(AssetTypeEnum), nullable=False)
    status: Mapped[AssetStatusEnum] = mapped_column(SQLEnum(AssetStatusEnum), nullable=False, default=AssetStatusEnum.UNKNOWN)
    # Using JSON for flexible location (e.g., GeoJSON Point or specific structure)
    location: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    properties: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)

    # Foreign Keys
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id"), nullable=False)

    # Relationships
    level: Mapped["Level"] = relationship("Level", back_populates="fixed_assets") 