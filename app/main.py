from fastapi import FastAPI
from app.api.endpoints import router as api_router
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.utils.helpers import setup_logging

# Initialize Logging
setup_logging()

# Initialize Limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize FastAPI App
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION
)

origins = [
    "http://localhost:8501",  # Streamlit default port
    # Add any other origins if necessary
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.limiter = limiter

# Add SlowAPI middleware
app.add_middleware(SlowAPIMiddleware)

# Include API router
app.include_router(api_router, prefix="/api")
