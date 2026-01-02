from datetime import date

from sqlalchemy import Date, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from contrib.models import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)  # AAAA-MM-DD
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    checking_account: Mapped["AccountModel"] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan", lazy="selectin"
    )
