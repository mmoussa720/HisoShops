from fastapi import APIRouter, Path, Body, Query
from .schemas import CategoryRead, CategoryCreate, CategoryUpdate
from typing import Any, Annotated
from .dependencies import CategoryServiceDep
from ...infrastructure.dependencies import AsyncSessionDep

router = APIRouter(tags=["Categories"])


@router.get(
    "/",
    summary="List all categories",
    description="Retrieves a paginated list of all categories in the system",
    response_description="A paginated list of categories with total count and pagination metadata",
    responses={
        401: {"description": "Not authenticated"},
        403: {"description": "Not authorized"},
    },
)
async def get_categories(
    service: CategoryServiceDep,
    db: AsyncSessionDep,
    skip: Annotated[int, Query(description="Number of records to skip", ge=0)] = 0,
    limit: Annotated[int, Query(description="Maximum number of records", ge=1)] = 100,
):
    return await service.get_categories_paginated(db, skip=skip, limit=limit)


@router.get(
    "/{slug}",
    status_code=200,
    response_model=CategoryRead | None,
    summary="Return a category by its slug",
    description="Returns all the necessary category data by its slug",
    response_description="A json item of the desired category with all the necessary information",
    responses={
        200: {"description": "Category data retrieved"},
        404: {"description": "Category not found"},
    },
)
async def get_category_by_slug(
    slug: Annotated[str, Path(description="The slug of the category")],
    service: CategoryServiceDep,
    db: AsyncSessionDep,
):
    return await service.find_category_by_slug(slug, db)


@router.post(
    "/",
    status_code=201,
    response_model=CategoryRead,
    summary="Create new category",
    description="Creates a new category in the system",
    response_description="The created category with assigned ID and slug",
    responses={
        201: {"description": "Category created"},
        400: {"description": "Invalid category data"},
        409: {"description": "A category with this name already exists"},
    },
)
async def create_category(
    category: CategoryCreate,
    db: AsyncSessionDep,
    service: CategoryServiceDep,
) -> dict[str, Any]:
    return await service.create_category(category, db)


@router.put(
    "/{slug}",
    status_code=200,
    summary="Update a category",
    description="This endpoint updates a category's data",
    response_description="The updated category data",
    responses={
        200: {"description": "Category has been updated successfully"},
        404: {"description": "Category not found"},
        409: {"description": "A category with this name already exists"},
    },
)
async def update_category(
    slug: Annotated[str, Path(description="The slug of the category")],
    data: Annotated[CategoryUpdate, Body(description="The new data")],
    db: AsyncSessionDep,
    service: CategoryServiceDep,
):
    return await service.update_category(data, slug, db=db)


@router.delete(
    "/{slug}",
    status_code=200,
    summary="Delete a category",
    description="This endpoint deletes a category from the system",
    response_description="A message confirming the category deletion",
    responses={
        200: {"description": "Category has been deleted successfully"},
        404: {"description": "Category not found"},
    },
)
async def delete_category(
    slug: Annotated[str, Path(description="The slug of the category")],
    db: AsyncSessionDep,
    service: CategoryServiceDep,
):
    return await service.delete_a_category(slug, db)
