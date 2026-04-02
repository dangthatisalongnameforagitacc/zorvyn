"""Authentication request and response schemas."""
from pydantic import BaseModel, EmailStr


class TokenRequest(BaseModel):
    """Login request with email and password."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response after successful authentication."""
    access_token: str
    token_type: str = "bearer"


class Me(BaseModel):
    """Current user information."""
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True
