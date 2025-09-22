# app/models/confirmed_order.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base

class ConfirmedOrder(Base):
    __tablename__ = "confirmed_orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)

    user = relationship("User")
    product = relationship("Product")
