from fastapi import APIRouter, Path, Body
from .schemas import CartRead, CartCreate, CartUpdate
from typing import Any, Annotated
from .dependencies import CartServiceDep
from ...infrastructure.dependencies import AsyncSessionDep
from ...infrastructure.auth.dependencies import getCurrentUserDep

router = APIRouter(tags=["Cart"])


@router.get(
    "/",
    status_code=200,
    summary="Get cart items for current user",
    description="Retrieves all cart items for the authenticated user",
    response_description="A list of cart items",
    responses={200: {"description": "Cart items retrieved"}, 401: {"description": "Not authenticated"}},
)
async def get_cart(
    db: AsyncSessionDep,
    service: CartServiceDep,
    current_user: getCurrentUserDep,
):
    return await service.get_cart_by_user(current_user["id"], db)


@router.post(
    "/",
    status_code=201,
    response_model=CartRead,
    summary="Add an item to cart",
    description="Adds a product to the authenticated user's cart",
    response_description="The created cart item",
    responses={
        201: {"description": "Item added to cart"},
        409: {"description": "Product already in cart"},
    },
)
async def add_to_cart(
    item: CartCreate,
    db: AsyncSessionDep,
    service: CartServiceDep,
    current_user: getCurrentUserDep,
) -> dict[str, Any]:
    return await service.add_to_cart(item, current_user["id"], db)

@router.delete(
    "/{item_id}",
    status_code=200,
    summary="Remove an item from cart",
    description="Removes an item from the authenticated user's cart",
    response_description="A message confirming the removal",
    responses={200: {"description": "Item removed from cart"}, 404: {"description": "Cart item not found"}},
)
async def delete_cart_item(
    item_id: Annotated[str, Path(description="The id of the cart item")],
    db: AsyncSessionDep,
    service: CartServiceDep,
    current_user: getCurrentUserDep,
):
    return await service.delete_cart_item(item_id, current_user["id"], db)
