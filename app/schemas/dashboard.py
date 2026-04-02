"""Dashboard analytics response schemas."""
from pydantic import BaseModel
from app.models.financial_record import EntryType


class CategoryTotal(BaseModel):
    """Total amount by category and entry type."""
    category: str
    entry_type: EntryType
    total: float
    count: int


class DashboardSummary(BaseModel):
    """Overall financial summary."""
    total_income: float
    total_expenses: float
    net_balance: float
    total_records: int


class MonthlyTrend(BaseModel):
    """Monthly income vs expenses trend."""
    year: int
    month: int
    income: float
    expenses: float
    net: float


class WeeklyTrend(BaseModel):
    """Weekly income vs expenses trend."""
    year: int
    week: int
    income: float
    expenses: float
    net: float


class RecentActivity(BaseModel):
    """Recent financial record."""
    id: int
    amount: float
    entry_type: EntryType
    category: str
    description: str
    date: str

    class Config:
        from_attributes = True


class DashboardData(BaseModel):
    """Complete dashboard data for frontend."""
    summary: DashboardSummary
    category_totals: list[CategoryTotal]
    monthly_trends: list[MonthlyTrend]
    weekly_trends: list[WeeklyTrend]
    recent_activity: list[RecentActivity]
