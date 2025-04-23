from src.repository.base import CRUDBase
from src.models.workspace import Workspace
from src.schemas.workspace import WorkspaceCreate, WorkspaceUpdate

class WorkspaceRepository(CRUDBase[Workspace, WorkspaceCreate, WorkspaceUpdate]):
    pass

workspace_repo = WorkspaceRepository(Workspace) 