# Import repositories for easy access
from .user import user_repo
from .workspace import workspace_repo
from .workspace_membership import workspace_membership_repo
from .project import project_repo
from .map import map_repo
from .level import level_repo
from .map_feature import map_feature_repo
from .fixed_asset import fixed_asset_repo
from .robot import robot_repo

__all__ = [
    "user_repo",
    "workspace_repo",
    "workspace_membership_repo",
    "project_repo",
    "map_repo",
    "level_repo",
    "map_feature_repo",
    "fixed_asset_repo",
    "robot_repo",
]
