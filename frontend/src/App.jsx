import React, { useState, createContext } from 'react'
import Header from './components/Header'
import ImageUpload from './components/ImageUpload'
import TextDisplay from './components/TextDisplay'
import AnalysisDashboard from './components/AnalysisDashboard'
import { InsightLensProvider } from './contexts/InsightLensContext'
import './App.css'

function App() {
  return (
    <InsightLensProvider>
      <div className="min-h-screen bg-gray-50">
        <Header />
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
    </InsightLensProvider>
  )
}

export default App 