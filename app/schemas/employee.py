from pydantic import BaseModel
from typing import Optional

class EmployeeBase(BaseModel):
    name: str
    position: str
    salary: float

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    name: Optional[str] = None
    position: Optional[str] = None
    salary: Optional[float] = None

class Employee(EmployeeBase):
    id: int

    class Config:
        orm_mode = True
