from datetime import datetime, time, timezone
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.execptions import AccountNotFoundError, BusinessError
from src.models.account import AccountModel
from src.models.transaction import TransactionModel, TransactionType
from src.schemas.transaction import TransactionIn


class TransactionService:

    async def create_deposit(
        self, transaction_in: TransactionIn, account_id: int, db_session: AsyncSession
    ) -> TransactionModel:

        query = select(AccountModel).where(AccountModel.pk_id == account_id).with_for_update()
        result = await db_session.execute(query)
        print(result)
        account = result.scalars().first()

        if not account:
            raise AccountNotFoundError

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

    async def create_withdrawal(
        self, transaction_in: TransactionIn, account_id: int, db_session: AsyncSession
    ) -> TransactionModel:

        query = select(AccountModel).where(AccountModel.pk_id == account_id).with_for_update()
        result = await db_session.execute(query)
        account = result.scalars().first()

        if not account:
            raise AccountNotFoundError

        midnight = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

        query = select(func.sum(TransactionModel.amount)).where(
            and_(
                TransactionModel.account_id == account_id,
                TransactionModel.type == "saque",
                TransactionModel.created_at >= midnight,
            )
        )
        ##print(query)
        result = await db_session.execute(query)

        amount_withdrawn_today = result.scalar() or Decimal(0)

        if (account.balance - transaction_in.amount) < 0:
            raise BusinessError(message="Not enough balance for this transaction.")

        if (transaction_in.amount + amount_withdrawn_today) > account.daily_withdrawal_limit:
            raise BusinessError(
                message=(
                    f"This transaction exceeds your daily withdrawal limit (${account.daily_withdrawal_limit})."
                    f"Today you've already withdrawn ${amount_withdrawn_today}."
                    f"Your remaining limit for today is ${account.daily_withdrawal_limit - amount_withdrawn_today}."
                )
            )

        ### ok
        account.balance -= transaction_in.amount
        db_session.add(account)

        transaction_model = TransactionModel(
            **transaction_in.model_dump(),
            id=uuid4(),
            created_at=datetime.now(timezone.utc),
            type=TransactionType.WITHDRAWAL,
            account_id=account_id,
        )

        db_session.add(transaction_model)
        await db_session.commit()
        await db_session.refresh(transaction_model, attribute_names=["account"])

        return transaction_model
