from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.cart import Cart
from app.models.database import get_db
from app.models.product import Product
from app.dto.cart_dto import CartItemCreate

router = APIRouter()

#  Add to Cart
@router.post("/add")
def add_to_cart(item: CartItemCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.in_stock < item.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")

    # Decrease stock
    product.in_stock -= item.quantity

    # Check if product already in cart for user
    existing = db.query(Cart).filter(Cart.user_id == item.user_id, Cart.product_id == item.product_id).first()
    if existing:
        existing.quantity += item.quantity
    else:
        new_cart = Cart(user_id=item.user_id, product_id=item.product_id, quantity=item.quantity)
        db.add(new_cart)

    db.commit()
    return {"message": "Product added to cart"}

#  View Cart
@router.get("/view/{user_id}")
def view_cart(user_id: int, db: Session = Depends(get_db)):
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
    result = []

    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        result.append({
            "cart_id": item.id,
            "product_id": item.product_id,
            "product_name": product.name if product else "Unknown",
            "quantity": item.quantity,
            "price_per_item": product.price if product else 0,
            "total_price": item.quantity * (product.price if product else 0),
            "image": product.image if product else None
        })

    return result

# Remove from Cart
@router.delete("/remove/{cart_id}")
def remove_from_cart(cart_id: int, db: Session = Depends(get_db)):
    cart_item = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    # Restore product stock
    product = db.query(Product).filter(Product.id == cart_item.product_id).first()
    if product:
        product.in_stock += cart_item.quantity

    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart"}

