import os
import requests
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class OCRService:
    """Service for text extraction using OCR.space API"""
    
    def __init__(self):
        self.api_key = os.getenv("OCR_SPACE_API_KEY")
        self.api_url = "https://api.ocr.space/parse/image"
        
        # Allow running without API key for development/testing
        if not self.api_key:
            print("Warning: OCR_SPACE_API_KEY not set. OCR features may not work.")
            self.api_key = "demo_key"  # Fallback for development
    
    async def extract_text_from_image(self, image_data: bytes, filename: str) -> dict:
        """
        Extract text from image using OCR.space API
        
        Args:
            image_data: Raw image data as bytes
            filename: Name of the uploaded file
            
        Returns:
            dict: Response containing extracted text and status
        """
        try:
            # Prepare the request payload
            payload = {
                'apikey': self.api_key,
                'language': 'eng',  # English language
                'isOverlayRequired': False,
                'filetype': self._get_file_extension(filename),
                'detectOrientation': True,
                'scale': True,
                'OCREngine': 2  # OCR Engine 2 for better accuracy
            }
            
            # Prepare files for upload
            files = {
                'file': (filename, image_data, 'image/*')
            }
            
            # Make the API request
            response = requests.post(
                self.api_url,
                data=payload,
                files=files,
                timeout=60  # Increased timeout to 60 seconds
            )
            
            # Check if request was successful
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            print(f"OCR Response: {result}")
            
            # Check if OCR was successful
            if result.get('IsErroredOnProcessing', False):
                error_message = result.get('ErrorMessage', 'Unknown OCR error')
                print(f"OCR Error: {error_message}")
                return {
                    'success': False,
                    'text': '',
                    'message': f'OCR processing failed: {error_message}'
                }
            
            # Extract text from parsed results
            parsed_results = result.get('ParsedResults', [])
            if not parsed_results:
                return {
                    'success': False,
                    'text': '',
                    'message': 'No text found in the image'
                }
            
            # Combine all extracted text
            extracted_text = '\n'.join([
                parsed_result.get('ParsedText', '')
                for parsed_result in parsed_results
            ]).strip()
            
            if not extracted_text:
                return {
                    'success': False,
                    'text': '',
                    'message': 'No text could be extracted from the image'
                }
            
            # Clean the extracted text
            from app.services.ai_analysis_service import clean_text
            cleaned_text = clean_text(extracted_text)
            
            return {
                'success': True,
                'text': cleaned_text,
                'message': 'Text extracted and cleaned successfully'
            }
            
        except requests.exceptions.Timeout as e:
            return {
                'success': False,
                'text': '',
                'message': f'OCR service timeout: The request took too long to complete. Please try again.'
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'text': '',
                'message': f'Network error: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'text': '',
                'message': f'Unexpected error: {str(e)}'
            }
    
    def _get_file_extension(self, filename: str) -> str:
        """Extract file extension from filename"""
        return filename.split('.')[-1].lower() if '.' in filename else 'jpg' 