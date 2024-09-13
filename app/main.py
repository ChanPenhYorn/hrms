# app/main.py
from fastapi import FastAPI
from app.db.session import engine
from app.models import user
from app.api.v1 import users

# Create the database tables
user.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include user API routes
app.include_router(users.router, prefix="/users", tags=["users"])
