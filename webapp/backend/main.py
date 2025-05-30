from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
from fastapi.exceptions import HTTPException

from core.config import settings
from core.logging import setup_logging
from core.database import create_db_and_tables
from routers import analysis, health, info, audit

# Setup logging
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables
    create_db_and_tables()
    yield
    # Shutdown: add cleanup here if needed

# Create FastAPI app
app = FastAPI(
    title="Crystal-Clear API",
    description="API for analyzing Ethereum smart contracts",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.middleware("http")
async def timeout_middleware(request: Request, call_next):
    try:
        return await asyncio.wait_for(call_next(request), timeout=settings.request_timeout)
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Request timed out")

# Include routers
app.include_router(health.router)
app.include_router(analysis.router)
app.include_router(info.router)
app.include_router(audit.router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to the Crystal-Clear API!",
        "docs": "/docs",
        "redoc": "/redoc",
    }
