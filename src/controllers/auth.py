from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.contrib.dependencies import DatabaseDependency
from src.security import sign_jwt, verify_password
from src.services.user import UserService

router = APIRouter(tags=["auth"])
user_service = UserService()


@router.post("/login", include_in_schema=False)
async def login(db: DatabaseDependency, form_data: OAuth2PasswordRequestForm = Depends()):

    # form_data.username → email ou cpf
    user = await user_service.get_user_by_email_or_cpf(db, form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos",
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos",
        )

    return sign_jwt(user.id)
