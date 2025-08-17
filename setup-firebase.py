#!/usr/bin/env python3
"""
Firebase Setup Script for InsightLens
This script helps you configure Firebase for the InsightLens application.
"""

import os
import json
import sys

def create_env_file():
    """Create .env file in the backend directory"""
    
    print("🔥 Firebase Setup for InsightLens")
    print("=" * 50)
    print()
    
    # Check if .env already exists
    env_path = os.path.join("backend", ".env")
    if os.path.exists(env_path):
        response = input("⚠️  .env file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    print("To configure Firebase, you need to:")
    print("1. Go to https://console.firebase.google.com/")
    print("2. Create a new project or select existing one")
    print("3. Go to Project Settings > Service Accounts")
    print("4. Click 'Generate new private key'")
    print("5. Download the JSON file")
    print()
    
    # Get Firebase configuration
    print("Enter your Firebase configuration:")
    print()
    
    # Option 1: JSON configuration
    use_json = input("Do you have the Firebase service account JSON file? (y/N): ").lower() == 'y'
    
    env_content = []
    
    if use_json:
        print("\nOption 1: JSON Configuration (Recommended)")
        print("- Copy the entire content of your Firebase service account JSON file")
        print("- Paste it below (press Enter twice when done):")
        print()
        
        json_lines = []
        while True:
            line = input()
            if line.strip() == "" and json_lines:
                break
            json_lines.append(line)
        
        if json_lines:
            try:
                json_content = "\n".join(json_lines)
                # Validate JSON
                json.loads(json_content)
                env_content.append(f'FIREBASE_CONFIG_JSON={json_content}')
                print("✅ JSON configuration added successfully!")
            except json.JSONDecodeError:
                print("❌ Invalid JSON format. Please check your configuration.")
                return
    else:
        print("\nOption 2: Individual Environment Variables")
        print("Enter the following values from your Firebase service account:")
        print()
        
        project_id = input("Project ID: ").strip()
        private_key_id = input("Private Key ID: ").strip()
        private_key = input("Private Key (with \\n for newlines): ").strip()
        client_email = input("Client Email: ").strip()
        client_id = input("Client ID: ").strip()
        client_x509_cert_url = input("Client X509 Cert URL (optional): ").strip()
        
        if all([project_id, private_key_id, private_key, client_email, client_id]):
            env_content.extend([
                f'FIREBASE_PROJECT_ID={project_id}',
                f'FIREBASE_PRIVATE_KEY_ID={private_key_id}',
                f'FIREBASE_PRIVATE_KEY="{private_key}"',
                f'FIREBASE_CLIENT_EMAIL={client_email}',
                f'FIREBASE_CLIENT_ID={client_id}'
            ])
            
            if client_x509_cert_url:
                env_content.append(f'FIREBASE_CLIENT_X509_CERT_URL={client_x509_cert_url}')
            
            print("✅ Individual configuration added successfully!")
        else:
            print("❌ Missing required Firebase configuration values.")
            return
    
    # Get other required environment variables
    print("\n" + "=" * 50)
    print("Other Required Configuration")
    print("=" * 50)
    print()
    
    # JWT Secret
    jwt_secret = input("JWT Secret Key (for authentication): ").strip()
    if not jwt_secret:
        jwt_secret = "your-super-secret-jwt-key-change-this-in-production"
        print("⚠️  Using default JWT secret. Change this in production!")
    
    env_content.append(f'JWT_SECRET_KEY={jwt_secret}')
    
    # API Keys
    ocr_key = input("OCR.space API Key (get from https://ocr.space/ocrapi): ").strip()
    if ocr_key:
        env_content.append(f'OCR_SPACE_API_KEY={ocr_key}')
    else:
        print("⚠️  OCR API key not provided. Text extraction will not work.")
    
    cohere_key = input("Cohere API Key (get from https://cohere.ai/): ").strip()
    if cohere_key:
        env_content.append(f'COHERE_API_KEY={cohere_key}')
    else:
        print("⚠️  Cohere API key not provided. AI analysis will not work.")
    
    # CORS
    cors_origins = input("CORS Origins (comma-separated, default: http://localhost:5173): ").strip()
    if not cors_origins:
        cors_origins = "http://localhost:5173"
    env_content.append(f'CORS_ORIGINS={cors_origins}')
    
    # Optional Hugging Face token
    hf_token = input("Hugging Face API Token (optional, for fallback analysis): ").strip()
    if hf_token:
        env_content.append(f'HUGGING_FACE_API_TOKEN={hf_token}')
    
    # Write .env file
    try:
        os.makedirs("backend", exist_ok=True)
        with open(env_path, 'w') as f:
            f.write('\n'.join(env_content))
        
        print("\n" + "=" * 50)
        print("✅ Configuration Complete!")
        print("=" * 50)
        print(f"📁 .env file created at: {env_path}")
        print()
        print("Next steps:")
        print("1. Start the backend: cd backend && python -m uvicorn app.main:app --reload")
        print("2. Start the frontend: cd frontend && npm run dev")
        print("3. Open http://localhost:5173 in your browser")
        print()
        print("🔒 Security Note: Keep your .env file secure and never commit it to version control!")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {str(e)}")
        return

if __name__ == "__main__":
    try:
        create_env_file()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
    except Exception as e:
        print(f"\n❌ Setup failed: {str(e)}")
        sys.exit(1)
