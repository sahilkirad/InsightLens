@echo off
REM InsightLens Quick Start Script for Windows
REM This script helps you set up and run the InsightLens application

echo 🚀 Welcome to InsightLens Setup!
echo ==================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16 or higher.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed!

REM Backend setup
echo.
echo 🔧 Setting up Backend...
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  Please create a .env file with your API credentials:
    echo    Copy env.example to .env and fill in your API keys
    echo    Required: OCR_SPACE_API_KEY, HUGGING_FACE_API_TOKEN, FIREBASE_CONFIG_JSON
)

cd ..

REM Frontend setup
echo.
echo 🎨 Setting up Frontend...
cd frontend

REM Install dependencies
echo Installing Node.js dependencies...
npm install

cd ..

echo.
echo 🎉 Setup complete!
echo.
echo 📋 Next steps:
echo 1. Configure your API keys in backend\.env
echo 2. Start the backend: cd backend ^&^& venv\Scripts\activate ^&^& uvicorn app.main:app --reload
echo 3. Start the frontend: cd frontend ^&^& npm run dev
echo 4. Open http://localhost:5173 in your browser
echo.
echo 📚 For detailed instructions, see setup.md
pause 