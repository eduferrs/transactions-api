import pytest
import pytest_asyncio
from httpx import AsyncClient


@pytest_asyncio.fixture()
async def user_2(user_factory):
    return await user_factory(
        full_name="User2", cpf="12345678999", email="user2@yahoo.com", account_number_mock="10001-1"
    )


@pytest.mark.parametrize(
    "data",
    [
        {"full_name": "new name", "email": "new_email@gmail.com"},
        {"full_name": "new name"},
        {"email": "new_email@gmail.com"},
        {},
    ],
)
async def test_update_user_success(client: AsyncClient, created_user, access_token, data):
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}

    # When
    response = await client.patch("/users/me", json=data, headers=headers)

    # Then
    assert response.status_code == 200

    if len(data) == 0:
        assert created_user.full_name == "User1"
        assert created_user.email == "user@yahoo.com"
    elif len(data) == 2:
        assert created_user.full_name == "new name"
        assert created_user.email == "new_email@gmail.com"
    elif "full_name" in data:
        assert created_user.full_name == "new name"
        assert created_user.email == "user@yahoo.com"
    else:
        assert created_user.full_name == "User1"
        assert created_user.email == "new_email@gmail.com"


async def test_user_update_fail(client: AsyncClient, created_user, access_token, user_2):
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"full_name": "new name", "email": "user2@yahoo.com"}

    # When
    response = await client.patch("/users/me", json=data, headers=headers)

    # Then
    assert response.status_code == 400
    assert response.json()["detail"] == "E-mail already used"
    assert created_user.full_name == "User1"
    assert created_user.email == "user@yahoo.com"


async def test_not_authorized_fail(client: AsyncClient, created_user):
    # Given
    data = {"full_name": "new name", "email": "new_email@gmail.com"}

    # When
    response = await client.patch("/users/me", json=data)

    # Then
    assert response.status_code == 401


async def test_invalid_token_fail(client: AsyncClient, access_token):
    # Given
    data = {"full_name": "new name", "email": "new_email@gmail.com"}
    headers = {"Authorization": "Bearer invalid_token"}

    # When
    response = await client.patch("/users/me", json=data, headers=headers)

    # Then
    assert response.status_code == 401
