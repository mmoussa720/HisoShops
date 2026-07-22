from .services import CartService
from fastapi import Depends
from typing import Annotated


def get_cart_service() -> CartService:
    return CartService()


CartServiceDep = Annotated[CartService, Depends(get_cart_service)]
