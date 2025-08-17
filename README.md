# InsightLens

A full-stack web application for extracting and analyzing text from images using OCR and AI.

## Features

- **Image Upload & OCR**: Upload images via drag-and-drop and extract text using advanced OCR technology
- **Text Preview**: Instantly preview extracted text with copy functionality
- **AI-Powered Analysis**: Summarize, analyze sentiment, or ask questions about extracted text using Cohere AI
- **Custom Prompts**: Guide summarization and Q&A with your own prompts for tailored results
- **Analysis Dashboard**: View all analysis results in a clean, organized dashboard
- **User Authentication**: Secure user registration, login, and password management
- **Forgot Password**: Secure password reset functionality via email
- **User Data Management**: View and manage your extraction history and analysis results
- **Modern UI**: Responsive, user-friendly interface built with React, Vite, and Tailwind CSS
- **Secure & Private**: No images stored, only extracted text and analysis results saved securely

## New Features

### Forgot Password Functionality
- **Password Reset Request**: Users can request a password reset by entering their email address
- **Secure Email Links**: Reset links are sent via email with secure tokens that expire in 1 hour
- **Password Reset**: Users can set a new password using the secure reset link
- **Email Configuration**: Supports SMTP email configuration for password reset emails

## Setup Instructions

### Prerequisites
- Node.js (v16 or higher)
- Python (v3.8 or higher)
- Firebase project with Firestore enabled
- OCR.space API key
- Cohere API key

### Frontend Setup
1. Navigate to the frontend directory
2. Install dependencies: `npm install`
3. Start development server: `npm run dev`

### Backend Setup
1. Navigate to the backend directory
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your API credentials
6. Start development server: `uvicorn app.main:app --reload`

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```
OCR_SPACE_API_KEY=your_ocr_space_api_key
COHERE_API_KEY=your_cohere_api_key
FIREBASE_CONFIG_JSON={"type": "service_account", ...}
```

## API Endpoints

### POST /api/extract-text
Extracts text from uploaded image using OCR.

**Request**: Multipart form data with image file
**Response**: JSON with extracted text

### POST /api/analyze
Performs AI analysis on extracted text using Cohere AI.

**Request**: JSON with text, analysis_type, and optional prompt
**Response**: JSON with analysis results

## Testing

Run the Cohere integration test:
```bash
python test_cohere_only.py
```

## Deployment

### Frontend (Vercel)
1. Connect your GitHub repository to Vercel
2. Set build command: `npm run build`
3. Set output directory: `dist`
4. Deploy

### Backend (Render)
1. Connect your GitHub repository to Render
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables in Render dashboard
5. Deploy

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License. 