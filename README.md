# BudgetBuddy Pro 
## Backend Status

The backend API is functional and includes:

- FastAPI REST API
- PostgreSQL database with Docker
- SQLAlchemy ORM
- Alembic migrations
- JWT authentication
- Protected user-specific routes
- Transactions CRUD
- Budgets CRUD
- Savings goals CRUD
- Recurring transactions CRUD
- Dashboard statistics
- Smart alerts
- CSV export
- Input validation with Pydantic
- Automated tests with pytest
- GitHub Actions CI

Backend documentation:

- `docs/backend-api.md`
- `docs/backend-architecture.md`




## Backend Setup

### 1. Start PostgreSQL with Docker

```bash
docker compose up -d

2. Go to the backend folder
cd backend
3. Create and activate a virtual environment
python -m venv .venv

Windows:

.venv\Scripts\activate
4. Install dependencies
pip install -r requirements.txt
5. Create the environment file

Create a .env file based on .env.example.

6. Apply database migrations
alembic upgrade head
7. Run the backend
python -m fastapi dev app/main.py

Backend URL:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs
8. Run backend tests
pytest