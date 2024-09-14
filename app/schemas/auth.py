from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel, EmailStr

# class UserCreate(BaseModel):
#     email: EmailStr
#     password: str
#     firstname: str
#     lastname: str
#     gender: str
#     dob: int
#     department_id: Optional[int] = None
#     project_id: Optional[int] = None
#     position_id: Optional[int] = None
#     photo: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str
