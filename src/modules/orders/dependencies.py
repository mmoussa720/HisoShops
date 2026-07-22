from .services import OrderService
from fastapi import Depends
from typing import Annotated


def get_order_service() -> OrderService:
    return OrderService()


OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]
