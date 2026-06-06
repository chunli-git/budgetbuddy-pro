import pytest
from pydantic import ValidationError

from app.schemas.transaction import TransactionCreate


def test_transaction_amount_must_be_positive():
    with pytest.raises(ValidationError):
        TransactionCreate(
            amount=-20,
            description="Test",
            category="Food",
            transaction_type="expense",
            transaction_date="2026-06-06",
        )


def test_transaction_type_must_be_valid():
    with pytest.raises(ValidationError):
        TransactionCreate(
            amount=20,
            description="Test",
            category="Food",
            transaction_type="wrong",
            transaction_date="2026-06-06",
        )


def test_transaction_valid_data():
    transaction = TransactionCreate(
        amount=20,
        description="Groceries",
        category="Food",
        transaction_type="expense",
        transaction_date="2026-06-06",
    )

    assert transaction.amount == 20
    assert transaction.description == "Groceries"
    assert transaction.category == "Food"
    assert transaction.transaction_type == "expense"