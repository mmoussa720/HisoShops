from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Annotated
from .types import RiderStatus


class RiderBase(BaseModel):
    first_name: Annotated[str, Field(min_length=2, max_length=30, examples=["John"])]
    last_name: Annotated[str, Field(min_length=2, max_length=30, examples=["Doe"])]
    phone_number: Annotated[str, Field(min_length=8, max_length=20, examples=["+1234567890"])]
    email: Annotated[EmailStr, Field(examples=["john.doe@example.com"])]


class RiderRead(BaseModel):
    id: Annotated[str, Field(description="The unique id of the rider")]
    first_name: Annotated[str, Field(description="The first name of the rider")]
    last_name: Annotated[str, Field(description="The last name of the rider")]
    phone_number: Annotated[str, Field(description="The phone number of the rider")]
    email: Annotated[EmailStr, Field(description="The email of the rider")]
    status: Annotated[RiderStatus, Field(description="The status of the rider (busy/available)")]


class RiderCreate(RiderBase):
    status: Annotated[RiderStatus, Field(default=RiderStatus.available, description="The status of the rider")]
    model_config = ConfigDict(extra="forbid")


class RiderCreateInternal(RiderBase):
    status: Annotated[str, Field(default="available")]


class RiderUpdate(BaseModel):
    first_name: Annotated[str | None, Field(min_length=2, max_length=30, default=None)]
    last_name: Annotated[str | None, Field(min_length=2, max_length=30, default=None)]
    phone_number: Annotated[str | None, Field(min_length=8, max_length=20, default=None)]
    email: Annotated[EmailStr | None, Field(default=None)]
    status: Annotated[RiderStatus | None, Field(default=None)]


class RiderUpdateInternal(BaseModel):
    first_name: Annotated[str | None, Field(min_length=2, max_length=30, default=None)]
    last_name: Annotated[str | None, Field(min_length=2, max_length=30, default=None)]
    phone_number: Annotated[str | None, Field(min_length=8, max_length=20, default=None)]
    email: Annotated[EmailStr | None, Field(default=None)]
    status: Annotated[str | None, Field(default=None)]
