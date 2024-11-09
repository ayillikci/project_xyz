from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import Offer, User
from database import get_db
from auth_routes import get_current_user
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter()

class OfferBase(BaseModel):
    product_name: str
    product_description: str
    product_price: float
    location: str  # use `str` to represent points or location strings

class OfferOut(OfferBase):
    id: int
    # user_id: int
@router.post("/offers/", response_model=OfferOut)
async def create_offer(
    offer: OfferBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print(f"Current user: {current_user}")
    print(f"Current user ID: {current_user.id}")

    new_offer = Offer(
        **offer.dict(),
        user_id=current_user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_offer)
    db.commit()
    db.refresh(new_offer)
    return new_offer

# Commented while fixing the created_at (and updated_at, if necessary).
"""@router.post("/offers/", response_model=OfferOut)
async def create_offer(offer: OfferBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_offer = Offer(**offer.dict(), user_id=current_user.id)
    db.add(new_offer)
    db.commit()
    db.refresh(new_offer)
    return new_offer
"""
@router.get("/offers/{offer_id}", response_model=OfferOut)
async def get_offer(offer_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer

@router.put("/offers/{offer_id}", response_model=OfferOut)
async def update_offer(offer_id: int, offer_update: OfferBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    offer.product_name = offer_update.product_name
    offer.product_description = offer_update.product_description
    offer.product_price = offer_update.product_price
    offer.location = offer_update.location
    db.commit()
    db.refresh(offer)
    return offer

@router.delete("/offers/{offer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_offer(offer_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    db.delete(offer)
    db.commit()
    return {"detail": "Offer deleted successfully"}
