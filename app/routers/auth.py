"""Authentication routers."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import TokenRequest, TokenResponse, Me
from app.models.user import User
from app.services import user_service
from app.core.security import verify_password, create_access_token
from app.dependencies import get_current_active_user
from app.core.exceptions import UnauthorizedException

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(
    payload: TokenRequest,
    db: Session = Depends(get_db),
):
    """
    Register a new user.
    
    Returns a JWT token for immediate login.
    """
    # Create user with viewer role by default
    from app.schemas.user import UserCreate
    
    try:
        user = user_service.create_user(
            db,
            UserCreate(
                email=payload.email,
                password=payload.password,
                full_name="",
                role="viewer",
            ),
        )
    except Exception as e:
        raise UnauthorizedException(f"Registration failed: {str(e)}")
    
    # Issue token
    access_token = create_access_token(data={"sub": user.id})
    return TokenResponse(access_token=access_token)


@router.post("/login", response_model=TokenResponse)
def login(
    payload: TokenRequest,
    db: Session = Depends(get_db),
):
    """
    Login with email and password.
    
    Returns a JWT token.
    """
    user = user_service.get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise UnauthorizedException("Invalid email or password")
    
    if not user.is_active:
        raise UnauthorizedException("User account is inactive")
    
    access_token = create_access_token(data={"sub": user.id})
    return TokenResponse(access_token=access_token)


@router.get("/me", response_model=Me)
async def get_me(current_user: User = Depends(get_current_active_user)):
    """Get current authenticated user information."""
    return Me(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role.value,
        is_active=current_user.is_active,
    )
