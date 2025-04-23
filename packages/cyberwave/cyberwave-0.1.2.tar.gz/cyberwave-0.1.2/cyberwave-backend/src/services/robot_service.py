from typing import List, Optional
import logging # Import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status # Import HTTPException

from src import models, schemas, repository

# Get a logger instance
logger = logging.getLogger(__name__)

class RobotService:

    async def get_robots(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.Robot]:
        """Retrieve robots with pagination."""
        # TODO: Add filtering by level_id or other criteria
        return await repository.robot_repo.get_multi(db, skip=skip, limit=limit)

    async def get_robot_by_id(
        self, db: AsyncSession, robot_id: int
    ) -> Optional[models.Robot]:
        """Get a single robot by ID."""
        return await repository.robot_repo.get(db, id=robot_id)

    async def create_robot(
        self, db: AsyncSession, *, robot_in: schemas.RobotCreate
    ) -> models.Robot:
        """Create a new robot record in the database."""
        # Basic validation (e.g., level_id is provided implicitly now by endpoint)
        if robot_in.level_id is None:
             # This shouldn't happen if endpoint logic is correct
             raise ValueError("level_id must be provided to create_robot service method")

        logger.info(f"Creating robot '{robot_in.name}' for level {robot_in.level_id}")
        # The core repository create method handles DB interaction
        new_robot = await repository.robot_repo.create(db, obj_in=robot_in)
        return new_robot

    async def update_robot(
        self,
        db: AsyncSession,
        *,
        db_robot: models.Robot,
        robot_in: schemas.RobotUpdate
    ) -> models.Robot:
        """Update an existing robot."""
        # Add validation for status transitions, etc. if needed
        return await repository.robot_repo.update(db, db_obj=db_robot, obj_in=robot_in)

    async def delete_robot(
        self, db: AsyncSession, *, robot_id: int
    ) -> Optional[models.Robot]:
        """Delete a robot by ID."""
        # Add logic to check if robot is currently active, etc. if needed
        return await repository.robot_repo.remove(db, id=robot_id)

robot_service = RobotService() 