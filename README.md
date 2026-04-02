# Finance Dashboard Backend

A well-architected REST API backend for a multi-user finance dashboard system with role-based access control, financial record management, and powerful analytics.

Built with **Python + FastAPI + SQLite + SQLAlchemy ORM + JWT Authentication**.

---

## Key Features

✅ **Role-Based Access Control (RBAC)**
- Three roles: Viewer, Analyst, Admin
- Role hierarchy with clear permission boundaries
- JWT token-based authentication

✅ **Financial Records Management**
- CRUD operations for income/expense transactions
- Filtering by category, type, date range
- Pagination support (up to 100 items per page)
- Soft-delete for audit trail preservation

✅ **Dashboard Analytics**
- Total income, expenses, net balance
- Category-wise breakdowns
- Monthly and weekly trend analysis
- Recent activity feed
- Efficient SQL-level aggregations (not memory-based)

✅ **Data Validation & Error Handling**
- Pydantic v2 schema validation
- Consistent HTTP status codes
- User-friendly error messages
- Input constraints (positive amounts, date ranges)

✅ **Production-Ready Architecture**
- Separation of concerns (models, schemas, services, routes)
- Dependency injection for clean testing
- Custom exception handlers
- CORS support

---

## Tech Stack

| Layer         | Technology                      | Why                                             |
|---------------|---------------------------------|-------------------------------------------------|
| Language      | Python 3.13                     | Readable, widely supported                      |
| Framework     | FastAPI                         | Async-ready, auto-generated docs, validation   |
| Database      | SQLite via SQLAlchemy ORM       | Zero-setup, file-based, easily swappable       |
| Auth          | JWT + bcrypt                    | Stateless, secure, industry-standard           |
| Validation    | Pydantic v2                     | Type-safe, descriptive errors, easy schemas    |

---

## Project Structure

```
zorvyna/
├── app/
│   ├── __init__.py                # Package marker
│   ├── config.py                  # Configuration (JWT, DB, pagination)
│   ├── database.py                # SQLAlchemy setup, session management
│   ├── dependencies.py            # Authentication dependencies
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                # User model, Role enum
│   │   └── financial_record.py    # FinancialRecord model, EntryType enum
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py                # TokenRequest, TokenResponse, Me
│   │   ├── user.py                # UserCreate, UserUpdate, UserResponse
│   │   ├── financial_record.py    # Record schemas (Create/Update/Filter/Response)
│   │   └── dashboard.py           # Dashboard response schemas
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py            # JWT & bcrypt utilities
│   │   ├── exceptions.py          # Custom exception classes
│   │   └── permissions.py         # Role-based permission dependencies
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py        # User CRUD & business logic
│   │   ├── record_service.py      # Record CRUD & filtering logic
│   │   └── dashboard_service.py   # Aggregations & analytics
│   │
│   └── routers/
│       ├── __init__.py
│       ├── auth.py                # Authentication (login, register, me)
│       ├── users.py               # User management (admin only)
│       ├── records.py             # Financial records (role-restricted)
│       └── dashboard.py           # Analytics endpoints (analyst+)
│
├── main.py                        # FastAPI app entry point
├── seed.py                        # Database seeding script
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## Setup & Running

### 1. Clone & Install Dependencies

```bash
# Navigate to the project directory
cd zorvyna

# Install Python packages
pip install -r requirements.txt
```

### 2. Seed the Database

```bash
# Creates finance.db and populates with test data
python seed.py
```

Creates:
- 3 test users (admin, analyst, viewer)
- 180 financial records spanning 12 months
- Sample categories and transactions

### 3. Start the Server

```bash
# Option A: Using uvicorn directly
uvicorn app.main:app --reload

# Option B: Using Python module
python -m uvicorn app.main:app --reload

# Option C: Using the main.py __main__ block
python main.py
```

The API will be available at:
- **API Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

---

## Test Accounts

| Email                  | Password     | Role     | Can Do                                |
|------------------------|--------------|----------|---------------------------------------|
| admin@finance.com      | admin123     | Admin    | Everything (create, delete, manage users) |
| analyst@finance.com    | analyst123   | Analyst  | View records + access analytics       |
| viewer@finance.com     | viewer123    | Viewer   | View records only                     |

---

## API Endpoints

### Authentication (`/auth`)

| Method | Endpoint         | Description             | Auth Required |
|--------|------------------|-------------------------|---------------|
| POST   | `/auth/register` | Create new account      | No            |
| POST   | `/auth/login`    | Login and get JWT token | No            |
| GET    | `/auth/me`       | Get current user info   | Yes           |

**Example Login:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@finance.com", "password": "admin123"}'

# Response:
# {"access_token": "eyJhbGc...", "token_type": "bearer"}
```

### Financial Records (`/records`)

| Method | Endpoint           | Description         | Auth | Permission |
|--------|-------------------|---------------------|------|------------|
| GET    | `/records/`       | List records        | Yes  | Viewer+    |
| GET    | `/records/{id}`   | Get single record   | Yes  | Viewer+    |
| POST   | `/records/`       | Create record       | Yes  | Admin      |
| PATCH  | `/records/{id}`   | Update record       | Yes  | Admin      |
| DELETE | `/records/{id}`   | Soft-delete record  | Yes  | Admin      |

**Query Parameters for Listing:**
- `entry_type` (income/expense)
- `category` (e.g., "Food", "Salary")
- `date_from` (YYYY-MM-DD)
- `date_to` (YYYY-MM-DD)
- `page` (default: 1)
- `page_size` (1-100, default: 20)

**Example Record Creation:**
```bash
curl -X POST http://localhost:8000/records/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 50.00,
    "entry_type": "expense",
    "category": "Food",
    "date": "2024-04-02",
    "description": "Groceries"
  }'
```

### User Management (`/users`)

| Method | Endpoint       | Description    | Auth | Permission |
|--------|---------------|----------------|------|------------|
| GET    | `/users/`     | List users     | Yes  | Admin      |
| GET    | `/users/{id}` | Get user       | Yes  | Admin      |
| POST   | `/users/`     | Create user    | Yes  | Admin      |
| PATCH  | `/users/{id}` | Update user    | Yes  | Admin      |
| DELETE | `/users/{id}` | Delete user    | Yes  | Admin      |

### Dashboard Analytics (`/dashboard`)

| Method | Endpoint                       | Description              | Auth | Permission |
|--------|-------------------------------|--------------------------|------|------------|
| GET    | `/dashboard/summary`          | Financial summary        | Yes  | Analyst+   |
| GET    | `/dashboard/categories`       | Category breakdown       | Yes  | Analyst+   |
| GET    | `/dashboard/trends/monthly`   | Monthly trends (12 mo)   | Yes  | Analyst+   |
| GET    | `/dashboard/trends/weekly`    | Weekly trends (8 weeks)  | Yes  | Analyst+   |
| GET    | `/dashboard/recent`           | Recent transactions      | Yes  | Analyst+   |
| GET    | `/dashboard/`                 | Full dashboard data      | Yes  | Analyst+   |

**Example Dashboard Request:**
```bash
curl http://localhost:8000/dashboard/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Returns:
# {
#   "summary": {
#     "total_income": 50000.0,
#     "total_expenses": 12000.0,
#     "net_balance": 38000.0,
#     "total_records": 180
#   },
#   "category_totals": [...],
#   "monthly_trends": [...],
#   "weekly_trends": [...],
#   "recent_activity": [...]
# }
```

---

## Authentication Flow

All protected endpoints require a JWT token in the `Authorization` header:

```
Authorization: Bearer <your_jwt_token>
```

**Token Lifecycle:**
1. User logs in via `/auth/login` with email & password
2. Server returns JWT token (valid for 30 minutes by default)
3. User includes token in `Authorization` header for subsequent requests
4. Server validates token and checks user is active
5. Token expires after 30 minutes (user must login again)

---

## Role-Based Access Control

The system enforces a **role hierarchy**:

```
Viewer (0) → Analyst (1) → Admin (2)
```

**Permissions by Role:**

| Action                  | Viewer | Analyst | Admin |
|-------------------------|--------|---------|-------|
| View records            | ✓      | ✓       | ✓     |
| View dashboard          | ✗      | ✓       | ✓     |
| Create records          | ✗      | ✗       | ✓     |
| Update records          | ✗      | ✗       | ✓     |
| Delete records          | ✗      | ✗       | ✓     |
| Manage users            | ✗      | ✗       | ✓     |

---

## Data Models

### User
```python
- id: int
- email: str (unique)
- hashed_password: str (bcrypt)
- full_name: str
- role: Role (viewer | analyst | admin)
- is_active: bool
- created_at: datetime
- updated_at: datetime
```

### FinancialRecord
```python
- id: int
- amount: float (positive)
- entry_type: EntryType (income | expense)
- category: str
- date: date
- description: str
- created_by: int (User ID)
- is_deleted: bool (soft-delete flag)
- created_at: datetime
- updated_at: datetime
```

---

## Design Decisions & Tradeoffs

### 1. **Soft Deletes**
- Records marked `is_deleted = True` instead of hard-deleting
- **Benefit**: Maintains audit trail, reversible deletions
- **Tradeoff**: Queries must filter `is_deleted = False`

### 2. **SQLite for Production**
- Chosen for simplicity and zero setup
- **Strength**: File-based, no external dependencies
- **Upgrade Path**: SQLAlchemy ORM is DB-agnostic; swap to PostgreSQL by changing `DATABASE_URL`

### 3. **Service-Centric Architecture**
- Business logic lives in `services/`, not routers
- **Benefit**: Reusable, testable, separated from HTTP concerns
- **Example**: Same `record_service.list_records()` works for API or CLI

### 4. **JWT Tokens (Stateless Auth)**
- Server doesn't store tokens; verifies them cryptographically
- **Benefit**: Scalable, no session storage needed
- **Limitation**: Can't revoke tokens before expiry (accepted tradeoff)

### 5. **Aggregated Dashboard Queries**
- Dashboard uses SQL-level `func.sum()`, `func.count()` instead of Python loops
- **Benefit**: Performant with large datasets
- **Example**: Summing 10,000+ records takes milliseconds vs seconds

### 6. **Pagination with Limits**
- Records endpoint returns 20 items per page by default (capped at 100)
- **Benefit**: Prevents accidental huge responses
- **Tradeoff**: Frontend must paginate

---

## Error Handling & Status Codes

The API uses standard HTTP status codes:

| Code | Meaning              | Example                    |
|------|----------------------|----------------------------|
| 200  | OK                   | Successful GET/PATCH       |
| 201  | Created              | POST /records/             |
| 204  | No Content           | DELETE (soft-delete)       |
| 400  | Bad Request          | Invalid input validation   |
| 401  | Unauthorized         | Missing/expired token      |
| 403  | Forbidden            | User lacks permission      |
| 404  | Not Found            | Resource doesn't exist     |
| 409  | Conflict             | Email already registered   |
| 500  | Server Error         | Unexpected exception       |

**Error Response Format:**
```json
{
  "detail": "Access denied. Required role: 'admin' or higher. Your role: 'viewer'."
}
```

---

## Testing the API

### Using cURL

```bash
# 1. Login
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@finance.com", "password": "admin123"}' \
  | jq -r '.access_token')

# 2. Create a record
curl -X POST http://localhost:8000/records/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 100.50,
    "entry_type": "income",
    "category": "Freelance",
    "date": "2024-04-02",
    "description": "Project payment"
  }'

# 3. Get dashboard summary
curl http://localhost:8000/dashboard/summary \
  -H "Authorization: Bearer $TOKEN"
```

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Login
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "admin@finance.com",
    "password": "admin123"
})
token = response.json()["access_token"]

# Create record
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(f"{BASE_URL}/records/", headers=headers, json={
    "amount": 100,
    "entry_type": "expense",
    "category": "Food",
    "date": "2024-04-02",
    "description": "Lunch"
})
print(response.json())

# Get dashboard
response = requests.get(f"{BASE_URL}/dashboard/", headers=headers)
dashboard = response.json()
print(f"Net Balance: ${dashboard['summary']['net_balance']}")
```

---

## Future Enhancements

🔲 **Unit & Integration Tests** — Pytest suite covering all services  
🔲 **API Rate Limiting** — Prevent abuse (slowapi)  
🔲 **Email Notifications** — Send summaries to users  
🔲 **Export to CSV/PDF** — Financial reports  
🔲 **Budget Tracking** — Set limits by category  
🔲 **Mobile API** — Optimized for mobile clients  
🔲 **Scheduled Reports** — Auto-generate monthly summaries  
🔲 **Docker Support** — Containerized deployment  

---

## Assumptions & Notes

1. **Email Uniqueness**: Users register with unique emails; no two users can have the same email.
2. **Inactive Users**: Users with `is_active = False` cannot login; existing tokens remain valid until expiry.
3. **Soft Deletes Only**: There's no hard-delete endpoint; deleted records stay in the database.
4. **Amount Validation**: Amounts must be positive (> 0). Zero or negative amounts are rejected.
5. **Timezone**: All dates are stored as local dates (no timezone info). Server uses UTC for timestamps.
6. **Category Free Text**: Categories are user-defined strings (no predefined list). Frontend can suggest common ones.
7. **Simple Demo**: This is a learning/assessment backend. For production, add rate limiting, logging, caching.

---

## License

MIT

---

**Questions or Feedback?**
This backend demonstrates principles of clean architecture, RBAC, data validation, and practical API design. Enjoy! ✨

## API Reference

### Authentication

| Method | Endpoint          | Access  | Description                        |
|--------|-------------------|---------|------------------------------------|
| POST   | /auth/register    | Public  | Self-register (always viewer role) |
| POST   | /auth/login       | Public  | Login, receive Bearer token        |
| GET    | /auth/me          | Any     | Get current user profile           |

**Login example:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -d "username=admin@finance.com&password=admin123"
```

Use the returned token in all subsequent requests:
```
Authorization: Bearer <token>
```

---

### Users — `/users/` (Admin only)

| Method | Endpoint        | Description                              |
|--------|-----------------|------------------------------------------|
| GET    | /users/         | List all users (paginated)               |
| GET    | /users/{id}     | Get a single user                        |
| POST   | /users/         | Create user with any role                |
| PATCH  | /users/{id}     | Update name, role, or active status      |
| DELETE | /users/{id}     | Permanently delete a user                |

**Create user example:**
```json
POST /users/
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "password": "secure123",
  "role": "analyst"
}
```

---

### Financial Records — `/records/`

| Method | Endpoint         | Role Required | Description                   |
|--------|------------------|---------------|-------------------------------|
| GET    | /records/        | Viewer+       | List records with filters      |
| GET    | /records/{id}    | Viewer+       | Get a single record            |
| POST   | /records/        | Admin         | Create a new record            |
| PATCH  | /records/{id}    | Admin         | Update a record                |
| DELETE | /records/{id}    | Admin         | Soft-delete a record           |

**Filter parameters for GET /records/:**
| Param       | Type   | Description                        |
|-------------|--------|------------------------------------|
| entry_type  | string | `income` or `expense`              |
| category    | string | Partial match (case-insensitive)   |
| date_from   | date   | ISO format: `YYYY-MM-DD`           |
| date_to     | date   | ISO format: `YYYY-MM-DD`           |
| page        | int    | Page number (default: 1)           |
| page_size   | int    | Items per page (default: 20, max: 100) |

**Example:**
```
GET /records/?entry_type=expense&category=rent&date_from=2026-01-01&page=1&page_size=10
```

**Create record body:**
```json
{
  "amount": 5000.00,
  "entry_type": "income",
  "category": "salary",
  "date": "2026-04-01",
  "notes": "Monthly salary"
}
```

---

### Dashboard & Analytics — `/dashboard/` (Analyst + Admin)

| Method | Endpoint                    | Description                                       |
|--------|-----------------------------|---------------------------------------------------|
| GET    | /dashboard/summary          | Total income, expenses, net balance, record count |
| GET    | /dashboard/by-category      | Totals grouped by category and entry type         |
| GET    | /dashboard/trends/monthly   | Monthly income vs expenses (`?months=12`)         |
| GET    | /dashboard/trends/weekly    | Weekly income vs expenses (`?weeks=8`)            |
| GET    | /dashboard/recent           | Most recent records (`?limit=10`)                 |
| GET    | /dashboard/overview         | All of the above in a single response             |

---

## Access Control Design

Roles follow a strict hierarchy enforced via FastAPI dependencies:

```
viewer  →  read records only
analyst →  viewer + all dashboard/analytics endpoints
admin   →  analyst + create/update/delete records + manage users
```

The `_require_role()` factory in `app/core/permissions.py` generates a
dependency for any minimum role level. Routers declare their requirement
with a single line:

```python
@router.post("/records/", dependencies=[Depends(require_admin)])
@router.get("/dashboard/summary", dependencies=[Depends(require_analyst)])
@router.get("/records/", dependencies=[Depends(require_viewer)])
```

This means access rules are declared at the router level — no scattered
`if user.role == "admin"` checks in business logic.

---

## Data Model

### User

| Field         | Type     | Notes                              |
|---------------|----------|------------------------------------|
| id            | int      | Primary key                        |
| name          | string   | Display name                       |
| email         | string   | Unique, used as login username     |
| password_hash | string   | bcrypt hash                        |
| role          | enum     | `viewer`, `analyst`, `admin`       |
| is_active     | bool     | Deactivated users cannot log in    |
| created_at    | datetime |                                    |
| updated_at    | datetime |                                    |

### FinancialRecord

| Field       | Type     | Notes                                       |
|-------------|----------|---------------------------------------------|
| id          | int      | Primary key                                 |
| amount      | decimal  | Positive, precision to 2dp                  |
| entry_type  | enum     | `income` or `expense`                       |
| category    | string   | Lowercased on write, filterable             |
| date        | date     | Logical date of the transaction             |
| notes       | text     | Optional description                        |
| created_by  | FK→User  | Who created the record                      |
| is_deleted  | bool     | Soft delete flag                            |
| deleted_at  | datetime | Set on soft delete                          |
| created_at  | datetime |                                             |
| updated_at  | datetime |                                             |

---

## Key Design Decisions & Assumptions

**Soft delete over hard delete**
Financial records are never permanently removed. Deleting sets `is_deleted=True`
and records a `deleted_at` timestamp. This preserves audit history — a common
requirement in financial systems.

**Routers are thin, services hold logic**
Routers handle only HTTP concerns (request parsing, status codes, response
serialization). All business logic lives in the service layer. This makes
services independently testable and routers easy to read.

**Category is free-text, lowercased**
Rather than a fixed category table, categories are stored as lowercased strings.
This keeps the API flexible for a frontend that lets users define their own
categories. Filtering uses `ILIKE` for partial matching.

**Self-registration is always viewer**
`POST /auth/register` is public but forces the `viewer` role regardless of what
the caller sends. Role elevation requires an admin via `PATCH /users/{id}`.
This prevents privilege escalation on signup.

**SQLite → PostgreSQL migration**
Changing to PostgreSQL requires only two changes: `DATABASE_URL` in
`database.py` and removing `check_same_thread` from the engine args.
SQLAlchemy abstracts everything else.

**JWT is stateless**
Tokens are not stored server-side. Expiry is set to 8 hours. In production,
add a token revocation list (Redis) if you need immediate logout capability.

---

## Validation Behaviour

| Scenario                      | Response                              |
|-------------------------------|---------------------------------------|
| Negative or zero amount       | 422 — "Input should be greater than 0" |
| Missing required field        | 422 — field-level error detail        |
| Duplicate email on register   | 409 — "user already exists"           |
| Wrong password on login       | 400 — "Invalid email or password"     |
| Expired / malformed token     | 401 — "Invalid or expired token"      |
| Inactive user tries to act    | 403 — "Account has been deactivated"  |
| Insufficient role             | 403 — role required vs role held      |
| Record not found              | 404 — "Record with id X not found"    |
| Admin deletes own account     | 400 — "Cannot delete your own account"|

---

## Optional Enhancements Included

- **JWT authentication** — Bearer token auth on all protected routes
- **Pagination** — all list endpoints support `page` and `page_size`
- **Filtering** — records filterable by type, category, and date range
- **Soft delete** — records flagged deleted, not removed from DB
- **Auto-generated API docs** — available at `/docs` (Swagger UI) and `/redoc`
- **Seed script** — realistic 12-month dataset for immediate testing
- **Health check** — `GET /health` liveness probe
