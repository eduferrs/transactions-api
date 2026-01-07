from fastapi import status
from httpx import AsyncClient

from src.services.user import UserService


async def test_create_user_succsess(client: AsyncClient, mocker):

    # Given
    mocker.patch.object(UserService, "_generate_account_number", return_value="10001-1")
    data = {
        "full_name": "nome",
        "birth_date": "31/12/2000",
        "cpf": "11111111100",
        "email": "EMAIL@YAHOO.COM",
        "password": "12345678",
    }

    # When
    response = await client.post("/new_user", json=data)
    user = response.json()

    # Then
    assert response.status_code == status.HTTP_201_CREATED
    assert user["id"] is not None
    assert user["checking_account"]["account_number"] == "10001-1"
    assert user["email"] == "email@yahoo.com"


async def test_create_user_conflict_fail(client: AsyncClient, created_user, mocker):
    # Given
    mocker.patch.object(UserService, "_generate_account_number", return_value="10001-1")
    data = {
        "full_name": "name",
        "birth_date": "31/12/2000",
        "cpf": "12345678900",
        "email": "email@gmail.com",
        "password": "12345678",
    }

    # When
    response = await client.post("/new_user", json=data)

    # Then
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "CPF ou E-mail já cadastrado"


async def test_create_user_invalid_payload_fail(client: AsyncClient, mocker):
    # Given
    mocker.patch.object(UserService, "_generate_account_number", return_value="10001-1")
    data = {
        "full_name": "A",
        "birth_date": "2000-31-12",
        "cpf": "123456789jk",
        "email": "email.yahoo.com",
    }

    # When
    response = await client.post("/new_user", json=data)
    content = response.json()

    errors = {error["loc"][-1]: error["msg"] for error in content["detail"]}
    # print(errors)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert errors["full_name"] == "String should have at least 2 characters"
    assert errors["birth_date"] == "Value error, A data deve estar no formato DD/MM/AAAA ou DD-MM-AAAA"
    assert errors["cpf"] == "Value error, CPF deve conter apenas números"
    assert errors["email"] == "value is not a valid email address: An email address must have an @-sign."
    assert errors["password"] == "Field required"
