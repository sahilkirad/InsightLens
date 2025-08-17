# InsightLens Deployment Guide

This guide will help you deploy the InsightLens application to production.

## Prerequisites

Before deploying, ensure you have:

1. **GitHub Account** - Your code should be in a GitHub repository
2. **Vercel Account** - For frontend deployment (free tier available)
3. **Render Account** - For backend deployment (free tier available)
4. **API Keys**:
   - OCR.space API key
   - Cohere API key
   - Firebase service account JSON

## Step 1: Prepare Your Repository

### 1.1 Update .gitignore
Ensure your `.gitignore` file excludes sensitive files:

```
node_modules/
frontend/node_modules/
.env
*.pyc
__pycache__/
venv/
.DS_Store
```

### 1.2 Environment Variables Setup

#### Backend Environment Variables
Create a `.env` file in the backend directory (DO NOT commit this file):

```env
OCR_SPACE_API_KEY=your_ocr_space_api_key
COHERE_API_KEY=your_cohere_api_key
FIREBASE_CONFIG_JSON={"type": "service_account", ...}
CORS_ORIGINS=https://your-frontend-domain.vercel.app
```

#### Frontend Environment Variables
Create a `.env` file in the frontend directory (DO NOT commit this file):

```env
VITE_API_URL=https://your-backend-domain.onrender.com
```

## Step 2: Deploy Backend to Render

### 2.1 Connect to Render
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository

### 2.2 Configure Backend Service
- **Name**: `insightlens-backend`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Root Directory**: `backend` (if your repo structure has backend in a subdirectory)

### 2.3 Add Environment Variables
In Render dashboard, add these environment variables:
- `OCR_SPACE_API_KEY`
- `COHERE_API_KEY`
- `FIREBASE_CONFIG_JSON`
- `CORS_ORIGINS` (set to your frontend URL once deployed)

### 2.4 Deploy
Click "Create Web Service" and wait for deployment to complete.

## Step 3: Deploy Frontend to Vercel

### 3.1 Connect to Vercel
1. Go to [vercel.com](https://vercel.com) and sign up/login
2. Click "New Project"
3. Import your GitHub repository

### 3.2 Configure Frontend Project
- **Framework Preset**: `Vite`
- **Root Directory**: `frontend` (if your repo structure has frontend in a subdirectory)
- **Build Command**: `npm run build`
- **Output Directory**: `dist`

### 3.3 Add Environment Variables
In Vercel dashboard, add:
- `VITE_API_URL` (set to your Render backend URL)

### 3.4 Deploy
Click "Deploy" and wait for deployment to complete.

## Step 4: Update CORS Configuration

After both deployments are complete:

1. Go back to your Render backend service
2. Update the `CORS_ORIGINS` environment variable to include your Vercel frontend URL
3. Redeploy the backend service

## Step 5: Test Your Deployment

1. Visit your Vercel frontend URL
2. Upload an image and test text extraction
3. Test AI analysis features
4. Check that data is being saved to Firebase

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure `CORS_ORIGINS` includes your frontend URL
2. **API Key Errors**: Verify all environment variables are set correctly
3. **Build Failures**: Check that all dependencies are in requirements.txt
4. **Firebase Connection**: Ensure Firebase service account JSON is properly formatted

### Debugging

- Check Render logs for backend issues
- Check Vercel build logs for frontend issues
- Use browser developer tools to debug API calls

## Alternative Deployment Options

### Backend Alternatives
- **Railway**: Similar to Render, good for Python apps
- **Heroku**: More established platform (paid)
- **DigitalOcean App Platform**: Good for scaling

### Frontend Alternatives
- **Netlify**: Similar to Vercel, great for static sites
- **GitHub Pages**: Free but limited features
- **Firebase Hosting**: Good if using other Firebase services

## Monitoring and Maintenance

1. **Set up monitoring**: Use Render's built-in monitoring
2. **Set up alerts**: Configure notifications for service downtime
3. **Regular updates**: Keep dependencies updated
4. **Backup strategy**: Ensure your code is backed up in Git

## Cost Considerations

- **Vercel**: Free tier includes 100GB bandwidth/month
- **Render**: Free tier includes 750 hours/month
- **API Costs**: Monitor usage of OCR.space and Cohere APIs

## Security Best Practices

1. **Environment Variables**: Never commit API keys to Git
2. **HTTPS**: Both Vercel and Render provide HTTPS by default
3. **CORS**: Restrict CORS origins to your frontend domain only
4. **Rate Limiting**: Consider implementing rate limiting for API endpoints
