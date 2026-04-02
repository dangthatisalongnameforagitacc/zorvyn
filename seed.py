"""Seed database with sample data for testing."""
from datetime import datetime, timedelta
import random

from app.database import SessionLocal, Base, engine
from app.models.user import User, Role
from app.models.financial_record import FinancialRecord, EntryType
from app.core.security import hash_password

# Create all tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Clear existing data
db.query(FinancialRecord).delete()
db.query(User).delete()
db.commit()

# ── Create test users ──────────────────────────────────────────────────────────
users_data = [
    {
        "email": "admin@finance.com",
        "password": "admin123",
        "full_name": "Admin User",
        "role": Role.admin,
    },
    {
        "email": "analyst@finance.com",
        "password": "analyst123",
        "full_name": "Analyst User",
        "role": Role.analyst,
    },
    {
        "email": "viewer@finance.com",
        "password": "viewer123",
        "full_name": "Viewer User",
        "role": Role.viewer,
    },
]

users = []
for user_data in users_data:
    user = User(
        email=user_data["email"],
        hashed_password=hash_password(user_data["password"]),
        full_name=user_data["full_name"],
        role=user_data["role"],
        is_active=True,
    )
    db.add(user)
    users.append(user)

db.commit()
db.refresh(users[0])
admin_id = users[0].id

print(f"✓ Created {len(users)} test users")

# ── Create sample financial records ────────────────────────────────────────────
categories = ["Salary", "Freelance", "Food", "Transport", "Utilities", "Entertainment", "Investment", "Rent"]
descriptions = [
    "Monthly salary",
    "Freelance project payment",
    "Groceries",
    "Gas",
    "Electric bill",
    "Movie tickets",
    "Stock purchase",
    "Apartment rent",
]

base_date = datetime.now().date()
records = []

# Generate 180 records over 12 months
for i in range(180):
    # Spread records over the past 12 months
    days_ago = random.randint(0, 365)
    record_date = base_date - timedelta(days=days_ago)
    
    # 60% income, 40% expense
    if random.random() < 0.6:
        entry_type = EntryType.income
        category = random.choice(["Salary", "Freelance", "Investment"])
        amount = round(random.uniform(1000, 5000), 2)
    else:
        entry_type = EntryType.expense
        category = random.choice(["Food", "Transport", "Utilities", "Entertainment", "Rent"])
        amount = round(random.uniform(10, 500), 2)
    
    record = FinancialRecord(
        amount=amount,
        entry_type=entry_type,
        category=category,
        date=record_date,
        description=random.choice(descriptions),
        created_by=admin_id,
    )
    db.add(record)
    records.append(record)

db.commit()
print(f"✓ Created {len(records)} sample financial records")

# Print summary
print("\n" + "=" * 60)
print("DATABASE SEEDED SUCCESSFULLY")
print("=" * 60)
print("\nTest Accounts:")
print("┌─ Admin (full access)")
print("│  Email: admin@finance.com")
print("│  Password: admin123")
print("├─ Analyst (view + analytics)")
print("│  Email: analyst@finance.com")
print("│  Password: analyst123")
print("└─ Viewer (view only)")
print("   Email: viewer@finance.com")
print("   Password: viewer123")
print("\n")
