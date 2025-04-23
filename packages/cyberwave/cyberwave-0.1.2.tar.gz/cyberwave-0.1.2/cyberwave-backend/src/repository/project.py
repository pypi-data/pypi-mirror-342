from src.repository.base import CRUDBase
from src.models.project import Project
from src.schemas.project import ProjectCreate, ProjectUpdate

class ProjectRepository(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    # Add custom methods if needed, e.g., get by workspace ID
    pass

project_repo = ProjectRepository(Project) 