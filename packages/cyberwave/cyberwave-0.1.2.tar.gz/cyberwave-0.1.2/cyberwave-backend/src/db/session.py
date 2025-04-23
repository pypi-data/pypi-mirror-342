from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

# Create async engine
engine_args = {
    "pool_pre_ping": True, # Check connection before using it
    "echo": False # Set to True for debugging SQL statements
}

# Add connect_args specifically for SQLite
if settings.DATABASE_URL.startswith("sqlite"):
    engine_args["connect_args"] = {"check_same_thread": False}

engine = create_async_engine(settings.DATABASE_URL, **engine_args)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False, # Keep objects accessible after commit
    autoflush=False,
    autocommit=False
)

async def get_db_session() -> AsyncSession:
    """FastAPI dependency to get an async database session."""
    async with AsyncSessionLocal() as session:
        yield session 