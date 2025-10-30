from pydantic import BaseModel, EmailStr
from typing import Literal

class UserIn(BaseModel):
    """User registration/creation"""
    email: EmailStr
    password: str
    role: Literal["admin", "user"] = "user"

class UserOut(BaseModel):
    """User response"""
    id: str
    email: str
    role: str

class LoginRequest(BaseModel):
    """Login credentials"""
    email: EmailStr
    password: str

