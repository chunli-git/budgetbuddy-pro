from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionRead

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = Transaction(
        amount=transaction_data.amount,
        description=transaction_data.description,
        category=transaction_data.category,
        transaction_type=transaction_data.transaction_type,
        transaction_date=transaction_data.transaction_date,
        user_id=current_user.id,
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction


@router.get("/", response_model=list[TransactionRead])
def get_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Transaction)
        .filter(Transaction.user_id == current_user.id)
        .order_by(Transaction.transaction_date.desc())
        .all()
    )