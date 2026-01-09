from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.account import AccountModel
from src.models.transaction import TransactionModel, TransactionType
from src.schemas.transaction import TransactionIn


class TransactionService:

    async def create_deposit(
        self, transaction_in: TransactionIn, account_id: int, db_session: AsyncSession
    ) -> TransactionModel:

        query = select(AccountModel).where(AccountModel.pk_id == account_id).with_for_update()
        result = await db_session.execute(query)
        account = result.scalars().first()

        if not account:
            raise Exception("Conta bancária não localizada")

        account.balance += transaction_in.amount
        db_session.add(account)

        transaction_model = TransactionModel(
            **transaction_in.model_dump(),
            id=uuid4(),
            created_at=datetime.now(timezone.utc),
            type=TransactionType.DEPOSIT,
            account_id=account_id,
        )

        db_session.add(transaction_model)
        await db_session.commit()
        await db_session.refresh(transaction_model, attribute_names=["account"])

        return transaction_model
