from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class EmployeeBase(BaseModel):
    firstname: str = Field(..., max_length=255)
    lastname: str = Field(..., max_length=255)
    gender: Optional[str] = Field(None, max_length=10)
    dob: Optional[datetime] = None
    active: bool = Field(default=True)
    department_id: Optional[int] = None
    project_id: Optional[int] = None
    position_id: Optional[int] = None
    photo: Optional[str] = None
    email: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    password: str = Field(..., min_length=8)  # This is required for creating a new employee

class EmployeeUpdate(EmployeeBase):
    password: Optional[str] = None  # This is optional for updates

class EmployeeResponse(EmployeeBase):
    id: int

class EmployeeInDB(EmployeeBase):
    id: int
    created_at: datetime
    created_by: Optional[str] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None
# class EmployeeLogin():
#     email: EmailStr
#     password: str

    class Config:
        orm_mode = True
