import pytest
from pydantic import ValidationError

from app.schemas.recurring_transaction import RecurringTransactionCreate


def test_recurring_transaction_amount_must_be_positive():
    with pytest.raises(ValidationError):
        RecurringTransactionCreate(
            amount=-50,
            description="Netflix",
            category="Subscriptions",
            transaction_type="expense",
            frequency="monthly",
            start_date="2026-06-06",
            next_run_date="2026-06-06",
            is_active=True,
        )


def test_recurring_transaction_type_must_be_valid():
    with pytest.raises(ValidationError):
        RecurringTransactionCreate(
            amount=50,
            description="Netflix",
            category="Subscriptions",
            transaction_type="wrong",
            frequency="monthly",
            start_date="2026-06-06",
            next_run_date="2026-06-06",
            is_active=True,
        )


def test_recurring_transaction_frequency_must_be_valid():
    with pytest.raises(ValidationError):
        RecurringTransactionCreate(
            amount=50,
            description="Netflix",
            category="Subscriptions",
            transaction_type="expense",
            frequency="yearly",
            start_date="2026-06-06",
            next_run_date="2026-06-06",
            is_active=True,
        )


def test_recurring_transaction_valid_data():
    recurring = RecurringTransactionCreate(
        amount=50,
        description="Netflix",
        category="Subscriptions",
        transaction_type="expense",
        frequency="monthly",
        start_date="2026-06-06",
        next_run_date="2026-06-06",
        is_active=True,
    )

    assert recurring.amount == 50
    assert recurring.description == "Netflix"
    assert recurring.category == "Subscriptions"
    assert recurring.transaction_type == "expense"
    assert recurring.frequency == "monthly"