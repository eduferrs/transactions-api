from fastapi import FastAPI

from src.controllers import auth, transaction
from src.models.account import AccountModel
from src.models.transaction import TransactionModel
from src.models.user import UserModel

app = FastAPI()
app.include_router(auth.router)
app.include_router(transaction.router)
