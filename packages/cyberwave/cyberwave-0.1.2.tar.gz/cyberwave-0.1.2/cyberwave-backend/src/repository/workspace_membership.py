from typing import Optional # Import Optional
from sqlalchemy.ext.asyncio import AsyncSession # Import AsyncSession
from sqlalchemy import select # Import select

from src.repository.base import CRUDBase
from src.models.workspace_membership import WorkspaceMembership
from src.schemas.workspace_membership import WorkspaceMembershipCreate, WorkspaceMembershipInDB # Placeholder Update

# Note: CRUD for join tables often needs custom logic, base might not be fully suitable
class WorkspaceMembershipRepository(CRUDBase[WorkspaceMembership, WorkspaceMembershipCreate, WorkspaceMembershipInDB]): # Replace InDB with Update
    
    async def get_by_user_and_workspace(
        self, db: AsyncSession, *, user_id: int, workspace_id: int
    ) -> Optional[WorkspaceMembership]:
        """Get a specific membership entry by user ID and workspace ID."""
        query = select(self.model).filter(
            self.model.user_id == user_id,
            self.model.workspace_id == workspace_id
        )
        result = await db.execute(query)
        return result.scalars().first()

workspace_membership_repo = WorkspaceMembershipRepository(WorkspaceMembership) 