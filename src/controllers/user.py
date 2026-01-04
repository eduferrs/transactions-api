from fastapi import APIRouter, Depends, status

from src.contrib.dependencies import DatabaseDependency
from src.schemas.user import UserIn
from src.services.user import UserService
from src.views.user import UserOut

router = APIRouter(tags=["User"])
user_service = UserService()


@router.post("/new_user", summary="Criar nova conta", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(
    user: UserIn,
    db: DatabaseDependency,
):
    created_user = await user_service.register_user(user, db)
    return created_user
