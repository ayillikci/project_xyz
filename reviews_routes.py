from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from models import Review, User, Offer
from database import get_db
from auth_routes import get_current_user

router = APIRouter()

# Pydantic models for request/response validation
class ReviewBase(BaseModel):
    offer_id: int
    rating: int
    comment: str
    status: str

class ReviewOut(ReviewBase):
    id: int
    user_id: int

# Endpoint to create a new review
@router.post("/reviews/", response_model=ReviewOut)
async def create_review(
    review: ReviewBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if the offer exists before creating a review
    offer = db.query(Offer).filter(Offer.id == review.offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    new_review = Review(
        offer_id=review.offer_id,
        user_id=current_user.id,
        rating=review.rating,
        comment=review.comment,
        status=review.status
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

# Endpoint to get all reviews for an offer
@router.get("/reviews/offer/{offer_id}", response_model=List[ReviewOut])
async def get_reviews_by_offer(
    offer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Review).filter(Review.offer_id == offer_id).all()

# Endpoint to get a specific review by ID
@router.get("/reviews/{review_id}", response_model=ReviewOut)
async def get_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

# Endpoint to update a review
@router.put("/reviews/{review_id}", response_model=ReviewOut)
async def update_review(
    review_id: int,
    review_update: ReviewBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    review.rating = review_update.rating
    review.comment = review_update.comment
    review.status = review_update.status
    db.commit()
    db.refresh(review)
    return review

# Endpoint to delete a review
@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
    return {"detail": "Review deleted successfully"}
