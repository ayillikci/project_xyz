from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import auth_routes
import users_routes
import offers_routes
import categories_routes
import reviews_routes

app = FastAPI()

# Allow specific origins (your frontend URL)
origins = [
    "https://project-xyz-front-end.onrender.com",
    "http://localhost:3000"  # Add this for local development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your routes

# Include auth routes with a specific prefix, like "/auth" (optional)
app.include_router(auth_routes.router, prefix="/auth")

app.include_router(auth_routes.router, prefix="/auth")
app.include_router(users_routes.router, prefix="/users")
app.include_router(offers_routes.router, prefix="/offers")
app.include_router(categories_routes.router, prefix="/categories")
app.include_router(reviews_routes.router, prefix="/reviews")


@app.get("/")
def read_root():
    return {"Hello": "World"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""