from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.budget import Budget
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.dashboard import BudgetHealthScore

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/health-score", response_model=BudgetHealthScore)
def get_budget_health_score(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    total_income = (
        db.query(func.sum(Transaction.amount))
        .filter(
            Transaction.user_id == current_user.id,
            Transaction.transaction_type == "income",
        )
        .scalar()
        or Decimal("0.00")
    )

    total_expenses = (
        db.query(func.sum(Transaction.amount))
        .filter(
            Transaction.user_id == current_user.id,
            Transaction.transaction_type == "expense",
        )
        .scalar()
        or Decimal("0.00")
    )

    total_budget_limits = (
        db.query(func.sum(Budget.limit_amount))
        .filter(Budget.user_id == current_user.id)
        .scalar()
        or Decimal("0.00")
    )

    balance = total_income - total_expenses

    if total_budget_limits > 0:
        budget_usage_percentage = float((total_expenses / total_budget_limits) * 100)
    else:
        budget_usage_percentage = 0.0

    score = 100

    if balance < 0:
        score -= 40

    if budget_usage_percentage > 100:
        score -= 30
    elif budget_usage_percentage > 80:
        score -= 15

    if total_income == 0:
        score -= 20

    score = max(score, 0)

    if score >= 80:
        status_text = "Excellent"
    elif score >= 60:
        status_text = "Good"
    elif score >= 40:
        status_text = "Needs attention"
    else:
        status_text = "Critical"

    return {
        "score": score,
        "status": status_text,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance,
        "budget_usage_percentage": round(budget_usage_percentage, 2),
    }