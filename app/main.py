

from fastapi import FastAPI
from app.db.session import engine, SessionLocal
from app.models import user
from app.api.v1 import users
from time import time
import logging
from sqlalchemy.exc import OperationalError
from app.core.config import settings  # Import settings
from sqlalchemy.sql import text


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    # Create the database tables
    user.Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
    
    # Check database connectivity
    try:
        # Attempt to connect to the database
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
        logger.info("Database connection successful")
    except OperationalError as e:
        logger.error(f"Database connection failed: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    # Clean up actions can be added here (e.g., closing database connections)
    logger.info("Application shutting down")

@app.middleware("http")
async def log_middleware(request, call_next):
    start_time = time()
    response = await call_next(request)
    end_time = time()
    process_time = end_time - start_time
    logger.info(f"Request: {request.method} {request.url} - Processing Time: {process_time:.6f}s")
    return response

# Include user API routes

async def hello():
    return {"message": "Hello, World!"}
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
# app.include_router(users.router, prefix="/users", tags=["users"])

logger.info("FastAPI application started with SECRET_KEY: %s", settings.SECRET_KEY)
