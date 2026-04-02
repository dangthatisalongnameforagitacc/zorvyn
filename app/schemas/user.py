"""User request and response schemas."""
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import Role


class UserCreate(BaseModel):
    """Request body for creating a new user."""
    email: EmailStr
    password: str
    full_name: str = ""
    role: Role = Role.viewer


class UserUpdate(BaseModel):
    """Request body for updating user information."""
    full_name: Optional[str] = None
    role: Optional[Role] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    """User data in responses (no password)."""
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True
