import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from faker import Faker
from datetime import datetime

pytestmark=pytest.mark.asyncio
fake=Faker()
endpoint="/api/v1/users/"

def generate_unique_user_data():
    return {
        "first_name":fake.first_name(),
        "last_name":fake.last_name(),
        "email":fake.email(),
        "user_name":fake.user_name(),
        "role":'admin',
        "password":"Password@1234"
    }

async def test_update_user_success(client:AsyncClient,db_session:AsyncSession,test_user:dict):
    update_data=generate_unique_user_data()
    response=await client.put(f"{endpoint}{test_user['id']}",json=update_data)
    assert response.status_code==200
    data=response.json()
    assert "password" not in data
