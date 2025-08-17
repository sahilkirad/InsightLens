from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.api import text_extraction, analysis, auth, user_data
from app.utils.firebase_config import initialize_firebase

# Load environment variables
load_dotenv()

# Initialize Firebase
initialize_firebase()

# Create FastAPI app
app = FastAPI(
    title="InsightLens API",
    description="A Web-Based Text Extraction and Analysis Platform",
    version="1.0.0"
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(user_data.router, prefix="/api/user", tags=["user-data"])
app.include_router(text_extraction.router, prefix="/api", tags=["text-extraction"])
app.include_router(analysis.router, prefix="/api", tags=["analysis"])

@app.get("/")
async def root():
    """Root endpoint for health check"""
    return {"message": "InsightLens API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "InsightLens API"} 