import pytest
from httpx import AsyncClient
from faker import Faker

pytestmark = pytest.mark.asyncio
fake = Faker()
endpoint = "/api/v1/reviews/"


async def test_update_review_success(
    auth_client: AsyncClient, test_review: dict, test_user: dict
):
    new_rating = 5
    response = await auth_client.put(
        f"{endpoint}{test_review['id']}",
        json={"rating": new_rating},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["rating"] == new_rating


async def test_update_review_not_found(
    auth_client: AsyncClient,
):
    response = await auth_client.put(
        f"{endpoint}non-existent-id",
        json={"rating": 3},
    )
    assert response.status_code == 404


async def test_update_review_unauthenticated(
    client: AsyncClient, test_review: dict
):
    response = await client.put(
        f"{endpoint}{test_review['id']}",
        json={"rating": 2},
    )
    assert response.status_code == 403
