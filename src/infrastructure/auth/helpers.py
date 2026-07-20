import os
from http.client import HTTPException
import jwt
from asyncpg.pgproto.pgproto import timedelta
from datetime import datetime, timezone
from dotenv import load_dotenv
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2AuthorizationCodeBearer
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from fastapi import Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from ..utils import verify_password, get_password_hash
from ...modules.users.schemas import UserRead
from ...modules.users.exceptions import UserNotFoundError
from ...modules.users.dependencies import UserServiceDep
from .exceptions import NotAuthorizedError
from ..dependencies import AsyncSessionDep
from ...modules.users.crud import crud_users

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
bearer_scheme = HTTPBearer()


def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    service: UserServiceDep,
    db: AsyncSessionDep,
):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise NotAuthorizedError()
    except InvalidTokenError:
        raise NotAuthorizedError()
    user = await service.find_user_by_user_name(user_name=username, db=db)
    if user is None:
        raise NotAuthorizedError()
    return user


async def authenticate_user(
    db: AsyncSession, username: str, password: str
) -> UserRead | None:
    user = await crud_users.get(db=db, user_name=username)
    if not user:
        raise UserNotFoundError("This user doesn't exist")
    if not await verify_password(password, user["hashed_password"]):
        return None
    return UserRead(**user)
