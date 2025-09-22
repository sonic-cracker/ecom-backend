
from pydantic import BaseModel

class CartItemCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int
