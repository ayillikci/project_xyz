from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import User
from database import get_db
from auth_routes import get_current_user
from pydantic import BaseModel
from utils import hash_password
from datetime import datetime


router = APIRouter()

class UserOut(BaseModel):
    id: int
    email: str
    user_type: str
    registered_at: datetime  # Use datetime here

class UserCreate(BaseModel):
    email: str
    password: str
    username: str
    user_type: str

class UserUpdate(BaseModel):
    email: str
    password: str
    user_type: str

@router.post("/users/", response_model=UserOut)
async def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, password_hash=hashed_password, user_type=user.user_type)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserOut)
async def update_user(
        user_id: int,
        user_update: UserUpdate,  # Make sure this matches the Pydantic model you defined
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the user fields based on the incoming data
    user.email = user_update.email
    user.password_hash = hash_password(user_update.password)
    user.user_type = user_update.user_type
    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}

