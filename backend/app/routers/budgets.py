from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.budget import Budget
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.budget import BudgetCreate, BudgetRead, BudgetStatus, BudgetUpdate

router = APIRouter(prefix="/budgets", tags=["budgets"])


def get_next_month(month_date: date) -> date:
    if month_date.month == 12:
        return date(month_date.year + 1, 1, 1)

    return date(month_date.year, month_date.month + 1, 1)


@router.post("/", response_model=BudgetRead, status_code=status.HTTP_201_CREATED)
def create_budget(
    budget_data: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    budget = Budget(
        category=budget_data.category,
        limit_amount=budget_data.limit_amount,
        period_month=budget_data.period_month,
        user_id=current_user.id,
    )

    db.add(budget)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Budget already exists for this category and month",
        )

    db.refresh(budget)

    return budget


@router.get("/", response_model=list[BudgetRead])
def get_budgets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Budget)
        .filter(Budget.user_id == current_user.id)
        .order_by(Budget.period_month.desc())
        .all()
    )


@router.get("/status", response_model=list[BudgetStatus])
def get_budgets_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    budgets = db.query(Budget).filter(Budget.user_id == current_user.id).all()

    results = []

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

        remaining_amount = budget.limit_amount - spent_amount
        percentage_used = float((spent_amount / budget.limit_amount) * 100)

        results.append(
            {
                "budget_id": budget.id,
                "category": budget.category,
                "limit_amount": budget.limit_amount,
                "spent_amount": spent_amount,
                "remaining_amount": remaining_amount,
                "percentage_used": round(percentage_used, 2),
                "period_month": budget.period_month,
            }
        )

    return results


@router.get("/{budget_id}", response_model=BudgetRead)
def get_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    budget = (
        db.query(Budget)
        .filter(
            Budget.id == budget_id,
            Budget.user_id == current_user.id,
        )
        .first()
    )

    if budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")

    return budget


@router.patch("/{budget_id}", response_model=BudgetRead)
def update_budget(
    budget_id: int,
    budget_data: BudgetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    budget = (
        db.query(Budget)
        .filter(
            Budget.id == budget_id,
            Budget.user_id == current_user.id,
        )
        .first()
    )

    if budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")

    update_data = budget_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(budget, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Budget already exists for this category and month",
        )

    db.refresh(budget)

    return budget


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    budget = (
        db.query(Budget)
        .filter(
            Budget.id == budget_id,
            Budget.user_id == current_user.id,
        )
        .first()
    )

    if budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")

    db.delete(budget)
    db.commit()

    return None