from sqlalchemy import Column, Integer, String
from app.models.database import Base
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String)
    contact_number = Column(String)
    email = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    profile_image = Column(String, nullable=True)

    orders = relationship("Order", back_populates="user")
