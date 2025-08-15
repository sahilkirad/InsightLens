from datetime import datetime
from typing import Dict, Any, List, Optional
from firebase_admin import firestore
from app.utils.firebase_config import get_firestore_client
from app.models.schemas import AnalysisRecord, ExtractionDocument, AnalysisType

class FirestoreService:
    """Service for Firestore database operations"""
    
    def __init__(self):
        try:
            self.db = get_firestore_client()
            self.collection_name = "extractions"
            self.enabled = True
        except Exception as e:
            print(f"Firestore not available: {str(e)}")
            self.db = None
            self.enabled = False
    
    async def create_extraction_document(self, extracted_text: str, image_url: Optional[str] = None) -> str:
        """
        Create a new extraction document in Firestore
        
        Args:
            extracted_text: The text extracted from the image
            image_url: Optional URL of the uploaded image
            
        Returns:
            str: The document ID of the created document
        """
        if not self.enabled:
            print("Firestore is disabled. Skipping document creation.")
            return "demo-doc-id"
            
        try:
            doc_data = {
                'created_at': datetime.utcnow(),
                'image_url': image_url,
                'extracted_text': extracted_text,
                'analyses': []
            }
            
            doc_ref = self.db.collection(self.collection_name).add(doc_data)
            print(f"Created Firestore document with ID: {doc_ref[1].id}")
            return doc_ref[1].id
            
        except Exception as e:
            print(f"Failed to create extraction document: {str(e)}")
            return "error-doc-id"
    
    async def add_analysis_to_document(self, document_id: str, analysis_type: AnalysisType, 
                                     result: Dict[str, Any], prompt: Optional[str] = None) -> bool:
        """
        Add an analysis result to an existing extraction document
        
        Args:
            document_id: The ID of the extraction document
            analysis_type: Type of analysis performed
            result: The analysis result
            prompt: Optional prompt used for the analysis
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            analysis_record = {
                'type': analysis_type.value,
                'result': result,
                'timestamp': datetime.utcnow(),
                'prompt': prompt
            }
            
            doc_ref = self.db.collection(self.collection_name).document(document_id)
            doc_ref.update({
                'analyses': firestore.ArrayUnion([analysis_record])
            })
            
            return True
            
        except Exception as e:
            print(f"Failed to add analysis to document: {str(e)}")
            return False
    
    async def get_extraction_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve an extraction document by ID
        
        Args:
            document_id: The ID of the document to retrieve
            
        Returns:
            Optional[Dict]: The document data or None if not found
        """
        try:
            doc_ref = self.db.collection(self.collection_name).document(document_id)
            doc = doc_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            else:
                return None
                
        except Exception as e:
            print(f"Failed to retrieve document: {str(e)}")
            return None
    
    async def get_recent_extractions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent extraction documents
        
        Args:
            limit: Maximum number of documents to retrieve
            
        Returns:
            List[Dict]: List of recent extraction documents
        """
        try:
            docs = (self.db.collection(self.collection_name)
                   .order_by('created_at', direction=firestore.Query.DESCENDING)
                   .limit(limit)
                   .stream())
            
            return [doc.to_dict() for doc in docs]
            
        except Exception as e:
            print(f"Failed to retrieve recent extractions: {str(e)}")
            return []
    
    async def delete_extraction_document(self, document_id: str) -> bool:
        """
        Delete an extraction document
        
        Args:
            document_id: The ID of the document to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            doc_ref = self.db.collection(self.collection_name).document(document_id)
            doc_ref.delete()
            return True
            
        except Exception as e:
            print(f"Failed to delete document: {str(e)}")
            return False 