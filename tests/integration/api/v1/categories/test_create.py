import pytest
from httpx import AsyncClient
from faker import Faker

pytestmark = pytest.mark.asyncio
fake = Faker()
endpoint = "/api/v1/categories/"


def generate_category_data():
    name = fake.unique.word().capitalize()
    return {
        "name": name,
        "description": fake.sentence(),
    }


async def test_create_category_success(client: AsyncClient):
    data = generate_category_data()
    response = await client.post(endpoint, json=data)
    assert response.status_code == 201
    result = response.json()
    assert result["name"] == data["name"]
    assert result["description"] == data["description"]
    assert "id" in result
    assert "slug" in result
    assert result["slug"] == data["name"].lower()


async def test_create_category_duplicate_name(client: AsyncClient):
    data = generate_category_data()
    await client.post(endpoint, json=data)
    response = await client.post(endpoint, json=data)
    assert response.status_code == 409
    assert "detail" in response.json()


async def test_create_category_empty_name(client: AsyncClient):
    response = await client.post(endpoint, json={"name": "", "description": ""})
    assert response.status_code == 422
