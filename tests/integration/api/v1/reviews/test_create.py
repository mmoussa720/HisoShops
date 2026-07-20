import pytest
from httpx import AsyncClient
from faker import Faker

pytestmark = pytest.mark.asyncio
fake = Faker()
endpoint = "/api/v1/reviews/"


async def test_create_review_success(
    auth_client: AsyncClient, test_product: dict
):
    data = {
        "rating": fake.random_int(1, 5),
        "comment": fake.sentence(),
        "product_slug": test_product["slug"],
    }
    response = await auth_client.post(endpoint, json=data)
    assert response.status_code == 201
    result = response.json()
    assert result["rating"] == data["rating"]
    assert result["comment"] == data["comment"]
    assert result["product_id"] == test_product["id"]
    assert "id" in result


async def test_create_review_duplicate(
    auth_client: AsyncClient, test_product: dict
):
    data = {
        "rating": 4,
        "comment": "Nice!",
        "product_slug": test_product["slug"],
    }
    await auth_client.post(endpoint, json=data)
    response = await auth_client.post(endpoint, json=data)
    assert response.status_code == 409
    assert "detail" in response.json()


async def test_create_review_unauthenticated(
    client: AsyncClient, test_product: dict
):
    data = {
        "rating": 3,
        "comment": "Okay",
        "product_slug": test_product["slug"],
    }
    response = await client.post(endpoint, json=data)
    assert response.status_code == 403


async def test_create_review_product_not_found(
    auth_client: AsyncClient,
):
    data = {
        "rating": 3,
        "comment": "Not found",
        "product_slug": "non-existent-product",
    }
    response = await auth_client.post(endpoint, json=data)
    assert response.status_code == 404
