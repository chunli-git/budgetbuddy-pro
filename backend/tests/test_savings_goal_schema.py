import pytest
from pydantic import ValidationError

from app.schemas.savings_goal import SavingsGoalCreate


def test_savings_goal_target_amount_must_be_positive():
    with pytest.raises(ValidationError):
        SavingsGoalCreate(
            name="Vacation",
            target_amount=-1000,
            current_amount=0,
            target_date="2026-12-31",
        )


def test_savings_goal_current_amount_must_not_be_negative():
    with pytest.raises(ValidationError):
        SavingsGoalCreate(
            name="Vacation",
            target_amount=1000,
            current_amount=-50,
            target_date="2026-12-31",
        )


def test_savings_goal_name_must_not_be_empty():
    with pytest.raises(ValidationError):
        SavingsGoalCreate(
            name="",
            target_amount=1000,
            current_amount=100,
            target_date="2026-12-31",
        )


def test_savings_goal_valid_data():
    goal = SavingsGoalCreate(
        name="Vacation",
        target_amount=1000,
        current_amount=100,
        target_date="2026-12-31",
    )

    assert goal.name == "Vacation"
    assert goal.target_amount == 1000
    assert goal.current_amount == 100