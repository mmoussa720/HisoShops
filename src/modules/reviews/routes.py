from fastapi import APIRouter, Path, Body
from .schemas import ReviewRead, ReviewCreate, ReviewUpdate
from typing import Any, Annotated
from .dependencies import ReviewServiceDep
from ...infrastructure.dependencies import AsyncSessionDep
from ...infrastructure.auth.dependencies import getCurrentUserDep

router = APIRouter(tags=["Reviews"])


@router.get(
    "/product/{product_slug}",
    status_code=200,
    summary="Get all reviews for a product",
    description="Retrieves all reviews for a given product by its slug",
    response_description="A list of reviews for the product",
    responses={200: {"description": "Reviews retrieved"}, 404: {"description": "Product not found"}},
)
async def get_reviews_by_product(
    product_slug: Annotated[str, Path(description="The slug of the product")],
    db: AsyncSessionDep,
    service: ReviewServiceDep,
):
    return await service.get_reviews_by_product(product_slug, db)


@router.get(
    "/product/{product_slug}/average-rating",
    status_code=200,
    summary="Get average rating for a product",
    description="Calculates and returns the average rating for a given product",
    response_description="The average rating of the product",
    responses={200: {"description": "Average rating calculated"}, 404: {"description": "Product not found"}},
)
async def get_product_average_rating(
    product_slug: Annotated[str, Path(description="The slug of the product")],
    db: AsyncSessionDep,
    service: ReviewServiceDep,
):
    return await service.get_product_average_rating(product_slug, db)


@router.post(
    "/",
    status_code=201,
    response_model=ReviewRead,
    summary="Create a review",
    description="Creates a new review for a product. A user can only review a product once.",
    response_description="The created review",
    responses={
        201: {"description": "Review created"},
        400: {"description": "Invalid data"},
        404: {"description": "User or product not found"},
        409: {"description": "You have already reviewed this product"},
    },
)
async def create_review(
    review: ReviewCreate,
    db: AsyncSessionDep,
    service: ReviewServiceDep,
    current_user: getCurrentUserDep,
) -> dict[str, Any]:
    return await service.create_review(review, current_user["id"], db)


@router.put(
    "/{review_id}",
    status_code=200,
    summary="Update a review",
    description="Updates an existing review. Only the review author can update it.",
    response_description="The updated review",
    responses={
        200: {"description": "Review updated"},
        404: {"description": "Review not found"},
        400: {"description": "You can only update your own review"},
    },
)
async def update_review(
    review_id: Annotated[str, Path(description="The id of the review")],
    data: Annotated[ReviewUpdate, Body(description="The new data")],
    db: AsyncSessionDep,
    service: ReviewServiceDep,
    current_user: getCurrentUserDep,
):
    return await service.update_review(data, review_id, current_user["id"], db)


@router.delete(
    "/{review_id}",
    status_code=200,
    summary="Delete a review",
    description="Deletes a review. Only the review author can delete it.",
    response_description="A message confirming the review deletion",
    responses={
        200: {"description": "Review deleted"},
        404: {"description": "Review not found"},
        400: {"description": "You can only delete your own review"},
    },
)
async def delete_review(
    review_id: Annotated[str, Path(description="The id of the review")],
    db: AsyncSessionDep,
    service: ReviewServiceDep,
    current_user: getCurrentUserDep,
):
    return await service.delete_review(review_id, current_user["id"], db)
