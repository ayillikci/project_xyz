from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    password_hash = Column(Text, nullable=False)
    email = Column(String, unique=True, nullable=False)
    user_type = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, nullable=False)

    offers = relationship("Offer", back_populates="user")
    reviews = relationship("Review", back_populates="user")

class Offer(Base):
    __tablename__ = 'offers'

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    product_description = Column(Text, nullable=True)
    product_price = Column(DECIMAL, nullable=False)
    location = Column(String)  # Example for a simple point string; you may change it
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    #created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    #updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=True)
    # Automatically set timestamps for created_at and updated_at
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, nullable=True, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="offers")
    category = relationship("Category", back_populates="offers")
    reviews = relationship("Review", back_populates="offer")
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    offers = relationship("Offer", back_populates="category")

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    offer_id = Column(Integer, ForeignKey('offers.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
    status = Column(String, nullable=False)

    user = relationship("User", back_populates="reviews")
    offer = relationship("Offer", back_populates="reviews")