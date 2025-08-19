#!/bin/bash

# InsightLens Frontend Deployment Script for Vercel
# This script helps prepare and deploy the frontend to Vercel

echo "🎨 InsightLens Frontend Deployment to Vercel"
echo "============================================="

# Check if package.json exists
if [ ! -f "frontend/package.json" ]; then
    echo "❌ Error: frontend/package.json not found!"
    exit 1
fi

echo "✅ Package.json found"
echo ""

# Check if .env file exists
if [ ! -f "frontend/.env" ]; then
    echo "⚠️  Warning: frontend/.env file not found!"
    echo "Creating default .env file..."
    echo "VITE_API_URL=http://localhost:8000" > frontend/.env
    echo "✅ Created frontend/.env with default localhost URL"
    echo "📝 Remember to update VITE_API_URL with your backend URL after deployment"
else
    echo "✅ Frontend environment file found"
fi

echo ""

# Check if vercel.json exists
if [ ! -f "frontend/vercel.json" ]; then
    echo "❌ Error: frontend/vercel.json not found!"
    exit 1
fi

echo "✅ Vercel configuration found"
echo ""

# Check if main React files exist
if [ ! -f "frontend/src/App.jsx" ]; then
    echo "❌ Error: frontend/src/App.jsx not found!"
    exit 1
fi

echo "✅ Main React application found"
echo ""

echo "📋 Deployment Checklist:"
echo "1. ✅ Package.json configured"
echo "2. ✅ Environment variables set"
echo "3. ✅ Vercel configuration ready"
echo "4. ✅ React application code ready"
echo ""
echo "🎯 Next Steps for Vercel Deployment:"
echo ""
echo "1. Go to https://vercel.com and sign up/login"
echo "2. Click 'New Project'"
echo "3. Import your GitHub repository"
echo "4. Configure the project:"
echo "   - Framework Preset: Vite"
echo "   - Root Directory: frontend"
echo "   - Build Command: npm run build"
echo "   - Output Directory: dist"
echo ""
echo "5. Add Environment Variables in Vercel dashboard:"
echo "   - VITE_API_URL (set to your Render backend URL)"
echo ""
echo "6. Click 'Deploy'"
echo ""
echo "🔗 Your frontend will be available at: https://your-project-name.vercel.app"
echo ""
echo "📝 Important: Update VITE_API_URL with your backend URL after backend deployment"
echo ""
echo "✅ Frontend deployment preparation complete!"
