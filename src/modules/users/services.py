from .schemas import UserUpdate, UserRead, UserCreateInternal, UserCreate, User
from .crud import crud_users
from src.infrastructure.utils import get_password_hash
from .exceptions import UserExistsError, UserNotFoundError, UserCreationError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any


class UserService:
    async def get_users_paginated(self, db: AsyncSession) -> dict[str, Any]:
        data = await crud_users.get_multi(
            db, schema_to_select=UserRead,
        )
        return data

    async def create_user(self, user: UserCreate, db: AsyncSession) -> dict[str, Any]:
        email_exists = await crud_users.exists(db=db, email=user.email)
        if email_exists:
            raise UserExistsError("Email already registered")
        username_exists = await crud_users.exists(db=db, user_name=user.user_name)
        if username_exists:
            raise UserExistsError("Username already taken")
        user_internal_dict = user.model_dump()
        user_internal_dict["hashed_password"] = get_password_hash(
            password=user_internal_dict["password"]
        )
        del user_internal_dict["password"]
        user_internal = UserCreateInternal(**user_internal_dict)
        created_user = await crud_users.create(
            db=db, object=user_internal, schema_to_select=UserRead
        )
        if not created_user:
            raise UserCreationError("Failed to create user")
        return created_user

    async def find_user_by_email(self, email: str, db: AsyncSession) -> UserRead:
        user = await crud_users.get(db=db, email=email, schema_to_select=UserRead)
        if not user:
            raise UserNotFoundError("User not found")
        return user

    async def find_user_by_user_name(
        self, user_name: str, db: AsyncSession
    ) -> UserRead:
        user = await crud_users.get(
            db=db, user_name=user_name, schema_to_select=UserRead
        )
        if not user:
            raise UserNotFoundError("User not found")
        return user

    async def find_user_by_id(self, id: str, db: AsyncSession) -> UserRead:
        user = await crud_users.get(db=db, id=id, schema_to_select=UserRead)
        if not user:
            raise UserNotFoundError("User not found")
        return user

    async def delete_a_user(self, id: str, db: AsyncSession):
        user = await crud_users.get(db=db, id=id, schema_to_select=UserRead)
        if not user:
            raise UserNotFoundError("User not found")
        await crud_users.delete(db=db, id=id)
        return {"message": "User deleted successfully"}

    async def update_user(self, data: UserUpdate, id: str, db: AsyncSession):
        user: UserRead | None = await crud_users.get(
            id=id, db=db, schema_to_select=UserRead
        )
        if not user:
            raise UserNotFoundError("This user doesn't exist")
        update_data = data.model_dump()
        if "email" in update_data and update_data["email"] != user["email"]:
            email_exists = await crud_users.get(email=update_data["email"], db=db)
            if email_exists:
                raise UserExistsError("Email already registered")
        if "user_name" in update_data and update_data["user_name"] != user["user_name"]:
            user_name_exists = await crud_users.get(
                user_name=update_data["user_name"], db=db
            )
            if user_name_exists:
                raise UserExistsError("Username already registered")
        update_user = await crud_users.update(
            db=db,
            object=data,
            id=id,
            return_columns=list(User.model_fields.keys()),
        )
        return update_user
