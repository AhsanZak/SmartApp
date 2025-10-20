"""
Smart App Core - FastAPI Backend
Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config.settings import get_settings
from config.database import engine, Base
from api import chat, documents, models, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    settings = get_settings()
    print(f"Starting {settings.app_name}...")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
    
    yield
    
    # Shutdown
    print("Shutting down application...")


# Initialize FastAPI app
app = FastAPI(
    title="Smart App API",
    description="Intelligent document analysis platform with multi-model support",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
app.include_router(documents.router, prefix="/api/v1", tags=["Documents"])
app.include_router(models.router, prefix="/api/v1", tags=["Models"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Smart App API",
        "version": "1.0.0",
        "docs": "/docs"
    }

