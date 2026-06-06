from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class RecurringTransactionCreate(BaseModel):
    amount: Decimal = Field(gt=0)
    description: str = Field(min_length=1, max_length=255)
    category: str = Field(min_length=1, max_length=100)
    transaction_type: Literal["income", "expense"]
    frequency: Literal["daily", "weekly", "monthly"]
    start_date: date
    next_run_date: date
    is_active: bool = True


class RecurringTransactionUpdate(BaseModel):
    amount: Decimal | None = Field(default=None, gt=0)
    description: str | None = Field(default=None, min_length=1, max_length=255)
    category: str | None = Field(default=None, min_length=1, max_length=100)
    transaction_type: Literal["income", "expense"] | None = None
    frequency: Literal["daily", "weekly", "monthly"] | None = None
    start_date: date | None = None
    next_run_date: date | None = None
    is_active: bool | None = None


class RecurringTransactionRead(BaseModel):
    id: int
    amount: Decimal
    description: str
    category: str
    transaction_type: str
    frequency: str
    start_date: date
    next_run_date: date
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RecurringTransactionProcessResult(BaseModel):
    created_transactions: int