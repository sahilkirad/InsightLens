#!/bin/bash

# InsightLens Backend Deployment Script
# This script helps prepare and deploy the backend to Render

echo "🚀 Starting InsightLens Backend Deployment..."

# Check if we're in the right directory
if [ ! -f "backend/requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found. Make sure you're in the project root directory."
    exit 1
fi

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Warning: .env file not found in backend directory."
    echo "Please create backend/.env with the following variables:"
    echo "  OCR_SPACE_API_KEY=your_ocr_space_api_key"
    echo "  COHERE_API_KEY=your_cohere_api_key"
    echo "  FIREBASE_CONFIG_JSON=your_firebase_config_json"
    echo "  CORS_ORIGINS=https://your-frontend-domain.vercel.app"
    echo ""
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
cd backend
pip install -r requirements.txt

# Run tests if available
if [ -f "test_cohere_only.py" ]; then
    echo "🧪 Running tests..."
    python test_cohere_only.py
fi

# Check if uvicorn is available
if ! command -v uvicorn &> /dev/null; then
    echo "❌ Error: uvicorn not found. Please install it: pip install uvicorn[standard]"
    exit 1
fi

echo "✅ Backend is ready for deployment!"
echo ""
echo "📋 Next steps:"
echo "1. Push your code to GitHub"
echo "2. Go to render.com and create a new Web Service"
echo "3. Connect your GitHub repository"
echo "4. Set the following configuration:"
echo "   - Environment: Python 3"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: uvicorn app.main:app --host 0.0.0.0 --port \$PORT"
echo "   - Root Directory: backend"
echo "5. Add your environment variables in Render dashboard"
echo "6. Deploy!"
echo ""
echo "🔗 Your backend will be available at: https://your-app-name.onrender.com"
