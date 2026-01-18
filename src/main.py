from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination

from src.controllers import account, auth, transaction, user
from src.execptions import *
from src.models.account import AccountModel
from src.models.transaction import TransactionModel
from src.models.user import UserModel

tags_metadata = [
    {
        "name": "Transaction",
        "description": "Handles financial movements",
        "externalDocs": {
            "description": "return to repository",
            "url": "https://github.com/eduferrs/transactions-api",
        },
    },
    {
        "name": "User",
        "description": "Customer profile",
    },
]

app = FastAPI(
    title="Bank API",
    version="1.0.0",
    summary="A asynchronous REST API designed for financial operations and account management.",
    openapi_tags=tags_metadata,
)

app.include_router(auth.router)
app.include_router(transaction.router)
app.include_router(user.router)
app.include_router(account.router)
add_pagination(app)


@app.exception_handler(CreateUserError)
async def create_user_exception_handler(request: Request, exc: CreateUserError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(AccountNotFoundError)
async def account_not_found_exception_handler(request: Request, exc: AccountNotFoundError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(UserUpdateError)
async def user_update_exception_handler(request: Request, exc: UserUpdateError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(BusinessError)
async def business_exception_handler(request: Request, exc: BusinessError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(InternalServerError)
async def internal_server_exception_handler(request: Request, exc: InternalServerError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
