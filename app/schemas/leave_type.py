from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LeaveTypeBase(BaseModel):
    type: str
    description: Optional[str] = None
    created_by: str
    updated_by: Optional[str] = None
    active: Optional[bool] = True

class LeaveTypeCreate(LeaveTypeBase):
    pass

class LeaveTypeUpdate(LeaveTypeBase):
    pass

class LeaveTypeResponse(LeaveTypeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
