import datetime
import uuid
import enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, UUID, func, Enum as SQLEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional

from src.db.base_class import Base

def default_uuid():
    return uuid.uuid4()

# Define LevelStatus enum
class LevelStatusEnum(str, enum.Enum):
    TEMPORARY = "temporary"
    PENDING_VERIFICATION = "pending_verification"
    ACTIVE = "active"
    # ARCHIVED = "archived" # Maybe later?

class Level(Base):
    __tablename__ = "levels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    share_token: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, index=True, default=default_uuid
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    # --- New Fields --- 
    status: Mapped[LevelStatusEnum] = mapped_column(
        SQLEnum(LevelStatusEnum), nullable=False, default=LevelStatusEnum.ACTIVE, server_default=LevelStatusEnum.ACTIVE.value
    )
    owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    expires_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    # --- End New Fields ---

    # Foreign Keys
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    primary_map_id: Mapped[Optional[int]] = mapped_column(ForeignKey("maps.id"), nullable=True)

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="levels")
    primary_map: Mapped[Optional["Map"]] = relationship("Map", back_populates="levels", foreign_keys=[primary_map_id])
    robots: Mapped[List["Robot"]] = relationship(
        "Robot", back_populates="level", cascade="all, delete-orphan"
    )
    fixed_assets: Mapped[List["FixedAsset"]] = relationship(
        "FixedAsset", back_populates="level", cascade="all, delete-orphan"
    )
    # --- New Relationship --- 
    owner: Mapped[Optional["User"]] = relationship("User") # Simple relationship to owner
    # --- End New Relationship --- 