from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Dict, Any
from app.services.auth_service import AuthService
from app.services.firestore_service import FirestoreService
from app.models.schemas import UserResponse

router = APIRouter()
security = HTTPBearer()
auth_service = AuthService()
firestore_service = FirestoreService()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserResponse:
    """Dependency to get current authenticated user"""
    token = credentials.credentials
    user = await auth_service.get_current_user(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.get("/extractions", response_model=List[Dict[str, Any]])
async def get_user_extractions(
    limit: int = 20,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Get all extraction documents for the current user
    """
    try:
        print(f"🔍 Getting extractions for user: {current_user.id}")
        print(f"🔍 User email: {current_user.email}")
        extractions = await firestore_service.get_user_extractions(current_user.id, limit)
        print(f"📄 Found {len(extractions)} extractions")
        return extractions
    except Exception as e:
        print(f"❌ Error getting extractions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user extractions: {str(e)}"
        )

@router.get("/extractions/{document_id}")
async def get_user_extraction(
    document_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Get a specific extraction document for the current user
    """
    try:
        document = await firestore_service.get_extraction_document(document_id)
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        
        # Check if the document belongs to the current user
        if document.get('user_id') != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        return document
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve document: {str(e)}"
        )

@router.delete("/extractions/{document_id}")
async def delete_user_extraction(
    document_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Delete a specific extraction document for the current user
    """
    try:
        # First check if the document belongs to the current user
        document = await firestore_service.get_extraction_document(document_id)
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        
        if document.get('user_id') != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        success = await firestore_service.delete_extraction_document(document_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete document"
            )
        
        return {"message": "Document deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete document: {str(e)}"
        )

@router.get("/stats")
async def get_user_stats(current_user: UserResponse = Depends(get_current_user)):
    """
    Get user statistics (total extractions, recent activity, etc.)
    """
    try:
        extractions = await firestore_service.get_user_extractions(current_user.id, 1000)  # Get all for stats
        
        total_extractions = len(extractions)
        total_analyses = sum(len(doc.get('analyses', [])) for doc in extractions)
        
        # Get recent activity (last 7 days)
        from datetime import datetime, timedelta
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_extractions = []
        
        for doc in extractions:
            created_at = doc.get('created_at')
            if created_at:
                # Handle both Firestore timestamp and Python datetime
                if hasattr(created_at, 'timestamp'):
                    # Firestore timestamp
                    doc_datetime = datetime.fromtimestamp(created_at.timestamp())
                else:
                    # Python datetime
                    doc_datetime = created_at
                
                if doc_datetime > week_ago:
                    recent_extractions.append(doc)
        
        stats = {
            "total_extractions": total_extractions,
            "total_analyses": total_analyses,
            "recent_extractions": len(recent_extractions),
            "user_id": current_user.id,
            "user_email": current_user.email,
            "user_name": current_user.full_name
        }
        
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user stats: {str(e)}"
        )
