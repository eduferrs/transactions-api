import pytest_asyncio
from fastapi import status
from httpx import AsyncClient


async def test_access_protected_endpoint_success(client: AsyncClient, access_token):
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}

    # When
    response = await client.post("/test", headers=headers)

    # Then
    assert response.status_code == 200
    assert response.json() == "test"


async def test_access_protected_endpoint_fail(client: AsyncClient):
    # Given
    # Sem token -> headers={"Authorization": ...

    # When
    response = await client.post("/test", headers={})

    # Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
