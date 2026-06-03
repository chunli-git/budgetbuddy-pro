from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    amount: Decimal = Field(gt=0)
    description: str = Field(min_length=1, max_length=255)
    category: str = Field(min_length=1, max_length=100)
    transaction_type: Literal["income", "expense"]
    transaction_date: date


class TransactionRead(BaseModel):
    id: int
    amount: Decimal
    description: str
    category: str
    transaction_type: str
    transaction_date: date
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True