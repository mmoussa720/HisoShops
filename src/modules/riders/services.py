from .schemas import (
    RiderUpdate,
    RiderRead,
    RiderCreateInternal,
RiderUpdateInternal,
    RiderCreate,
)
from .models import Rider
from .crud import crud_riders
from .exceptions import RiderExistsError, RiderNotFoundError, RiderCreationError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any


class RiderService:
    async def get_riders_paginated(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        data = await crud_riders.get_multi(
            db, schema_to_select=RiderRead, offset=skip, limit=limit
        )
        return data

    async def create_rider(
        self, rider: RiderCreate, db: AsyncSession
    ) -> dict[str, Any]:
        email_exists = await crud_riders.exists(db=db, email=rider.email)
        if email_exists:
            raise RiderExistsError("A rider with this email already exists")
        rider_internal_dict = rider.model_dump()
        rider_internal_dict["status"] = rider.status.value
        rider_internal = RiderCreateInternal(**rider_internal_dict)
        created_rider = await crud_riders.create(
            db=db, object=rider_internal, schema_to_select=RiderRead
        )
        if not created_rider:
            raise RiderCreationError("Failed to create rider")
        return created_rider

    async def find_rider_by_id(
        self, rider_id: str, db: AsyncSession
    ) -> RiderRead:
        rider = await crud_riders.get(
            db=db, id=rider_id, schema_to_select=RiderRead
        )
        if not rider:
            raise RiderNotFoundError("Rider not found")
        return rider

    async def delete_a_rider(self, rider_id: str, db: AsyncSession):
        rider = await crud_riders.get(
            db=db, id=rider_id, schema_to_select=RiderRead
        )
        if not rider:
            raise RiderNotFoundError("Rider not found")
        await crud_riders.delete(db=db, id=rider_id)
        return {"message": "Rider deleted successfully"}

    async def update_rider(
        self, data: RiderUpdate, rider_id: str, db: AsyncSession
    ):
        rider = await crud_riders.get(
            id=rider_id, db=db, schema_to_select=RiderRead
        )
        if not rider:
            raise RiderNotFoundError("Rider not found")
        update_data = data.model_dump(exclude_unset=True)
        if "email" in update_data and update_data["email"] != rider["email"]:
            email_exists = await crud_riders.get(email=update_data["email"], db=db)
            if email_exists:
                raise RiderExistsError("A rider with this email already exists")
        if "status" in update_data:
            update_data["status"] = update_data["status"].value
        updated_rider = await crud_riders.update(
            db=db,
            object=RiderUpdateInternal(**update_data),
            id=rider_id,
            return_columns=[c.name for c in Rider.__table__.columns],
        )
        return updated_rider
