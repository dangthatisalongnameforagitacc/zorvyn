"""Dashboard analytics routers."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.core.permissions import require_analyst
from app.services.dashboard_service import (
    get_summary,
    get_category_totals,
    get_monthly_trends,
    get_weekly_trends,
    get_recent_activity,
    get_dashboard_data,
)
from app.schemas.dashboard import (
    DashboardSummary,
    CategoryTotal,
    MonthlyTrend,
    WeeklyTrend,
    RecentActivity,
    DashboardData,
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard Analytics"])


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    _: User = Depends(require_analyst),
):
    """
    Get overall financial summary.
    
    Includes: total income, total expenses, net balance, record count.
    Available to analysts and admins.
    """
    return get_summary(db)


@router.get("/categories", response_model=list[CategoryTotal])
def get_category_breakdown(
    db: Session = Depends(get_db),
    _: User = Depends(require_analyst),
):
    """
    Get financial totals by category and type.
    
    Available to analysts and admins.
    """
    return get_category_totals(db)


@router.get("/trends/monthly", response_model=list[MonthlyTrend])
def get_monthly_data(
    months: int = Query(12, ge=1, le=60),
    db: Session = Depends(get_db),
    _: User = Depends(require_analyst),
):
    """
    Get monthly income vs expenses trends.
    
    Available to analysts and admins.
    """
    return get_monthly_trends(db, months=months)


@router.get("/trends/weekly", response_model=list[WeeklyTrend])
def get_weekly_data(
    weeks: int = Query(8, ge=1, le=52),
    db: Session = Depends(get_db),
    _: User = Depends(require_analyst),
):
    """
    Get weekly income vs expenses trends.
    
    Available to analysts and admins.
    """
    return get_weekly_trends(db, weeks=weeks)


@router.get("/recent", response_model=list[RecentActivity])
def get_recent_activity_list(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(require_analyst),
):
    """
    Get recently created financial records.
    
    Available to analysts and admins.
    """
    return get_recent_activity(db, limit=limit)


@router.get("/", response_model=DashboardData)
def get_full_dashboard(
    db: Session = Depends(get_db),
    _: User = Depends(require_analyst),
):
    """
    Get complete dashboard data.
    
    Includes summary, categories, monthly trends, weekly trends, and recent activity.
    Available to analysts and admins.
    """
    return get_dashboard_data(db)
