from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select # Needed for custom queries

from src import models, schemas, repository

class ProjectService:

    async def get_projects(
        self,
        db: AsyncSession,
        workspace_id: Optional[int] = None, # Allow filtering by workspace
        skip: int = 0,
        limit: int = 100
    ) -> List[models.Project]:
        """Retrieve projects, optionally filtered by workspace."""
        # Example of adding custom query logic beyond base repository
        if workspace_id is not None:
            query = select(models.Project).filter(models.Project.workspace_id == workspace_id).offset(skip).limit(limit)
            result = await db.execute(query)
            return result.scalars().all()
        else:
            # Use base repository method if no filter
            return await repository.project_repo.get_multi(db, skip=skip, limit=limit)

    async def get_project_by_id(
        self, db: AsyncSession, project_id: int
    ) -> Optional[models.Project]:
        """Get a single project by ID."""
        return await repository.project_repo.get(db, id=project_id)

    async def create_project(
        self, db: AsyncSession, *, project_in: schemas.ProjectCreate
    ) -> models.Project:
        """Create a new project."""
        # Add validation: e.g., check if workspace_id exists
        # workspace = await repository.workspace_repo.get(db, id=project_in.workspace_id)
        # if not workspace:
        #     raise HTTPException(status_code=404, detail="Workspace not found")
        return await repository.project_repo.create(db, obj_in=project_in)

    async def update_project(
        self,
        db: AsyncSession,
        *,
        db_project: models.Project,
        project_in: schemas.ProjectUpdate
    ) -> models.Project:
        """Update an existing project."""
        return await repository.project_repo.update(db, db_obj=db_project, obj_in=project_in)

    async def delete_project(
        self, db: AsyncSession, *, project_id: int
    ) -> Optional[models.Project]:
        """Delete a project by ID."""
        # Add validation: e.g., check if project contains levels
        return await repository.project_repo.remove(db, id=project_id)

project_service = ProjectService() 