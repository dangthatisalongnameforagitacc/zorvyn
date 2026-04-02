"""Database configuration and session factory."""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import DATABASE_URL

# ── Engine and Session Factory ─────────────────────────────────────────────────
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ── Base class for all models ──────────────────────────────────────────────────
Base = declarative_base()


def get_db():
    """Dependency: gets a database session for request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
