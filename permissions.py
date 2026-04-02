"""
Role-Based Access Control (RBAC) — permission guards as FastAPI dependencies.

Role hierarchy:
    viewer  → can view records only
    analyst → viewer + dashboard analytics
    admin   → analyst + create/update/delete records + manage users

Usage in routers:
    @router.post("/records", dependencies=[Depends(require_admin)])
    @router.get("/dashboard", dependencies=[Depends(require_analyst)])
"""
from fastapi import Depends, HTTPException, status

from app.dependencies import get_current_active_user
from app.models.user import Role, User

# Role ordering for hierarchy checks
ROLE_RANK = {Role.viewer: 0, Role.analyst: 1, Role.admin: 2}


def _require_role(minimum_role: Role):
    """Factory: returns a dependency that enforces a minimum role level."""
    def _checker(current_user: User = Depends(get_current_active_user)) -> User:
        if ROLE_RANK[current_user.role] < ROLE_RANK[minimum_role]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: '{minimum_role.value}' or higher. "
                       f"Your role: '{current_user.role.value}'.",
            )
        return current_user
    return _checker


# Convenient named dependencies — import and use directly in routers
require_viewer  = _require_role(Role.viewer)   # Any authenticated active user
require_analyst = _require_role(Role.analyst)  # Analyst or Admin
require_admin   = _require_role(Role.admin)    # Admin only
