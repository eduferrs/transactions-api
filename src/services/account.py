from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import TransactionModel


class AccountService:
    def __init__(self, session: AsyncSession):
        self.session = session

    def get_statement(self, account_id: int):

        return (
            select(TransactionModel)
            .where(TransactionModel.account_id == account_id)
            .order_by(TransactionModel.created_at.desc())
        )
