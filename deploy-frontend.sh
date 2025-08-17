#!/bin/bash

# InsightLens Frontend Deployment Script
# This script helps prepare and deploy the frontend to Vercel

echo "🚀 Starting InsightLens Frontend Deployment..."

# Check if we're in the right directory
if [ ! -f "frontend/package.json" ]; then
    echo "❌ Error: package.json not found. Make sure you're in the project root directory."
    exit 1
fi

# Check if .env file exists
if [ ! -f "frontend/.env" ]; then
    echo "⚠️  Warning: .env file not found in frontend directory."
    echo "Please create frontend/.env with the following variables:"
    echo "  VITE_API_URL=https://your-backend-domain.onrender.com"
    echo ""
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Install dependencies
echo "📦 Installing Node.js dependencies..."
cd frontend
npm install

# Check if build works
echo "🔨 Testing build process..."
npm run build

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
else
    echo "❌ Build failed. Please fix the errors and try again."
    exit 1
fi

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

echo "✅ Frontend is ready for deployment!"
echo ""
echo "📋 Next steps:"
echo "1. Push your code to GitHub"
echo "2. Go to vercel.com and create a new project"
echo "3. Import your GitHub repository"
echo "4. Set the following configuration:"
echo "   - Framework Preset: Vite"
echo "   - Root Directory: frontend"
echo "   - Build Command: npm run build"
echo "   - Output Directory: dist"
echo "5. Add your environment variables in Vercel dashboard:"
echo "   - VITE_API_URL=https://your-backend-domain.onrender.com"
echo "6. Deploy!"
echo ""
echo "🔗 Your frontend will be available at: https://your-app-name.vercel.app"
echo ""
echo "💡 Alternative: Use Vercel CLI for direct deployment:"
echo "   cd frontend && vercel"
