from typing import Optional
from pydantic import BaseModel, EmailStr

# For user registration input
class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    contact_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None

# For login input
class UserLogin(BaseModel):
    username: str
    password: str

# For returning user data (response model)
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    contact_number: str | None = None
    address: str | None = None
    city: str | None = None
    state: Optional[str] = None
    zip_code: str | None = None

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    contact_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    profile_image: Optional[str] = None

class ChangePasswordRequest(BaseModel):
    user_id: int
    old_password: str
    new_password: str