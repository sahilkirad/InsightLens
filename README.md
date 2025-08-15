# InsightLens

A Web-Based Text Extraction and Analysis Platform

## Overview

InsightLens is a full-stack web application that allows users to upload images, extract text using OCR, and perform AI-powered analyses on the extracted text. The application features a modern, responsive interface with drag-and-drop functionality and real-time analysis capabilities.

## Features

- **Image Upload**: Drag-and-drop or file picker for image uploads
- **Text Extraction**: Automatic OCR using OCR.space API
- **AI Analysis**: Multiple analysis tools including:
  - Text summarization
  - Sentiment analysis
  - Question answering
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Real-time Processing**: Live feedback with loading states
- **Data Persistence**: Firebase Firestore integration for session storage
- **Context-Only Responses**: AI only answers based on extracted text, not general knowledge

## Technology Stack

### Frontend
- React.js with Vite
- Tailwind CSS
- Axios for API communication
- React Hooks for state management

### Backend
- Python FastAPI
- OCR.space API for text extraction
- Cohere AI for text analysis
- Firebase Firestore for data storage

### Deployment
- Frontend: Vercel
- Backend: Render

## Project Structure

```
InsightLens/
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── services/         # API services
│   │   ├── contexts/         # React contexts
│   │   └── utils/           # Utility functions
│   ├── public/
│   └── package.json
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── api/             # API routes
│   │   ├── services/        # Business logic
│   │   ├── models/          # Data models
│   │   └── utils/           # Utility functions
│   ├── requirements.txt
│   └── .env.example
└── README.md
```

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