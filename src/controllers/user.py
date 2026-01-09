from fastapi import APIRouter, Depends, status

from src.contrib.dependencies import DatabaseDependency
from src.schemas.user import UserIn
from src.services.user import UserService
from src.views.user import UserOut

router = APIRouter(prefix="/users", tags=["User"])
user_service = UserService()


@router.post("/new_user", summary="Create new account", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(
    user: UserIn,
    db: DatabaseDependency,
):
    return await user_service.register_user(user, db)
