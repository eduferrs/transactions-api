from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import apaginate

from src.contrib.dependencies import get_account_service
from src.models.user import UserModel
from src.security import get_current_user
from src.services.account import AccountService
from src.views.transaction import StatementOut

router = APIRouter(prefix="/accounts", tags=["Account"])


@router.get(
    "/statement", response_model=Page[StatementOut], response_model_exclude_none=True, status_code=status.HTTP_200_OK
)
async def get_statement(
    current_user: UserModel = Depends(get_current_user),
    account_service: AccountService = Depends(get_account_service),
):
    query = account_service.get_statement(current_user.checking_account.pk_id)
    return await apaginate(account_service.session, query)
