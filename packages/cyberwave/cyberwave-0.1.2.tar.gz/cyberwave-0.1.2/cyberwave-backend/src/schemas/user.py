from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Basic User schema for seeding reference (expand later)
class UserBase(BaseModel):
    email: EmailStr
    external_auth_id: str
    name: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserInDB(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 