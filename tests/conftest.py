import pytest
import pytest_asyncio
import os
from faker import Faker
from httpx import AsyncClient, ASGITransport
from sqlmodel.ext.asyncio.session import AsyncSession
from testcontainers.core.docker_client import DockerClient
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from testcontainers.postgres import PostgresContainer
from sqlalchemy.orm import sessionmaker
from src.infrastructure.auth.helpers import get_current_user
from src.infrastructure.utils import get_password_hash
from src.infrastructure.common.helpers import generate_slug
from src.interfaces.main import app
from src.infrastructure.database import async_session
from src.infrastructure.database.session import Base
from src.modules.users.models import User
from src.modules.categories.models import Category
from src.modules.products.models import Product, ProductCategory
from src.modules.reviews.models import Review


load_dotenv()


def is_docker_running():
    try:
        DockerClient()
        return True
    except Exception:
        return False


@pytest_asyncio.fixture(scope="function")
async def pg_container():
    if not is_docker_running():
        pytest.skip("Docker is required,but not running")
    with PostgresContainer() as pg:
        yield pg


@pytest_asyncio.fixture(scope="function")
async def test_db_url(pg_container):
    host = pg_container.get_container_host_ip()
    port_to_expose = 5432
    if hasattr(pg_container, "port_to_expose"):
        port_to_expose = pg_container.port_to_expose
    port = pg_container.get_exposed_port(port_to_expose)
    db = "test"
    user = "test"
    password = "test"
    if hasattr(pg_container, "POSTGRES_USER"):
        user = pg_container.POSTGRES_USER
    if hasattr(pg_container, "POSTGRES_PASSWORD"):
        password = pg_container.POSTGRES_PASSWORD
    if hasattr(pg_container, "POSTGRES_DB"):
        db = pg_container.POSTGRES_DB
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"


@pytest_asyncio.fixture(scope="function")
async def test_db_engine(test_db_url):
    engine = create_async_engine(test_db_url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def test_db(test_db_engine):
    test_session = sessionmaker(
        test_db_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with test_session() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def db_session(test_db):
    yield test_db


@pytest_asyncio.fixture(scope="function")
async def client(test_db):
    app.dependency_overrides = {}

    async def override_get_db():
        yield test_db

    app.dependency_overrides[async_session] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides = {}


# --- User Fixtures ---

@pytest_asyncio.fixture
async def test_user(db_session: AsyncSession):
    fake = Faker()
    user: User = User(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        user_name=f"u{fake.random_int(10000, 99999)}",
        hashed_password=get_password_hash("Password@123"),
        is_deleted=False,
        profile_image_url="https://example.com/test.jpg",
    )
    db_session.add(user)
    await db_session.commit()
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "user_name": user.user_name,
        "email": user.email,
        "password": "Password@123",
        "profile_image_url": user.profile_image_url,
        "is_super_user": False,
    }


@pytest_asyncio.fixture
async def auth_client(client: AsyncClient, test_user: dict):
    async def override_get_current_user():
        return test_user

    app.dependency_overrides[get_current_user] = override_get_current_user
    yield client
    app.dependency_overrides.pop(get_current_user, None)


@pytest_asyncio.fixture
async def test_admin(db_session: AsyncSession):
    fake = Faker()
    user = User(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        user_name=f"u{fake.random_int(10000, 99999)}",
        hashed_password=get_password_hash("Password@123"),
    )
    db_session.add(user)
    await db_session.commit()
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "user_name": user.user_name,
        "email": user.email,
        "role": "admin",
        "password": "Password@123",
        "profile_image_url": user.profile_image_url,
        "is_super_user": False,
    }


@pytest_asyncio.fixture
async def test_super_user(db_session: AsyncSession):
    fake = Faker()
    user = User(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        user_name=f"u{fake.random_int(10000, 99999)}",
        hashed_password=get_password_hash("Password@123"),
    )
    db_session.add(user)
    await db_session.commit()
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "user_name": user.user_name,
        "email": user.email,
        "password": "Password@123",
        "role": "admin",
        "profile_image_url": user.profile_image_url,
        "is_super_user": True,
    }


# --- Category Fixtures ---

@pytest_asyncio.fixture
async def test_category(db_session: AsyncSession):
    fake = Faker()
    name = fake.unique.word().capitalize()
    category = Category(
        slug=generate_slug(name),
        name=name,
        description=fake.sentence(),
    )
    db_session.add(category)
    await db_session.commit()
    return {
        "id": category.id,
        "slug": category.slug,
        "name": category.name,
        "description": category.description,
    }


# --- Product Fixtures ---

@pytest_asyncio.fixture
async def test_product(db_session: AsyncSession, test_category: dict):
    fake = Faker()
    name = fake.unique.word().capitalize() + " Product"
    product = Product(
        slug=generate_slug(name),
        name=name,
        price=fake.random_int(10, 500),
        description=fake.sentence(),
        quantity=fake.random_int(1, 100),
    )
    db_session.add(product)
    await db_session.flush()
    pcat = ProductCategory(product_id=product.id, category_id=test_category["id"])
    db_session.add(pcat)
    await db_session.commit()
    return {
        "id": product.id,
        "slug": product.slug,
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "quantity": product.quantity,
        "category_id": test_category["id"],
    }


# --- Review Fixtures ---

@pytest_asyncio.fixture
async def test_review(
    db_session: AsyncSession, test_user: dict, test_product: dict
):
    fake = Faker()
    review = Review(
        rating=fake.random_int(1, 5),
        comment=fake.sentence(),
        user_id=test_user["id"],
        product_id=test_product["id"],
    )
    db_session.add(review)
    await db_session.commit()
    return {
        "id": review.id,
        "rating": review.rating,
        "comment": review.comment,
        "user_id": review.user_id,
        "product_id": review.product_id,
    }
