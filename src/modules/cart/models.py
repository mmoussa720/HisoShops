import uuid
from sqlalchemy import String, Float, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from ...infrastructure.database.session import Base


class Cart(Base):
    __tablename__ = "cart"
    product_name: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id",ondelete="CASCADE",onupdate="CASCADE"), nullable=False)
    product_id: Mapped[str] = mapped_column(ForeignKey("product.id",ondelete="CASCADE",onupdate="CASCADE"), nullable=False)
    size: Mapped[str | None] = mapped_column(String, default=None)
    id: Mapped[str] = mapped_column(
        "id", unique=True, primary_key=True, default_factory=lambda: str(uuid.uuid4())
    )
    user: Mapped["User"] = relationship(lazy="selectin", init=False)
    product: Mapped["Product"] = relationship(lazy="selectin", init=False)
