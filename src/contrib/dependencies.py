from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.services.account import AccountService

DatabaseDependency = Annotated[AsyncSession, Depends(get_session)]


async def get_account_service(session: AsyncSession = Depends(get_session)):
    return AccountService(session)
