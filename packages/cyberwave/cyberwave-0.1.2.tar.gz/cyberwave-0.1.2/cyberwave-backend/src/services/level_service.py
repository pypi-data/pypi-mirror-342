from typing import List, Optional
from datetime import datetime, timedelta, timezone # Import timezone
import logging # Import logging
import uuid # Import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status # Import HTTPException and status

from src import models, schemas, repository
from src.services.workspace_service import workspace_service # Need this for creating workspace
from src.services.project_service import project_service # Need this for creating project

# Get logger
logger = logging.getLogger(__name__)

# --- Default expiration for temporary levels --- 
TEMP_LEVEL_EXPIRATION_HOURS = 1

class LevelService:

    async def create_temporary_level(self, db: AsyncSession) -> models.Level:
        """
        Creates a temporary Workspace, Project, and Level for frictionless onboarding.
        """
        logger.info("Creating temporary resources for new session...")
        try:
            # 1. Create temporary Workspace
            temp_workspace_schema = schemas.WorkspaceCreate(name="Temporary Workspace")
            temp_workspace = await workspace_service.create_workspace(db=db, workspace_in=temp_workspace_schema)
            logger.info(f"Created temporary workspace ID: {temp_workspace.id}")

            # 2. Create temporary Project in that Workspace
            temp_project_schema = schemas.ProjectCreate(
                name="Temporary Project",
                workspace_id=temp_workspace.id
            )
            temp_project = await project_service.create_project(db=db, project_in=temp_project_schema)
            logger.info(f"Created temporary project ID: {temp_project.id}")

            # 3. Create temporary Level in that Project
            # We must ensure UTC for comparison
            expires_at = datetime.now(timezone.utc) + timedelta(hours=TEMP_LEVEL_EXPIRATION_HOURS)
            temp_level_schema = schemas.LevelCreate(
                name="Temporary Level",
                project_id=temp_project.id
            )
            # Use repository directly to allow setting status/expires_at before commit
            level_data = temp_level_schema.model_dump()
            db_level = models.Level(**level_data)
            db_level.status = models.LevelStatusEnum.TEMPORARY
            # Store timezone-aware datetime
            db_level.expires_at = expires_at 
            db_level.owner_id = None

            db.add(db_level)
            await db.commit()
            await db.refresh(db_level)

            logger.info(f"Created temporary level ID: {db_level.id} (Token: {db_level.share_token}), expires at {expires_at}")
            return db_level

        except Exception as e:
            logger.error(f"Failed to create temporary level resources: {e}", exc_info=True)
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create temporary session resources."
            ) 

    async def get_level_by_share_token(
        self, db: AsyncSession, share_token: str
    ) -> Optional[models.Level]:
        """Get a level by its share_token, checking for expiration."""
        logger.debug(f"Attempting to find level by share_token: {share_token}")
        try:
            token_uuid = uuid.UUID(share_token) 
        except ValueError:
            logger.warning(f"Invalid share_token format: {share_token}")
            return None

        query = select(models.Level).filter(models.Level.share_token == token_uuid)
        result = await db.execute(query)
        level = result.scalars().first()

        if not level:
            logger.debug(f"No level found for share_token: {share_token}")
            return None

        # Check expiration for temporary levels
        if level.status == models.LevelStatusEnum.TEMPORARY:
            # Ensure comparison is between timezone-aware datetimes
            if level.expires_at:
                # Make expires_at timezone-aware if it isn't already
                if level.expires_at.tzinfo is None:
                    level.expires_at = level.expires_at.replace(tzinfo=timezone.utc)
                if level.expires_at < datetime.now(timezone.utc):
                    logger.warning(f"Temporary level {level.id} (token: {share_token}) has expired.")
                    return None

        logger.debug(f"Found level {level.id} for share_token: {share_token}")
        return level

    async def get_levels(
        self,
        db: AsyncSession,
        project_id: Optional[int] = None, # Allow filtering by project
        skip: int = 0,
        limit: int = 100
    ) -> List[models.Level]:
        """Retrieve levels, optionally filtered by project."""
        if project_id is not None:
            query = select(models.Level).filter(models.Level.project_id == project_id).offset(skip).limit(limit)
            result = await db.execute(query)
            return result.scalars().all()
        else:
            return await repository.level_repo.get_multi(db, skip=skip, limit=limit)

    async def get_level_by_id(
        self, db: AsyncSession, level_id: int
    ) -> Optional[models.Level]:
        """Get a single level by ID."""
        return await repository.level_repo.get(db, id=level_id)

    async def create_level(
        self, db: AsyncSession, *, level_in: schemas.LevelCreate
    ) -> models.Level:
        """Create a new 'ACTIVE' level (use create_temporary_level for temp ones)."""
        level_data = level_in.model_dump()
        db_level = models.Level(**level_data)
        db_level.status = models.LevelStatusEnum.ACTIVE
        db_level.owner_id = None # TODO: Set owner later
        # Ensure expires_at is timezone-aware if set
        if db_level.expires_at and db_level.expires_at.tzinfo is None:
            db_level.expires_at = db_level.expires_at.replace(tzinfo=timezone.utc)

        db.add(db_level)
        await db.commit()
        await db.refresh(db_level)
        return db_level

    async def update_level(
        self,
        db: AsyncSession,
        *,
        db_level: models.Level,
        level_in: schemas.LevelUpdate
    ) -> models.Level:
        """Update an existing level."""
        return await repository.level_repo.update(db, db_obj=db_level, obj_in=level_in)

    async def delete_level(
        self, db: AsyncSession, *, level_id: int
    ) -> Optional[models.Level]:
        """Delete a level by ID."""
        # Add validation: e.g., check if level contains robots or assets
        return await repository.level_repo.remove(db, id=level_id)

level_service = LevelService() 