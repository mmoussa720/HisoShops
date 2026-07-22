from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated
from .types import OrderStatus


class OrderItemBase(BaseModel):
    product_id: Annotated[str, Field(description="The id of the product")]
    quantity: Annotated[int, Field(ge=1, description="Quantity of the product")]
    price: Annotated[float, Field(gt=0, description="Price per unit")]


class OrderItemRead(BaseModel):
    product_id: Annotated[str, Field(description="The id of the product")]
    quantity: Annotated[int, Field(description="Quantity of the product")]
    price: Annotated[float, Field(description="Price per unit")]


class OrderBase(BaseModel):
    customer_id: Annotated[str, Field(description="The id of the customer")]
    rider_id: Annotated[str | None, Field(default=None, description="The id of the assigned rider")]
    total: Annotated[float, Field(gt=0, description="Total price of the order")]


class OrderRead(BaseModel):
    id: Annotated[str, Field(description="The unique id of the order")]
    customer_id: Annotated[str, Field(description="The id of the customer")]
    rider_id: Annotated[str | None, Field(description="The id of the assigned rider")]
    total: Annotated[float, Field(description="Total price of the order")]
    status: Annotated[OrderStatus, Field(description="The status of the order")]


class OrderCreate(BaseModel):
    items: Annotated[list[OrderItemBase], Field(min_length=1, description="List of order items")]
    rider_id: Annotated[str | None, Field(default=None, description="The id of the assigned rider")]
    model_config = ConfigDict(extra="forbid")


class OrderCreateInternal(BaseModel):
    id: str
    customer_id: str
    rider_id: str | None = None
    total: float
    status: str = "pending"


class OrderUpdate(BaseModel):
    status: Annotated[OrderStatus | None, Field(default=None)]


class OrderUpdateInternal(BaseModel):
    status: Annotated[str | None, Field(default=None)]
    rider_id: Annotated[str | None, Field(default=None)]


class OrderAssignRider(BaseModel):
    rider_id: Annotated[str, Field(description="The id of the rider to assign")]
