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
