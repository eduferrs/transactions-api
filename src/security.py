import time
from typing import Annotated
from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.contrib.dependencies import DatabaseDependency
from src.models.user import UserModel

# to get a string like this: "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" (secret)
# run: openssl rand -hex 32
SECRET = "my_secret"
ALGORITHM = "HS256"

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", description="OBS.: username = cpf ou email\n")


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


class AccessToken(BaseModel):
    iss: str
    sub: str
    aud: str
    exp: float
    iat: float
    nbf: float
    jti: str


class JWTToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


def sign_jwt(user_uuid: int) -> JWTToken:
    now = time.time()
    payload = {
        "iss": "rr-bankapi.com.br",
        "sub": str(user_uuid),
        "aud": "rr-bankapi",
        "exp": now + (60 * 30),  # 30 minutos
        "iat": now,
        "nbf": now,
        "jti": uuid4().hex,
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}


async def decode_jwt(token: str) -> dict | None:
    try:
        decoded_token = jwt.decode(
            token, SECRET, audience="rr-bankapi", issuer="rr-bankapi.com.br", algorithms=[ALGORITHM]
        )
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except Exception as e:
        print(f"Erro ao decodificar: {e}")
        return None


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db_session: DatabaseDependency) -> UserModel:
    payload = await decode_jwt(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
        )

    user_uuid = payload.get("sub")

    query = select(UserModel).options(selectinload(UserModel.checking_account)).where(UserModel.id == user_uuid)
    result = await db_session.execute(query)
    current_user = result.scalars().first()

    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não localizado",
        )

    return current_user
