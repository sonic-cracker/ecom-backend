from fastapi import APIRouter, Depends ,HTTPException
from sqlalchemy.orm import Session

from app.models.review import Review
from app.dto.review_dto import ReviewCreate,ReviewOut
from app.models.database import get_db
from app.models.user import User
from app.models.confirmOrder import ConfirmedOrder


router=APIRouter()

@router.post("/ratings", response_model=ReviewOut)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    # ✅ Step 1: Check if user actually purchased this product
    confirmed = db.query(ConfirmedOrder).filter(
        ConfirmedOrder.user_id == review.user_id,
        ConfirmedOrder.product_id == review.product_id
    ).first()

    if not confirmed:
        raise HTTPException(status_code=403, detail="You can only review products you've purchased.")

    # ✅ Step 2: Save review
    db_review = Review(**review.model_dump())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    user = db.query(User).filter(User.id == db_review.user_id).first()
    return {
        "id": db_review.id,
        "user_id": db_review.user_id,
        "product_id": db_review.product_id,
        "rating": db_review.rating,
        "comment": db_review.comment,
        "username": user.username if user else None
    }

@router.get("/{product_id}", response_model=list[ReviewOut])
def get_reviews(product_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.product_id == product_id).all()
    return [
        {
            "id": r.id,
            "user_id": r.user_id,
            "product_id": r.product_id,
            "rating": r.rating,
            "comment": r.comment,
            "username": r.user.username if r.user else "Anonymous"  # 👈 Pull username from related user
        }
        for r in reviews
    ]

