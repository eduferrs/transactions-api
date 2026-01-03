from fastapi import APIRouter

from src.contrib.dependencies import DatabaseDependency
from src.services.transaction import TransactionService

service = TransactionService()
router = APIRouter(tags=["Transactions"])


@router.post("/")
def test():
    return "test"


# @router.post("/", response_model=TransactionOut)
# async def criar(transacao_in: TransactionIn, db: DatabaseDependency):


#    return await service.create_transaction(transacao_in, db)
