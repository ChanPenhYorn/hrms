from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DepartmentBase(BaseModel):
    name: str = Field(..., max_length=255)
    active: bool = Field(default=True)
    created_by: str = Field(..., max_length=255)
    updated_by: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=255)

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(DepartmentBase):
    pass
    
class DepartmentResponse(DepartmentBase):
    id: int

class DepartmentInDB(DepartmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
