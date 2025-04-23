from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Shared properties
class BaseSchema(BaseModel):
    pass

# Properties to receive via API on creation
class CreateSchema(BaseSchema):
    pass

# Properties to receive via API on update
class UpdateSchema(BaseSchema):
    pass

# Properties shared by models stored in DB
class InDBSchema(BaseSchema):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True # Replace orm_mode = True 