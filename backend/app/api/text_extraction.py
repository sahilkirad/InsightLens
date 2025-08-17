from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.ocr_service import OCRService
from app.services.firestore_service import FirestoreService
from app.services.auth_service import AuthService
from app.models.schemas import TextExtractionResponse, UserResponse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
security = HTTPBearer()
auth_service = AuthService()

# Initialize services (will be initialized when needed)
ocr_service = None
firestore_service = None

def get_services():
    """Get or initialize services"""
    global ocr_service, firestore_service
    if ocr_service is None:
        ocr_service = OCRService()
    if firestore_service is None:
        firestore_service = FirestoreService()
    return ocr_service, firestore_service

@router.post("/extract-text", response_model=TextExtractionResponse)
async def extract_text_from_image(
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Extract text from uploaded image using OCR
    
    Args:
        file: The image file to process
        
    Returns:
        TextExtractionResponse: Contains extracted text and status
    """
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload an image file."
            )
        
        # Validate file size (max 10MB)
        if file.size and file.size > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="File size too large. Maximum size is 10MB."
            )
        
        # Read file content
        image_data = await file.read()
        
        if not image_data:
            raise HTTPException(
                status_code=400,
                detail="Empty file uploaded."
            )
        
        logger.info(f"Processing image: {file.filename}")
        
        # Get current user
        token = credentials.credentials
        current_user = await auth_service.get_current_user(token)
        if not current_user:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials"
            )
        
        # Get services
        ocr_service, firestore_service = get_services()
        
        # Extract text using OCR
        ocr_result = await ocr_service.extract_text_from_image(image_data, file.filename)
        
        print(f"🔍 OCR Result: {ocr_result}")
        
        if not ocr_result['success']:
            logger.error(f"OCR failed: {ocr_result['message']}")
            print(f"❌ OCR failed with message: {ocr_result['message']}")
            raise HTTPException(
                status_code=422,
                detail=f"Text extraction failed: {ocr_result['message']}"
            )
        
        extracted_text = ocr_result['text']
        
        # Store in Firestore
        try:
            document_id = await firestore_service.create_extraction_document(
                extracted_text=extracted_text,
                user_id=current_user.id,
                image_url=None  # For now, we don't store the image URL
            )
            logger.info(f"Created Firestore document: {document_id}")
        except Exception as e:
            logger.error(f"Failed to store in Firestore: {str(e)}")
            # Continue without storing if Firestore fails
        
        return TextExtractionResponse(
            text=extracted_text,
            success=True,
            message="Text extracted successfully",
            document_id=document_id
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error in text extraction: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during text extraction"
        )

@router.get("/health")
async def health_check():
    """Health check endpoint for text extraction service"""
    return {"status": "healthy", "service": "text-extraction"} 