from datetime import datetime
from typing import Dict, Any, List, Optional
from firebase_admin import firestore
from app.utils.firebase_config import get_firestore_client
from app.models.schemas import AnalysisRecord, ExtractionDocument, AnalysisType, UserDocument

class FirestoreService:
    """Service for Firestore database operations"""
    
    def __init__(self):
        self.db = None
        self.extractions_collection = "extractions"
        self.users_collection = "users"
        self.enabled = None  # Will be determined when first accessed
    
    def _ensure_initialized(self):
        """Ensure Firestore client is initialized"""
        if self.enabled is None:
            try:
                self.db = get_firestore_client()
                self.enabled = True
                print("✅ Firestore service initialized successfully")
            except Exception as e:
                print(f"⚠️  Firestore not available: {str(e)}")
                print("The app will run in development mode without database features.")
                print("To enable database features, please configure Firebase (see env.example)")
                self.db = None
                self.enabled = False
    
    async def create_extraction_document(self, extracted_text: str, user_id: str, image_url: Optional[str] = None) -> str:
        """
        Create a new extraction document in Firestore
        
        Args:
            extracted_text: The text extracted from the image
            user_id: The ID of the user who created the document
            image_url: Optional URL of the uploaded image
            
        Returns:
            str: The document ID of the created document
        """
        self._ensure_initialized()
        if not self.enabled:
            print("Firestore is disabled. Skipping document creation.")
            return "demo-doc-id"
            
        try:
            doc_data = {
                'user_id': user_id,
                'created_at': datetime.utcnow().replace(tzinfo=None),
                'image_url': image_url,
                'extracted_text': extracted_text,
                'analyses': []
            }
            
            doc_ref = self.db.collection(self.extractions_collection).add(doc_data)
            document_id = doc_ref[1].id
            print(f"Created Firestore document with ID: {document_id} for user: {user_id}")
            return document_id
            
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
        self._ensure_initialized()
        if not self.enabled:
            print("Firestore is disabled. Skipping analysis storage.")
            return False
            
        try:
            analysis_record = {
                'type': analysis_type.value,
                'result': result,
                'timestamp': datetime.utcnow().replace(tzinfo=None),
                'prompt': prompt
            }
            
            doc_ref = self.db.collection(self.extractions_collection).document(document_id)
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
        self._ensure_initialized()
        if not self.enabled:
            print("Firestore is disabled. Cannot retrieve document.")
            return None
            
        try:
            doc_ref = self.db.collection(self.extractions_collection).document(document_id)
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
        self._ensure_initialized()
        if not self.enabled:
            print("Firestore is disabled. Cannot retrieve recent extractions.")
            return []
            
        try:
            docs = (self.db.collection(self.extractions_collection)
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
        self._ensure_initialized()
        if not self.enabled:
            print("Firestore is disabled. Cannot delete document.")
            return False
            
        try:
            doc_ref = self.db.collection(self.extractions_collection).document(document_id)
            doc_ref.delete()
            return True
            
        except Exception as e:
            print(f"Failed to delete document: {str(e)}")
            return False
    
    # User Management Methods
    async def create_user(self, user_data: Dict[str, Any]) -> str:
        """
        Create a new user in Firestore
        
        Args:
            user_data: User data dictionary
            
        Returns:
            str: The user ID
        """
        self._ensure_initialized()
        if not self.enabled:
            print("Firestore is disabled. Skipping user creation.")
            return "demo-user-id"
            
        try:
            doc_ref = self.db.collection(self.users_collection).add(user_data)
            print(f"Created user with ID: {doc_ref[1].id}")
            return doc_ref[1].id
            
        except Exception as e:
            print(f"Failed to create user: {str(e)}")
            return "error-user-id"
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get user by email address
        
        Args:
            email: User's email address
            
        Returns:
            Optional[Dict]: User data or None if not found
        """
        self._ensure_initialized()
        if not self.enabled:
            print("Firestore is disabled. Cannot get user by email.")
            return None
            
        try:
            docs = (self.db.collection(self.users_collection)
                   .where('email', '==', email)
                   .limit(1)
                   .stream())
            
            for doc in docs:
                user_data = doc.to_dict()
                user_data['id'] = doc.id
                return user_data
            
            return None
            
        except Exception as e:
            print(f"Failed to get user by email: {str(e)}")
            return None
    
    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user by ID
        
        Args:
            user_id: User's ID
            
        Returns:
            Optional[Dict]: User data or None if not found
        """
        self._ensure_initialized()
        if not self.enabled:
            print("Firestore is disabled. Cannot get user by ID.")
            return None
            
        try:
            doc_ref = self.db.collection(self.users_collection).document(user_id)
            doc = doc_ref.get()
            
            if doc.exists:
                user_data = doc.to_dict()
                user_data['id'] = doc.id
                return user_data
            else:
                return None
                
        except Exception as e:
            print(f"Failed to get user by ID: {str(e)}")
            return None
    
    async def update_user_last_login(self, user_id: str) -> bool:
        """
        Update user's last login timestamp
        
        Args:
            user_id: User's ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        self._ensure_initialized()
        if not self.enabled:
            print("Firestore is disabled. Cannot update user last login.")
            return False
            
        try:
            doc_ref = self.db.collection(self.users_collection).document(user_id)
            doc_ref.update({
                'last_login': datetime.utcnow().replace(tzinfo=None)
            })
            return True
            
        except Exception as e:
            print(f"Failed to update user last login: {str(e)}")
            return False
    
    async def get_user_extractions(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get extraction documents for a specific user
        
        Args:
            user_id: User's ID
            limit: Maximum number of documents to retrieve
            
        Returns:
            List[Dict]: List of user's extraction documents
        """
        self._ensure_initialized()
        if not self.enabled:
            print("Firestore is disabled. Cannot get user extractions.")
            return []
            
        try:
            print(f"🔍 Querying extractions for user_id: {user_id}")
            # First get all documents for the user without ordering
            docs = (self.db.collection(self.extractions_collection)
                   .where('user_id', '==', user_id)
                   .stream())
            
            extractions = []
            for doc in docs:
                doc_data = doc.to_dict()
                doc_data['id'] = doc.id  # Add document ID to the data
                extractions.append(doc_data)
                print(f"📄 Found extraction: {doc.id} with user_id: {doc_data.get('user_id')}")
            
            # Sort in Python instead of Firestore to avoid index requirement
            extractions.sort(key=lambda x: x.get('created_at', datetime.utcnow().replace(tzinfo=None)), reverse=True)
            
            # Apply limit after sorting
            extractions = extractions[:limit]
            
            print(f"✅ Retrieved {len(extractions)} extractions for user {user_id}")
            return extractions
            
        except Exception as e:
            print(f"❌ Failed to retrieve user extractions: {str(e)}")
            return []

    # Password Reset Methods
    async def store_reset_token(self, user_id: str, reset_token: str, expires: datetime) -> bool:
        """
        Store password reset token for a user
        
        Args:
            user_id: User's ID
            reset_token: The reset token
            expires: Token expiration time
            
        Returns:
            bool: True if successful, False otherwise
        """
        self._ensure_initialized()
        if not self.enabled:
            print("Firestore is disabled. Cannot store reset token.")
            return False
            
        try:
            doc_ref = self.db.collection(self.users_collection).document(user_id)
            doc_ref.update({
                'reset_token': reset_token,
                'reset_token_expires': expires
            })
            return True
            
        except Exception as e:
            print(f"Failed to store reset token: {str(e)}")
            return False

    async def get_reset_token(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get password reset token for a user
        
        Args:
            user_id: User's ID
            
        Returns:
            Optional[Dict]: Reset token data or None if not found
        """
        self._ensure_initialized()
        if not self.enabled:
            print("Firestore is disabled. Cannot get reset token.")
            return None
            
        try:
            doc_ref = self.db.collection(self.users_collection).document(user_id)
            doc = doc_ref.get()
            
            if doc.exists:
                user_data = doc.to_dict()
                if 'reset_token' in user_data and 'reset_token_expires' in user_data:
                    return {
                        'token': user_data['reset_token'],
                        'expires': user_data['reset_token_expires']
                    }
            return None
            
        except Exception as e:
            print(f"Failed to get reset token: {str(e)}")
            return None

    async def clear_reset_token(self, user_id: str) -> bool:
        """
        Clear password reset token for a user
        
        Args:
            user_id: User's ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        self._ensure_initialized()
        if not self.enabled:
            print("Firestore is disabled. Cannot clear reset token.")
            return False
            
        try:
            doc_ref = self.db.collection(self.users_collection).document(user_id)
            doc_ref.update({
                'reset_token': firestore.DELETE_FIELD,
                'reset_token_expires': firestore.DELETE_FIELD
            })
            return True
            
        except Exception as e:
            print(f"Failed to clear reset token: {str(e)}")
            return False

    async def update_user_password(self, user_id: str, hashed_password: str) -> bool:
        """
        Update user's password
        
        Args:
            user_id: User's ID
            hashed_password: New hashed password
            
        Returns:
            bool: True if successful, False otherwise
        """
        self._ensure_initialized()
        if not self.enabled:
            print("Firestore is disabled. Cannot update password.")
            return False
            
        try:
            doc_ref = self.db.collection(self.users_collection).document(user_id)
            doc_ref.update({
                'hashed_password': hashed_password
            })
            return True
            
        except Exception as e:
            print(f"Failed to update password: {str(e)}")
            return False 