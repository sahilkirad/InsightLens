import React, { useState } from 'react'
import { Brain, MessageSquare, TrendingUp, Search, Send, AlertCircle } from 'lucide-react'
import { useInsightLens } from '../contexts/InsightLensContext'
import { analysisAPI, handleAPIError } from '../services/api'
import AnalysisResult from './AnalysisResult'

const AnalysisDashboard = () => {
  const { state, actions } = useInsightLens()
  const { extractedText, isAnalyzing, analysisResults } = state
  const [question, setQuestion] = useState('')
  const [summaryPrompt, setSummaryPrompt] = useState('')

  const handleAnalysis = async (analysisType, prompt = null) => {
    if (!extractedText) {
      actions.setError('Please extract text from an image first')
      return
    }

    try {
      actions.setAnalyzing(true)
      actions.clearError()

      const response = await analysisAPI.analyzeText({
        text: extractedText,
        analysis_type: analysisType,
        ...(prompt && { prompt })
      })

      if (response.success) {
        actions.addAnalysisResult({
          id: Date.now(),
          type: analysisType,
          result: response.result,
          timestamp: new Date().toISOString(),
          prompt: prompt
        })
      } else {
        actions.setError(response.message || 'Analysis failed')
      }
    } catch (error) {
      const errorInfo = handleAPIError(error)
      console.error('Analysis error details:', errorInfo)
      
      // Provide more specific error messages
      let errorMessage = errorInfo.message
      if (errorInfo.status === 422) {
        errorMessage = 'Analysis failed: Invalid input or model error. Please try again.'
      } else if (errorInfo.status === 400) {
        errorMessage = 'Analysis failed: Please check your input and try again.'
      } else if (errorInfo.status === 0) {
        errorMessage = 'Network error: Please check your connection and try again.'
      }
      
      actions.setError(errorMessage)
    } finally {
      actions.setAnalyzing(false)
    }
  }

  const handleQuestionSubmit = (e) => {
    e.preventDefault()
    if (question.trim()) {
      handleAnalysis('question', question.trim())
      setQuestion('')
    }
  }

  // Remove summarize tool from analysisTools, handle it separately
  const analysisTools = [
    {
      type: 'sentiment',
      name: 'Analyze Sentiment',
      description: 'Check emotional tone',
      icon: MessageSquare,
      color: 'bg-green-500',
      action: () => handleAnalysis('sentiment')
    }
  ]

  if (!extractedText) {
    return (
      <div className="card">
        <div className="text-center py-12">
          <Brain className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Analysis Dashboard
          </h3>
          <p className="text-gray-500">
            Extract text from an image to start analyzing
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Analysis Tools */}
      <div className="card">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Analysis Tools
        </h2>

        {/* Summarize Text Tool with Prompt */}
        <div className="mb-6">
          <div className="flex items-center mb-2">
            <div className="w-10 h-10 rounded-lg flex items-center justify-center bg-blue-500 mr-3">
              <TrendingUp className="w-5 h-5 text-white" />
            </div>
            <div className="text-left">
              <h3 className="font-medium text-gray-900">Summarize Text</h3>
              <p className="text-sm text-gray-600">Generate a concise summary</p>
            </div>
          </div>
          <div className="flex flex-col md:flex-row gap-2">
            <input
              type="text"
              value={summaryPrompt}
              onChange={e => setSummaryPrompt(e.target.value)}
              placeholder="Enter a prompt to guide the summary (optional)"
              disabled={isAnalyzing}
              className="flex-1 input-field"
            />
            <button
              onClick={() => handleAnalysis('summarize', summaryPrompt.trim() || null)}
              disabled={isAnalyzing}
              className="btn-primary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <TrendingUp className="w-4 h-4" />
              <span>Summarize</span>
            </button>
          </div>
        </div>

        {/* Other Analysis Tools */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          {analysisTools.map((tool) => (
            <button
              key={tool.type}
              onClick={tool.action}
              disabled={isAnalyzing}
              className={`
                flex items-center space-x-3 p-4 rounded-lg border border-gray-200 hover:border-primary-300 hover:bg-primary-50 transition-all duration-200
                ${isAnalyzing ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
              `}
            >
              <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${tool.color}`}>
                <tool.icon className="w-5 h-5 text-white" />
              </div>
              <div className="text-left">
                <h3 className="font-medium text-gray-900">{tool.name}</h3>
                <p className="text-sm text-gray-600">{tool.description}</p>
              </div>
            </button>
          ))}
        </div>

        {/* Question Input */}
        <div className="space-y-3">
          <h3 className="font-medium text-gray-900">Ask a Question</h3>
          <form onSubmit={handleQuestionSubmit} className="flex space-x-2">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask a question about the text..."
              disabled={isAnalyzing}
              className="flex-1 input-field"
            />
            <button
              type="submit"
              disabled={isAnalyzing || !question.trim()}
              className="btn-primary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="w-4 h-4" />
              <span>Ask</span>
            </button>
          </form>
        </div>

        {/* Loading State */}
        {isAnalyzing && (
          <div className="flex items-center justify-center space-x-2 mt-4 p-4 bg-blue-50 rounded-lg">
            <div className="loading-spinner"></div>
            <span className="text-blue-700">Analyzing text...</span>
          </div>
        )}
      </div>

      {/* Analysis Results */}
      {analysisResults.length > 0 && (
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900">
              Analysis Results
            </h2>
            <button
              onClick={actions.clearAnalysisResults}
              className="text-sm text-gray-600 hover:text-red-600 transition-colors duration-200"
            >
              Clear All
            </button>
          </div>

          <div className="space-y-4">
            {analysisResults.map((result) => (
              <AnalysisResult key={result.id} result={result} />
            ))}
          </div>
        </div>
      )}

      {/* Error Display */}
      {state.error && (
        <div className="card border-red-200 bg-red-50">
          <div className="flex items-start space-x-3">
            <AlertCircle className="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" />
            <div className="flex-1">
              <h3 className="text-sm font-medium text-red-800">Analysis Error</h3>
              <p className="text-sm text-red-700 mt-1">{state.error}</p>
              
              {/* Helpful tips for insufficient text */}
              {(state.error.includes('insufficient') || 
                state.error.includes('Insufficient') || 
                state.error.includes('meaningful content') ||
                state.error.includes('readable text')) && (
                <div className="mt-3 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                  <div className="flex items-start space-x-2">
                    <div className="text-blue-600 text-sm">💡</div>
                    <div className="text-sm text-blue-800">
                      <strong>Tip:</strong> Make sure your image contains clear, readable text. The AI can only analyze what it can extract from the image. Try:
                      <ul className="mt-1 ml-4 list-disc space-y-1">
                        <li>Using a higher resolution image</li>
                        <li>Ensuring good lighting and contrast</li>
                        <li>Making sure text is clearly visible and not blurry</li>
                        <li>Avoiding handwritten text if possible</li>
                      </ul>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default AnalysisDashboard 