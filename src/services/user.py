import random
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.execptions import *
from src.models.account import AccountModel
from src.models.user import UserModel
from src.schemas.user import UserIn, UserUpdate
from src.security import get_password_hash


class UserService:

    async def _generate_account_number(self, db_session: AsyncSession) -> str:
        query = select(func.nextval("account_number_seq"))
        result = await db_session.execute(query)

        next_num = result.scalar()
        digit = random.randint(0, 9)

        return f"{next_num}-{digit}"

    async def register_user(self, user_in: UserIn, db_session: AsyncSession):

        query = select(UserModel).where(or_(UserModel.cpf == user_in.cpf, UserModel.email == user_in.email))
        result = await db_session.execute(query)
        if result.scalars().first():
            raise CreateUserError

        try:
            account_num = await self._generate_account_number(db_session)
            account_model = AccountModel(account_number=account_num)

            user_model = UserModel(
                **user_in.model_dump(exclude={"password"}),
                id=uuid4(),
                created_at=datetime.now(timezone.utc),
                password=get_password_hash(user_in.password),
                checking_account=account_model,
            )

            db_session.add(user_model)
            await db_session.commit()

            query = (
                select(UserModel)
                .options(selectinload(UserModel.checking_account))
                .where(UserModel.pk_id == user_model.pk_id)
            )
            result = await db_session.execute(query)
            new_user = result.scalars().first()

            return new_user
        except Exception as e:
            await db_session.rollback()
            raise InternalServerError

    async def update(self, user_up: UserUpdate, current_user: UserModel, db_session: AsyncSession) -> UserModel:

        user_update = user_up.model_dump(exclude_unset=True)

        if "email" in user_update:
            if user_update["email"] != current_user.email:
                query = select(UserModel).where(UserModel.email == user_update["email"])
                result = await db_session.execute(query)
                found = result.scalars().first()

                if found:
                    raise UserUpdateError

        for key, value in user_update.items():
            setattr(current_user, key, value)

        await db_session.commit()
        await db_session.refresh(current_user)
        return current_user

    async def delete(self, user: UserModel, db_session: AsyncSession) -> None:
        # Lock para evitar novas transações durante a deleção
        query = select(AccountModel).where(AccountModel.user_id == user.pk_id).with_for_update()
        result = await db_session.execute(query)
        account = result.scalars().first()

        if account.balance != 0:
            raise BusinessError("Your balance must be 0 before closing the account")

        user.is_active = False
        account.is_active = False

        db_session.add(user)
        await db_session.commit()

    async def get_user_by_email_or_cpf(self, db_session: AsyncSession, username: str) -> UserModel | None:
        query = select(UserModel).where(
            or_(UserModel.cpf == username, UserModel.email == username), UserModel.is_active == True
        )
        result = await db_session.execute(query)

        return result.scalars().first()

    async def get_user_by_account_number(self, db_session: AsyncSession, account_number: str) -> UserModel | None:

        query = (
            select(UserModel)
            .join(UserModel.checking_account)
            .where(
                AccountModel.account_number == account_number,
                AccountModel.is_active == True,
                UserModel.is_active == True,
            )
            .with_for_update(of=AccountModel)
        )
        result = await db_session.execute(query)
        return result.scalars().first()
