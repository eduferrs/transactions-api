import pytest_asyncio
from httpx import AsyncClient


async def test_login_success(client: AsyncClient, created_user):
    # Given
    data = {"username": "user@yahoo.com", "password": "secret123"}

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    # When
    response = await client.post("/login", data=data, headers=headers)

    # Then
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


async def test_login_invalid_credentials(client: AsyncClient, created_user):
    # Given
    data = {"username": "user@yahoo.com", "password": "wrong-password"}

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    # When
    response = await client.post(
        "/login",
        data=data,
        headers=headers,
    )

    # Then
    assert response.status_code == 401
