import pytest
from pydantic import ValidationError

from app.schemas.budget import BudgetCreate


def test_budget_limit_amount_must_be_positive():
    with pytest.raises(ValidationError):
        BudgetCreate(
            category="Food",
            limit_amount=-500,
            period_month="2026-06-01",
        )


def test_budget_category_must_not_be_empty():
    with pytest.raises(ValidationError):
        BudgetCreate(
            category="",
            limit_amount=500,
            period_month="2026-06-01",
        )


def test_budget_valid_data():
    budget = BudgetCreate(
        category="Food",
        limit_amount=500,
        period_month="2026-06-01",
    )

    assert budget.category == "Food"
    assert budget.limit_amount == 500