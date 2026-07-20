from fastapi import APIRouter, Path, Body
from fastapi.params import Depends

from .schemas import UserRead, UserCreate, UserUpdate
from typing import Any, Annotated
from .dependencies import UserServiceDep
from ...infrastructure.common.utils.role_checker import RoleChecker
from ...infrastructure.dependencies import AsyncSessionDep

router = APIRouter(tags=["Users"])


@router.get(
    "/",
    summary="List all users",
    description="Retrieves a paginated list of all users in the system",
    response_description="A paginated list of users with total count and pagination metadata",
    responses={
        401: {"description": "Not authenticated"},
        403: {"description": "Not authorized"},
    },
)
async def get_users(service: UserServiceDep, db: AsyncSessionDep):
    return await service.get_users_paginated(db)


@router.get(
    "/{user_name}",
    status_code=200,
    response_model=UserRead | None,
    summary="Return a user data by its user name",
    description="Returns all the necessary user's data by his username",
    response_description="A json item of the desired user with all the necessary information (first_name, last_name, email, user_name...)",
    responses={
        200: {"description": "User's data retrieved"},
        404: {"description": "User not found"},
    },
)
async def get_user_by_user_name(
    user_name: Annotated[str, Path(description="The username of the user")],
    service: UserServiceDep,
    db: AsyncSessionDep,
):
    return await service.find_user_by_user_name(user_name, db)


@router.get(
    "/email/{email}",
    status_code=200,
    response_model=UserRead | None,
    summary="Return a user data by its email",
    description="Returns all the necessary user's data by his email address",
    response_description="A json item of the desired user with all the necessary information (first_name, last_name, email, user_name...)",
    responses={
        200: {"description": "User's data retrieved"},
        404: {"description": "User not found"},
    },
)
async def get_user_by_email(
    email: Annotated[str, Path(description="The email of the user")],
    service: UserServiceDep,
    db: AsyncSessionDep,
):
    return await service.find_user_by_email(email, db)


@router.get(
    "/id/{id}",
    status_code=200,
    response_model=UserRead | None,
    summary="Return a user data by its id",
    description="Returns all the necessary user's data by his unique id",
    response_description="A json item of the desired user with all the necessary information (first_name, last_name, email, user_name...)",
    responses={
        200: {"description": "User's data retrieved"},
        404: {"description": "User not found"},
    },
)
async def get_user_by_id(
    id: Annotated[str, Path(description="The unique id of the user")],
    service: UserServiceDep,
    db: AsyncSessionDep,
):
    return await service.find_user_by_id(id, db)


@router.post(
    "/",
    status_code=201,
    response_model=UserRead,
    summary="Create new user account",
    description="""Creates a new user account in the system.
                This endpoint allows registration of new users with their basic information:
                - First name
                - Last name
                - Email address
                - Password (with security requirements)
    """,
    response_description="The created user profile with assigned ID",
    responses={
        201: {"description": "User account created"},
        400: {"description": "Invalid user data"},
        409: {"description": "Username or email already exists"},
    },
    dependencies=[Depends(RoleChecker(allowed_roles=["admin"]))]
)
async def create_user(
    user: UserCreate,
    db: AsyncSessionDep,
    service: UserServiceDep,
) -> dict[str, Any]:
    return await service.create_user(user, db)


@router.put(
    "/{id}",
    status_code=200,
    summary="Update a user's data",
    description="This endpoint updates parts or all the possible user's data",
    response_description="The updated user data",
    responses={
        200: {"description": "User has been updated successfully"},
        404: {"description": "User not found"},
        409: {"description": "Username or email already exists"},
    },
)
async def update_user(
    id: Annotated[str, Path(description="The id of the user")],
    data: Annotated[UserUpdate, Body(description="The new data")],
    db: AsyncSessionDep,
    service: UserServiceDep,
):
    return await service.update_user(data, id, db=db)


@router.delete(
    "/{id}",
    status_code=200,
    summary="Delete a user",
    description="This endpoint soft deletes a user from the system",
    response_description="A message confirming the user deletion",
    responses={
        200: {"description": "User has been deleted successfully"},
        404: {"description": "User not found"},
    },
)
async def delete_user(
    id: Annotated[str, Path(description="The id of the user")],
    db: AsyncSessionDep,
    service: UserServiceDep,
):
    return await service.delete_a_user(id, db)
