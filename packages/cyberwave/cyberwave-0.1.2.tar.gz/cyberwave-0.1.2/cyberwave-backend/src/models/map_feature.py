from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Dict, Any
import enum

from src.db.base_class import Base

# Define FeatureType enum
class FeatureTypeEnum(str, enum.Enum):
    ZONE = "ZONE"
    POINT_OF_INTEREST = "POINT_OF_INTEREST"
    PATH = "PATH"
    RESTRICTED_AREA = "RESTRICTED_AREA"

class MapFeature(Base):
    __tablename__ = "map_features"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    feature_type: Mapped[FeatureTypeEnum] = mapped_column(SQLEnum(FeatureTypeEnum), nullable=False)
    # Using JSON to store flexible geometry (e.g., GeoJSON Point, Polygon, LineString)
    geometry: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    metadata_: Mapped[Dict[str, Any]] = mapped_column("metadata", JSON, nullable=True)

    # Foreign Keys
    map_id: Mapped[int] = mapped_column(ForeignKey("maps.id"), nullable=False)

    # Relationships
    map: Mapped["Map"] = relationship("Map", back_populates="map_features") 