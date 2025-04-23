from fastapi import FastAPI

from src.core.config import settings
# Import the main API router
from src.api.v1.router import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Basic health check endpoint
@app.get("/health", tags=["Health"])
def read_root():
    return {"status": "OK"}

# Include the main API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Placeholder for future startup/shutdown events
@app.on_event("startup")
async def startup_event():
    pass

@app.on_event("shutdown")
async def shutdown_event():
    pass 