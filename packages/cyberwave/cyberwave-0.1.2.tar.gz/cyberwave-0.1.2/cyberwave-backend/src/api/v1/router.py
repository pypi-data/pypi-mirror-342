from fastapi import APIRouter

from src.api.v1.endpoints import workspaces, robots, projects, levels

api_router = APIRouter()

# Include endpoint routers here
api_router.include_router(workspaces.router, prefix="/workspaces", tags=["Workspaces"])
api_router.include_router(robots.router, prefix="/robots", tags=["Robots"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
api_router.include_router(levels.router, prefix="/levels", tags=["Levels"])
# Add other routers like levels, etc. later
# api_router.include_router(projects.router, prefix="/projects", tags=["Projects"]) 