from pydantic import BaseModel, Field
from typing import Optional


class ProductDTO(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str
    image:str
    price: float = Field(gt=0)
    category: str = Field(min_length=1, max_length=50)
    in_stock: int = Field(ge=0)


class ProductResponse(ProductDTO):
    id: int

    class Config:
        orm_mode = True

class UpdateProductDTO(BaseModel):
    name: Optional[str]
    description: Optional[str]
    image: Optional[str]
    price: Optional[float]
    category: Optional[str]
    in_stock: Optional[int]