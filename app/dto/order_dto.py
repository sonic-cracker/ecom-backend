from pydantic import BaseModel
from typing import Optional


class OrderItemDTO(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    price_per_item: float
    total_price: float
    review_exists: bool

    class Config:
        orm_mode = True
