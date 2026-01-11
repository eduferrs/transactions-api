import pytest
from httpx import AsyncClient


async def test_success_withdrawal(client: AsyncClient, created_user, access_token):
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"amount": 25}

    # When
    await client.post("/transactions/deposit", json={"amount": 1000}, headers=headers)
    response = await client.post("/transactions/withdrawal", json=data, headers=headers)

    # Then
    assert response.status_code == 201
    assert created_user.checking_account.balance == 975


async def test_insufficient_balance_fail(client: AsyncClient, created_user, access_token):
    # Give
    data = {"amount": 1}
    headers = {"Authorization": f"Bearer {access_token}"}

    # When
    response = await client.post("/transactions/withdrawal", json=data, headers=headers)

    # Then
    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough balance for this transaction."


async def test_over_withdrawal_limit_fail(client: AsyncClient, created_user, access_token):
    # Given
    data = {"amount": 500}
    headers = {"Authorization": f"Bearer {access_token}"}

    # When
    await client.post("/transactions/deposit", json={"amount": 2000}, headers=headers)
    await client.post("/transactions/withdrawal", json=data, headers=headers)
    await client.post("/transactions/withdrawal", json={"amount": 250}, headers=headers)
    response = await client.post("/transactions/withdrawal", json=data, headers=headers)

    # Then
    assert response.status_code == 400
    assert response.json()["detail"] == (
        f"This transaction exceeds your daily withdrawal limit ($1000)."
        f"Today you've already withdrawn $750.00."
        f"Your remaining limit for today is $250.00."
    )


@pytest.mark.parametrize(
    "invalid_amount",
    [
        "a",
        0.001,
        -1,
        1234567891234.99,
    ],
)
async def test_withdrawal_invalid_amount_fail(client: AsyncClient, access_token, invalid_amount):
    # Given
    data = {"amount": invalid_amount}
    headers = {"Authorization": f"Bearer {access_token}"}

    # When
    response = await client.post("/transactions/withdrawal", json=data, headers=headers)

    # Then
    assert response.status_code == 422


async def test_withdrawal_not_authenticated_fail(client: AsyncClient, created_user):
    # Given
    data = {"amount": 1}

    # When
    response = await client.post("/transactions/withdrawal", json=data)

    # Then
    assert response.status_code == 401


async def test_withdrawal_invalid_token_fail(client: AsyncClient, created_user):
    # Given
    data = {"amount": 1}
    headers = {"Authorization": f"Bearer fake_token"}

    # When
    response = await client.post("/transactions/withdrawal", json=data, headers=headers)

    # Then
    assert response.status_code == 401
