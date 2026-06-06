from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


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

    model_config = ConfigDict(from_attributes=True)


class BudgetStatus(BaseModel):
    category: str
    limit_amount: Decimal
    spent_amount: Decimal
    remaining_amount: Decimal
    usage_percentage: float
    status: str