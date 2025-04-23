from typing import List, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, status, Header, Response, Body
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas, models
from src.services.robot_service import robot_service
from src.services.level_service import level_service
from src.db.session import get_db_session

router = APIRouter()

@router.get("", response_model=List[schemas.RobotInDB])
async def read_robots(
    db: AsyncSession = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100,
    x_share_token: Optional[str] = Header(None, alias="X-Share-Token"),
):
    """Retrieve all robots. Requires X-Share-Token for temporary levels."""
    level_id_filter = None
    if x_share_token:
        level = await level_service.get_level_by_share_token(db, share_token=x_share_token)
        if not level:
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Share token is invalid, expired, or level not found."
            )
        level_id_filter = level.id
    else:
        pass

    robots = await robot_service.get_robots(db=db, skip=skip, limit=limit)
    return robots

class RobotCreateResponse(schemas.RobotInDB):
    share_token: Optional[str] = None
    share_url: Optional[str] = None

    class Config:
        from_attributes = True

@router.post("", response_model=RobotCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_robot(
    response: Response,
    *,
    db: AsyncSession = Depends(get_db_session),
    robot_in: schemas.RobotCreate = Body(..., embed=False),
    x_share_token: Optional[str] = Header(None, alias="X-Share-Token")
):
    """
    Register a new robot.
    - If `X-Share-Token` header is provided, adds robot to that session's level.
    - If no header and no `level_id` in body, creates a new temporary session.
    - If `level_id` in body and no header, requires standard auth (TODO).
    """
    level_id_to_use: Optional[int] = robot_in.level_id
    share_token_for_response: Optional[str] = None
    share_url_for_response: Optional[str] = None
    target_level: Optional[models.Level] = None

    if x_share_token:
        print(f"Received share token: {x_share_token}")
        target_level = await level_service.get_level_by_share_token(db, share_token=x_share_token)
        if not target_level:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Share token invalid/expired.")
        level_id_to_use = target_level.id
        if robot_in.level_id is not None and robot_in.level_id != level_id_to_use:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="level_id in body conflicts with X-Share-Token level.")
        print(f"Using existing level {level_id_to_use} from share token.")

    elif level_id_to_use is None:
        print("No share token or level_id in body, creating temporary session...")
        target_level = await level_service.create_temporary_level(db)
        level_id_to_use = target_level.id
        share_token_for_response = str(target_level.share_token)
        share_url_for_response = f"http://localhost:8000/shared/{share_token_for_response}"
        response.headers["X-Share-Token"] = share_token_for_response
        print(f"Created temporary level {level_id_to_use}. Token: {share_token_for_response}")

    else:
        print(f"Level ID {level_id_to_use} provided in body, no share token. (Auth TODO)")
        target_level = await level_service.get_level_by_id(db, level_id=level_id_to_use)
        if not target_level:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Level {level_id_to_use} not found.")
        if target_level.status == models.LevelStatusEnum.TEMPORARY:
             print(f"Warning: Adding robot to temporary level {target_level.id} using ID. Consider requiring token.")
             pass

    if level_id_to_use is None:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not determine target level ID.")

    final_robot_in_dict = robot_in.model_dump(exclude_unset=True)
    final_robot_in_dict['level_id'] = level_id_to_use
    final_robot_create = schemas.RobotCreate(**final_robot_in_dict)

    # Create the robot
    # Note: The hardcoded user (101) linking logic in RobotService might need review
    new_robot = await robot_service.create_robot(db=db, robot_in=final_robot_create)

    # Use the defined response model for serialization
    # FastAPI will automatically convert `new_robot` ORM object to `RobotCreateResponse`
    # We need to ensure the extra fields are available somehow if not on the ORM model
    # A cleaner way is to return a dictionary/Pydantic model explicitly
    response_content = schemas.RobotInDB.model_validate(new_robot) # Validate base fields
    
    # Manually create the final response model with extra fields
    final_response = RobotCreateResponse(
        **response_content.model_dump(), # Unpack validated base fields
        share_token=share_token_for_response, 
        share_url=share_url_for_response
    )

    return final_response

@router.get("/{robot_id}", response_model=schemas.RobotInDB)
async def read_robot_by_id(
    robot_id: int,
    db: AsyncSession = Depends(get_db_session),
    x_share_token: Optional[str] = Header(None, alias="X-Share-Token"),
):
    """Retrieve a specific robot by ID. Requires X-Share-Token for temp levels."""
    robot = await robot_service.get_robot_by_id(db=db, robot_id=robot_id)
    if not robot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Robot {robot_id} not found")

    if robot.level.status == models.LevelStatusEnum.TEMPORARY:
        if not x_share_token or str(robot.level.share_token) != x_share_token:
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access to robot requires valid X-Share-Token for its temporary level.")
        await level_service.get_level_by_share_token(db, share_token=x_share_token)

    return robot

@router.put("/{robot_id}", response_model=schemas.RobotInDB)
async def update_robot(
    robot_id: int,
    *,
    db: AsyncSession = Depends(get_db_session),
    robot_in: schemas.RobotUpdate,
    x_share_token: Optional[str] = Header(None, alias="X-Share-Token"),
):
    """Update a specific robot. Requires X-Share-Token for temp levels."""
    db_robot = await robot_service.get_robot_by_id(db=db, robot_id=robot_id)
    if not db_robot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Robot {robot_id} not found")

    if db_robot.level.status == models.LevelStatusEnum.TEMPORARY:
        if not x_share_token or str(db_robot.level.share_token) != x_share_token:
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access requires valid X-Share-Token for temporary level.")
        await level_service.get_level_by_share_token(db, share_token=x_share_token)

    if robot_in.level_id is not None and robot_in.level_id != db_robot.level_id:
        print(f"Warning: Robot level change requested from {db_robot.level_id} to {robot_in.level_id}. (Validation TODO)")

    updated_robot = await robot_service.update_robot(db=db, db_robot=db_robot, robot_in=robot_in)
    return updated_robot

@router.delete("/{robot_id}", response_model=schemas.RobotInDB)
async def delete_robot(
    robot_id: int,
    db: AsyncSession = Depends(get_db_session),
    x_share_token: Optional[str] = Header(None, alias="X-Share-Token"),
):
    """Delete a specific robot. Requires X-Share-Token for temp levels."""
    db_robot = await robot_service.get_robot_by_id(db=db, robot_id=robot_id)
    if not db_robot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Robot {robot_id} not found")
    
    if db_robot.level.status == models.LevelStatusEnum.TEMPORARY:
        if not x_share_token or str(db_robot.level.share_token) != x_share_token:
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access requires valid X-Share-Token for temporary level.")
        await level_service.get_level_by_share_token(db, share_token=x_share_token)

    deleted_robot = await robot_service.delete_robot(db=db, robot_id=robot_id)
    if not deleted_robot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Robot {robot_id} not found during deletion.")
        
    return deleted_robot 