"""User model and role enumeration."""
from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum as SQLEnum, Boolean, DateTime
from app.database import Base


class Role(str, Enum):
    """Role hierarchy: viewer < analyst < admin."""
    viewer = "viewer"
    analyst = "analyst"
    admin = "admin"


class User(Base):
    """User account with role-based access control."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, default="")
    role = Column(SQLEnum(Role), default=Role.viewer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role}, is_active={self.is_active})>"
