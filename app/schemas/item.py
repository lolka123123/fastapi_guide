from pydantic import BaseModel, Field

class ItemBase(BaseModel):
    title: str = Field(..., max_length=100)
    price: float