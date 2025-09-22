from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.cart import Cart
from app.models.order import Order
from app.models.product import Product



router = APIRouter()


@router.post("/confirm/{user_id}")
def confirm_order(user_id: int, db: Session = Depends(get_db)):
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    for item in cart_items:
        # ✅ Fetch the product to get the current price
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product ID {item.product_id} not found")

        order = Order(
            user_id=user_id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_per_item=product.price,  # ✅ Correct source of price
            total_price=item.quantity * product.price,
        )
        db.add(order)

    db.commit()  # 🧠 Save all orders
    db.query(Cart).filter(Cart.user_id == user_id).delete()  # 🧹 Empty cart
    db.commit()
    return {"message": "Order confirmed"}



@router.get("/history/{user_id}")
def get_order_history(user_id: int, db: Session = Depends(get_db)):
    orders = (
        db.query(Order)
        .filter(Order.user_id == user_id)
        .join(Product)
        .all()
    )

    for order in orders:
        order.seen = True
    db.commit()

    return [
        {
            "product_name": order.product.name,
            "quantity": order.quantity,
            "price_per_item": round(order.total_price / order.quantity, 2),
            "total_price": order.total_price
        }
        for order in orders
    ]
