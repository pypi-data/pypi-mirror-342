from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.services.level_service import level_service
from src.db.session import get_db_session

router = APIRouter()

@router.get("", response_model=List[schemas.LevelInDB])
async def read_levels(
    db: AsyncSession = Depends(get_db_session),
    project_id: Optional[int] = Query(None, description="Filter levels by project ID"),
    skip: int = 0,
    limit: int = 100,
):
    """Retrieve levels, optionally filtered by project."""
    levels = await level_service.get_levels(
        db=db, project_id=project_id, skip=skip, limit=limit
    )
    return levels

@router.post("", response_model=schemas.LevelInDB, status_code=status.HTTP_201_CREATED)
async def create_level(
    *,
    db: AsyncSession = Depends(get_db_session),
    level_in: schemas.LevelCreate,
):
    """Create a new level within a project."""
    # Add validation (e.g., ensure project_id exists) in service or here
    new_level = await level_service.create_level(db=db, level_in=level_in)
    return new_level

@router.get("/{level_id}", response_model=schemas.LevelInDB)
async def read_level_by_id(
    level_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    """Retrieve a specific level by ID."""
    level = await level_service.get_level_by_id(db=db, level_id=level_id)
    if not level:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Level with ID {level_id} not found",
        )
    return level

@router.put("/{level_id}", response_model=schemas.LevelInDB)
async def update_level(
    level_id: int,
    *,
    db: AsyncSession = Depends(get_db_session),
    level_in: schemas.LevelUpdate,
):
    """Update a specific level by ID."""
    db_level = await level_service.get_level_by_id(db=db, level_id=level_id)
    if not db_level:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Level with ID {level_id} not found",
        )
    # Prevent changing project_id via this endpoint if needed
    updated_level = await level_service.update_level(
        db=db, db_level=db_level, level_in=level_in
    )
    return updated_level

@router.delete("/{level_id}", response_model=schemas.LevelInDB)
async def delete_level(
    level_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    """Delete a specific level by ID."""
    deleted_level = await level_service.delete_level(db=db, level_id=level_id)
    if not deleted_level:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Level with ID {level_id} not found",
        )
    return deleted_level 