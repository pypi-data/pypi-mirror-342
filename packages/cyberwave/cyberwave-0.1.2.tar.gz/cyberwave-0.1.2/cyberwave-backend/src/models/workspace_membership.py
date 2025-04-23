import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Enum as SQLEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
import enum

from src.db.base_class import Base

# Define Role enum if needed elsewhere, otherwise can be inline
class RoleEnum(str, enum.Enum):
    admin = "admin"
    member = "member"
    viewer = "viewer"

class WorkspaceMembership(Base):
    __tablename__ = "workspace_memberships"

    # Composite primary key
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"), primary_key=True)

    role: Mapped[RoleEnum] = mapped_column(SQLEnum(RoleEnum), nullable=False, default=RoleEnum.member)
    joined_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships to parent tables
    user: Mapped["User"] = relationship("User", back_populates="workspace_memberships")
    workspace: Mapped["Workspace"] = relationship("Workspace", back_populates="workspace_memberships") 