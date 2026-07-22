from .schemas import (
    OrderUpdate,
    OrderUpdateInternal,
    OrderRead,
    OrderCreateInternal,
    OrderCreate,
    OrderItemRead,
    OrderAssignRider,
)
from .models import Order, OrderItem, generate_order_id
from .crud import crud_orders
from .exceptions import OrderNotFoundError, OrderCreationError
from ...modules.products.crud import crud_products
from ...modules.riders.crud import crud_riders
from ...modules.riders.exceptions import RiderNotFoundError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any


class OrderService:
    async def get_orders_paginated(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        data = await crud_orders.get_multi(
            db, schema_to_select=OrderRead, offset=skip, limit=limit
        )
        return data

    async def create_order(
        self, order: OrderCreate, customer_id: str, db: AsyncSession
    ) -> dict[str, Any]:
        if order.rider_id:
            rider = await crud_riders.get(db=db, id=order.rider_id)
            if not rider:
                raise RiderNotFoundError("Rider not found")
        order_id = await generate_order_id(db)
        total = sum(item.price * item.quantity for item in order.items)
        order_internal = OrderCreateInternal(
            id=order_id,
            customer_id=customer_id,
            rider_id=order.rider_id,
            total=total,
            status="pending",
        )
        created_order = await crud_orders.create(
            db=db, object=order_internal, schema_to_select=OrderRead
        )
        if not created_order:
            raise OrderCreationError("Failed to create order")
        for item in order.items:
            product = await crud_products.get(db=db, id=item.product_id)
            if not product:
                raise OrderCreationError(f"Product {item.product_id} not found")
            await db.execute(
                OrderItem.__table__.insert().values(
                    order_id=order_id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.price,
                )
            )
        await db.commit()
        return created_order

    async def find_order_by_id(
        self, order_id: str, db: AsyncSession
    ) -> OrderRead:
        order = await crud_orders.get(
            db=db, id=order_id, schema_to_select=OrderRead
        )
        if not order:
            raise OrderNotFoundError("Order not found")
        return order

    async def delete_a_order(self, order_id: str, db: AsyncSession):
        order = await crud_orders.get(
            db=db, id=order_id, schema_to_select=OrderRead
        )
        if not order:
            raise OrderNotFoundError("Order not found")
        await db.execute(
            OrderItem.__table__.delete().where(OrderItem.order_id == order_id)
        )
        await crud_orders.delete(db=db, id=order_id)
        return {"message": "Order deleted successfully"}

    async def update_order(
        self, data: OrderUpdate, order_id: str, db: AsyncSession
    ):
        order = await crud_orders.get(
            id=order_id, db=db, schema_to_select=OrderRead
        )
        if not order:
            raise OrderNotFoundError("Order not found")
        update_data = data.model_dump(exclude_unset=True)
        if "status" in update_data:
            update_data["status"] = update_data["status"].value
        updated_order = await crud_orders.update(
            db=db,
            object=OrderUpdateInternal(**update_data),
            id=order_id,
            return_columns=[c.name for c in Order.__table__.columns],
        )
        return updated_order

    async def assign_rider(
        self, data: OrderAssignRider, order_id: str, db: AsyncSession
    ):
        order = await crud_orders.get(
            id=order_id, db=db, schema_to_select=OrderRead
        )
        if not order:
            raise OrderNotFoundError("Order not found")
        rider = await crud_riders.get(db=db, id=data.rider_id)
        if not rider:
            raise RiderNotFoundError("Rider not found")
        updated_order = await crud_orders.update(
            db=db,
            object=OrderUpdateInternal(rider_id=data.rider_id),
            id=order_id,
            return_columns=[c.name for c in Order.__table__.columns],
        )
        return updated_order
