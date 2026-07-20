from http.client import responses

import pytest
from faker import Faker
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_session
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import uuid4
from datetime import datetime

pytestmark=pytest.mark.asyncio
fake = Faker()
endpoint="/api/v1/users/"

def generate_unique_user_data():
    return {
        "first_name":fake.first_name(),
        "last_name":fake.last_name(),
        "email":fake.email(),
        "user_name":fake.user_name(),
        "role":'admin',
        "password":"Password@123"
    }

#async def test_create_user_success(client:AsyncClient,db_session:AsyncClient,superuser_auth_client:dict):
#    response=await client.post(endpoint,json=user_data,headers={"Authorization":f"Bearer {auth_data['access']}"})
#    assert response.status_code==201
#    data=response.json()
#    assert data["user_name"]==user_data["user_name"]
#    assert data["email"]==user_data["email"]
#    assert "id" in data
#    assert "password" not in data
#    assert "hashed_password" not in data


async def test_create_user_invalid_email(client:AsyncClient,db_session:AsyncSession):
    user_data=generate_unique_user_data()
    user_data["email"]="invalid_email"
    response=await client.post(endpoint)
    assert response.status_code==422
    data=response.json()
    assert "detail" in data

async def test_create_user_duplicate_user_name(client:AsyncClient,db_session:AsyncSession,test_user:dict):
    user_data=generate_unique_user_data()
    user_data["user_name"]=test_user["user_name"]
    response=await client.post(endpoint,json=user_data)
    assert response.status_code==409
    data=response.json()
    assert "detail" in data

async def test_admin_role_required(client:AsyncClient,db_session:AsyncSession):
    user_data=generate_unique_user_data()
    user_data["role"]="admin"
    response=await client.post(endpoint,json=user_data)
    assert response.status_code==201
    data=response.json()
    assert "detail" in data

async def test_create_user_duplicate_email(client:AsyncClient,db_session:AsyncSession,test_user:dict):
    user_data=generate_unique_user_data()
    user_data["email"]=test_user["email"]
    response=await client.post(endpoint,json=user_data)
    assert response.status_code==409
    data=response.json()
    assert "detail" in data
