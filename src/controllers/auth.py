from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel

from src.contrib.dependencies import DatabaseDependency
from src.schemas.auth import LoginIn
from src.schemas.user import UserIn
from src.security import sign_jwt
from src.services.auth import AuthService
from src.views.user import UserOut

# from views.auth import LoginOut

router = APIRouter(tags=["auth"])
auth_service = AuthService()


@router.post("/new_user", summary="Criar nova conta", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(
    user: UserIn,
    db: DatabaseDependency,
):
    created_user = await auth_service.register_user(user, db)
    return created_user


# @router.post("/login", response_model=LoginOut)
# async def login(data: LoginIn):
#    return sign_jwt(user_id=data.user_id)


####################################################################################################################
