from datetime import date
from typing import Annotated

from pydantic import Field

from src.contrib.schemas import BaseSchema, OutMixin
from src.views.account import AccountOut


class UserOut(BaseSchema, OutMixin):
    full_name: Annotated[str, Field(description="Nome completo", example="Eduardo Silva", max_length=60)]
    cpf: Annotated[str, Field(description="CPF (apenas números)", example="12345678900", max_length=11)]
    email: Annotated[str, Field(description="E-mail", example="email@yahoo.com", max_length=50)]
    birth_date: Annotated[date, Field(description="Data de nascimento", example="31-12-2000")]
    checking_account: Annotated[AccountOut, Field(description="Conta-corrente")]

    # Do mixin:
    # uuid
    # created_at
