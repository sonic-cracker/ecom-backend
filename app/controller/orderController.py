from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.database import get_db
from app.models.cart import Cart
from app.models.order import OrderItem, Order
from app.models.product import Product
from app.dto.order_dto import OrderItemDTO
from app.models.review import Review

router = APIRouter()

# Confirm order
@router.post("/confirm/{user_id}")
def confirm_order(user_id: int, db: Session = Depends(get_db)):
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    new_order = Order(user_id=user_id)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product ID {item.product_id} not found")

        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_per_item=product.price,
            total_price=item.quantity * product.price
        )
        db.add(order_item)

    db.commit()
    db.query(Cart).filter(Cart.user_id == user_id).delete()
    db.commit()

    return {"message": "Order confirmed", "order_id": new_order.id}

# Order history
@router.get("/history/{user_id}")
def get_order_history(user_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    history = []

    for order in orders:
        for item in order.items:
            history.append({
                "product_name": item.product.name,
                "quantity": item.quantity,
                "price_per_item": round(item.total_price / item.quantity, 2),
                "total_price": item.total_price
            })
        order.seen = True

    db.commit()
    return history

# Latest order
@router.get("/latest")
def get_latest_order(user_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.user_id == user_id).order_by(Order.id.desc()).first()
    if not order:
        raise HTTPException(status_code=404, detail="No orders found")

    items = []
    for item in order.items:
        review_exists = db.query(Review).filter(
            Review.user_id == user_id, Review.product_id == item.product_id
        ).first() is not None

        items.append(OrderItemDTO(
            product_id=item.product_id,
            product_name=item.product.name,
            quantity=item.quantity,
            price_per_item=item.price_per_item,
            total_price=item.total_price,
            review_exists=review_exists
        ))
    return items
