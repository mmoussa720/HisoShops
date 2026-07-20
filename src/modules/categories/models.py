import uuid
from typing import List
from sqlalchemy import String, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from ...infrastructure.database.session import Base


class Category(Base):
    __tablename__ = "category"
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, default=None)
    id: Mapped[str] = mapped_column(
        "id", unique=True, primary_key=True, default_factory=lambda: str(uuid.uuid4())
    )
    products: Mapped[List["Product"] | None] = relationship(
        secondary="product_category",
        back_populates="categories",
        lazy="selectin",
        default_factory=list,
        init=False,
    )
