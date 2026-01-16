import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import select

from src.models.transaction import TransactionModel, TransactionType


@pytest_asyncio.fixture()
async def user_2(user_factory):
    return await user_factory(
        full_name="User2", cpf="12345678999", email="user2@yahoo.com", account_number_mock="10001-1"
    )


async def test_transfer_success(client: AsyncClient, created_user, access_token, user_2, db_session):
    # Given
    data = {
        "amount": 2500,
        "counterparty_branch": "0001",
        "counterparty_account_number": "10001-1",
    }
    headers = {"Authorization": f"Bearer {access_token}"}

    # When
    await client.post("/transactions/deposit", json={"amount": 2500}, headers=headers)
    response = await client.post("/transactions/transfer", json=data, headers=headers)

    query = select(TransactionModel).where(TransactionModel.account_id == user_2.checking_account.pk_id)
    result = await db_session.execute(query)
    receiver_register = result.scalars().first()

    query = select(TransactionModel).where(
        TransactionModel.account_id == created_user.checking_account.pk_id,
        TransactionModel.type == TransactionType.TRANSFER_OUT,
    )
    result = await db_session.execute(query)
    sender_register = result.scalars().first()

    # Then
    assert response.status_code == 201
    assert sender_register.operation_id == receiver_register.operation_id
    assert sender_register.counterparty_name == user_2.full_name
    assert sender_register.counterparty_branch == user_2.checking_account.branch
    assert sender_register.counterparty_account_number == user_2.checking_account.account_number
    assert receiver_register.counterparty_account_number == created_user.checking_account.account_number
    assert receiver_register.counterparty_branch == created_user.checking_account.branch
    assert receiver_register.counterparty_name == created_user.full_name
    assert created_user.checking_account.balance == 0
    assert user_2.checking_account.balance == 2500


async def test_transfer_not_enough_balance_fail(client: AsyncClient, created_user, access_token, user_2):
    # Given
    data = {
        "amount": 1,
        "counterparty_branch": "0001",
        "counterparty_account_number": "10001-1",
    }
    headers = {"Authorization": f"Bearer {access_token}"}

    # When
    response = await client.post("/transactions/transfer", json=data, headers=headers)

    # Then
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient balance for this transaction."


async def test_transfer_over_limit_fail(client: AsyncClient, created_user, access_token, user_2):
    # Given
    data = {
        "amount": 2500.01,
        "counterparty_branch": "0001",
        "counterparty_account_number": "10001-1",
    }
    headers = {"Authorization": f"Bearer {access_token}"}

    # When
    await client.post("/transactions/deposit", json={"amount": 100000}, headers=headers)
    response = await client.post("/transactions/transfer", json=data, headers=headers)

    # Then
    assert response.status_code == 400
    assert response.json()["detail"] == "Amount exceeds transfer limit."


async def test_transfer_invalid_account_fail(client: AsyncClient, created_user, access_token, user_2):
    # Given
    data = {
        "amount": 1,
        "counterparty_branch": "0001",
        "counterparty_account_number": "10001-0",
    }
    headers = {"Authorization": f"Bearer {access_token}"}

    # When
    await client.post("/transactions/deposit", json={"amount": 1}, headers=headers)
    response = await client.post("/transactions/transfer", json=data, headers=headers)

    # Then
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid branch or account number."


async def test_transfer_invalid_branch_fail(client: AsyncClient, created_user, access_token, user_2):
    # Given
    data = {
        "amount": 1,
        "counterparty_branch": "0002",
        "counterparty_account_number": "10001-1",
    }
    headers = {"Authorization": f"Bearer {access_token}"}

    # When
    await client.post("/transactions/deposit", json={"amount": 1}, headers=headers)
    response = await client.post("/transactions/transfer", json=data, headers=headers)

    # Then
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid branch or account number."


async def test_transfer_to_self_fail(client: AsyncClient, created_user, access_token):
    # Given
    data = {
        "amount": 1,
        "counterparty_branch": created_user.checking_account.branch,
        "counterparty_account_number": created_user.checking_account.account_number,
    }
    headers = {"Authorization": f"Bearer {access_token}"}

    # When
    await client.post("/transactions/deposit", json={"amount": 1}, headers=headers)
    response = await client.post("/transactions/transfer", json=data, headers=headers)

    # Then
    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot transfer to own account"


@pytest.mark.parametrize(
    "invalid_amount",
    [
        0.001,
        1234567890123.99,
        -1,
        "a",
    ],
)
async def test_transfer_invalid_amount_fail(client: AsyncClient, created_user, access_token, invalid_amount, user_2):
    # Given
    data = {
        "amount": invalid_amount,
        "counterparty_branch": "0001",
        "counterparty_account_number": "10001-1",
    }
    headers = {"Authorization": f"Bearer {access_token}"}

    # When
    await client.post("/transactions/deposit", json={"amount": 100000}, headers=headers)
    response = await client.post("/transactions/transfer", json=data, headers=headers)

    # Then
    assert response.status_code == 422


async def test_transfer_invalid_payload_fail(client: AsyncClient, created_user, access_token, user_2):
    # Given
    data = {
        "amount": 1,
        "counterparty_branch": "0001",
    }
    headers = {"Authorization": f"Bearer {access_token}"}

    # When
    await client.post("/transactions/deposit", json={"amount": 100000}, headers=headers)
    response = await client.post("/transactions/transfer", json=data, headers=headers)

    # Then
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "counterparty_account_number"]


async def test_transfer_not_authenticated_fail(client: AsyncClient, created_user):
    # Given
    data = {
        "amount": 1,
        "counterparty_branch": "0001",
        "counterparty_account_number": "10001-1",
    }

    # When
    response = await client.post("/transactions/transfer", json=data)

    # Then
    assert response.status_code == 401


async def test_transfer_invalid_token_fail(client: AsyncClient, created_user):
    # Given
    data = {
        "amount": 1,
        "counterparty_branch": "0001",
        "counterparty_account_number": "10001-1",
    }
    headers = {"Authorization": "Bearer fake_token"}

    # When
    response = await client.post("/transactions/transfer", json=data, headers=headers)

    # Then
    assert response.status_code == 401
