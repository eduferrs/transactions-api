from services.transaction import TransactionService


service = TransactionService()

@router.post("/", response_model=TransactionOut)
async def criar(transacao_in: TransactionIn, db: DatabaseDependency):
    # O controller apenas chama o serviço e repassa o objeto completo
    return await service.create_transaction(transacao_in, db)