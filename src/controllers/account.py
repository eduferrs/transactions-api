from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page

from src.contrib.dependencies import DatabaseDependency
from src.models.user import UserModel
from src.security import get_current_user
from src.services.account import AccountService
from src.views.transaction import StatementOut

router = APIRouter(prefix="/accounts", tags=["Account"])
account_service = AccountService()


@router.get(
    "/statement", response_model=Page[StatementOut], response_model_exclude_none=True, status_code=status.HTTP_200_OK
)
async def get_statement(db_session: DatabaseDependency, current_user: UserModel = Depends(get_current_user)):

    return await account_service.get_statement(current_user.checking_account.pk_id, db_session)
