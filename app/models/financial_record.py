"""Financial record model."""
from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum as SQLEnum, Float, DateTime, Boolean, Date
from app.database import Base


class EntryType(str, Enum):
    """Type of financial entry."""
    income = "income"
    expense = "expense"


class FinancialRecord(Base):
    """Financial transaction or entry record."""
    __tablename__ = "financial_records"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    entry_type = Column(SQLEnum(EntryType), nullable=False)
    category = Column(String, nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    description = Column(String, default="")
    created_by = Column(Integer, nullable=False)  # User ID of creator
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return (
            f"<FinancialRecord("
            f"id={self.id}, "
            f"amount={self.amount}, "
            f"type={self.entry_type}, "
            f"category={self.category}, "
            f"date={self.date}"
            f")>"
        )
