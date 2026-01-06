import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings
from src.contrib.models import Base
from src.database import get_session
from src.schemas.user import UserIn
from src.services.user import UserService

TEST_DB_URL = "sqlite+aiosqlite:///./test.db"
settings.DB_URL = TEST_DB_URL

engine_test = create_async_engine(TEST_DB_URL, echo=False)

AsyncSessionTest = sessionmaker(
    engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest_asyncio.fixture
async def client(db_session):
    from src.main import app

    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def db_session():
    import src.models.account
    import src.models.transaction
    import src.models.user

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionTest() as session:
        yield session

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def user_factory(db_session, mocker):
    async def create_user_func(
        full_name="User1",
        birth_date="31/12/2000",
        cpf="12345678900",
        email="user@yahoo.com",
        password="secret123",
        account_number_mock="10000-0",
    ):

        mocker.patch.object(UserService, "_generate_account_number", return_value=account_number_mock)
        user_in = UserIn(full_name=full_name, birth_date=birth_date, cpf=cpf, email=email, password=password)

        service = UserService()
        return await service.register_user(user_in, db_session)

    return create_user_func


@pytest_asyncio.fixture
async def created_user(user_factory):

    return await user_factory()


@pytest_asyncio.fixture
async def access_token(client: AsyncClient, created_user):
    response = await client.post(
        "/login",
        data={"username": "user@yahoo.com", "password": "secret123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return response.json()["access_token"]
