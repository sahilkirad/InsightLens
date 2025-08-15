# InsightLens Setup Guide

This guide will help you set up and run the InsightLens application locally.

## Prerequisites

Before you begin, make sure you have the following installed:

- **Node.js** (v16 or higher) - [Download here](https://nodejs.org/)
- **Python** (v3.8 or higher) - [Download here](https://python.org/)
- **Git** - [Download here](https://git-scm.com/)

## Required API Keys

You'll need to obtain the following API keys:

### 1. OCR.space API Key
- Go to [OCR.space](https://ocr.space/ocrapi)
- Sign up for a free account
- Get your API key from the dashboard
- Free tier includes 500 requests per day

### 2. Hugging Face API Token
- Go to [Hugging Face](https://huggingface.co/)
- Create an account
- Go to Settings > Access Tokens
- Create a new token
- Free tier includes generous limits

### 3. Firebase Configuration
- Go to [Firebase Console](https://console.firebase.google.com/)
- Create a new project
- Enable Firestore Database
- Go to Project Settings > Service Accounts
- Generate a new private key (JSON file)
- Copy the entire JSON content

## Backend Setup

### 1. Navigate to Backend Directory
```bash
cd InsightLens/backend
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
# Copy the example file
cp env.example .env

# Edit .env file with your API keys
```

Edit the `.env` file with your actual API credentials:

```env
# OCR.space API Configuration
OCR_SPACE_API_KEY="your_ocr_space_api_key_here"

# Hugging Face API Configuration
HUGGING_FACE_API_TOKEN="your_hugging_face_api_token_here"

# Firebase Configuration
FIREBASE_CONFIG_JSON='{"type": "service_account", "project_id": "your-project-id", ...}'

# Application Configuration
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

### 5. Run the Backend
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

## Frontend Setup

### 1. Navigate to Frontend Directory
```bash
cd InsightLens/frontend
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Configure Environment Variables (Optional)
```bash
# Copy the example file
cp env.example .env

# Edit .env file if you need to change the API URL
```

### 4. Run the Frontend
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Testing the Application

1. Open your browser and go to `http://localhost:5173`
2. Upload an image containing text
3. Wait for text extraction to complete
4. Use the analysis tools to analyze the extracted text

## API Endpoints

### Text Extraction
- `POST /api/extract-text` - Extract text from uploaded image

### Text Analysis
- `POST /api/analyze` - Analyze text using AI models
- `GET /api/analysis-types` - Get available analysis types

### Health Checks
- `GET /health` - Backend health check
- `GET /` - Root endpoint

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Make sure the backend is running on port 8000
   - Check that CORS_ORIGINS includes your frontend URL

2. **API Key Errors**
   - Verify all API keys are correctly set in the `.env` file
   - Check that the keys are valid and have sufficient quota

3. **Firebase Connection Issues**
   - Ensure the Firebase project is created and Firestore is enabled
   - Verify the service account JSON is correctly formatted

4. **Port Already in Use**
   - Change the port in the uvicorn command: `--port 8001`
   - Update the frontend API URL accordingly

### Logs

- Backend logs will appear in the terminal where you ran uvicorn
- Frontend logs will appear in the browser console (F12)

## Deployment

### Backend (Render)
1. Push your code to GitHub
2. Connect your repository to Render
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables in Render dashboard
6. Deploy

### Frontend (Vercel)
1. Push your code to GitHub
2. Connect your repository to Vercel
3. Set build command: `npm run build`
4. Set output directory: `dist`
5. Add environment variables if needed
6. Deploy

## Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Verify all API keys are valid
3. Check the browser console and backend logs
4. Ensure all dependencies are installed correctly

## License

This project is licensed under the MIT License. 