from fastapi import APIRouter, Path, Body, Depends, Query
from .schemas import RiderRead, RiderCreate, RiderUpdate
from typing import Any, Annotated
from .dependencies import RiderServiceDep
from ...infrastructure.dependencies import AsyncSessionDep
from ...infrastructure.common.utils.role_checker import RoleChecker

router = APIRouter(tags=["Riders"])
admin_only = RoleChecker(["admin"])


@router.get(
    "/",
    summary="List all riders",
    description="Retrieves a paginated list of all riders (admin only)",
    response_description="A paginated list of riders",
    responses={401: {"description": "Not authenticated"}, 403: {"description": "Not authorized"}},
    dependencies=[Depends(admin_only)],
)
async def get_riders(
    service: RiderServiceDep,
    db: AsyncSessionDep,
    skip: Annotated[int, Query(description="Number of records to skip", ge=0)] = 0,
    limit: Annotated[int, Query(description="Maximum number of records", ge=1)] = 100,
):
    return await service.get_riders_paginated(db, skip=skip, limit=limit)


@router.get(
    "/{rider_id}",
    status_code=200,
    response_model=RiderRead | None,
    summary="Return a rider by id",
    description="Returns all the necessary rider data by its id (admin only)",
    response_description="A json item of the desired rider",
    responses={200: {"description": "Rider data retrieved"}, 404: {"description": "Rider not found"}},
    dependencies=[Depends(admin_only)],
)
async def get_rider_by_id(
    rider_id: Annotated[str, Path(description="The id of the rider")],
    service: RiderServiceDep,
    db: AsyncSessionDep,
):
    return await service.find_rider_by_id(rider_id, db)


@router.post(
    "/",
    status_code=201,
    response_model=RiderRead,
    summary="Create a new rider",
    description="Creates a new delivery rider (admin only)",
    response_description="The created rider",
    responses={201: {"description": "Rider created"}, 400: {"description": "Invalid data"}, 409: {"description": "Rider with this email already exists"}},
    dependencies=[Depends(admin_only)],
)
async def create_rider(
    rider: RiderCreate,
    db: AsyncSessionDep,
    service: RiderServiceDep,
) -> dict[str, Any]:
    return await service.create_rider(rider, db)


@router.put(
    "/{rider_id}",
    status_code=200,
    summary="Update a rider",
    description="Updates a rider's data (admin only)",
    response_description="The updated rider",
    responses={200: {"description": "Rider updated"}, 404: {"description": "Rider not found"}, 409: {"description": "Rider with this email already exists"}},
    dependencies=[Depends(admin_only)],
)
async def update_rider(
    rider_id: Annotated[str, Path(description="The id of the rider")],
    data: RiderUpdate,
    db: AsyncSessionDep,
    service: RiderServiceDep,
):
    return await service.update_rider(data, rider_id, db)


@router.delete(
    "/{rider_id}",
    status_code=200,
    summary="Delete a rider",
    description="Deletes a rider from the system (admin only)",
    response_description="A message confirming the deletion",
    responses={200: {"description": "Rider deleted"}, 404: {"description": "Rider not found"}},
    dependencies=[Depends(admin_only)],
)
async def delete_rider(
    rider_id: Annotated[str, Path(description="The id of the rider")],
    db: AsyncSessionDep,
    service: RiderServiceDep,
):
    return await service.delete_a_rider(rider_id, db)
