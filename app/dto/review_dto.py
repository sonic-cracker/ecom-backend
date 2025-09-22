from pydantic import BaseModel
from typing import Optional


class ReviewCreate(BaseModel):
    user_id: int
    product_id: int
    rating: int
    comment: str

class ReviewOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    rating: int
    comment: str
    username: Optional[str]

    class Config:
        orm_mode = True
