import pytest
from httpx import AsyncClient

pytestmark=pytest.mark.asyncio

endpoint="/api/v1/users/"

async def test_get_user_by_user_name_success(client:AsyncClient,test_user:dict):
    user_name=test_user["user_name"]
    response=await client.get(endpoint+user_name)
    assert response.status_code==200
    data = response.json()
    assert "id" in data
    assert data["user_name"]==user_name
    assert "password" not in data
    assert "hashed_password" not in data
