from ..database.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey,Text,func
from datetime import datetime
from sqlalchemy import DateTime

class RefreshTokens(Base):
    __tablename__ = "refresh_tokens"
    user_id:Mapped[str]=mapped_column(ForeignKey("user.id"),primary_key=True)
    token:Mapped[str]=mapped_column(Text,primary_key=True)
    user:Mapped["User"]=relationship(back_populates="refresh_tokens",lazy="selectin",init=False)
    created_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True),server_default=func.now(),default=None)
    updated_at:Mapped[datetime|None]=mapped_column(server_onupdate=func.now(),default=None)

