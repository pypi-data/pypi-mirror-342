import asyncio
import json
import logging
import os
from datetime import datetime
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

# Adjust imports based on your project structure
# Ensure the script can find the 'src' directory
import sys
# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.db.session import AsyncSessionLocal
from src.models import (
    User, Workspace, Project, Map, Level, MapFeature,
    FixedAsset, Robot, WorkspaceMembership
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Relative path to the seed data file from this script's location
SEED_DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'seed-data.json')

# Helper to parse datetime strings, handling potential None
def parse_datetime(dt_str: str | None) -> datetime | None:
    if dt_str is None:
        return None
    try:
        # Attempt ISO format with timezone 'Z'
        return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    except ValueError:
        logger.warning(f"Could not parse datetime string: {dt_str}")
        return None

# Helper to parse UUID strings, handling potential None
def parse_uuid(uuid_str: str | None) -> UUID | None:
    if uuid_str is None:
        return None
    try:
        return UUID(uuid_str)
    except ValueError:
        logger.warning(f"Could not parse UUID string: {uuid_str}")
        return None

async def seed_data(db: AsyncSession):
    logger.info("Starting database seeding...")

    try:
        with open(SEED_DATA_FILE, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.error(f"Seed data file not found at: {SEED_DATA_FILE}")
        return
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {SEED_DATA_FILE}: {e}")
        return

    # Seeding order matters due to foreign key constraints

    # 1. Users
    logger.info("Seeding Users...")
    for user_data in data.get("users", []):
        db_user = User(
            id=user_data.get("id"),
            external_auth_id=user_data.get("external_auth_id"),
            email=user_data.get("email"),
            name=user_data.get("name"),
            created_at=parse_datetime(user_data.get("created_at"))
        )
        db.add(db_user)

    # 2. Workspaces
    logger.info("Seeding Workspaces...")
    for ws_data in data.get("workspaces", []):
        db_ws = Workspace(
            id=ws_data.get("id"),
            name=ws_data.get("name"),
            created_at=parse_datetime(ws_data.get("created_at"))
        )
        db.add(db_ws)

    # 3. Projects
    logger.info("Seeding Projects...")
    for proj_data in data.get("projects", []):
        db_proj = Project(
            id=proj_data.get("id"),
            workspace_id=proj_data.get("workspace_id"),
            name=proj_data.get("name"),
            created_at=parse_datetime(proj_data.get("created_at"))
        )
        db.add(db_proj)

    # 4. Maps
    logger.info("Seeding Maps...")
    for map_data in data.get("maps", []):
        db_map = Map(
            id=map_data.get("id"),
            project_id=map_data.get("project_id"),
            name=map_data.get("name"),
            map_type=map_data.get("map_type"),
            map_data_uri=map_data.get("map_data_uri"),
            origin_pose=map_data.get("origin_pose"),
            resolution=map_data.get("resolution"),
            created_at=parse_datetime(map_data.get("created_at"))
        )
        db.add(db_map)

    # 5. Levels
    logger.info("Seeding Levels...")
    for level_data in data.get("levels", []):
        db_level = Level(
            id=level_data.get("id"),
            project_id=level_data.get("project_id"),
            primary_map_id=level_data.get("primary_map_id"),
            name=level_data.get("name"),
            share_token=parse_uuid(level_data.get("share_token")), # Use helper
            description=level_data.get("description"),
            created_at=parse_datetime(level_data.get("created_at"))
        )
        db.add(db_level)

    # 6. Map Features
    logger.info("Seeding Map Features...")
    for feature_data in data.get("mapFeatures", []):
        db_feature = MapFeature(
            id=feature_data.get("id"),
            map_id=feature_data.get("map_id"),
            name=feature_data.get("name"),
            feature_type=feature_data.get("feature_type"),
            geometry=feature_data.get("geometry"),
            metadata_=feature_data.get("metadata") # Note the underscore mapping
        )
        db.add(db_feature)

    # 7. Fixed Assets
    logger.info("Seeding Fixed Assets...")
    for asset_data in data.get("fixedAssets", []):
        db_asset = FixedAsset(
            id=asset_data.get("id"),
            level_id=asset_data.get("level_id"),
            name=asset_data.get("name"),
            asset_type=asset_data.get("asset_type"),
            status=asset_data.get("status"),
            location=asset_data.get("location"),
            properties=asset_data.get("properties")
        )
        db.add(db_asset)

    # 8. Robots
    logger.info("Seeding Robots...")
    for robot_data in data.get("robots", []):
        db_robot = Robot(
            id=robot_data.get("id"),
            level_id=robot_data.get("level_id"),
            name=robot_data.get("name"),
            robot_type=robot_data.get("robot_type"),
            serial_number=robot_data.get("serial_number"),
            status=robot_data.get("status"),
            capabilities=robot_data.get("capabilities"),
            initial_pos_x=robot_data.get("initial_pos_x"),
            initial_pos_y=robot_data.get("initial_pos_y"),
            initial_pos_z=robot_data.get("initial_pos_z"),
            metadata_=robot_data.get("metadata"), # Note the underscore mapping
            current_battery_percentage=robot_data.get("current_battery_percentage"),
            registration_date=parse_datetime(robot_data.get("registration_date"))
        )
        db.add(db_robot)

    # 9. Workspace Memberships (after Users and Workspaces)
    logger.info("Seeding Workspace Memberships...")
    for membership_data in data.get("workspaceMemberships", []):
        db_membership = WorkspaceMembership(
            user_id=membership_data.get("user_id"),
            workspace_id=membership_data.get("workspace_id"),
            role=membership_data.get("role"),
            joined_at=parse_datetime(membership_data.get("joined_at"))
        )
        db.add(db_membership)

    try:
        await db.commit()
        logger.info("Database successfully seeded.")
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"Database seeding failed due to integrity error: {e}")
        logger.error("Data might already exist or there's a constraint violation.")
    except Exception as e:
        await db.rollback()
        logger.error(f"An unexpected error occurred during seeding commit: {e}")

async def main():
    logger.info("Initializing database session for seeding...")
    async with AsyncSessionLocal() as session:
        await seed_data(session)

if __name__ == "__main__":
    # Ensure the event loop is managed correctly
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main()) 