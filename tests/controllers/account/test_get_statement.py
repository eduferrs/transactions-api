from httpx import AsyncClient


async def test_get_statement_success(client: AsyncClient, created_user, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}

    for i in range(90):
        await client.post("/transactions/deposit", json={"amount": 1.99}, headers=headers)

    # When
    response = await client.get("/accounts/statement?page=5&size=10", headers=headers)

    # Then
    assert response.status_code == 200
    assert len(response.json()["items"]) == 10
    assert response.json()["total"] == 90
    assert response.json()["pages"] == 9
    assert response.json()["page"] == 5


async def test_get_statement_empty_success(client: AsyncClient, access_token):
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}

    # When
    response = await client.get("/accounts/statement", headers=headers)

    # Then
    assert response.status_code == 200
    assert response.json()["items"] == []
    assert response.json()["total"] == 0
    assert response.json()["page"] == 1


async def test_not_authenticated_fail(client: AsyncClient):
    # Given
    # headers = {"Authorization": f"Bearer {access_token}"}

    # When
    response = await client.get("/accounts/statement")

    # Then
    assert response.status_code == 401


async def test_invalid_token_fail(client: AsyncClient, access_token):
    # Given
    headers = {"Authorization": "Bearer invalid_token"}

    # When
    response = await client.get("/accounts/statement")

    # Then
    assert response.status_code == 401
