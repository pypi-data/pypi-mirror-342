from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src import models, schemas, repository

class WorkspaceService:

    async def get_workspaces(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.Workspace]:
        """Retrieve workspaces with pagination."""
        # Business logic could go here (e.g., filtering based on user roles,
        # validating parameters, enriching data)
        workspaces = await repository.workspace_repo.get_multi(
            db, skip=skip, limit=limit
        )
        return workspaces

    async def get_workspace_by_id(
        self, db: AsyncSession, workspace_id: int
    ) -> Optional[models.Workspace]:
        """Get a single workspace by ID."""
        # Business logic could go here (e.g., check user permissions)
        return await repository.workspace_repo.get(db, id=workspace_id)

    async def create_workspace(
        self, db: AsyncSession, *, workspace_in: schemas.WorkspaceCreate
    ) -> models.Workspace:
        """Create a new workspace."""
        # Business logic could go here (e.g., check for duplicate names)
        # db_workspace = await repository.workspace_repo.get_by_name(db, name=workspace_in.name)
        # if db_workspace:
        #     raise HTTPException(status_code=400, detail="Workspace name already registered")
        return await repository.workspace_repo.create(db, obj_in=workspace_in)

    async def update_workspace(
        self,
        db: AsyncSession,
        *, 
        db_workspace: models.Workspace, # Pass the existing model
        workspace_in: schemas.WorkspaceUpdate
    ) -> models.Workspace:
        """Update an existing workspace."""
        # Business logic could go here (e.g., validate name changes)
        return await repository.workspace_repo.update(
            db, db_obj=db_workspace, obj_in=workspace_in
        )

    async def delete_workspace(
        self, db: AsyncSession, *, workspace_id: int
    ) -> Optional[models.Workspace]:
        """Delete a workspace by ID."""
        # Business logic could go here (e.g., check if workspace has projects)
        # Check if workspace exists first (handled by remove method implicitly, but could be explicit)
        deleted_workspace = await repository.workspace_repo.remove(db, id=workspace_id)
        # Trigger events if needed
        return deleted_workspace

workspace_service = WorkspaceService() 