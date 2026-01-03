from decimal import Decimal
from typing import Annotated

from pydantic import Field

from src.contrib.schemas import BaseSchema


class AccountOut(BaseSchema):
    branch: Annotated[str, Field(description="Agência", example="0001")]
    account_number: Annotated[str, Field(description="Número da conta", example="12345-6")]
    balance: Annotated[Decimal, Field(description="Saldo", example=0.00)]
    daily_withdrawal_limit: Annotated[Decimal, Field(description="Limite diário de saque", example=1000.00)]
    transfer_limit: Annotated[Decimal, Field(description="Limite de cada transferência", example=2500.00)]
