import jwt
import pytest
from sqlmodel.ext.asyncio.session import AsyncSession
from httpx import AsyncClient
from faker import Faker
from fastapi import status
from dotenv import load_dotenv
import os


SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")

pytestmark=pytest.mark.asyncio
endpoint="/api/v1/auth/login"
async def test_login_success(client:AsyncClient,test_user:dict):
    response=await client.post(endpoint,json={"user_name":test_user["user_name"],"password":test_user["password"]})
    assert response.status_code==status.HTTP_200_OK
    data=response.json()
    assert "access" in data
    assert "refresh" in data
    token=data["access"]
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == test_user["user_name"]
    assert "exp" in payload


async def test_user_not_found(client:AsyncClient):
    fake=Faker()
    response=await client.post(endpoint,json={"user_name":fake.user_name(),"password":"Password@123"})
    assert response.status_code==status.HTTP_404_NOT_FOUND
    data=response.json()
    assert "detail" in data

async def test_invalid_password(client:AsyncClient,test_user:dict):
    response=await client.post(endpoint,json={"user_name":test_user["user_name"],"password":"WrongPassword"})
    assert response.status_code==401
    data=response.json()
    assert "detail" in data
