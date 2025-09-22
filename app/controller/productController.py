from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.product import Product
from app.dto.product_dto import ProductResponse,ProductDTO,UpdateProductDTO
from app.models.database import get_db

router = APIRouter()

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductDTO, db: Session = Depends(get_db)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()
    print("Fetched from DB:", products)
    return products

@router.get("/{id}", response_model=ProductResponse)
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.get(Product, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{id}", response_model=ProductResponse)
def update_product(id: int, product: UpdateProductDTO, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product.model_dump(exclude_unset=True).items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).get(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"detail": "Product deleted"}

@router.get("/category/{category}", response_model=list[ProductResponse])
def get_products_by_category(category: str, db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.category == category).all()

