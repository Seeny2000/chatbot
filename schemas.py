from pydantic import BaseModel, EmailStr, Field,validator
from typing import Optional
import re
from fastapi import HTTPException

class AdminCreate(BaseModel):
    username: str = Field(..., min_length=3, description="Please enter a username")    
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long")

    @validator("password")
    def validate_password(cls, password: str):
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one numeric character")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("Password must contain at least one special character")
        return password
# class AdminCreate(BaseModel):    
#     username: str
#     email: EmailStr
#     password: str
#     @classmethod
#     def validate_password(cls, password: str):
#         if not re.search(r"\d", password):
#             raise ValueError("Password must contain at least one numeric character")
#         if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
#             raise ValueError("Password must contain at least one special character")
#         return password

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_password

class AdminLogin(BaseModel):
    username: str
    email: str
    password: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# class verifyOTP(BaseModel):
#     email: EmailStr
#     opt: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class ChatCreate(BaseModel):
    user_id: int
    username: Optional[str] = None
    password: Optional[str] = None
    message: Optional[str] = None
    response: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True