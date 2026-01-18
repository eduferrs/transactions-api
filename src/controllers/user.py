from fastapi import APIRouter, Body, Depends, status

from src.contrib.dependencies import DatabaseDependency
from src.models import UserModel
from src.schemas.user import UserIn, UserUpdate
from src.security import get_current_user
from src.services.user import UserService
from src.views.user import UserOut

router = APIRouter(prefix="/users", tags=["User"])
user_service = UserService()


@router.post("/new_user", summary="Create new account", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(
    user: UserIn,
    db_session: DatabaseDependency,
):
    return await user_service.register_user(user, db_session)


@router.patch("/me", status_code=status.HTTP_200_OK, response_model=UserOut)
async def update_user(
    db_session: DatabaseDependency, user_up: UserUpdate, current_user: UserModel = Depends(get_current_user)
):
    return await user_service.update(user_up, current_user, db_session)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db_session: DatabaseDependency, current_user: UserModel = Depends(get_current_user)):
    return await user_service.delete(current_user, db_session)
