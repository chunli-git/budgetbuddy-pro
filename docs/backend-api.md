# BudgetBuddy Pro — Backend API Documentation

## Overview

BudgetBuddy Pro backend is a REST API built with FastAPI, PostgreSQL, SQLAlchemy, Alembic and JWT authentication.

The API allows users to manage:

- Authentication
- Transactions
- Budgets
- Savings goals
- Recurring transactions
- Dashboard statistics
- Smart alerts
- CSV exports

Base URL in development:

```txt
http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs


Authentication

Most routes are protected and require a JWT token.

Register
POST /auth/register
Login
POST /auth/login

Example body:

{
  "email": "test4@budgetbuddy.com",
  "password": "Password123"
}
Current user
GET /auth/me
Transactions
Create transaction
POST /transactions/
List transactions
GET /transactions/

Supports filters:

transaction_type
category
start_date
end_date
search
Transaction summary
GET /transactions/summary
Export transactions as CSV
GET /transactions/export/csv
Get one transaction
GET /transactions/{transaction_id}
Update transaction
PATCH /transactions/{transaction_id}
Delete transaction
DELETE /transactions/{transaction_id}
Budgets
Create budget
POST /budgets/
List budgets
GET /budgets/
Get one budget
GET /budgets/{budget_id}
Update budget
PATCH /budgets/{budget_id}
Delete budget
DELETE /budgets/{budget_id}
Budget status
GET /budgets/status
Savings Goals
Create savings goal
POST /savings-goals/
List savings goals
GET /savings-goals/
Get one savings goal
GET /savings-goals/{goal_id}
Update savings goal
PATCH /savings-goals/{goal_id}
Delete savings goal
DELETE /savings-goals/{goal_id}
Recurring Transactions
Create recurring transaction
POST /recurring-transactions/
List recurring transactions
GET /recurring-transactions/
Get one recurring transaction
GET /recurring-transactions/{recurring_id}
Update recurring transaction
PATCH /recurring-transactions/{recurring_id}
Delete recurring transaction
DELETE /recurring-transactions/{recurring_id}
Process due recurring transactions
POST /recurring-transactions/process-due
Dashboard
Budget Health Score
GET /dashboard/health-score
Smart alerts
GET /dashboard/alerts
Expenses by category
GET /dashboard/expenses-by-category
Monthly summary
GET /dashboard/monthly-summary
Dashboard overview
GET /dashboard/overview
Recent transactions
GET /dashboard/recent-transactions
Validation Rules

The API validates user input with Pydantic.

Examples:

Amounts must be positive.
Descriptions and categories cannot be empty.
Transaction type must be either income or expense.
Recurring frequency must be daily, weekly, or monthly.
Passwords must have a valid length.
Testing

Backend tests are written with pytest.

Run tests locally:

pytest

GitHub Actions automatically runs backend tests on every push to main.


