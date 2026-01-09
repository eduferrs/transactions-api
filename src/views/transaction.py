from decimal import Decimal
from typing import Annotated

from pydantic import Field

from src.contrib.schemas import BaseSchema, OutMixin
from src.views.account import AccountBasicOut


class TransactionOut(BaseSchema, OutMixin):
    amount: Annotated[
        Decimal,
        Field(
            description="Valor da operação",
            json_schema_extra={"example": 1.99},
            ge=0.01,
            decimal_places=2,
            max_digits=14,
        ),
    ]
    account: Annotated[AccountBasicOut, Field(description="Conta-corrente")]
