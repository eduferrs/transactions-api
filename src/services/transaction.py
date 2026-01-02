class TransactionService:
    ...
    async def create_transaction(self, data: TransactionIn, db: AsyncSession) -> TransactionModel:
    # Lógica de negócio (verificar saldo, etc) aqui
    new_transaction = TransactionModel(**data.model_dump())
    
    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction) # Pega o ID e o created_at do banco
    
    return new_transaction # Retorna o objeto completo