import pytest
from httpx import AsyncClient
from faker import Faker

pytestmark = pytest.mark.asyncio
fake = Faker()
endpoint = "/api/v1/products/"


def generate_product_data(category_id: str):
    name = fake.unique.word().capitalize() + " Test"
    return {
        "name": name,
        "description": fake.sentence(),
        "price": fake.random_int(10, 500),
        "quantity": fake.random_int(1, 100),
        "category_ids": category_id,
    }


async def test_create_product_success(
    client: AsyncClient, test_category: dict
):
    data = generate_product_data(test_category["id"])
    response = await client.post(endpoint, data=data)
    assert response.status_code == 201
    result = response.json()
    assert result["name"] == data["name"]
    assert result["price"] == data["price"]
    assert "id" in result
    assert "slug" in result


async def test_create_product_duplicate_name(
    client: AsyncClient, test_category: dict
):
    data = generate_product_data(test_category["id"])
    await client.post(endpoint, data=data)
    response = await client.post(endpoint, data=data)
    assert response.status_code == 409
    assert "detail" in response.json()


async def test_create_product_invalid_price(
    client: AsyncClient, test_category: dict
):
    data = generate_product_data(test_category["id"])
    data["price"] = -10
    response = await client.post(endpoint, data=data)
    assert response.status_code == 422
