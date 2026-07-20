import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio
endpoint = "/api/v1/categories/"


async def test_delete_category_success(
    client: AsyncClient, test_category: dict
):
    response = await client.delete(f"{endpoint}{test_category['slug']}")
    assert response.status_code == 200
    assert "message" in response.json()


async def test_delete_category_not_found(client: AsyncClient):
    response = await client.delete(f"{endpoint}non-existent-slug")
    assert response.status_code == 404


async def test_delete_category_then_fetch(
    client: AsyncClient, test_category: dict
):
    await client.delete(f"{endpoint}{test_category['slug']}")
    response = await client.get(f"{endpoint}{test_category['slug']}")
    assert response.status_code == 404
