from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from models import Category, User
from database import get_db
from auth_routes import get_current_user

router = APIRouter()

# Pydantic models for request/response validation
class CategoryBase(BaseModel):
    name: str
    description: str

class CategoryOut(CategoryBase):
    id: int

# Endpoint to create a new category
@router.post("/categories/", response_model=CategoryOut)
async def create_category(
    category: CategoryBase, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    new_category = Category(name=category.name, description=category.description)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

# Endpoint to get all categories
@router.get("/categories/", response_model=List[CategoryOut])
async def get_categories(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return db.query(Category).all()

# Endpoint to get a specific category by ID
@router.get("/categories/{category_id}", response_model=CategoryOut)
async def get_category(
    category_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# Endpoint to update a category
@router.put("/categories/{category_id}", response_model=CategoryOut)
async def update_category(
    category_id: int, 
    category_update: CategoryBase, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category.name = category_update.name
    category.description = category_update.description
    db.commit()
    db.refresh(category)
    return category

# Endpoint to delete a category
@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"detail": "Category deleted successfully"}
