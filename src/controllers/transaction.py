from fastapi import APIRouter, Depends, status

from src.contrib.dependencies import DatabaseDependency
from src.security import get_current_user
from src.services.transaction import TransactionService

service = TransactionService()
router = APIRouter(tags=["Transactions"])


@router.post("/", dependencies=[Depends(get_current_user)])
def test():
    return "test"


# @router.post("/", response_model=TransactionOut)
# async def criar(transacao_in: TransactionIn, db: DatabaseDependency):


#    return await service.create_transaction(transacao_in, db)
