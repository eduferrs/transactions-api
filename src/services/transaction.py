from src.models.transaction import TransactionModel


class TransactionService:
    pass
    # async def create_transaction(self, data: TransactionIn, db: AsyncSession) -> TransactionModel:
    # verificar saldo, etc aqui
    # new_transaction = TransactionModel(**data.model_dump())

    # db.add(new_transaction)
    # await db.commit()
    # await db.refresh(new_transaction)

    # return new_transaction     #return new_transaction
