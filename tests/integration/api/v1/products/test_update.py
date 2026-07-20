import pytest
from httpx import AsyncClient
from faker import Faker

pytestmark = pytest.mark.asyncio
fake = Faker()
endpoint = "/api/v1/products/"


async def test_update_product_success(
    client: AsyncClient, test_product: dict
):
    new_name = fake.unique.word().capitalize() + " Updated"
    response = await client.put(
        f"{endpoint}{test_product['slug']}",
        data={"name": new_name, "price": 99.99},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_name


async def test_update_product_not_found(client: AsyncClient):
    response = await client.put(
        f"{endpoint}non-existent-slug",
        data={"name": "NewName", "price": 10},
    )
    assert response.status_code == 404


async def test_update_product_duplicate_name(
    client: AsyncClient, test_product: dict
):
    name = fake.unique.word().capitalize() + " Dup"
    await client.post(
        endpoint,
        data={"name": name, "price": 10, "category_ids": ""},
    )
    response = await client.put(
        f"{endpoint}{test_product['slug']}",
        data={"name": name, "price": 20},
    )
    assert response.status_code == 409
