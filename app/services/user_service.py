"""User CRUD operations and business logic."""
from sqlalchemy.orm import Session
from typing import Optional

from app.models.user import User, Role
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password
from app.core.exceptions import ConflictException, NotFoundException


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Fetch a user by email."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> User:
    """Fetch a user by ID or raise 404."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundException("User not found")
    return user


def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user."""
    # Check email uniqueness
    if get_user_by_email(db, user.email):
        raise ConflictException("Email already registered")
    
    db_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        full_name=user.full_name,
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> User:
    """Update user information."""
    db_user = get_user_by_id(db, user_id)
    
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def list_users(db: Session, skip: int = 0, limit: int = 100) -> tuple[list[User], int]:
    """List all users with pagination."""
    total = db.query(User).count()
    users = db.query(User).offset(skip).limit(limit).all()
    return users, total


def delete_user(db: Session, user_id: int) -> None:
    """Delete a user."""
    db_user = get_user_by_id(db, user_id)
    db.delete(db_user)
    db.commit()
