from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer
from pydantic import BaseModel, Field

class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), index=True)
    price: Mapped[float] = mapped_column(Integer(), index=True)
class ItemBase(BaseModel):
    title: str = Field(..., max_length=100)
    price: float