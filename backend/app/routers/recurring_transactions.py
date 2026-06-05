from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.recurring_transaction import RecurringTransaction
from app.models.user import User
from app.schemas.recurring_transaction import (
    RecurringTransactionCreate,
    RecurringTransactionRead,
)

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