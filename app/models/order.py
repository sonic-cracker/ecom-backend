from sqlalchemy import String,Column, Integer,Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price_per_item = Column(Float)
    total_price = Column(Float)
    seen = Column(Boolean, default=False)

    rating = Column(Integer, nullable=True)
    review = Column(String, nullable=True)

    user = relationship("User", back_populates="orders")
    product = relationship("Product",backref="orders")
