from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PositionCreate(BaseModel):
    position: str
    active: bool
    description: Optional[str] = None
    created_by: int

class PositionUpdate(BaseModel):
    position: Optional[str] = None
    active: Optional[bool] = None
    description: Optional[str] = None
    updated_by: Optional[int] = None

class PositionResponse(BaseModel):
    id: int
    position: str
    active: bool
    description: Optional[str] = None
    created_by: int
    created_at: datetime
    updated_by: Optional[int] = None
    updated_at: datetime

    class Config:
        orm_mode = True
