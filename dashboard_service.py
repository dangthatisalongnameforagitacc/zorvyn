"""
Dashboard service — aggregation queries for the finance dashboard.
Intentionally uses raw SQL-level aggregates via SQLAlchemy for efficiency
rather than pulling all rows into Python and summing there.
"""
from sqlalchemy import func, extract
from sqlalchemy.orm import Session

from app.models.financial_record import EntryType, FinancialRecord
from app.schemas.dashboard import (
    CategoryTotal,
    DashboardSummary,
    MonthlyTrend,
    WeeklyTrend,
)
from app.schemas.financial_record import RecordResponse


def get_summary(db: Session) -> DashboardSummary:
    """Total income, total expenses, net balance, and record count."""
    base = db.query(FinancialRecord).filter(FinancialRecord.is_deleted == False)

    total_income = (
        base.filter(FinancialRecord.entry_type == EntryType.income)
        .with_entities(func.coalesce(func.sum(FinancialRecord.amount), 0))
        .scalar()
    )
    total_expenses = (
        base.filter(FinancialRecord.entry_type == EntryType.expense)
        .with_entities(func.coalesce(func.sum(FinancialRecord.amount), 0))
        .scalar()
    )
    total_records = base.count()

    return DashboardSummary(
        total_income=float(total_income),
        total_expenses=float(total_expenses),
        net_balance=float(total_income) - float(total_expenses),
        total_records=total_records,
    )


def get_category_totals(db: Session) -> list[CategoryTotal]:
    """Total amount and count per (category, entry_type) pair."""
    rows = (
        db.query(
            FinancialRecord.category,
            FinancialRecord.entry_type,
            func.sum(FinancialRecord.amount).label("total"),
            func.count(FinancialRecord.id).label("count"),
        )
        .filter(FinancialRecord.is_deleted == False)
        .group_by(FinancialRecord.category, FinancialRecord.entry_type)
        .order_by(func.sum(FinancialRecord.amount).desc())
        .all()
    )
    return [
        CategoryTotal(
            category=row.category,
            entry_type=row.entry_type,
            total=float(row.total),
            count=row.count,
        )
        for row in rows
    ]


def get_monthly_trends(db: Session, months: int = 12) -> list[MonthlyTrend]:
    """Income vs expenses per calendar month for the last N months."""
    rows = (
        db.query(
            extract("year", FinancialRecord.date).label("year"),
            extract("month", FinancialRecord.date).label("month"),
            FinancialRecord.entry_type,
            func.sum(FinancialRecord.amount).label("total"),
        )
        .filter(FinancialRecord.is_deleted == False)
        .group_by("year", "month", FinancialRecord.entry_type)
        .order_by("year", "month")
        .all()
    )

    # Pivot the rows into one MonthlyTrend per (year, month)
    pivot: dict[tuple, dict] = {}
    for row in rows:
        key = (int(row.year), int(row.month))
        if key not in pivot:
            pivot[key] = {"income": 0.0, "expenses": 0.0}
        if row.entry_type == EntryType.income:
            pivot[key]["income"] = float(row.total)
        else:
            pivot[key]["expenses"] = float(row.total)

    return [
        MonthlyTrend(
            year=year,
            month=month,
            income=data["income"],
            expenses=data["expenses"],
            net=data["income"] - data["expenses"],
        )
        for (year, month), data in sorted(pivot.items())
    ][-months:]


def get_weekly_trends(db: Session, weeks: int = 8) -> list[WeeklyTrend]:
    """Income vs expenses per ISO week for the last N weeks."""
    rows = (
        db.query(
            extract("year", FinancialRecord.date).label("year"),
            extract("week", FinancialRecord.date).label("week"),
            FinancialRecord.entry_type,
            func.sum(FinancialRecord.amount).label("total"),
        )
        .filter(FinancialRecord.is_deleted == False)
        .group_by("year", "week", FinancialRecord.entry_type)
        .order_by("year", "week")
        .all()
    )

    pivot: dict[tuple, dict] = {}
    for row in rows:
        key = (int(row.year), int(row.week))
        if key not in pivot:
            pivot[key] = {"income": 0.0, "expenses": 0.0}
        if row.entry_type == EntryType.income:
            pivot[key]["income"] = float(row.total)
        else:
            pivot[key]["expenses"] = float(row.total)

    return [
        WeeklyTrend(
            year=year,
            week=week,
            income=data["income"],
            expenses=data["expenses"],
            net=data["income"] - data["expenses"],
        )
        for (year, week), data in sorted(pivot.items())
    ][-weeks:]


def get_recent_activity(db: Session, limit: int = 10) -> list[FinancialRecord]:
    """Most recently created non-deleted records."""
    return (
        db.query(FinancialRecord)
        .filter(FinancialRecord.is_deleted == False)
        .order_by(FinancialRecord.created_at.desc())
        .limit(limit)
        .all()
    )
