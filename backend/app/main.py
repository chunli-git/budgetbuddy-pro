from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.routers import auth, transactions

app = FastAPI(title="BudgetBuddy Pro API")

app.include_router(auth.router)
app.include_router(transactions.router)


@app.get("/")
def root():
    return {"message": "BudgetBuddy Pro API is running"}


@app.get("/db-health")
def db_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "connected"}