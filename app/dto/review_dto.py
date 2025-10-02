from pydantic import BaseModel
from typing import Optional


class ReviewDTO(BaseModel):
    user_id: int
    product_id: int
    rating: int
    comment: str

    class Config:
        orm_mode = True

class ReviewOut(BaseModel):
    username: str
    rating: int
    comment: str
    created_at: str

    class Config:
        orm_mode = True