import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio
endpoint = "/api/v1/categories/"


async def test_get_category_by_slug_success(
    client: AsyncClient, test_category: dict
):
    response = await client.get(f"{endpoint}{test_category['slug']}")
    assert response.status_code == 200
    data = response.json()
    assert data["slug"] == test_category["slug"]
    assert data["name"] == test_category["name"]
    assert "id" in data


async def test_get_category_by_slug_not_found(client: AsyncClient):
    response = await client.get(f"{endpoint}non-existent-slug")
    assert response.status_code == 404
    assert "detail" in response.json()


async def test_get_categories_paginated(client: AsyncClient, test_category: dict):
    response = await client.get(endpoint)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
