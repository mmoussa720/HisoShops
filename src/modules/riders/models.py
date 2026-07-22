import uuid
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from ...infrastructure.database.session import Base


class Rider(Base):
    __tablename__ = "rider"
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="available")
    id: Mapped[str] = mapped_column(
        "id", unique=True, primary_key=True, default_factory=lambda: str(uuid.uuid4())
    )
