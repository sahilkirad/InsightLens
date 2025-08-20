from pydantic import BaseModel
from pydantic_extra_types import EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class AnalysisType(str, Enum):
    """Enumeration of available analysis types"""
    SUMMARIZE = "summarize"
    SENTIMENT = "sentiment"
    QUESTION = "question"

# User Authentication Models
class UserCreate(BaseModel):
    """Model for user registration"""
    email: EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    """Model for user login"""
    email: EmailStr
    password: str

class ForgotPasswordRequest(BaseModel):
    """Model for forgot password request"""
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    """Model for password reset"""
    email: EmailStr
    reset_token: str
    new_password: str

class PasswordResetResponse(BaseModel):
    """Model for password reset response"""
    message: str
    success: bool

class UserResponse(BaseModel):
    """Model for user response (without password)"""
    id: str
    email: EmailStr
    full_name: str
    created_at: datetime
    is_active: bool = True

class Token(BaseModel):
    """Model for JWT token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class TokenData(BaseModel):
    """Model for token payload data"""
    email: Optional[str] = None

# Existing Models (Updated to include user_id)
class TextExtractionResponse(BaseModel):
    """Response model for text extraction"""
    text: str
    success: bool
    message: Optional[str] = None
    document_id: Optional[str] = None

class AnalysisRequest(BaseModel):
    """Request model for text analysis"""
    text: str
    analysis_type: AnalysisType
    prompt: Optional[str] = None
    document_id: Optional[str] = None

class AnalysisResponse(BaseModel):
    """Response model for text analysis"""
    analysis_type: AnalysisType
    result: Any
    success: bool
    message: Optional[str] = None
    confidence: Optional[float] = None

class SentimentAnalysisResult(BaseModel):
    """Specific result model for sentiment analysis"""
    sentiment: str  # "positive", "negative", "neutral"
    confidence: float
    score: float
    emoji: str

class QuestionAnswerResult(BaseModel):
    """Specific result model for question answering"""
    answer: str
    confidence: float
    context: str

class SummaryResult(BaseModel):
    """Specific result model for text summarization"""
    summary: str
    original_length: int
    summary_length: int

class AnalysisRecord(BaseModel):
    """Model for storing analysis records in Firestore"""
    type: AnalysisType
    result: Dict[str, Any]
    timestamp: datetime
    prompt: Optional[str] = None

class ExtractionDocument(BaseModel):
    """Model for storing extraction documents in Firestore"""
    id: Optional[str] = None
    user_id: str
    created_at: datetime
    image_url: Optional[str] = None
    extracted_text: str
    analyses: List[AnalysisRecord] = []

class UserDocument(BaseModel):
    """Model for storing user documents in Firestore"""
    id: Optional[str] = None
    email: str
    full_name: str
    hashed_password: str
    created_at: datetime
    is_active: bool = True
    last_login: Optional[datetime] = None 