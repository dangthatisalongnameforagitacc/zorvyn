"""User management routers. Admin only."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services import user_service
from app.core.permissions import require_admin

router = APIRouter(prefix="/users", tags=["User Management"])


@router.get("/", response_model=list[UserResponse])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """List all users. Admin only."""
    users, _ = user_service.list_users(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """Create a new user. Admin only."""
    user = user_service.create_user(db, payload)
    return user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """Get a user by ID. Admin only."""
    user = user_service.get_user_by_id(db, user_id)
    return user


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """Update a user. Admin only."""
    user = user_service.update_user(db, user_id, payload)
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """Delete a user. Admin only."""
    user_service.delete_user(db, user_id)
