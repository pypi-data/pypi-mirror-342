import datetime
import json
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON, Enum as SQLEnum, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Dict, Any
import enum

from src.db.base_class import Base

# Define MapType enum
class MapTypeEnum(str, enum.Enum):
    OCCUPANCY_GRID = "OCCUPANCY_GRID"
    POINT_CLOUD = "POINT_CLOUD"
    VECTOR_MAP = "VECTOR_MAP"

class Map(Base):
    __tablename__ = "maps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    map_type: Mapped[MapTypeEnum] = mapped_column(SQLEnum(MapTypeEnum), nullable=False)
    map_data_uri: Mapped[str] = mapped_column(String, nullable=True) # URI to map file (e.g., S3)
    # Store pose as JSON or separate columns depending on query needs
    origin_pose: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    resolution: Mapped[float] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Foreign Keys
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="maps")
    levels: Mapped[List["Level"]] = relationship(
        "Level", back_populates="primary_map", foreign_keys="[Level.primary_map_id]"
    )
    map_features: Mapped[List["MapFeature"]] = relationship(
        "MapFeature", back_populates="map", cascade="all, delete-orphan"
    ) 