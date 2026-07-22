from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class CartBase(BaseModel):
    product_name: Annotated[str, Field(min_length=1, max_length=100, examples=["Classic T-Shirt"])]
    size: Annotated[str | None, Field(default=None, examples=["M"])]
    quantity: Annotated[int, Field(ge=1, examples=[2])]
    unit_price: Annotated[float, Field(gt=0, description="Price per unit", examples=[19.99])]
    product_id: Annotated[str, Field(description="The id of the product")]


class CartRead(BaseModel):
    id: Annotated[str, Field(description="The unique id of the cart item")]
    product_name: Annotated[str, Field(description="The name of the product")]
    size: Annotated[str | None, Field(description="The size of the product")]
    quantity: Annotated[int, Field(description="The quantity in the cart")]
    unit_price: Annotated[float, Field(description="Price per unit")]
    product_id: Annotated[str, Field(description="The id of the product")]
    user_id: Annotated[str, Field(description="The id of the user")]


class CartCreate(CartBase):
    model_config = ConfigDict(extra="forbid")

class CartCreateInternal(CartCreate):
    user_id: Annotated[str, Field(description="The id of the user")]


class CartUpdate(BaseModel):
    quantity: Annotated[int, Field(ge=1, examples=[3])]
