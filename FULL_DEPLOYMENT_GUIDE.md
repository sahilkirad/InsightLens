# 🚀 InsightLens Full Advanced Deployment Guide

Complete step-by-step guide to deploy InsightLens with full authentication and user management.

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] **GitHub Account** with your code pushed to a repository
- [ ] **Vercel Account** (free tier available)
- [ ] **Render Account** (free tier available)
- [ ] **Firebase Project** with Firestore enabled
- [ ] **API Keys**:
  - [ ] OCR.space API key
  - [ ] Cohere API key
  - [ ] Firebase service account JSON

## 🔧 Step 1: Environment Setup

### 1.1 Backend Environment Variables

Create `backend/.env` file with your actual API keys:

```env
# Firebase Configuration
FIREBASE_CONFIG_JSON={"type":"service_account","project_id":"your-actual-project-id","private_key_id":"your-actual-key-id","private_key":"-----BEGIN PRIVATE KEY-----\nyour-actual-private-key\n-----END PRIVATE KEY-----\n","client_email":"your-actual-service-account@your-project.iam.gserviceaccount.com","client_id":"your-actual-client-id","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"}

# JWT Configuration
JWT_SECRET_KEY=your-super-secure-jwt-secret-key-at-least-32-characters-long

# API Keys
OCR_SPACE_API_KEY=your-actual-ocr-space-api-key
COHERE_API_KEY=your-actual-cohere-api-key

# CORS Configuration
CORS_ORIGINS=http://localhost:5173,https://your-frontend-domain.vercel.app

# Email Configuration (for password reset)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@insightlens.com
FRONTEND_URL=http://localhost:5173
```

### 1.2 Frontend Environment Variables

Create `frontend/.env` file:

```env
VITE_API_URL=http://localhost:8000
```

## 🚀 Step 2: Backend Deployment (Render)

### 2.1 Deploy to Render

1. **Go to Render Dashboard**
   - Visit [render.com](https://render.com)
   - Sign up/login to your account

2. **Create New Web Service**
   - Click "New +" button
   - Select "Web Service"
   - Connect your GitHub repository

3. **Configure Service Settings**
   - **Name**: `insightlens-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `backend`

4. **Add Environment Variables**
   In Render dashboard, add these environment variables:
   - `OCR_SPACE_API_KEY` = your OCR.space API key
   - `COHERE_API_KEY` = your Cohere API key
   - `FIREBASE_CONFIG_JSON` = your complete Firebase service account JSON
   - `JWT_SECRET_KEY` = your secure JWT secret key
   - `CORS_ORIGINS` = `http://localhost:5173,https://your-frontend-domain.vercel.app`
   - `SMTP_SERVER` = `smtp.gmail.com`
   - `SMTP_PORT` = `587`
   - `SMTP_USERNAME` = your email
   - `SMTP_PASSWORD` = your app password
   - `FROM_EMAIL` = `noreply@insightlens.com`
   - `FRONTEND_URL` = `http://localhost:5173`

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Note your backend URL: `https://your-service-name.onrender.com`

### 2.2 Verify Backend Deployment

1. **Test Health Check**
   - Visit: `https://your-backend-url.onrender.com/health`
   - Should return: `{"status": "healthy", "service": "InsightLens API"}`

2. **Test API Documentation**
   - Visit: `https://your-backend-url.onrender.com/docs`
   - Should show FastAPI Swagger documentation

## 🎨 Step 3: Frontend Deployment (Vercel)

### 3.1 Deploy to Vercel

1. **Go to Vercel Dashboard**
   - Visit [vercel.com](https://vercel.com)
   - Sign up/login to your account

2. **Create New Project**
   - Click "New Project"
   - Import your GitHub repository

3. **Configure Project Settings**
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

4. **Add Environment Variables**
   In Vercel dashboard, add:
   - `VITE_API_URL` = `https://your-backend-url.onrender.com`

5. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - Note your frontend URL: `https://your-project-name.vercel.app`

### 3.2 Verify Frontend Deployment

1. **Test Frontend**
   - Visit your Vercel URL
   - Should load the InsightLens application
   - Check that the UI loads properly

## 🔄 Step 4: Update CORS Configuration

After both deployments are complete:

1. **Go back to Render Dashboard**
2. **Update CORS_ORIGINS**
   - Find your backend service
   - Go to Environment variables
   - Update `CORS_ORIGINS` to: `https://your-frontend-url.vercel.app`
3. **Redeploy Backend**
   - Click "Manual Deploy" to apply changes

## 🧪 Step 5: Test Complete System

### 5.1 Test User Registration
1. Visit your frontend URL
2. Click "Sign up here" on login page
3. Create a new account with valid email and password
4. Verify successful registration and automatic login

### 5.2 Test Core Features
1. **Image Upload & Text Extraction**
   - Upload an image
   - Verify text extraction works
   - Check extracted text appears

2. **AI Analysis**
   - Perform summarization
   - Test sentiment analysis
   - Try Q&A functionality

3. **User Dashboard**
   - Click "My Data" in header
   - Verify extraction history appears
   - Test copy and delete functions

### 5.3 Test Authentication Flow
1. **Logout and Login**
   - Logout from application
   - Login with credentials
   - Verify token persistence

2. **Password Reset** (if email configured)
   - Test forgot password flow
   - Verify email functionality

## 🔍 Step 6: Monitoring & Debugging

### 6.1 Backend Monitoring (Render)
- Check Render dashboard for deployment logs
- Monitor API request/response logs
- Verify database connections
- Check authentication flow logs

### 6.2 Frontend Monitoring (Vercel)
- Check Vercel dashboard for build logs
- Monitor deployment status
- Check for any build errors

### 6.3 Common Issues & Solutions

#### CORS Errors
- **Symptom**: Browser console shows CORS errors
- **Solution**: Verify CORS_ORIGINS includes your frontend URL

#### Authentication Issues
- **Symptom**: Login/registration fails
- **Solution**: Check Firebase configuration and JWT_SECRET_KEY

#### API Key Errors
- **Symptom**: Text extraction or analysis fails
- **Solution**: Verify OCR_SPACE_API_KEY and COHERE_API_KEY

#### Database Issues
- **Symptom**: Data not saving or loading
- **Solution**: Check Firebase service account JSON and permissions

## 📊 Step 7: Performance Optimization

### 7.1 Backend Optimizations
- Monitor API response times
- Check database query performance
- Implement caching if needed

### 7.2 Frontend Optimizations
- Monitor bundle size
- Check loading performance
- Optimize images and assets

## 🔒 Step 8: Security Review

### 8.1 Security Checklist
- [ ] Environment variables are not exposed in code
- [ ] CORS is properly configured
- [ ] JWT tokens are secure
- [ ] API keys are protected
- [ ] HTTPS is enabled (automatic with Vercel/Render)

### 8.2 Security Best Practices
- Regularly rotate API keys
- Monitor for suspicious activity
- Keep dependencies updated
- Use strong JWT secrets

## 📈 Step 9: Production Readiness

### 9.1 Monitoring Setup
- Set up error tracking (optional)
- Monitor API usage and costs
- Set up alerts for downtime

### 9.2 Backup Strategy
- Ensure code is backed up in Git
- Regular database backups
- Environment variable backups

### 9.3 Scaling Considerations
- Monitor resource usage
- Plan for increased traffic
- Consider paid plans if needed

## 🎉 Deployment Complete!

Your InsightLens application is now fully deployed with:

✅ **Secure Authentication System**
✅ **User Data Management**
✅ **Image Upload & OCR**
✅ **AI-Powered Analysis**
✅ **Modern Responsive UI**
✅ **Production-Ready Infrastructure**

### Your Application URLs:
- **Frontend**: `https://your-project-name.vercel.app`
- **Backend**: `https://your-service-name.onrender.com`
- **API Docs**: `https://your-service-name.onrender.com/docs`

### Next Steps:
1. **Share your application** with users
2. **Monitor performance** and usage
3. **Gather feedback** and iterate
4. **Scale as needed**

## 🆘 Support & Troubleshooting

If you encounter issues:

1. **Check deployment logs** in Render/Vercel dashboards
2. **Verify environment variables** are set correctly
3. **Test API endpoints** using the Swagger documentation
4. **Check browser console** for frontend errors
5. **Review this guide** for common solutions

---

**Congratulations! 🎉 Your InsightLens application is now live and ready for users!**
