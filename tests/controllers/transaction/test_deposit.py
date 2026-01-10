import pytest
from httpx import AsyncClient


async def test_deposit_success(client: AsyncClient, created_user, access_token):
    # Given
    data = {"amount": 999.99}
    headers = {"Authorization": f"Bearer {access_token}"}

    # When
    await client.post("/transactions/deposit", json=data, headers=headers)
    response = await client.post("/transactions/deposit", json={"amount": 0.01}, headers=headers)

    # Then
    assert response.status_code == 201
    assert created_user.checking_account.balance == 1000.00


@pytest.mark.parametrize(
    "invalid_amount",
    [
        0.001,
        1234567890123.99,
        -1,
        "a",
    ],
)
async def test_deposit_invalid_amount_fail(client: AsyncClient, created_user, access_token, invalid_amount):
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"amount": invalid_amount}

    # When
    response = await client.post("/transactions/deposit", json=data, headers=headers)

    # Then
    assert response.status_code == 422


async def test_deposit_not_authenticated_fail(client: AsyncClient, created_user):
    # Given
    data = {"amount": 1}
    # headers = {"Authorization": f"Bearer {access_token}"}

    # When
    response = await client.post("/transactions/deposit", json=data)

    # Then
    assert response.status_code == 401


async def test_deposit_invalid_token_fail(client: AsyncClient, created_user):
    # Given
    data = {"amount": 1}
    headers = {"Authorization": "Bearer fake-token"}

    # When
    response = await client.post("/transactions/deposit", json=data, headers=headers)

    # Then
    assert response.status_code == 401
