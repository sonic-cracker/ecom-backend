from pydantic import BaseModel
from typing import Optional

class OrderResponse(BaseModel):
    id: int
    product_name: str
    quantity: int
    price_per_item: float
    total_price: float

    # ⭐ Include these fields in the response
    rating: Optional[int]
    review: Optional[str]

    class Config:
        orm_mode = True
