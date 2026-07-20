from fastapi import Depends
from typing import Annotated
from .helpers import get_current_user
from .services import AuthService
from ...modules.users.schemas import UserRead


def get_auth_service() -> AuthService:
    return AuthService()


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
getCurrentUserDep = Annotated[UserRead, Depends(get_current_user)]
