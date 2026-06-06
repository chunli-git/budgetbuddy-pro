from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TransactionCreate(BaseModel):
    amount: Decimal = Field(gt=0)
    description: str = Field(min_length=1, max_length=255)
    category: str = Field(min_length=1, max_length=100)
    transaction_type: Literal["income", "expense"]
    transaction_date: date


class TransactionUpdate(BaseModel):
    amount: Decimal | None = Field(default=None, gt=0)
    description: str | None = Field(default=None, min_length=1, max_length=255)
    category: str | None = Field(default=None, min_length=1, max_length=100)
    transaction_type: Literal["income", "expense"] | None = None
    transaction_date: date | None = None


class TransactionRead(BaseModel):
    id: int
    amount: Decimal
    description: str
    category: str
    transaction_type: str
    transaction_date: date
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TransactionSummary(BaseModel):
    total_income: Decimal
    total_expenses: Decimal
    balance: Decimal