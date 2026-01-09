from fastapi import APIRouter, Depends, status

from src.contrib.dependencies import DatabaseDependency
from src.models.user import UserModel
from src.schemas.transaction import TransactionIn
from src.security import get_current_user
from src.services.transaction import TransactionService
from src.views.transaction import TransactionOut

service = TransactionService()
router = APIRouter(tags=["Transactions"])


@router.post(
    "/deposit",
    summary="Depositar na própria conta",
    status_code=status.HTTP_201_CREATED,
    response_model=TransactionOut,
)
async def make_deposit(
    transaction_in: TransactionIn, db_session: DatabaseDependency, current_user: UserModel = Depends(get_current_user)
):

    return await service.create_deposit(transaction_in, current_user.checking_account.pk_id, db_session)
