from fastapi import APIRouter, Path, Body, Query
from typing import Any, Annotated
from ...infrastructure.dependencies import AsyncSessionDep
from ...infrastructure.auth.dependencies import getCurrentUserDep
from .schemas import OrderCreate, OrderUpdate, OrderAssignRider
from .dependencies import OrderServiceDep

router = APIRouter(tags=["Orders"])


@router.get("/", status_code=200)
async def get_orders(
    db: AsyncSessionDep,
    service: OrderServiceDep,
    _admin: getCurrentUserDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1)] = 10,
):
    return await service.get_orders_paginated(db, skip, limit)


@router.get("/{order_id}", status_code=200)
async def get_order(
    order_id: Annotated[str, Path()],
    db: AsyncSessionDep,
    service: OrderServiceDep,
):
    return await service.find_order_by_id(order_id, db)


@router.post("/", status_code=201)
async def create_order(
    data: OrderCreate,
    db: AsyncSessionDep,
    service: OrderServiceDep,
    current_user: getCurrentUserDep,
) -> dict[str, Any]:
    return await service.create_order(data, current_user["id"], db)


@router.delete("/{order_id}", status_code=200)
async def delete_order(
    order_id: Annotated[str, Path()],
    db: AsyncSessionDep,
    service: OrderServiceDep,
    _admin: getCurrentUserDep,
):
    return await service.delete_a_order(order_id, db)


@router.put("/{order_id}", status_code=200)
async def update_order(
    data: OrderUpdate,
    order_id: Annotated[str, Path()],
    db: AsyncSessionDep,
    service: OrderServiceDep,
):
    return await service.update_order(data, order_id, db)


@router.put("/{order_id}/assign-rider", status_code=200)
async def assign_rider_to_order(
    data: OrderAssignRider,
    order_id: Annotated[str, Path()],
    db: AsyncSessionDep,
    service: OrderServiceDep,
):
    return await service.assign_rider(data, order_id, db)
