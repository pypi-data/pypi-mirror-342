from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.services.project_service import project_service
from src.db.session import get_db_session

router = APIRouter()

@router.get("", response_model=List[schemas.ProjectInDB])
async def read_projects(
    db: AsyncSession = Depends(get_db_session),
    workspace_id: Optional[int] = Query(None, description="Filter projects by workspace ID"),
    skip: int = 0,
    limit: int = 100,
):
    """Retrieve projects, optionally filtered by workspace."""
    projects = await project_service.get_projects(
        db=db, workspace_id=workspace_id, skip=skip, limit=limit
    )
    return projects

@router.post("", response_model=schemas.ProjectInDB, status_code=status.HTTP_201_CREATED)
async def create_project(
    *,
    db: AsyncSession = Depends(get_db_session),
    project_in: schemas.ProjectCreate,
):
    """Create a new project within a workspace."""
    # Add validation (e.g., ensure workspace_id exists) in service or here
    new_project = await project_service.create_project(db=db, project_in=project_in)
    return new_project

@router.get("/{project_id}", response_model=schemas.ProjectInDB)
async def read_project_by_id(
    project_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    """Retrieve a specific project by ID."""
    project = await project_service.get_project_by_id(db=db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found",
        )
    return project

@router.put("/{project_id}", response_model=schemas.ProjectInDB)
async def update_project(
    project_id: int,
    *,
    db: AsyncSession = Depends(get_db_session),
    project_in: schemas.ProjectUpdate,
):
    """Update a specific project by ID."""
    db_project = await project_service.get_project_by_id(db=db, project_id=project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found",
        )
    # Prevent changing workspace_id via this endpoint if needed
    # if project_in.workspace_id is not None and project_in.workspace_id != db_project.workspace_id:
    #     raise HTTPException(status_code=400, detail="Cannot change workspace ID via this endpoint")
    updated_project = await project_service.update_project(
        db=db, db_project=db_project, project_in=project_in
    )
    return updated_project

@router.delete("/{project_id}", response_model=schemas.ProjectInDB)
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    """Delete a specific project by ID."""
    deleted_project = await project_service.delete_project(db=db, project_id=project_id)
    if not deleted_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found",
        )
    return deleted_project 