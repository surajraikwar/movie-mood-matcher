"""Main FastAPI application for Movie Mood Matcher."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from loguru import logger

from .core.config import settings
from .api.routes import recommendation, content, genres, auth, chat
from .schemas.recommendation import ErrorResponse
from .database.config import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    
    # Create database tables
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error="HTTP_ERROR",
            message=exc.detail,
            status_code=exc.status_code
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred",
            status_code=500
        ).dict()
    )


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs"
    }


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.app_version
    }


# Include routers
# Authentication routes (no version prefix for standard auth endpoints)
app.include_router(
    auth.router,
    prefix="/api",
    tags=["authentication"]
)

app.include_router(
    recommendation.router,
    prefix="/api/v1/recommendations",
    tags=["recommendations"]
)

app.include_router(
    content.router,
    prefix="/api/v1/content",
    tags=["content"]
)

app.include_router(
    genres.router,
    prefix="/api/v1/genres",
    tags=["genres"]
)

app.include_router(
    chat.router,
    prefix="/api/v1",
    tags=["chat"]
)
