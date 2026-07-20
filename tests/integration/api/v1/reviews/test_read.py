import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio
endpoint = "/api/v1/reviews/"


async def test_get_reviews_by_product_success(
    client: AsyncClient, test_review: dict, test_product: dict
):
    response = await client.get(
        f"{endpoint}product/{test_product['slug']}"
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data


async def test_get_reviews_by_product_not_found(client: AsyncClient):
    response = await client.get(f"{endpoint}product/non-existent")
    assert response.status_code == 404


async def test_get_average_rating(
    client: AsyncClient, test_review: dict, test_product: dict
):
    response = await client.get(
        f"{endpoint}product/{test_product['slug']}/average-rating"
    )
    assert response.status_code == 200
    rating = response.json()
    assert isinstance(rating, float) or isinstance(rating, int)
