from typing import Annotated

from fastapi import APIRouter, Body, status
from .schemas import Request, Token
from ..dependencies import AsyncSessionDep
from .dependencies import AuthServiceDep
from ...modules.users.dependencies import UserServiceDep

router = APIRouter(tags=["Auth"])


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=Token,
    summary="Authenticates a user",
    description="This endpoint authenticates a user by its username and password",
)
async def login(
    request: Annotated[Request, Body(description="The body of the login method")],
    db: AsyncSessionDep,
    auth_service: AuthServiceDep,
    user_service: UserServiceDep,
):
    return await auth_service.login(request, db, user_service)
