from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.controllers import auth, transaction, user
from src.execptions import CreateUserError, InternalServerError
from src.models.account import AccountModel
from src.models.transaction import TransactionModel
from src.models.user import UserModel

app = FastAPI()
app.include_router(auth.router)
app.include_router(transaction.router)
app.include_router(user.router)


@app.exception_handler(CreateUserError)
async def create_user_exception_handler(request: Request, exc: CreateUserError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(InternalServerError)
async def internal_server_exception_handler(request: Request, exc: InternalServerError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
