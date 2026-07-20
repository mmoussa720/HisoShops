import uuid
from typing import List
from datetime import datetime
from sqlalchemy import String, Boolean, func, DateTime, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from ...infrastructure.database.session import Base


class User(Base):
    __tablename__ = "user"
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    user_name: Mapped[str] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=None
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_onupdate=func.now(), default=None
    )
    role: Mapped[str | None] = mapped_column(String, default=None)
    refresh_tokens: Mapped[List["RefreshTokens"] | None] = relationship(
        back_populates="user",
        default_factory=list,
        lazy="selectin",
        init=False,
    )
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    id: Mapped[str] = mapped_column(
        "id", unique=True, primary_key=True, default_factory=lambda:str(uuid.uuid4())
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    is_super_user: Mapped[bool] = mapped_column(Boolean, default=False)
    profile_image_url: Mapped[str] = mapped_column(
        String, default="https://profileimageurl.com"
    )
