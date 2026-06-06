from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SavingsGoalCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    target_amount: Decimal = Field(gt=0)
    current_amount: Decimal = Field(default=0, ge=0)
    target_date: date | None = None


class SavingsGoalUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    target_amount: Decimal | None = Field(default=None, gt=0)
    current_amount: Decimal | None = Field(default=None, ge=0)
    target_date: date | None = None


class SavingsGoalRead(BaseModel):
    id: int
    name: str
    target_amount: Decimal
    current_amount: Decimal
    target_date: date | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)