from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.user import User
from app.dto.user_dto import UserCreate, UserLogin, UserResponse ,ChangePasswordRequest
from app.models.database import get_db
from app.dto.user_dto import UserUpdate

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Register user with full details
@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        hashed_password=hashed_password,
        email=user.email,
        contact_number=user.contact_number,
        address=user.address,
        city = user.city,
        state = user.state,
        zip_code = user.zip_code
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Login endpoint
@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    print("Received login for:", user.username)
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        print("User not found")
    elif not pwd_context.verify(user.password, db_user.hashed_password):
        print("Password incorrect")

    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {
        "id": db_user.id,
        "username": db_user.username
    }

# Get user profile by ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/update/{user_id}", response_model=UserResponse)
def update_user_profile(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_update.model.dump(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

@router.post("/change-password")
def change_password(req: ChangePasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == req.user_id).first()
    if not user or not pwd_context.verify(req.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect current password")
    user.hashed_password = pwd_context.hash(req.new_password)
    db.commit()
    return {"message": "Password updated successfully"}

@router.get("/profile/{user_id}")
def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "state": user.state,
        "city": user.city,
        "zip_code": user.zip_code
    }



