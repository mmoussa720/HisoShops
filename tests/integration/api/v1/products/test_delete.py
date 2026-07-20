import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio
endpoint = "/api/v1/products/"


async def test_delete_product_success(
    client: AsyncClient, test_product: dict
):
    response = await client.delete(f"{endpoint}{test_product['slug']}")
    assert response.status_code == 200
    assert "message" in response.json()


async def test_delete_product_not_found(client: AsyncClient):
    response = await client.delete(f"{endpoint}non-existent-product")
    assert response.status_code == 404


async def test_delete_product_then_fetch(
    client: AsyncClient, test_product: dict
):
    await client.delete(f"{endpoint}{test_product['slug']}")
    response = await client.get(f"{endpoint}{test_product['slug']}")
    assert response.status_code == 404
