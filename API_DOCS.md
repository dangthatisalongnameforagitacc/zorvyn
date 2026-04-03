# Finance Dashboard API Documentation

**Version:** 1.0.0
**Description:** Backend for a multi-role finance dashboard system. Supports financial record management, role-based access control, and aggregated analytics for dashboard views.

---

## Table of Contents
- [Authentication](#authentication)
- [User Management](#user-management)
- [Financial Records](#financial-records)
- [Dashboard Analytics](#dashboard-analytics)
- [System](#system)
- [Data Models](#data-models)

---

## Authentication

### `POST` `/auth/register`
**Summary**: Register
**Description**: Register a new user. Returns a JWT token for immediate login.

- **Request Body**: `application/json`
  - Body Schema: `TokenRequest`
- **Responses**:
  - `201`: Successful Response (`TokenResponse`)
  - `422`: Validation Error

### `POST` `/auth/login`
**Summary**: Login
**Description**: Login with email and password. Returns a JWT token.

- **Request Body**: `application/json`
  - Body Schema: `TokenRequest`
- **Responses**:
  - `200`: Successful Response (`TokenResponse`)
  - `422`: Validation Error

### `GET` `/auth/me`
**Summary**: Get Me
**Description**: Get current authenticated user information.

- **Parameters**: 
  - `authorization` (header, optional)
- **Responses**:
  - `200`: Successful Response (`Me` or `UserResponse`)

---

## User Management

*Note: All endpoints under this section require Admin privileges.*

### `GET` `/users/`
**Summary**: List Users
**Description**: List all users. Admin only.

- **Parameters**:
  - `skip` (query, integer, default: 0)
  - `limit` (query, integer, default: 100)
- **Responses**:
  - `200`: List of `UserResponse`

### `POST` `/users/`
**Summary**: Create User
**Description**: Create a new user. Admin only.

- **Request Body**: `UserCreate`
- **Responses**:
  - `201`: Successful Response (`UserResponse`)

### `GET` `/users/{user_id}`
**Summary**: Get User
**Description**: Get a user by ID. Admin only.

- **Parameters**:
  - `user_id` (path, integer, required)
- **Responses**:
  - `200`: Successful Response (`UserResponse`)

### `PATCH` `/users/{user_id}`
**Summary**: Update User
**Description**: Update a user. Admin only.

- **Parameters**:
  - `user_id` (path, integer, required)
- **Request Body**: `UserUpdate`
- **Responses**:
  - `200`: Successful Response (`UserResponse`)

### `DELETE` `/users/{user_id}`
**Summary**: Delete User
**Description**: Delete a user. Admin only.

- **Parameters**:
  - `user_id` (path, integer, required)
- **Responses**:
  - `204`: Successful Response (No Content)

---

## Financial Records

### `GET` `/records/`
**Summary**: List Records
**Description**: List financial records with optional filters and pagination. Available to all authenticated active users.

- **Parameters**:
  - `entry_type` (query, `EntryType`, optional)
  - `category` (query, string, optional)
  - `date_from` (query, date string, optional)
  - `date_to` (query, date string, optional)
  - `page` (query, integer, default: 1)
  - `page_size` (query, integer, default: 20)
- **Responses**:
  - `200`: `PaginatedRecords`

### `POST` `/records/`
**Summary**: Create Record
**Description**: Create a new financial record. Admin only.

- **Request Body**: `RecordCreate`
- **Responses**:
  - `201`: `RecordResponse`

### `GET` `/records/{record_id}`
**Summary**: Get Record
**Description**: Retrieve a single record by ID. Available to all authenticated active users.

- **Parameters**:
  - `record_id` (path, integer, required)
- **Responses**:
  - `200`: `RecordResponse`

### `PATCH` `/records/{record_id}`
**Summary**: Update Record
**Description**: Update an existing financial record. Admin only.

- **Parameters**:
  - `record_id` (path, integer, required)
- **Request Body**: `RecordUpdate`
- **Responses**:
  - `200`: `RecordResponse`

### `DELETE` `/records/{record_id}`
**Summary**: Delete Record
**Description**: Soft-delete a financial record. Admin only. The record is flagged as deleted but kept in the database for audit purposes.

- **Parameters**:
  - `record_id` (path, integer, required)
- **Responses**:
  - `204`: Successful Response (No Content)

---

## Dashboard Analytics

*Note: All Dashboard Analytics endpoints are available to analysts and admins.*

### `GET` `/dashboard/summary`
**Summary**: Get Dashboard Summary
**Description**: Get overall financial summary. Includes: total income, total expenses, net balance, record count.

- **Responses**:
  - `200`: `DashboardSummary`

### `GET` `/dashboard/categories`
**Summary**: Get Category Breakdown
**Description**: Get financial totals by category and type.

- **Responses**:
  - `200`: List of `CategoryTotal`

### `GET` `/dashboard/trends/monthly`
**Summary**: Get Monthly Data
**Description**: Get monthly income vs expenses trends.

- **Parameters**:
  - `months` (query, integer, default: 12)
- **Responses**:
  - `200`: List of `MonthlyTrend`

### `GET` `/dashboard/trends/weekly`
**Summary**: Get Weekly Data
**Description**: Get weekly income vs expenses trends.

- **Parameters**:
  - `weeks` (query, integer, default: 8)
- **Responses**:
  - `200`: List of `WeeklyTrend`

### `GET` `/dashboard/recent`
**Summary**: Get Recent Activity List
**Description**: Get recently created financial records.

- **Parameters**:
  - `limit` (query, integer, default: 10)
- **Responses**:
  - `200`: List of `RecentActivity`

### `GET` `/dashboard/`
**Summary**: Get Full Dashboard
**Description**: Get complete dashboard data. Includes summary, categories, monthly trends, weekly trends, and recent activity.

- **Responses**:
  - `200`: `DashboardData`

---

## System

### `GET` `/health`
**Summary**: Health Check
**Description**: Simple liveness probe — returns OK if the server is running.

- **Responses**:
  - `200`: Successful Response

---

## Data Models

> [!NOTE]
> Below are the core schemas used in the requests and responses.

### Authentication & Users
- **TokenRequest**: `email` (string), `password` (string)
- **TokenResponse**: `access_token` (string), `token_type` (string)
- **UserCreate**: `email`, `password`, `full_name` (optional), `role` (viewer/analyst/admin)
- **UserResponse**: `id`, `email`, `full_name`, `role`, `is_active`

### Financial Records
- **EntryType**: Enum (`income`, `expense`)
- **RecordCreate**: `amount` (>0), `entry_type`, `category`, `date`, `description`
- **RecordResponse**: `id`, `amount`, `entry_type`, `category`, `date`, `description`, `created_by`, `created_at`
- **PaginatedRecords**: `total`, `page`, `page_size`, `total_pages`, `items` (List of `RecordResponse`)

### Dashboard
- **DashboardSummary**: `total_income`, `total_expenses`, `net_balance`, `total_records`
- **CategoryTotal**: `category`, `entry_type`, `total`, `count`
- **MonthlyTrend**: `year`, `month`, `income`, `expenses`, `net`
- **WeeklyTrend**: `year`, `week`, `income`, `expenses`, `net`
- **RecentActivity**: `id`, `amount`, `entry_type`, `category`, `description`, `date`
- **DashboardData**: Combined `summary`, `category_totals`, `monthly_trends`, `weekly_trends`, and `recent_activity`.
