Overview
This project is a backend API built with FastAPI that allows users to share, lend, and manage items in a resource-sharing marketplace. Users can sign up, log in, create offers, manage categories, and leave reviews for items.

Prerequisites
Python 3.9+
Docker and Docker Compose
PostgreSQL
Postman (optional, for testing API endpoints)
Project Setup
1. Clone the Repository
Clone the repository and navigate to the project directory.

bash
Copy code
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
2. Set Up Docker for PostgreSQL
Create a docker-compose.yml file to set up a PostgreSQL container for local development:

yaml
Copy code
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: yourusername
      POSTGRES_PASSWORD: yourpassword
      POSTGRES_DB: yourdatabase
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
Run Docker to start the PostgreSQL container:

bash
Copy code
docker-compose up -d
3. Create a Virtual Environment and Install Dependencies
bash
Copy code
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file to store environment variables. Add the following:

env
Copy code
DATABASE_URL=postgresql://yourusername:yourpassword@localhost:5432/yourdatabase
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
5. Initialize Alembic for Database Migrations
Initialize Alembic:

bash
Copy code
alembic init alembic
Configure Alembic to use the DATABASE_URL from .env in alembic.ini:

ini
Copy code
sqlalchemy.url = postgresql+psycopg2://yourusername:yourpassword@localhost:5432/yourdatabase
Run initial migrations to create tables:

bash
Copy code
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
6. Start the FastAPI Server
Run the FastAPI application with Uvicorn:

bash
Copy code
uvicorn main:app --reload
The API will be available at http://127.0.0.1:8000.

Project Structure
main.py - FastAPI application setup and router inclusion.
models.py - SQLAlchemy models for User, Offer, Category, and Review tables.
auth_routes.py - Authentication endpoints for signup, login, and user info.
offers_routes.py - CRUD endpoints for offers.
categories_routes.py - CRUD endpoints for categories.
reviews_routes.py - CRUD endpoints for reviews.
database.py - Database connection and session setup.
utils.py - Utility functions for password hashing and verification.
auth.py - JWT utility functions for creating and verifying tokens.
API Documentation
Authentication Endpoints
Signup - POST /auth/signup

Request Body:

json
Copy code
{
  "email": "user@example.com",
  "password": "password",
  "user_type": "user"
}
Login - POST /auth/login

Request Body:

json
Copy code
{
  "email": "user@example.com",
  "password": "password"
}
Get Current User - GET /auth/me

Headers:

makefile
Copy code
Authorization: Bearer <token>
User Endpoints
Create User - POST /users/

Request Body:

json
Copy code
{
  "email": "newuser@example.com",
  "password": "password",
  "user_type": "user"
}
Get User by ID - GET /users/{user_id}

Update User by ID - PUT /users/{user_id}

Delete User by ID - DELETE /users/{user_id}

Offer Endpoints
Create Offer - POST /offers/

Request Body:

json
Copy code
{
  "product_name": "Mountain Bike",
  "product_description": "A high-quality mountain bike",
  "product_price": 200.00,
  "location": "POINT(40.730610 -73.935242)",
  "category_id": 1
}
Get Offer by ID - GET /offers/{offer_id}

Update Offer by ID - PUT /offers/{offer_id}

Delete Offer by ID - DELETE /offers/{offer_id}

Category Endpoints
Create Category - POST /categories/

Request Body:

json
Copy code
{
  "name": "Electronics",
  "description": "Items related to electronics"
}
Get All Categories - GET /categories/

Get Category by ID - GET /categories/{category_id}

Update Category by ID - PUT /categories/{category_id}

Delete Category by ID - DELETE /categories/{category_id}

Review Endpoints
Create Review - POST /reviews/

Request Body:

json
Copy code
{
  "offer_id": 1,
  "rating": 4,
  "comment": "Great bike!",
  "status": "active"
}
Get Reviews by Offer ID - GET /reviews/offer/{offer_id}

Get Review by ID - GET /reviews/{review_id}

Update Review by ID - PUT /reviews/{review_id}

Delete Review by ID - DELETE /reviews/{review_id}

Testing the API with Postman
Set Up Environment: In Postman, create an environment with variables:

base_url = http://127.0.0.1:8000
token = leave empty initially
Signup and Login: Use /auth/signup and /auth/login to create a user and obtain a token.

Set Authorization: For endpoints requiring authentication, go to the Authorization tab, select Bearer Token, and set the token to {{token}}.

Test Each Endpoint: Use the API documentation above to test each endpoint by sending requests and verifying responses.

Future Improvements
Add rate limiting to protect against abuse.
Implement role-based access control to restrict certain actions.
Add more detailed validation and error handling.
License
This project is licensed under the MIT License.

