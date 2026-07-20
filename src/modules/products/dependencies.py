from .services import ProductService
from fastapi import Depends
from typing import Annotated


def get_product_service() -> ProductService:
    return ProductService()


ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]
