from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date, timedelta

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.recurring_transaction import RecurringTransaction
from app.models.user import User
from app.schemas.recurring_transaction import (
    RecurringTransactionCreate,
    RecurringTransactionRead,
    RecurringTransactionUpdate,
    RecurringTransactionProcessResult,
)
from app.models.transaction import Transaction

router = APIRouter(prefix="/recurring-transactions", tags=["recurring transactions"])


@router.post("/", response_model=RecurringTransactionRead, status_code=status.HTTP_201_CREATED)
def create_recurring_transaction(
    recurring_data: RecurringTransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recurring_transaction = RecurringTransaction(
        amount=recurring_data.amount,
        description=recurring_data.description,
        category=recurring_data.category,
        transaction_type=recurring_data.transaction_type,
        frequency=recurring_data.frequency,
        start_date=recurring_data.start_date,
        next_run_date=recurring_data.next_run_date,
        user_id=current_user.id,
    )

    db.add(recurring_transaction)
    db.commit()
    db.refresh(recurring_transaction)

    return recurring_transaction


@router.get("/", response_model=list[RecurringTransactionRead])
def get_recurring_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(RecurringTransaction)
        .filter(RecurringTransaction.user_id == current_user.id)
        .order_by(RecurringTransaction.created_at.desc())
        .all()
    )

@router.get("/{recurring_id}", response_model=RecurringTransactionRead)
def get_recurring_transaction(
    recurring_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recurring_transaction = (
        db.query(RecurringTransaction)
        .filter(
            RecurringTransaction.id == recurring_id,
            RecurringTransaction.user_id == current_user.id,
        )
        .first()
    )

    if recurring_transaction is None:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Recurring transaction not found")

    return recurring_transaction

@router.patch("/{recurring_id}", response_model=RecurringTransactionRead)
def update_recurring_transaction(
    recurring_id: int,
    recurring_data: RecurringTransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recurring_transaction = (
        db.query(RecurringTransaction)
        .filter(
            RecurringTransaction.id == recurring_id,
            RecurringTransaction.user_id == current_user.id,
        )
        .first()
    )

    if recurring_transaction is None:
        raise HTTPException(status_code=404, detail="Recurring transaction not found")

    update_data = recurring_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(recurring_transaction, field, value)

    db.commit()
    db.refresh(recurring_transaction)

    return recurring_transaction

@router.delete("/{recurring_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recurring_transaction(
    recurring_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recurring_transaction = (
        db.query(RecurringTransaction)
        .filter(
            RecurringTransaction.id == recurring_id,
            RecurringTransaction.user_id == current_user.id,
        )
        .first()
    )

    if recurring_transaction is None:
        raise HTTPException(status_code=404, detail="Recurring transaction not found")

    db.delete(recurring_transaction)
    db.commit()

    return None

def calculate_next_run_date(current_date: date, frequency: str) -> date:
    if frequency == "daily":
        return current_date + timedelta(days=1)

    if frequency == "weekly":
        return current_date + timedelta(weeks=1)

    if frequency == "monthly":
        if current_date.month == 12:
            return date(current_date.year + 1, 1, current_date.day)
        return date(current_date.year, current_date.month + 1, current_date.day)

    if frequency == "yearly":
        return date(current_date.year + 1, current_date.month, current_date.day)

    return current_date


@router.post("/process-due", response_model=RecurringTransactionProcessResult)
def process_due_recurring_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    today = date.today()

    due_recurring_transactions = (
        db.query(RecurringTransaction)
        .filter(
            RecurringTransaction.user_id == current_user.id,
            RecurringTransaction.is_active == True,
            RecurringTransaction.next_run_date <= today,
        )
        .all()
    )

    created_count = 0

    for recurring_transaction in due_recurring_transactions:
        transaction = Transaction(
            amount=recurring_transaction.amount,
            description=recurring_transaction.description,
            category=recurring_transaction.category,
            transaction_type=recurring_transaction.transaction_type,
            transaction_date=today,
            user_id=current_user.id,
        )

        db.add(transaction)

        recurring_transaction.next_run_date = calculate_next_run_date(
            recurring_transaction.next_run_date,
            recurring_transaction.frequency,
        )

        created_count += 1

    db.commit()

    return {
        "created_transactions": created_count,
        "message": f"{created_count} recurring transaction(s) processed",
    }