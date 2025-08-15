import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Global variable to store the Firestore client
db = None

def initialize_firebase():
    """Initialize Firebase Admin SDK with service account credentials"""
    global db
    
    try:
        # Check if Firebase is already initialized
        try:
            firebase_admin.get_app()
            print("Firebase already initialized")
            db = firestore.client()
            return
        except ValueError:
            pass
        
        # Get Firebase configuration from environment variables
        firebase_config_json = os.getenv("FIREBASE_CONFIG_JSON")
        
        if firebase_config_json:
            # Use JSON configuration
            firebase_config = json.loads(firebase_config_json)
            cred = credentials.Certificate(firebase_config)
        else:
            # Use individual environment variables
            project_id = os.getenv("FIREBASE_PROJECT_ID")
            private_key_id = os.getenv("FIREBASE_PRIVATE_KEY_ID")
            private_key = os.getenv("FIREBASE_PRIVATE_KEY")
            client_email = os.getenv("FIREBASE_CLIENT_EMAIL")
            client_id = os.getenv("FIREBASE_CLIENT_ID")
            
            if not all([project_id, private_key_id, private_key, client_email, client_id]):
                print("Warning: Firebase configuration not found. Database features will be disabled.")
                return
            
            firebase_config = {
                "type": "service_account",
                "project_id": project_id,
                "private_key_id": private_key_id,
                "private_key": private_key.replace('\\n', '\n'),
                "client_email": client_email,
                "client_id": client_id,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL", "")
            }
            cred = credentials.Certificate(firebase_config)
        
        # Initialize Firebase Admin SDK
        firebase_admin.initialize_app(cred, {
            'projectId': firebase_config.get('project_id', 'your-project-id')
        })
        
        # Get Firestore client
        db = firestore.client()
        
        print("Firebase initialized successfully")
        
    except Exception as e:
        print(f"Error initializing Firebase: {str(e)}")
        print("Database features will be disabled")
        db = None

def get_firestore_client():
    """Get the Firestore client instance"""
    if db is None:
        raise RuntimeError("Firebase not initialized. Call initialize_firebase() first.")
    return db 