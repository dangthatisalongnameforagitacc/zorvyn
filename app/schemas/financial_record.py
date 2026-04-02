"""Financial record request and response schemas."""
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from app.models.financial_record import EntryType


class RecordCreate(BaseModel):
    """Request body for creating a financial record."""
    amount: float = Field(gt=0, description="Must be a positive number")
    entry_type: EntryType
    category: str = Field(min_length=1, max_length=50)
    date: date
    description: str = ""


class RecordUpdate(BaseModel):
    """Request body for updating a financial record."""
    amount: Optional[float] = Field(default=None, gt=0)
    category: Optional[str] = Field(default=None, min_length=1, max_length=50)
    date: Optional[date] = None
    description: Optional[str] = None


class RecordFilter(BaseModel):
    """Query parameters for filtering records."""
    entry_type: Optional[EntryType] = None
    category: Optional[str] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    page: int = 1
    page_size: int = 20


class RecordResponse(BaseModel):
    """Financial record in responses."""
    id: int
    amount: float
    entry_type: EntryType
    category: str
    date: date
    description: str
    created_by: int
    created_at: str

    class Config:
        from_attributes = True
        json_encoders = {
            date: lambda v: v.isoformat()
        }


class PaginatedRecords(BaseModel):
    """Paginated list of financial records."""
    total: int
    page: int
    page_size: int
    total_pages: int
    items: list[RecordResponse]
