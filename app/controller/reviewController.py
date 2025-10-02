from fastapi import APIRouter, Depends ,HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.review import Review
from app.dto.review_dto import ReviewDTO,ReviewOut
from app.models.database import get_db
from app.models.user import User
from app.models.confirmOrder import ConfirmedOrder


router=APIRouter()

# Submit review
@router.post("/ratings")
def submit_review(review: ReviewDTO, db: Session = Depends(get_db)):
    exists = db.query(Review).filter(
        Review.user_id == review.user_id,
        Review.product_id == review.product_id
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="Review already exists")

    new_review = Review(
        user_id=review.user_id,
        product_id=review.product_id,
        rating=review.rating,
        comment=review.comment
    )
    db.add(new_review)
    db.commit()
    return {"message": "Review submitted successfully"}



# Get reviews of a product
@router.get("/{product_id}", response_model=List[ReviewOut])
def get_reviews(product_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.product_id == product_id).all()

    return [
        ReviewOut(
            username=r.user.username,
            rating=r.rating,
            comment=r.comment,
            created_at=r.created_at.strftime("%Y-%m-%d %H:%M")
        )
        for r in reviews
    ]
