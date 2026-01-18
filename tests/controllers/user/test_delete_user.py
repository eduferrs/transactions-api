from httpx import AsyncClient


async def test_delete_user_success(client: AsyncClient, created_user, access_token):
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}

    # When
    response = await client.delete("/users/me", headers=headers)

    # Then
    assert response.status_code == 204
    assert created_user.is_active == False
    assert created_user.checking_account.is_active == False


async def test_delete_user_with_balance_fail(client: AsyncClient, created_user, access_token, db_session):
    # Given
    created_user.checking_account.balance = 0.01
    db_session.add(created_user.checking_account)
    await db_session.commit()

    headers = {"Authorization": f"Bearer {access_token}"}

    # When
    response = await client.delete("/users/me", headers=headers)

    # Then
    assert response.status_code == 400
    assert response.json()["detail"] == "Your balance must be 0 before closing the account"
    assert created_user.is_active == True
    assert created_user.checking_account.is_active == True


async def test_not_authorized_fail(client: AsyncClient, created_user):
    # Given

    # When
    response = await client.delete("/users/me")

    # Then
    assert response.status_code == 401


async def test_invalid_token_fail(client: AsyncClient, access_token):
    # Given
    headers = {"Authorization": "Bearer invalid_token"}

    # When
    response = await client.delete("/users/me", headers=headers)

    # Then
    assert response.status_code == 401
