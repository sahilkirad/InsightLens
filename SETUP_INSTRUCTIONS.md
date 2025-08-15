# InsightLens Setup Instructions

## Prerequisites

1. **Python 3.8+** for the backend
2. **Node.js 16+** for the frontend
3. **API Keys** (see below)

## Required API Keys

### 1. Hugging Face API Token
- Go to [Hugging Face](https://huggingface.co/settings/tokens)
- Create a new token
- Add it to your environment variables

### 2. OCR.space API Key (Optional for testing)
- Go to [OCR.space](https://ocr.space/ocrapi)
- Get a free API key
- Add it to your environment variables

## Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd InsightLens/backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the backend directory:
   ```env
   HUGGING_FACE_API_TOKEN=your_token_here
   OCR_SPACE_API_KEY=your_key_here
   CORS_ORIGINS=http://localhost:5173
   ```

6. Start the backend server:
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd InsightLens/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file in the frontend directory:
   ```env
   VITE_API_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

## Usage

1. Open your browser and go to `http://localhost:5173`
2. Upload an image containing text
3. Use the analysis tools to:
   - Summarize the extracted text
   - Analyze sentiment
   - Ask questions about the content

## Troubleshooting

### Common Issues

1. **422 Validation Error**: Make sure your API keys are properly set
2. **OCR Not Working**: Check your OCR.space API key
3. **Sentiment Analysis Failing**: Verify your Hugging Face API token
4. **Frontend Not Loading**: Ensure the backend is running on port 8000

### Development Mode

The application can run in development mode without API keys, but with limited functionality:
- OCR will show demo responses
- AI analysis will show placeholder results

## API Endpoints

- `GET /` - Health check
- `POST /api/extract-text` - Extract text from image
- `POST /api/analyze` - Analyze text
- `GET /api/analysis-types` - Get available analysis types
- `GET /health` - Service health check
