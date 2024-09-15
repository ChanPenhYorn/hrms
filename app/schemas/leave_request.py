from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class LeaveRequestBase(BaseModel):
    employee_id: int
    reason: str
    leave_type_id: int
    start_date: date
    end_date: date
    status: str
    requested_on: Optional[date] = None
    approved_id: Optional[int] = None
    created_by: str
    updated_by: Optional[str] = None

class LeaveRequestCreate(LeaveRequestBase):
    pass

class LeaveRequestUpdate(LeaveRequestBase):
    pass

class LeaveRequestResponse(LeaveRequestBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
