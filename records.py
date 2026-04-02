"""
Financial records router.

GET    /records/        → list + filter records      [viewer, analyst, admin]
GET    /records/{id}    → get single record           [viewer, analyst, admin]
POST   /records/        → create a record             [admin]
PATCH  /records/{id}    → update a record             [admin]
DELETE /records/{id}    → soft-delete a record        [admin]
"""
import math

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.permissions import require_admin, require_viewer
from app.database import get_db
from app.models.financial_record import EntryType
from app.models.user import User
from app.schemas.financial_record import (
    PaginatedRecords,
    RecordCreate,
    RecordFilter,
    RecordResponse,
    RecordUpdate,
)
from app.services import record_service
from datetime import date

router = APIRouter(prefix="/records", tags=["Financial Records"])


@router.get("/", response_model=PaginatedRecords)
def list_records(
    entry_type: EntryType | None = Query(default=None),
    category: str | None = Query(default=None),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(require_viewer),
):
    """
    List financial records with optional filters and pagination.
    Available to all authenticated active users.
    """
    filters = RecordFilter(
        entry_type=entry_type,
        category=category,
        date_from=date_from,
        date_to=date_to,
        page=page,
        page_size=page_size,
    )
    records, total = record_service.list_records(db, filters)
    return PaginatedRecords(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=math.ceil(total / page_size) if total else 1,
        items=[RecordResponse.model_validate(r) for r in records],
    )


@router.get("/{record_id}", response_model=RecordResponse)
def get_record(
    record_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_viewer),
):
    """Retrieve a single record by ID. Available to all authenticated active users."""
    record = record_service.get_record_by_id(db, record_id)
    return RecordResponse.model_validate(record)


@router.post("/", response_model=RecordResponse, status_code=201)
def create_record(
    payload: RecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Create a new financial record. Admin only."""
    record = record_service.create_record(db, payload, created_by=current_user.id)
    return RecordResponse.model_validate(record)


@router.patch("/{record_id}", response_model=RecordResponse)
def update_record(
    record_id: int,
    payload: RecordUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """Update an existing financial record. Admin only."""
    record = record_service.update_record(db, record_id, payload)
    return RecordResponse.model_validate(record)


@router.delete("/{record_id}", status_code=204)
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Soft-delete a financial record. Admin only.
    The record is flagged as deleted but kept in the database for audit purposes.
    """
    record_service.soft_delete_record(db, record_id)
