from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ApproveBase(BaseModel):
    is_approved: Optional[bool] = False
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    description: Optional[str] = None
    created_by: str
    updated_by: Optional[str] = None
    
class ApproveResponse(BaseModel):
    is_approved: Optional[bool] = False
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    description: Optional[str] = None
    created_by: str
    updated_by: Optional[str] = None



class ApproveCreate(ApproveBase):
    pass


class ApproveUpdate(ApproveBase):
    is_approved: Optional[bool]
    approved_by: Optional[str]
    approved_at: Optional[datetime]
    description: Optional[str]
    updated_by: Optional[str]


class ApproveOut(ApproveBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
