"""Dependency injection for authentication and authorization."""
from fastapi import Depends, Header
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.core.security import decode_token
from app.core.exceptions import UnauthorizedException


async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
) -> User:
    """Get the current authenticated user from JWT token."""
    if not authorization:
        raise UnauthorizedException("Missing authorization header")
    
    # Extract token from "Bearer <token>"
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise UnauthorizedException("Invalid authentication scheme")
    except ValueError:
        raise UnauthorizedException("Invalid authorization header format")
    
    # Decode and verify token
    payload = decode_token(token)
    if not payload:
        raise UnauthorizedException("Invalid or expired token")
    
    user_id: int = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Invalid token")
    
    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UnauthorizedException("User not found")
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Ensure the current user is active."""
    if not current_user.is_active:
        raise UnauthorizedException("User account is inactive")
    
    return current_user
