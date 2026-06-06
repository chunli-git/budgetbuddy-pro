from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.budget import Budget
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.dashboard import BudgetHealthScore, CategoryExpense, SmartAlert

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def get_next_month(month_date: date) -> date:
    if month_date.month == 12:
        return date(month_date.year + 1, 1, 1)

    return date(month_date.year, month_date.month + 1, 1)


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


@router.get("/alerts", response_model=list[SmartAlert])
def get_smart_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    alerts = []

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

    balance = total_income - total_expenses

    if total_income == 0:
        alerts.append(
            {
                "type": "income",
                "title": "No income recorded",
                "message": "You have not recorded any income yet.",
                "severity": "warning",
            }
        )

    if balance < 0:
        alerts.append(
            {
                "type": "balance",
                "title": "Negative balance",
                "message": "Your expenses are higher than your income.",
                "severity": "critical",
            }
        )

    budgets = db.query(Budget).filter(Budget.user_id == current_user.id).all()

    for budget in budgets:
        month_start = budget.period_month
        month_end = get_next_month(month_start)

        spent_amount = (
            db.query(func.sum(Transaction.amount))
            .filter(
                Transaction.user_id == current_user.id,
                Transaction.category == budget.category,
                Transaction.transaction_type == "expense",
                Transaction.transaction_date >= month_start,
                Transaction.transaction_date < month_end,
            )
            .scalar()
            or Decimal("0.00")
        )

        percentage_used = float((spent_amount / budget.limit_amount) * 100)

        if percentage_used >= 100:
            alerts.append(
                {
                    "type": "budget",
                    "title": f"{budget.category} budget exceeded",
                    "message": f"You have used {round(percentage_used, 2)}% of your budget.",
                    "severity": "critical",
                }
            )
        elif percentage_used >= 80:
            alerts.append(
                {
                    "type": "budget",
                    "title": f"{budget.category} budget almost reached",
                    "message": f"You have used {round(percentage_used, 2)}% of your budget.",
                    "severity": "warning",
                }
            )

    return alerts

@router.get("/expenses-by-category", response_model=list[CategoryExpense])
def get_expenses_by_category(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    results = (
        db.query(
            Transaction.category,
            func.sum(Transaction.amount).label("total_amount"),
        )
        .filter(
            Transaction.user_id == current_user.id,
            Transaction.transaction_type == "expense",
        )
        .group_by(Transaction.category)
        .order_by(func.sum(Transaction.amount).desc())
        .all()
    )

    return [
        {
            "category": category,
            "total_amount": Decimal(total_amount).quantize(Decimal("0.01")),
        }
        for category, total_amount in results
    ]