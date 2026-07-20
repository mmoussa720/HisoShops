from .services import ReviewService
from fastapi import Depends
from typing import Annotated


def get_review_service() -> ReviewService:
    return ReviewService()


ReviewServiceDep = Annotated[ReviewService, Depends(get_review_service)]
