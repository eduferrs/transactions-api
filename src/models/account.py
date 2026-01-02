from decimal import Decimal

from sqlalchemy import DECIMAL, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from contrib.models import BaseModel


class AccountModel(BaseModel):
    __tablename__ = "accounts"

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    branch: Mapped[str] = mapped_column(String(4), default="0001", nullable=False)
    account_number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)

    balance: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False)
    daily_withdrawal_limit: Mapped[Decimal] = mapped_column(
        DECIMAL(12, 2), default=5000.00, nullable=False, comment="Maximum cumulative withdrawal amount allowed per day."
    )
    transfer_limit: Mapped[Decimal] = mapped_column(
        DECIMAL(12, 2), default=5000.00, nullable=False, comment="Maximum amount allowed per transfer."
    )
    transactions: Mapped[list["TransactionModel"]] = relationship(back_populates="account", lazy="selectin")

    user: Mapped["UserModel"] = relationship(back_populates="checking_account")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.pk_id"))
