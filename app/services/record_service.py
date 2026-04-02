"""Financial record CRUD operations and business logic."""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional

from app.models.financial_record import FinancialRecord, EntryType
from app.schemas.financial_record import RecordCreate, RecordUpdate, RecordFilter
from app.core.exceptions import NotFoundException


def get_record_by_id(db: Session, record_id: int) -> FinancialRecord:
    """Fetch a non-deleted record by ID or raise 404."""
    record = (
        db.query(FinancialRecord)
        .filter(
            and_(
                FinancialRecord.id == record_id,
                FinancialRecord.is_deleted == False
            )
        )
        .first()
    )
    if not record:
        raise NotFoundException("Financial record not found")
    return record


def list_records(
    db: Session,
    filters: RecordFilter,
) -> tuple[list[FinancialRecord], int]:
    """
    List financial records with optional filtering and pagination.
    
    Filters:
        - entry_type: income or expense
        - category: string match
        - date_from, date_to: date range
        - page, page_size: pagination
    """
    query = db.query(FinancialRecord).filter(FinancialRecord.is_deleted == False)
    
    # Apply filters
    if filters.entry_type:
        query = query.filter(FinancialRecord.entry_type == filters.entry_type)
    if filters.category:
        query = query.filter(FinancialRecord.category.ilike(f"%{filters.category}%"))
    if filters.date_from:
        query = query.filter(FinancialRecord.date >= filters.date_from)
    if filters.date_to:
        query = query.filter(FinancialRecord.date <= filters.date_to)
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    offset = (filters.page - 1) * filters.page_size
    records = query.order_by(FinancialRecord.date.desc()).offset(offset).limit(filters.page_size).all()
    
    return records, total


def create_record(
    db: Session,
    record: RecordCreate,
    created_by: int,
) -> FinancialRecord:
    """Create a new financial record."""
    db_record = FinancialRecord(
        amount=record.amount,
        entry_type=record.entry_type,
        category=record.category,
        date=record.date,
        description=record.description,
        created_by=created_by,
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def update_record(
    db: Session,
    record_id: int,
    record_update: RecordUpdate,
) -> FinancialRecord:
    """Update a financial record."""
    db_record = get_record_by_id(db, record_id)
    
    update_data = record_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_record, field, value)
    
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def soft_delete_record(db: Session, record_id: int) -> None:
    """Soft-delete a record (mark as deleted but keep in database)."""
    db_record = get_record_by_id(db, record_id)
    db_record.is_deleted = True
    db.add(db_record)
    db.commit()
