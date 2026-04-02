"""
Finance Dashboard Backend — entry point.

Run with:  python -m uvicorn app.main:app --reload
           or: uvicorn app.main:app --reload
Docs at:   http://localhost:8000/docs
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.database import Base, engine
from app.models import User, FinancialRecord  # noqa: F401 — ensures models are registered
from app.routers import auth, users, records, dashboard

# ── Create tables ──────────────────────────────────────────────────────────────
Base.metadata.create_all(bind=engine)

# ── App instance ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="Finance Dashboard API",
    description=(
        "Backend for a multi-role finance dashboard system. "
        "Supports financial record management, role-based access control, "
        "and aggregated analytics for dashboard views."
    ),
    version="1.0.0",
    contact={"name": "Finance Dashboard Team"},
    license_info={"name": "MIT"},
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ── CORS ───────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Global error handlers ──────────────────────────────────────────────────────
@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=409,
        content={"detail": "A database conflict occurred. The record may already exist."},
    )

# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(records.router)
app.include_router(dashboard.router)


# ── Health check ───────────────────────────────────────────────────────────────
@app.get("/health", tags=["System"])
def health_check():
    """Simple liveness probe — returns OK if the server is running."""
    return {"status": "ok", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
