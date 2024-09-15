from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class AttendanceBase(BaseModel):
    type: str
    employee_id: int
    action_at: datetime
    status: str
    created_by: str
    updated_by: Optional[str] = None
    working_date: date

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdate(AttendanceBase):
    pass

class AttendanceResponse(AttendanceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
