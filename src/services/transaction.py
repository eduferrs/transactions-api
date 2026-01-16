from datetime import datetime, time, timezone
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.execptions import AccountNotFoundError, BusinessError
from src.models.account import AccountModel
from src.models.transaction import TransactionModel, TransactionType
from src.models.user import UserModel
from src.schemas.transaction import TransactionIn, TransferIn
from src.services.user import UserService

user_service = UserService()


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

    async def create_transfer(
        self, transfer_in: TransferIn, current_user: int, db_session: AsyncSession
    ) -> TransactionModel:

        # Fazendo join porque precisa do nome desse usuário para registrar no campo da transação
        # Se buscasse pelo UserModel, não haveria bloqueio na linha da conta
        # O bloqueio é sempre na linha do model dentro do select()
        query = select(AccountModel).join(UserModel).where(UserModel.pk_id == current_user.pk_id).with_for_update()
        result = await db_session.execute(query)
        account = result.scalars().first()
        user = account.user

        if not account:
            raise AccountNotFoundError

        if account.balance < transfer_in.amount:
            raise BusinessError("Insufficient balance for this transaction.")

        if account.transfer_limit < transfer_in.amount:
            raise BusinessError("Amount exceeds transfer limit.")

        counterparty = await user_service.get_user_by_account_number(
            db_session, transfer_in.counterparty_account_number
        )

        if (
            not counterparty
            or (counterparty.checking_account.branch != transfer_in.counterparty_branch)
            or (counterparty.checking_account.account_number != transfer_in.counterparty_account_number)
        ):
            raise BusinessError("Invalid branch or account number.")

        account.balance -= transfer_in.amount
        counterparty.checking_account.balance += transfer_in.amount
        db_session.add(account)
        db_session.add(counterparty)

        # Explicação complexa sobre ids no transactionModel
        operation_id = uuid4()

        transfer_out = TransactionModel(
            id=uuid4(),
            operation_id=operation_id,
            created_at=datetime.now(timezone.utc),
            type=TransactionType.TRANSFER_OUT,
            account_id=account.pk_id,
            amount=transfer_in.amount,
            counterparty_name=counterparty.full_name,
            counterparty_branch=counterparty.checking_account.branch,
            counterparty_account_number=counterparty.checking_account.account_number,
        )
        db_session.add(transfer_out)

        ############################## Não usando model_dumps aqui. Viria com ag e c/c do mesmo usuário (que recebeu)
        # Para não confundir, deixei a criação de cima também.
        transfer = TransactionModel(
            id=uuid4(),
            operation_id=operation_id,
            created_at=datetime.now(timezone.utc),
            type=TransactionType.TRANSFER_IN,
            account_id=counterparty.checking_account.pk_id,
            amount=transfer_in.amount,
            counterparty_name=user.full_name,
            counterparty_branch=user.checking_account.branch,
            counterparty_account_number=user.checking_account.account_number,
        )
        db_session.add(transfer)

        await db_session.commit()
        await db_session.refresh(transfer_out, attribute_names=["account"])

        return transfer_out
