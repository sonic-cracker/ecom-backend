from sqlalchemy import  Column, Integer, String, Float, CheckConstraint
from app.models.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(5000))
    image = Column(String)
    price = Column(Float)
    category = Column(String(50))
    in_stock = Column(Integer)

    __table_args__ = (
        CheckConstraint('price > 0', name='positive_price'),
        CheckConstraint('in_stock>= 0', name='non_negative_stock')
    )

