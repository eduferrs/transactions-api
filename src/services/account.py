from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import TransactionModel


class AccountService:
    async def get_statement(self, account_id: int, db_session: AsyncSession):

        query = (
            select(TransactionModel)
            .where(TransactionModel.account_id == account_id)
            .order_by(TransactionModel.created_at.desc())
        )

        return await apaginate(db_session, query)
