import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio
endpoint = "/api/v1/reviews/"


async def test_delete_review_success(
    auth_client: AsyncClient, test_review: dict
):
    response = await auth_client.delete(f"{endpoint}{test_review['id']}")
    assert response.status_code == 200
    assert "message" in response.json()


async def test_delete_review_not_found(auth_client: AsyncClient):
    response = await auth_client.delete(f"{endpoint}non-existent-id")
    assert response.status_code == 404


async def test_delete_review_unauthenticated(
    client: AsyncClient, test_review: dict
):
    response = await client.delete(f"{endpoint}{test_review['id']}")
    assert response.status_code == 403
