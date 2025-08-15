# Firebase Setup Guide for InsightLens

## 🔥 **Step 1: Create a Firebase Project**

1. **Go to Firebase Console**: Visit [https://console.firebase.google.com/](https://console.firebase.google.com/)
2. **Create New Project**: Click "Create a project" or "Add project"
3. **Enter Project Name**: Give your project a name (e.g., "insightlens-app")
4. **Choose Google Analytics** (optional): You can disable this for now
5. **Create Project**: Click "Create project"

## 🔥 **Step 2: Set Up Firestore Database**

1. **Navigate to Firestore**: In your Firebase project, click "Firestore Database" in the left sidebar
2. **Create Database**: Click "Create database"
3. **Choose Security Rules**: Select "Start in test mode" (we'll secure it later)
4. **Choose Location**: Select a location close to your users
5. **Create**: Click "Create database"

## 🔥 **Step 3: Get Service Account Credentials**

1. **Go to Project Settings**: Click the gear icon ⚙️ next to "Project Overview"
2. **Service Accounts Tab**: Click on "Service accounts" tab
3. **Generate New Private Key**: Click "Generate new private key"
4. **Download JSON**: Save the JSON file securely (this contains your credentials)

## 🔥 **Step 4: Configure Your Backend**

### Option A: Using JSON File (Recommended)

1. **Copy the JSON content** from the downloaded service account file
2. **Add to your `.env` file** in the backend directory:

```env
# Firebase Configuration
FIREBASE_CONFIG_JSON={"type":"service_account","project_id":"your-project-id","private_key_id":"...","private_key":"-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n","client_email":"firebase-adminsdk-xxxxx@your-project.iam.gserviceaccount.com","client_id":"123456789","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xxxxx%40your-project.iam.gserviceaccount.com"}

# Other configurations
HUGGING_FACE_API_TOKEN=your_token_here
OCR_SPACE_API_KEY=your_key_here
CORS_ORIGINS=http://localhost:5173
```

### Option B: Using Individual Environment Variables

```env
# Firebase Configuration
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY_ID=your_private_key_id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@your-project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your_client_id
FIREBASE_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xxxxx%40your-project.iam.gserviceaccount.com

# Other configurations
HUGGING_FACE_API_TOKEN=your_token_here
OCR_SPACE_API_KEY=your_key_here
CORS_ORIGINS=http://localhost:5173
```

## 🔥 **Step 5: View Your Data in Firebase Console**

### **Access Your Database**

1. **Firebase Console**: Go to [https://console.firebase.google.com/](https://console.firebase.google.com/)
2. **Select Your Project**: Choose your InsightLens project
3. **Firestore Database**: Click "Firestore Database" in the left sidebar

### **Data Structure**

Your data will be stored in the following structure:

```
📁 Collection: "extractions"
    📄 Document ID (auto-generated)
        ├── created_at: timestamp
        ├── image_url: string (optional)
        ├── extracted_text: string
        └── analyses: array
            ├── type: string (summarize/sentiment/question)
            ├── result: object
            ├── timestamp: timestamp
            └── prompt: string (optional)
```

### **What You'll See**

- **Documents**: Each text extraction creates a new document
- **Fields**: 
  - `created_at`: When the text was extracted
  - `extracted_text`: The cleaned text from the image
  - `analyses`: Array of analysis results (summaries, sentiment, Q&A)
- **Real-time Updates**: Data appears immediately when you upload images

## 🔥 **Step 6: Test the Setup**

1. **Start your backend**: `python -m uvicorn app.main:app --reload`
2. **Upload an image** through your frontend
3. **Check Firebase Console**: You should see a new document appear
4. **Run analysis**: Use the analysis tools and see results stored in the `analyses` array

## 🔥 **Step 7: Security Rules (Optional)**

For production, you should secure your Firestore database:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /extractions/{document} {
      allow read, write: if request.auth != null;
    }
  }
}
```

## 🔥 **Troubleshooting**

### **Common Issues**

1. **"Firebase not initialized"**: Check your environment variables
2. **"Permission denied"**: Verify your service account has proper permissions
3. **"No data appearing"**: Check the backend logs for Firebase connection errors

### **Debug Steps**

1. **Check Backend Logs**: Look for Firebase initialization messages
2. **Verify Environment Variables**: Make sure all Firebase config is set
3. **Test Connection**: The backend will print "Firebase initialized successfully" if working

### **Development Mode**

If Firebase is not configured, the app will run in development mode:
- Text extraction will work
- Analysis will work
- Data won't be stored (you'll see "Firestore is disabled" messages)

## 🔥 **Next Steps**

Once Firebase is working:
1. **Monitor Usage**: Check Firebase Console for data growth
2. **Set Up Backups**: Configure automated backups
3. **Add Authentication**: Implement user authentication
4. **Scale Up**: Consider upgrading Firebase plan for more usage

Your data will now be stored and viewable in the Firebase Console! 🎉
