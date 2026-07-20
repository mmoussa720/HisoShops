from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Annotated
from uuid import uuid4

class UserBase(BaseModel):
    first_name:Annotated[str,Field(min_length=2,max_length=30,examples=["User"])]
    last_name:Annotated[str,Field(min_length=2,max_length=30,examples=["Userson"])]
    user_name:Annotated[str,Field(min_length=2,max_length=20,examples=["User720"])]
    email:Annotated[EmailStr,Field(examples=["user.userson@example.com"])]

class User(UserBase):
    is_super_user:bool
    hashed_password:str
    profile_image_url:Annotated[str,Field(default="https://www.profileImageUrl.com",description="Url of the user's profile image")]


class UserRead(BaseModel):
    id:Annotated[str,Field(description="The unique id of the user")]
    first_name:Annotated[str,Field(description="The first name of the user")]
    last_name:Annotated[str,Field(description="The last name of the user")]
    user_name:Annotated[str,Field(description="The user name of the user")]
    email:Annotated[EmailStr,Field(description="The email of the user")]
    role:Annotated[str|None,Field(description="The role of the user")]
    profile_image_url:Annotated[str,Field(description="The profile image url of the user")]
    is_deleted:Annotated[bool,Field(description="Soft deletion",default=False)]
    is_super_user:Annotated[bool,Field(description="indicates if this user is super user or not")]
    email_verified:bool=False

class UserCreate(UserBase):
    password:Annotated[str,Field(examples=["UserPassword#123"],description="The user password",pattern=r"^.{8,}|[0-9]+|[A-Z]+|[a-z]+|[^a-zA-Z0-9]+$")]
    model_config=ConfigDict(extra="forbid")

class UserUpdate(BaseModel):
    first_name:Annotated[str,Field(min_length=2,max_length=30,examples=["User"],default=None)]
    last_name:Annotated[str,Field(min_length=2,max_length=30,examples=["Userson"],default=None)]
    user_name:Annotated[str,Field(min_length=2,max_length=20,examples=["User720"],default=None)]
    email:Annotated[EmailStr,Field(examples=["user.userson@example.com"],default=None)]
    profile_image_url: Annotated[
        str | None,
        Field(
            pattern=r"^(https?|ftp)://[^\s/$.?#].[^\s]*$",
            examples=["https://www.profileimageurl.com"],
            default=None,
        ),
    ]
    is_deleted:bool=False
    email_verified:bool=False

class UserCreateInternal(UserBase):
    hashed_password:str
