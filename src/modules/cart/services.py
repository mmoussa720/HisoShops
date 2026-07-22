from .schemas import CartUpdate, CartRead, CartCreate, CartCreateInternal
from .models import Cart
from .crud import crud_cart
from .exceptions import CartItemExistsError, CartItemNotFoundError, CartItemCreationError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from ..products import ProductNotFoundError
from ..products.crud import crud_products


class CartService:
    async def get_cart_by_user(
        self, user_id: str, db: AsyncSession
    ) -> dict[str, Any]:
        data = await crud_cart.get_multi(
            db, schema_to_select=CartRead, user_id=user_id
        )
        return data

    async def add_to_cart(
        self, item: CartCreate, user_id: str, db: AsyncSession
    ) -> dict[str, Any]:
        existing = await crud_cart.exists(
            db=db, user_id=user_id, product_id=item.product_id, size=item.size
        )
        if existing:
            raise CartItemExistsError("This product is already in your cart")
        product_existing = await crud_products.exists(db=db, id=item.product_id)
        if not product_existing:
            raise ProductNotFoundError("This product doesn't exist")
        item_dict = item.model_dump()
        item_dict["user_id"]=user_id
        created = await crud_cart.create(
            db=db, object=CartCreateInternal(**item_dict), schema_to_select=CartRead
        )
        if not created:
            raise CartItemCreationError("Failed to add item to cart")
        return created

    async def delete_cart_item(
        self, item_id: str, user_id: str, db: AsyncSession
    ):
        item = await crud_cart.get(
            id=item_id, db=db, schema_to_select=CartRead
        )
        if not item:
            raise CartItemNotFoundError("Cart item not found")
        if item["user_id"] != user_id:
            raise CartItemNotFoundError("Cart item not found")
        await crud_cart.delete(db=db, id=item_id)
        return {"message": "Item removed from cart"}
