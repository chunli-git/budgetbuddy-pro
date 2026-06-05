from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class RecurringTransaction(Base):
    __tablename__ = "recurring_transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    transaction_type: Mapped[str] = mapped_column(String(20), nullable=False)
    frequency: Mapped[str] = mapped_column(String(20), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    next_run_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="recurring_transactions")