from decimal import Decimal
from typing import Annotated

from pydantic import Field

from src.contrib.schemas import BaseSchema


class AccountBasicOut(BaseSchema):
    branch: Annotated[str, Field(description="Agência", json_schema_extra={"example": "0001"})]
    account_number: Annotated[str, Field(description="Número da conta", json_schema_extra={"example": "12345-6"})]
    balance: Annotated[Decimal, Field(description="Saldo", json_schema_extra={"example": 0.00})]


class AccountOut(BaseSchema):
    branch: Annotated[str, Field(description="Agência", json_schema_extra={"example": "0001"})]
    account_number: Annotated[str, Field(description="Número da conta", json_schema_extra={"example": "12345-6"})]
    balance: Annotated[Decimal, Field(description="Saldo", json_schema_extra={"example": 0.00})]
    daily_withdrawal_limit: Annotated[
        Decimal, Field(description="Limite diário de saque", json_schema_extra={"example": 1000.00})
    ]
    transfer_limit: Annotated[
        Decimal, Field(description="Limite de cada transferência", json_schema_extra={"example": 2500.00})
    ]
