from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class ReviewBase(BaseModel):
    rating: Annotated[int, Field(ge=1, le=5, description="Rating from 1 to 5", examples=[4])]
    comment: Annotated[str | None, Field(default=None, examples=["Great product!"])]


class ReviewRead(BaseModel):
    id: Annotated[str, Field(description="The unique id of the review")]
    rating: Annotated[int, Field(description="The rating of the review")]
    comment: Annotated[str | None, Field(description="The comment of the review")]
    user_id: Annotated[str, Field(description="The id of the reviewer")]
    product_id: Annotated[str, Field(description="The id of the product")]


class ReviewCreate(ReviewBase):
    product_slug: Annotated[str, Field(description="The slug of the product being reviewed")]
    model_config = ConfigDict(extra="forbid")


class ReviewUpdate(BaseModel):
    rating: Annotated[int | None, Field(ge=1, le=5, default=None)]
    comment: Annotated[str | None, Field(default=None)]


class ReviewCreateInternal(ReviewBase):
    user_id: str
    product_id: str
