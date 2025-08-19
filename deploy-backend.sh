#!/bin/bash

# InsightLens Backend Deployment Script for Render
# This script helps prepare and deploy the backend to Render

echo "🚀 InsightLens Backend Deployment to Render"
echo "=============================================="

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "❌ Error: backend/.env file not found!"
    echo "Please create backend/.env with your API keys before deploying."
    echo ""
    echo "Required environment variables:"
    echo "- FIREBASE_CONFIG_JSON"
    echo "- JWT_SECRET_KEY"
    echo "- OCR_SPACE_API_KEY"
    echo "- COHERE_API_KEY"
    echo "- CORS_ORIGINS"
    exit 1
fi

echo "✅ Environment file found"
echo ""

# Check if requirements.txt exists
if [ ! -f "backend/requirements.txt" ]; then
    echo "❌ Error: backend/requirements.txt not found!"
    exit 1
fi

echo "✅ Requirements file found"
echo ""

# Check if main.py exists
if [ ! -f "backend/app/main.py" ]; then
    echo "❌ Error: backend/app/main.py not found!"
    exit 1
fi

echo "✅ Main application file found"
echo ""

echo "📋 Deployment Checklist:"
echo "1. ✅ Environment variables configured"
echo "2. ✅ Dependencies listed in requirements.txt"
echo "3. ✅ Application code ready"
echo ""
echo "🎯 Next Steps for Render Deployment:"
echo ""
echo "1. Go to https://render.com and sign up/login"
echo "2. Click 'New +' and select 'Web Service'"
echo "3. Connect your GitHub repository"
echo "4. Configure the service:"
echo "   - Name: insightlens-backend"
echo "   - Environment: Python 3"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: uvicorn app.main:app --host 0.0.0.0 --port \$PORT"
echo "   - Root Directory: backend"
echo ""
echo "5. Add Environment Variables in Render dashboard:"
echo "   - OCR_SPACE_API_KEY"
echo "   - COHERE_API_KEY"
echo "   - FIREBASE_CONFIG_JSON"
echo "   - JWT_SECRET_KEY"
echo "   - CORS_ORIGINS (update with your frontend URL after deployment)"
echo ""
echo "6. Click 'Create Web Service'"
echo ""
echo "🔗 Your backend will be available at: https://your-service-name.onrender.com"
echo ""
echo "📝 Note: Update CORS_ORIGINS with your frontend URL after frontend deployment"
echo ""
echo "✅ Backend deployment preparation complete!"
