from .services import CategoryService
from fastapi import Depends
from typing import Annotated


def get_category_service() -> CategoryService:
    return CategoryService()


CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]
