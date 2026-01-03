import random
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.account import AccountModel
from src.models.user import UserModel
from src.schemas.auth import LoginIn
from src.schemas.user import UserIn
from src.security import get_password_hash, sign_jwt, verify_password


class AuthService:

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
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="CPF ou E-mail já cadastrado",
            )

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
            print(f"Erro: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno no servidor")

    async def authenticate_user(self, login_data: LoginIn, db_session: AsyncSession):
        query = select(UserModel).where(or_(UserModel.cpf == login_data.cpf, UserModel.email == login_data.email))
        result = await db_session.execute(query)
        user = result.scalars().first()

        if not user or not verify_password(login_data.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

        return sign_jwt(user_id=user.pk_id)
