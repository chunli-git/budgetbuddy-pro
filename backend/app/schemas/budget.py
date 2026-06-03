from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class BudgetCreate(BaseModel):
    category: str = Field(min_length=1, max_length=100)
    limit_amount: Decimal = Field(gt=0)
    period_month: date


class BudgetUpdate(BaseModel):
    category: str | None = Field(default=None, min_length=1, max_length=100)
    limit_amount: Decimal | None = Field(default=None, gt=0)
    period_month: date | None = None


class BudgetRead(BaseModel):
    id: int
    category: str
    limit_amount: Decimal
    period_month: date
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True

class BudgetStatus(BaseModel):
    budget_id: int
    category: str
    limit_amount: Decimal
    spent_amount: Decimal
    remaining_amount: Decimal
    percentage_used: float
    period_month: date