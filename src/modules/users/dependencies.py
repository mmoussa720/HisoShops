from .services import UserService
from fastapi import Depends
from typing import Annotated


def get_user_service() -> UserService:
    return UserService()


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
