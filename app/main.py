

from fastapi import FastAPI
from app.db.session import engine, SessionLocal
from app.api.v1 import  departments, employees, positions, projects, auth, approves
from time import time
import logging
from sqlalchemy.exc import OperationalError
from app.core.config import settings  # Import settings
from sqlalchemy.sql import text
from fastapi.middleware.cors import CORSMiddleware


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of origins allowed to make requests
    allow_credentials=True,
    allow_methods=["*"],  # List of methods allowed
    allow_headers=["*"],  # List of headers allowed
)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.on_event("startup")
async def startup_event():

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
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(employees.router, prefix="/api/v1/employees", tags=["employees"])
app.include_router(departments.router, prefix="/api/v1/departments", tags=["departments"])
app.include_router(positions.router, prefix="/api/v1/positions", tags=["positions"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(approves.router, prefix="/api/v1/approves", tags=["approves"])

logger.info("FastAPI application started with SECRET_KEY: %s", settings.SECRET_KEY)
