from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.models.schemas import UserCreate, UserLogin, UserResponse, TokenData
from app.services.firestore_service import FirestoreService
import os
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Email configuration for password reset
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@insightlens.com")

class AuthService:
    """Service for user authentication and authorization"""
    
    def __init__(self):
        self.firestore_service = FirestoreService()
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[TokenData]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                return None
            token_data = TokenData(email=email)
            return token_data
        except JWTError:
            return None
    
    async def register_user(self, user_data: UserCreate) -> UserResponse:
        """Register a new user"""
        # Check if user already exists
        existing_user = await self.firestore_service.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = self.get_password_hash(user_data.password)
        user_doc = {
            'email': user_data.email,
            'full_name': user_data.full_name,
            'hashed_password': hashed_password,
            'created_at': datetime.utcnow(),
            'is_active': True,
            'last_login': None
        }
        
        user_id = await self.firestore_service.create_user(user_doc)
        
        return UserResponse(
            id=user_id,
            email=user_data.email,
            full_name=user_data.full_name,
            created_at=user_doc['created_at'],
            is_active=True
        )
    
    async def authenticate_user(self, user_data: UserLogin) -> Optional[UserResponse]:
        """Authenticate a user with email and password"""
        user = await self.firestore_service.get_user_by_email(user_data.email)
        if not user:
            return None
        
        if not self.verify_password(user_data.password, user['hashed_password']):
            return None
        
        if not user.get('is_active', True):
            return None
        
        # Update last login
        await self.firestore_service.update_user_last_login(user['id'])
        
        return UserResponse(
            id=user['id'],
            email=user['email'],
            full_name=user['full_name'],
            created_at=user['created_at'],
            is_active=user.get('is_active', True)
        )
    
    async def get_current_user(self, token: str) -> Optional[UserResponse]:
        """Get current user from JWT token"""
        token_data = self.verify_token(token)
        if token_data is None:
            return None
        
        user = await self.firestore_service.get_user_by_email(token_data.email)
        if user is None:
            return None
        
        return UserResponse(
            id=user['id'],
            email=user['email'],
            full_name=user['full_name'],
            created_at=user['created_at'],
            is_active=user.get('is_active', True)
        )

    def generate_reset_token(self) -> str:
        """Generate a secure reset token"""
        return secrets.token_urlsafe(32)

    def send_reset_email(self, email: str, reset_token: str, user_name: str) -> bool:
        """Send password reset email"""
        try:
            print(f"Attempting to send reset email to: {email}")
            print(f"SMTP Configuration - Server: {SMTP_SERVER}, Port: {SMTP_PORT}")
            print(f"SMTP Username: {SMTP_USERNAME}")
            print(f"SMTP Password configured: {'Yes' if SMTP_PASSWORD else 'No'}")
            
            if not SMTP_USERNAME or not SMTP_PASSWORD:
                print("❌ SMTP credentials not configured. Skipping email send.")
                print("Please configure SMTP_USERNAME and SMTP_PASSWORD in your .env file")
                return False

            # Create message
            msg = MIMEMultipart()
            msg['From'] = FROM_EMAIL
            msg['To'] = email
            msg['Subject'] = "Password Reset Request - InsightLens"

            # Create reset link (you'll need to configure your frontend URL)
            frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
            reset_link = f"{frontend_url}/reset-password?token={reset_token}&email={email}"
            
            print(f"Reset link generated: {reset_link}")

            # Email body
            body = f"""
            Hello {user_name},

            You have requested to reset your password for your InsightLens account.

            To reset your password, please click on the following link:
            {reset_link}

            This link will expire in 1 hour.

            If you did not request this password reset, please ignore this email.

            Best regards,
            The InsightLens Team
            """

            msg.attach(MIMEText(body, 'plain'))

            print("Connecting to SMTP server...")
            # Send email
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            print("SMTP connection established, attempting login...")
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            print("SMTP login successful, sending email...")
            text = msg.as_string()
            server.sendmail(FROM_EMAIL, email, text)
            server.quit()

            print(f"✅ Password reset email sent successfully to {email}")
            return True

        except smtplib.SMTPAuthenticationError as e:
            print(f"❌ SMTP Authentication failed: {str(e)}")
            print("Please check your SMTP_USERNAME and SMTP_PASSWORD")
            return False
        except smtplib.SMTPException as e:
            print(f"❌ SMTP error occurred: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Failed to send reset email: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            return False

    async def request_password_reset(self, email: str) -> bool:
        """Request password reset for a user"""
        try:
            print(f"🔍 Processing password reset request for email: {email}")
            
            # Check if user exists
            user = await self.firestore_service.get_user_by_email(email)
            if not user:
                print(f"❌ User not found with email: {email}")
                return False  # Don't reveal if user exists or not

            print(f"✅ User found: {user['full_name']} (ID: {user['id']})")

            # Generate reset token
            reset_token = self.generate_reset_token()
            reset_expires = datetime.utcnow() + timedelta(hours=1)
            
            print(f"🔑 Generated reset token: {reset_token[:10]}...")
            print(f"⏰ Token expires at: {reset_expires}")

            # Store reset token in Firestore
            print("💾 Storing reset token in Firestore...")
            token_stored = await self.firestore_service.store_reset_token(
                user['id'], 
                reset_token, 
                reset_expires
            )
            
            if not token_stored:
                print("❌ Failed to store reset token in Firestore")
                return False
                
            print("✅ Reset token stored successfully")

            # Send reset email
            print("📧 Attempting to send reset email...")
            email_sent = self.send_reset_email(email, reset_token, user['full_name'])
            
            if email_sent:
                print("✅ Password reset process completed successfully")
                return True
            else:
                print("❌ Failed to send reset email")
                return False

        except Exception as e:
            print(f"❌ Failed to request password reset: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            return False

    async def validate_reset_token(self, email: str, reset_token: str) -> bool:
        """Validate a password reset token"""
        try:
            user = await self.firestore_service.get_user_by_email(email)
            if not user:
                return False

            stored_token = await self.firestore_service.get_reset_token(user['id'])
            if not stored_token:
                return False

            # Check if token matches and is not expired
            if (stored_token['token'] == reset_token and 
                stored_token['expires'] > datetime.utcnow()):
                return True

            return False

        except Exception as e:
            print(f"Failed to validate reset token: {str(e)}")
            return False

    async def reset_password(self, email: str, reset_token: str, new_password: str) -> bool:
        """Reset user password using reset token"""
        try:
            # Validate token
            if not await self.validate_reset_token(email, reset_token):
                return False

            # Get user
            user = await self.firestore_service.get_user_by_email(email)
            if not user:
                return False

            # Hash new password
            hashed_password = self.get_password_hash(new_password)

            # Update password in Firestore
            success = await self.firestore_service.update_user_password(
                user['id'], 
                hashed_password
            )

            if success:
                # Clear reset token
                await self.firestore_service.clear_reset_token(user['id'])

            return success

        except Exception as e:
            print(f"Failed to reset password: {str(e)}")
            return False
