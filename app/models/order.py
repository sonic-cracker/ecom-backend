from sqlalchemy import String,Column, Integer,Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    seen = Column(Boolean, default=False)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price_per_item = Column(Float)
    total_price = Column(Float)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
