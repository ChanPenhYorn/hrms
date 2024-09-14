from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    active: bool
    created_by: str

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = None
    updated_by: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    active: bool
    created_by: str
    created_at: date
    updated_by: Optional[str] = None
    updated_at: date

    class Config:
        orm_mode = True
