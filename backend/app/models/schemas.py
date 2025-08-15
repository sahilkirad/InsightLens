from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class AnalysisType(str, Enum):
    """Enumeration of available analysis types"""
    SUMMARIZE = "summarize"
    SENTIMENT = "sentiment"
    QUESTION = "question"

class TextExtractionResponse(BaseModel):
    """Response model for text extraction"""
    text: str
    success: bool
    message: Optional[str] = None

class AnalysisRequest(BaseModel):
    """Request model for text analysis"""
    text: str
    analysis_type: AnalysisType
    prompt: Optional[str] = None

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
    created_at: datetime
    image_url: Optional[str] = None
    extracted_text: str
    analyses: List[AnalysisRecord] = [] 