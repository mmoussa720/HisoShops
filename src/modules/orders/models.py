from datetime import datetime
from sqlalchemy import String, Float, Integer, DateTime, ForeignKey, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import mapped_column, Mapped, relationship
from ...infrastructure.database.session import Base, engine


class OrderItem(Base):
    __tablename__ = "order_item"
    order_id: Mapped[str] = mapped_column(
        ForeignKey("order.id",ondelete="CASCADE",onupdate="CASCADE"), primary_key=True
    )
    product_id: Mapped[str] = mapped_column(
        ForeignKey("product.id",ondelete="CASCADE",onupdate="CASCADE"), primary_key=True
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    order: Mapped["Order"] = relationship(
        back_populates="items", lazy="selectin", init=False
    )
    product: Mapped["Product"] = relationship(lazy="selectin", init=False)


class Order(Base):
    __tablename__ = "order"
    id: Mapped[str] = mapped_column(
        String, unique=True, primary_key=True
    )
    customer_id: Mapped[str] = mapped_column(ForeignKey("user.id",ondelete='CASCADE',onupdate="CASCADE"), nullable=False)
    total: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="pending")
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=None
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_onupdate=func.now(), default=None
    )
    rider_id: Mapped[str | None] = mapped_column(
        ForeignKey("rider.id",ondelete="CASCADE",onupdate="CASCADE"), nullable=True, default=None
    )
    customer: Mapped["User"] = relationship(lazy="selectin", init=False)
    rider: Mapped["Rider"] = relationship(lazy="selectin", init=False)
    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order", lazy="selectin", default_factory=list, init=False
    )


async def generate_order_id(db: AsyncSession) -> str:
    result = await db.execute(select(Order.id).order_by(Order.id.desc()).limit(1))
    last_id = result.scalar_one_or_none()
    if last_id:
        last_number = int(last_id.split("-")[1])
        return f"ORD-{last_number + 1:05d}"
    return "ORD-00001"
