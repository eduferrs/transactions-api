from datetime import date, datetime
from typing import Annotated, Optional

from pydantic import EmailStr, Field, field_validator

from src.contrib.schemas import BaseSchema


class UserIn(BaseSchema):
    full_name: Annotated[
        str,
        Field(description="Nome completo", json_schema_extra={"example": "Eduardo Silva"}, min_length=2, max_length=60),
    ]
    birth_date: Annotated[date, Field(description="Data de nascimento", json_schema_extra={"example": "31/12/2000"})]
    cpf: Annotated[
        str,
        Field(
            description="CPF (apenas números)",
            json_schema_extra={"example": "12345678900"},
            min_length=11,
            max_length=11,
        ),
    ]
    email: Annotated[
        EmailStr, Field(description="E-mail", json_schema_extra={"example": "email@yahoo.com"}, max_length=50)
    ]
    password: Annotated[
        str,
        Field(description="Senha do usuário", json_schema_extra={"example": "12345678"}, min_length=6, max_length=32),
    ]

    @field_validator("birth_date", mode="before")
    @classmethod
    def parse_birth_date(cls, value):
        if isinstance(value, date):
            return value

        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%d/%m/%Y").date()
            except ValueError:
                pass

            try:
                return datetime.strptime(value, "%d-%m-%Y").date()
            except ValueError:
                pass
        raise ValueError("A data deve estar no formato DD/MM/AAAA ou DD-MM-AAAA")

    @field_validator("cpf")
    def validate_cpf(cls, cpf):
        if not cpf.isdigit():
            raise ValueError("CPF deve conter apenas números")
        return cpf

    @field_validator("email", mode="after")
    @classmethod
    def lower_case_email(cls, email: str):
        return email.lower()


class UserUpdate(BaseSchema):
    full_name: Annotated[
        Optional[str],
        Field(
            None, description="Seu nome", json_schema_extra={"example": "Eduardo F. Silva"}, min_length=2, max_length=60
        ),
    ]
    email: Annotated[
        Optional[EmailStr],
        Field(
            None, description="Seu novo e-mail", json_schema_extra={"example": "novo-email@yahoo.com"}, max_length=50
        ),
    ]
