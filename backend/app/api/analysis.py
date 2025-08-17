from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.ai_analysis_service import AIAnalysisService
from app.services.alternative_ai_service import AlternativeAIAnalysisService
from app.services.firestore_service import FirestoreService
from app.services.auth_service import AuthService
from app.models.schemas import AnalysisRequest, AnalysisResponse, AnalysisType, UserResponse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
security = HTTPBearer()
auth_service = AuthService()

# Initialize services (will be initialized when needed)
ai_service = None
alternative_ai_service = None
firestore_service = None

def get_services():
    """Get or initialize services"""
    global ai_service, alternative_ai_service, firestore_service
    if ai_service is None:
        ai_service = AIAnalysisService()
    if alternative_ai_service is None:
        alternative_ai_service = AlternativeAIAnalysisService()
    if firestore_service is None:
        firestore_service = FirestoreService()
    return ai_service, alternative_ai_service, firestore_service

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_text(
    request: AnalysisRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Analyze text using AI models
    
    Args:
        request: AnalysisRequest containing text, analysis_type, and optional prompt
        
    Returns:
        AnalysisResponse: Contains analysis results and status
    """
    try:
        # Validate input
        if not request.text or not request.text.strip():
            raise HTTPException(
                status_code=400,
                detail="Text is required for analysis"
            )
        
        if not request.analysis_type:
            raise HTTPException(
                status_code=400,
                detail="Analysis type is required"
            )
        
        # For question analysis, prompt is required
        if request.analysis_type == AnalysisType.QUESTION and not request.prompt:
            raise HTTPException(
                status_code=400,
                detail="Prompt is required for question analysis"
            )
        
        # Get current user
        token = credentials.credentials
        current_user = await auth_service.get_current_user(token)
        if not current_user:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials"
            )
        
        logger.info(f"Analyzing text with type: {request.analysis_type} for user: {current_user.email}")
        
        # Get services
        ai_service, alternative_ai_service, firestore_service = get_services()
        
        # Clean the text before analysis
        from app.services.ai_analysis_service import clean_text
        cleaned_text = clean_text(request.text)
        
        if not cleaned_text:
            raise HTTPException(
                status_code=400,
                detail="No meaningful text found after cleaning"
            )
        
        # Use Cohere service if available, otherwise fallback to Hugging Face
        analysis_result = None
        if alternative_ai_service.cohere_api_key:
            logger.info("Using Cohere AI service")
            analysis_result = await alternative_ai_service.analyze_text(
                text=cleaned_text,
                analysis_type=request.analysis_type.value,
                prompt=request.prompt
            )
        
        # Fallback to original service if Cohere fails or not available
        if not analysis_result or not analysis_result.get('success'):
            logger.info("Using Hugging Face AI service")
            analysis_result = await ai_service.analyze_text(
                text=cleaned_text,
                analysis_type=request.analysis_type.value,
                prompt=request.prompt
            )
        
        if not analysis_result['success']:
            raise HTTPException(
                status_code=422,
                detail=analysis_result['message']
            )
        
        # Ensure confidence is properly capped at 100%
        result = analysis_result['result']
        if 'confidence' in result:
            result['confidence'] = min(result['confidence'], 100.0)
        
        # Store analysis result in Firestore if document_id is provided
        if request.document_id:
            try:
                await firestore_service.add_analysis_to_document(
                    document_id=request.document_id,
                    analysis_type=request.analysis_type,
                    result=result,
                    prompt=request.prompt
                )
                logger.info(f"Stored analysis result for document: {request.document_id}")
            except Exception as e:
                logger.error(f"Failed to store analysis result: {str(e)}")
                # Continue without storing if Firestore fails
        
        return AnalysisResponse(
            analysis_type=request.analysis_type,
            result=result,
            success=True,
            message=analysis_result['message'],
            confidence=result.get('confidence')
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error in text analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during text analysis"
        )

@router.get("/analysis-types")
async def get_analysis_types():
    """Get available analysis types"""
    return {
        "analysis_types": [
            {
                "type": "summarize",
                "name": "Text Summarization",
                "description": "Generate a concise summary using Cohere AI",
                "model": "cohere/summarize-xlarge"
            },
            {
                "type": "sentiment",
                "name": "Sentiment Analysis",
                "description": "Analyze the emotional tone using Cohere AI",
                "model": "cohere/command"
            },
            {
                "type": "question",
                "name": "Question Answering",
                "description": "Answer questions about the text using Cohere AI",
                "model": "cohere/command"
            }
        ]
    }

@router.get("/health")
async def health_check():
    """Health check endpoint for analysis service"""
    return {"status": "healthy", "service": "analysis"} 