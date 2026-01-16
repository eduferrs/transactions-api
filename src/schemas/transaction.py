from decimal import Decimal
from typing import Annotated

from pydantic import Field

from src.contrib.schemas import BaseSchema


class TransactionIn(BaseSchema):
    amount: Annotated[
        Decimal,
        Field(
            description="Valor",
            json_schema_extra={"example": 1.99},
            ge=0.01,
            decimal_places=2,
            max_digits=14,
        ),
    ]


class TransferIn(TransactionIn):
    counterparty_branch: Annotated[str, Field(description="AG", json_schema_extra={"example": "0001"}, max_length=4)]
    counterparty_account_number: Annotated[str, Field(description="C/C", json_schema_extra={"example": "10001-9"})]
