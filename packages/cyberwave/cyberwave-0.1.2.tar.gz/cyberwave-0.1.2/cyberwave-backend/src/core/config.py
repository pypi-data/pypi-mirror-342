import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "CyberWave Backend - Robot Registry"
    API_V1_STR: str = "/api/v1"

    # Database configuration - Default to SQLite
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./cyberwave.db")

    class Config:
        # If you have a .env file, settings will be loaded from it
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings() 