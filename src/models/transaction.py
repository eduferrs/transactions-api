import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DECIMAL, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from contrib.models import BaseModel


class TransactionType(str, enum.Enum):
    DEPOSIT = "deposito"
    WITHDRAWAL = "saque"
    TRANSFER_IN = "recebimento"
    TRANSFER_OUT = "envio"


class TransactionModel(BaseModel):
    __tablename__ = "transactions"

    amount: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False)
    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.pk_id"))
    account: Mapped["AccountModel"] = relationship(back_populates="transactions")

    counterparty_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    counterparty_branch: Mapped[str | None] = mapped_column(String(4), nullable=True)
    counterparty_account_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
