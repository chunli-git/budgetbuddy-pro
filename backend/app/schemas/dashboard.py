from decimal import Decimal

from pydantic import BaseModel


class BudgetHealthScore(BaseModel):
    score: int
    status: str
    total_income: Decimal
    total_expenses: Decimal
    balance: Decimal
    budget_usage_percentage: float


class SmartAlert(BaseModel):
    type: str
    title: str
    message: str
    severity: str

class CategoryExpense(BaseModel):
    category: str
    total_amount: Decimal