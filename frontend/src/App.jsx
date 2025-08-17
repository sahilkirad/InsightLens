import React, { useState, useEffect } from 'react'
import Header from './components/Header'
import ImageUpload from './components/ImageUpload'
import TextDisplay from './components/TextDisplay'
import AnalysisDashboard from './components/AnalysisDashboard'
import Login from './components/Login'
import Register from './components/Register'
import ForgotPassword from './components/ForgotPassword'
import ResetPassword from './components/ResetPassword'
import UserDashboard from './components/UserDashboard'
import { InsightLensProvider } from './contexts/InsightLensContext'
import { authAPI } from './services/api'
import './App.css'

function App() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('authToken'));
  const [showLogin, setShowLogin] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [showForgotPassword, setShowForgotPassword] = useState(false);
  const [showResetPassword, setShowResetPassword] = useState(false);
  const [showDashboard, setShowDashboard] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Check if user is already logged in
    if (token) {
      checkAuthStatus();
    }
    
    // Check for reset password URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const resetToken = urlParams.get('token');
    const resetEmail = urlParams.get('email');
    
    if (resetToken && resetEmail) {
      setShowResetPassword(true);
    }
  }, [token]);

  const checkAuthStatus = async () => {
    try {
      const userData = await authAPI.getCurrentUser();
      setUser(userData);
    } catch (error) {
      console.error('Auth check failed:', error);
      logout();
    }
  };

  const handleLogin = async (credentials) => {
    setIsLoading(true);
    try {
      const response = await authAPI.login(credentials);
      localStorage.setItem('authToken', response.access_token);
      setToken(response.access_token);
      setUser(response.user);
      setShowLogin(false);
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Login failed');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegister = async (userData) => {
    setIsLoading(true);
    try {
      await authAPI.register(userData);
      // After successful registration, log them in
      await handleLogin({
        email: userData.email,
        password: userData.password
      });
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Registration failed');
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    setToken(null);
    setUser(null);
    setShowDashboard(false);
  };

  return (
    <InsightLensProvider>
      {/* Show authentication screens if not logged in */}
      {!user ? (
        <>
          {showResetPassword ? (
            <ResetPassword
              onBackToLogin={() => {
                setShowResetPassword(false);
                setShowLogin(false);
                // Clear URL parameters
                window.history.replaceState({}, document.title, window.location.pathname);
              }}
            />
          ) : showForgotPassword ? (
            <ForgotPassword
              onBackToLogin={() => setShowForgotPassword(false)}
            />
          ) : showRegister ? (
            <Register
              onRegister={handleRegister}
              onSwitchToLogin={() => setShowRegister(false)}
              isLoading={isLoading}
            />
          ) : (
            <Login
              onLogin={handleLogin}
              onSwitchToRegister={() => setShowRegister(true)}
              onForgotPassword={() => setShowForgotPassword(true)}
              isLoading={isLoading}
            />
          )}
        </>
      ) : (
        /* Show user dashboard if requested */
        showDashboard ? (
          <>
            {console.log('🔍 Passing user to UserDashboard:', user)}
            <UserDashboard
              user={user}
              onLogout={logout}
              token={token}
              onBackToApp={() => setShowDashboard(false)}
            />
          </>
        ) : (
          /* Show main application */
          <div className="min-h-screen bg-gray-50">
            <Header 
              user={user}
              onLogout={logout}
              onShowDashboard={() => setShowDashboard(true)}
              showDashboard={showDashboard}
            />
            <main className="container mx-auto px-4 py-8">
              <div className="max-w-7xl mx-auto">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  {/* Left Column - Image Upload and Preview */}
                  <div className="space-y-6">
                    <ImageUpload />
                  </div>
                  
                  {/* Right Column - Text Display and Analysis */}
                  <div className="space-y-6">
                    <TextDisplay />
                    <AnalysisDashboard />
                  </div>
                </div>
              </div>
            </main>
            {/* Features Section */}
            <section id="features" className="bg-white border-t border-gray-200 py-12 px-4">
              <div className="max-w-4xl mx-auto">
                <h2 className="text-2xl font-bold text-primary-700 mb-4">Features</h2>
                <ul className="list-disc pl-6 space-y-2 text-gray-800">
                  <li><strong>Image Upload & OCR:</strong> Upload images via drag-and-drop. Extracts text using advanced OCR (Optical Character Recognition) technology.</li>
                  <li><strong>Text Preview:</strong> Instantly preview extracted text, with options to copy or analyze.</li>
                  <li><strong>AI-Powered Analysis:</strong> Summarize, analyze sentiment, or ask questions about the extracted text using Cohere AI.</li>
                  <li><strong>Custom Prompts:</strong> Guide the summarization and Q&A with your own prompts for more relevant, tailored results.</li>
                  <li><strong>Analysis Dashboard:</strong> View all your analysis results in a clean, organized dashboard. Each result is timestamped and easy to copy.</li>
                  <li><strong>Modern UI:</strong> Responsive, user-friendly interface built with React, Vite, and Tailwind CSS.</li>
                  <li><strong>Secure & Private:</strong> No images are stored. Only extracted text and analysis results are saved securely in Firestore for your session.</li>
                  <li><strong>Open Source:</strong> View and contribute to the project on <a href="https://github.com/sahilkirad" className="text-primary-600 underline" target="_blank" rel="noopener noreferrer">GitHub</a>.</li>
                </ul>
              </div>
            </section>
            {/* About Section */}
            <section id="about" className="bg-gray-100 border-t border-gray-200 py-12 px-4">
              <div className="max-w-4xl mx-auto">
                <h2 className="text-2xl font-bold text-primary-700 mb-4">About InsightLens</h2>
                <p className="text-gray-800 mb-4">
                  <strong>InsightLens</strong> is a full-stack web application designed to make information extraction and analysis from images effortless. Whether you're a student, researcher, or professional, InsightLens helps you turn images into actionable insights using cutting-edge AI.
                </p>
                <p className="text-gray-800 mb-4">
                  The app leverages OCR.space for high-accuracy text extraction and Cohere AI for summarization, sentiment analysis, and question answering. All your data is managed securely using Google Firebase Firestore.
                </p>
                <p className="text-gray-800 mb-4">
                  <strong>Key Use Cases:</strong>
                </p>
                <ul className="list-disc pl-6 space-y-2 text-gray-800 mb-4">
                  <li>Extracting and summarizing notes from handwritten or printed documents.</li>
                  <li>Analyzing the sentiment of text in posters, flyers, or screenshots.</li>
                  <li>Quickly answering questions about the content of technical diagrams or reports.</li>
                  <li>Digitizing and organizing information from books, receipts, or whiteboards.</li>
                </ul>
                <p className="text-gray-800">
                  <strong>Built by <a href="https://github.com/sahilkirad" className="text-primary-600 underline" target="_blank" rel="noopener noreferrer">@sahilkirad</a></strong> using modern, free-tier technologies. Contributions and feedback are welcome!
                </p>
              </div>
            </section>
          </div>
        )
      )}
    </InsightLensProvider>
  )
}

export default App 