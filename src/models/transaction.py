import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DECIMAL, UUID, CheckConstraint, DateTime, Enum, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.contrib.models import BaseModel


def get_enum_values(enum):
    values = []
    for item in enum:
        values.append(item.value)
    return values


class TransactionType(str, enum.Enum):
    DEPOSIT = "deposito"
    WITHDRAWAL = "saque"
    TRANSFER_IN = "recebimento"
    TRANSFER_OUT = "envio"


class TransactionModel(BaseModel):
    __tablename__ = "transactions"

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False)
    type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType, values_callable=get_enum_values), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.pk_id"))
    account: Mapped["AccountModel"] = relationship(back_populates="transactions")

    operation_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    counterparty_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    counterparty_branch: Mapped[str | None] = mapped_column(String(4), nullable=True)
    counterparty_account_number: Mapped[str | None] = mapped_column(String(20), nullable=True)

    __table_args__ = (
        CheckConstraint(
            """
            type NOT IN ('recebimento', 'envio')
            OR
            operation_id IS NOT NULL
            """,
            name="chk_operation_id_transfer",
        ),
        Index("ix_transactions_account_date", "account_id", "created_at"),
        Index(
            "ix_transactions_operation_id",
            "operation_id",
            postgresql_where=(operation_id.is_not(None)),
        ),
    )
