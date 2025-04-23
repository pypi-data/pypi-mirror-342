from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
# Import the service instead of the repository
from src.services.workspace_service import workspace_service
from src.db.session import get_db_session

router = APIRouter()

@router.get("", response_model=List[schemas.WorkspaceInDB])
async def read_workspaces(
    db: AsyncSession = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100,
):
    """Retrieve all workspaces."""
    # Call the service layer method
    workspaces = await workspace_service.get_workspaces(db=db, skip=skip, limit=limit)
    return workspaces

@router.post("", response_model=schemas.WorkspaceInDB, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    *, # Enforce keyword-only arguments
    db: AsyncSession = Depends(get_db_session),
    workspace_in: schemas.WorkspaceCreate,
):
    """Create a new workspace."""
    # Add logic here or in the service to check for duplicate names if needed
    new_workspace = await workspace_service.create_workspace(db=db, workspace_in=workspace_in)
    return new_workspace

@router.get("/{workspace_id}", response_model=schemas.WorkspaceInDB)
async def read_workspace_by_id(
    workspace_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    """Retrieve a specific workspace by ID."""
    workspace = await workspace_service.get_workspace_by_id(db=db, workspace_id=workspace_id)
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workspace with ID {workspace_id} not found",
        )
    return workspace

@router.put("/{workspace_id}", response_model=schemas.WorkspaceInDB)
async def update_workspace(
    workspace_id: int,
    *, # Enforce keyword-only arguments
    db: AsyncSession = Depends(get_db_session),
    workspace_in: schemas.WorkspaceUpdate,
):
    """Update a specific workspace by ID."""
    db_workspace = await workspace_service.get_workspace_by_id(db=db, workspace_id=workspace_id)
    if not db_workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workspace with ID {workspace_id} not found",
        )
    updated_workspace = await workspace_service.update_workspace(
        db=db, db_workspace=db_workspace, workspace_in=workspace_in
    )
    return updated_workspace

@router.delete("/{workspace_id}", response_model=schemas.WorkspaceInDB)
async def delete_workspace(
    workspace_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    """Delete a specific workspace by ID."""
    deleted_workspace = await workspace_service.delete_workspace(db=db, workspace_id=workspace_id)
    if not deleted_workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workspace with ID {workspace_id} not found",
        )
    # Optionally return the deleted object or just status 204 No Content
    return deleted_workspace

# Add other workspace endpoints (POST, GET by ID, PUT, DELETE) here later 