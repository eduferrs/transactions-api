from decimal import Decimal
from typing import Annotated

from pydantic import UUID4, Field, computed_field

from src.contrib.schemas import BaseSchema, OutMixin
from src.models.transaction import TransactionType
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


class TransferOut(TransactionOut):
    operation_id: Annotated[UUID4, Field(description="Id da operação")]
    counterparty_name: Annotated[
        str, Field(description="Beneficiário", json_schema_extra={"example": "Elder S."}, max_length=60)
    ]
    counterparty_branch: Annotated[
        str, Field(description="Agência do destinatário", max_length=4, json_schema_extra={"example": "0001"})
    ]
    counterparty_account_number: Annotated[
        str, Field(description="Conta do destinatário", json_schema_extra={"example": "10001-9"}, max_length=20)
    ]


class StatementOut(BaseSchema, OutMixin):
    type: Annotated[TransactionType, Field(description="Tipo da transação")]
    operation_id: Annotated[UUID4 | None, Field(description="Id compartilhado (transferências)")] = None
    amount: Annotated[
        Decimal,
        Field(
            description="Valor da transação",
            json_schema_extra={"example": 1.99},
            decimal_places=2,
            max_digits=14,
        ),
    ]
    counterparty_name: Annotated[str | None, Field(description="Nome da contraparte")] = None
    counterparty_branch: Annotated[str | None, Field(description="Agência da contraparte")] = None
    counterparty_account_number: Annotated[str | None, Field(description="Conta da contraparte")] = None
