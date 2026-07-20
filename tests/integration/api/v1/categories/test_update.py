import pytest
from httpx import AsyncClient
from faker import Faker

pytestmark = pytest.mark.asyncio
fake = Faker()
endpoint = "/api/v1/categories/"


async def test_update_category_success(
    client: AsyncClient, db_session, test_category: dict
):
    new_name = fake.unique.word().capitalize()
    response = await client.put(
        f"{endpoint}{test_category['slug']}",
        json={"name": new_name},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_name


async def test_update_category_not_found(client: AsyncClient):
    response = await client.put(
        f"{endpoint}non-existent-slug",
        json={"name": "NewName"},
    )
    assert response.status_code == 404


async def test_update_category_duplicate_name(
    client: AsyncClient, test_category: dict
):
    name = fake.unique.word().capitalize()
    await client.post(endpoint, json={"name": name})
    response = await client.put(
        f"{endpoint}{test_category['slug']}",
        json={"name": name},
    )
    assert response.status_code == 409
