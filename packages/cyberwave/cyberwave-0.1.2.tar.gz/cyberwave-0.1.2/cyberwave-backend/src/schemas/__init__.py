# Import schemas for easy access
from .base import BaseSchema, CreateSchema, UpdateSchema, InDBSchema
from .user import UserBase, UserCreate, UserInDB
from .workspace import WorkspaceBase, WorkspaceCreate, WorkspaceUpdate, WorkspaceInDB
from .workspace_membership import WorkspaceMembershipBase, WorkspaceMembershipCreate, WorkspaceMembershipInDB
from .project import ProjectBase, ProjectCreate, ProjectUpdate, ProjectInDB
from .map import MapBase, MapCreate, MapInDB
from .level import LevelBase, LevelCreate, LevelUpdate, LevelInDB
from .map_feature import MapFeatureBase, MapFeatureCreate, MapFeatureInDB
from .fixed_asset import FixedAssetBase, FixedAssetCreate, FixedAssetInDB
from .robot import RobotBase, RobotCreate, RobotUpdate, RobotInDB

__all__ = [
    "BaseSchema", "CreateSchema", "UpdateSchema", "InDBSchema",
    "UserBase", "UserCreate", "UserInDB",
    "WorkspaceBase", "WorkspaceCreate", "WorkspaceUpdate", "WorkspaceInDB",
    "WorkspaceMembershipBase", "WorkspaceMembershipCreate", "WorkspaceMembershipInDB",
    "ProjectBase", "ProjectCreate", "ProjectUpdate", "ProjectInDB",
    "MapBase", "MapCreate", "MapInDB",
    "LevelBase", "LevelCreate", "LevelUpdate", "LevelInDB",
    "MapFeatureBase", "MapFeatureCreate", "MapFeatureInDB",
    "FixedAssetBase", "FixedAssetCreate", "FixedAssetInDB",
    "RobotBase", "RobotCreate", "RobotUpdate", "RobotInDB",
]
