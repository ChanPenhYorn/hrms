from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EmployeeBase(BaseModel):
    __tablename__ = "employees"
    
   
    firstname: str
    lastname: str
    gender: str
    dob: int  # Date of birth as int (consider changing it to a proper date format)
    active: bool
    department_id: int
    project_id: int
    position_id: int
    photo: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    
    id: Optional[int] = None

    class Config:
        orm_mode = True
