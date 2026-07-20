import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio
endpoint = "/api/v1/products/"


async def test_get_product_by_slug_success(
    client: AsyncClient, test_product: dict
):
    response = await client.get(f"{endpoint}{test_product['slug']}")
    assert response.status_code == 200
    data = response.json()
    assert data["slug"] == test_product["slug"]
    assert data["name"] == test_product["name"]
    assert "id" in data


async def test_get_product_by_slug_not_found(client: AsyncClient):
    response = await client.get(f"{endpoint}non-existent-product")
    assert response.status_code == 404


async def test_get_products_paginated(client: AsyncClient, test_product: dict):
    response = await client.get(endpoint)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data


async def test_get_products_by_category(
    client: AsyncClient, test_product: dict, test_category: dict
):
    response = await client.get(f"{endpoint}?category_slug={test_category['slug']}")
    assert response.status_code == 200
