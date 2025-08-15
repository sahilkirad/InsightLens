import React from 'react'
import { TrendingUp, MessageSquare, Search, Clock, Copy, Check } from 'lucide-react'

const AnalysisResult = ({ result }) => {
  const [copied, setCopied] = React.useState(false)

  const handleCopy = async (text) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (error) {
      console.error('Failed to copy text:', error)
    }
  }

  const getAnalysisIcon = (type) => {
    switch (type) {
      case 'summarize':
        return <TrendingUp className="w-5 h-5 text-blue-600" />
      case 'sentiment':
        return <MessageSquare className="w-5 h-5 text-green-600" />
      case 'question':
        return <Search className="w-5 h-5 text-purple-600" />
      default:
        return <TrendingUp className="w-5 h-5 text-gray-600" />
    }
  }

  const getAnalysisTitle = (type) => {
    switch (type) {
      case 'summarize':
        return 'Text Summary'
      case 'sentiment':
        return 'Sentiment Analysis'
      case 'question':
        return 'Question Answer'
      default:
        return 'Analysis Result'
    }
  }

  const getAnalysisColor = (type) => {
    switch (type) {
      case 'summarize':
        return 'border-blue-200 bg-blue-50'
      case 'sentiment':
        return 'border-green-200 bg-green-50'
      case 'question':
        return 'border-purple-200 bg-purple-50'
      default:
        return 'border-gray-200 bg-gray-50'
    }
  }

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString()
  }

  const renderResultContent = () => {
    switch (result.type) {
      case 'summarize':
        return (
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">
                Summary ({result.result.summary_length} characters)
              </span>
              <button
                onClick={() => handleCopy(result.result.summary)}
                className="flex items-center space-x-1 text-xs text-gray-500 hover:text-gray-700"
              >
                {copied ? (
                  <>
                    <Check className="w-3 h-3" />
                    <span>Copied!</span>
                  </>
                ) : (
                  <>
                    <Copy className="w-3 h-3" />
                    <span>Copy</span>
                  </>
                )}
              </button>
            </div>
            <p className="text-gray-900 leading-relaxed">
              {result.result.summary}
            </p>
            {result.result.confidence && (
              <div className="w-full bg-gray-200 rounded-full h-1.5">
                <div
                  className="bg-blue-500 h-1.5 rounded-full transition-all duration-300"
                  style={{ width: `${Math.min(result.result.confidence || 0, 100)}%` }}
                ></div>
              </div>
            )}
            <div className="flex items-center justify-between text-xs text-gray-500">
              <span>Original: {result.result.original_length} characters</span>
              <div className="flex items-center space-x-2">
                {result.result.confidence && (
                  <span>Confidence: {Math.min(result.result.confidence || 0, 100).toFixed(1)}%</span>
                )}
                {result.result.api_used && (
                  <span className="text-blue-600">via {result.result.api_used}</span>
                )}
              </div>
            </div>
          </div>
        )

      case 'sentiment':
        return (
          <div className="space-y-3">
            <div className="flex items-center space-x-3">
              <span className="text-3xl">{result.result.emoji}</span>
              <div className="flex-1">
                <div className="font-medium text-gray-900 capitalize">
                  {result.result.sentiment}
                </div>
                <div className="text-sm text-gray-600">
                  Confidence: {Math.min(result.result.confidence || 0, 100).toFixed(1)}%
                </div>
              </div>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className={`h-2 rounded-full transition-all duration-300 ${
                  result.result.sentiment === 'Positive' ? 'bg-green-500' :
                  result.result.sentiment === 'Negative' ? 'bg-red-500' : 'bg-yellow-500'
                }`}
                style={{ width: `${Math.min(result.result.confidence || 0, 100)}%` }}
              ></div>
            </div>
            {result.result.analysis && (
              <div className="text-xs text-gray-600 bg-gray-50 p-2 rounded">
                <strong>Analysis:</strong> {result.result.analysis}
              </div>
            )}
            {result.result.api_used && (
              <div className="text-xs text-blue-600 text-right">
                via {result.result.api_used}
              </div>
            )}
          </div>
        )

      case 'question':
        return (
          <div className="space-y-3">
            <div className="bg-gray-100 rounded-lg p-3">
              <div className="text-sm font-medium text-gray-700 mb-1">Question:</div>
              <div className="text-gray-900">{result.prompt}</div>
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700">Answer:</span>
                <button
                  onClick={() => handleCopy(result.result.answer)}
                  className="flex items-center space-x-1 text-xs text-gray-500 hover:text-gray-700"
                >
                  {copied ? (
                    <>
                      <Check className="w-3 h-3" />
                      <span>Copied!</span>
                    </>
                  ) : (
                    <>
                      <Copy className="w-3 h-3" />
                      <span>Copy</span>
                    </>
                  )}
                </button>
              </div>
              <p className="text-gray-900 leading-relaxed">
                {result.result.answer}
                {result.result.answer && result.result.answer.includes('[Based on extracted text]') && (
                  <span className="inline-block ml-2 px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">
                    📄 Extracted Text Only
                  </span>
                )}
              </p>
              <div className="space-y-2">
                <div className="w-full bg-gray-200 rounded-full h-1.5">
                  <div
                    className="bg-purple-500 h-1.5 rounded-full transition-all duration-300"
                    style={{ width: `${Math.min(result.result.confidence || 0, 100)}%` }}
                  ></div>
                </div>
                <div className="flex items-center justify-between text-xs text-gray-500">
                  <span>Confidence: {Math.min(result.result.confidence || 0, 100).toFixed(1)}%</span>
                  {result.result.api_used && (
                    <span className="text-blue-600">via {result.result.api_used}</span>
                  )}
                </div>
              </div>
            </div>
          </div>
        )

      default:
        return (
          <div className="text-gray-900">
            <pre className="whitespace-pre-wrap text-sm">
              {JSON.stringify(result.result, null, 2)}
            </pre>
          </div>
        )
    }
  }

  return (
    <div className={`border rounded-lg p-4 ${getAnalysisColor(result.type)}`}>
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center space-x-2">
          {getAnalysisIcon(result.type)}
          <h3 className="font-medium text-gray-900">
            {getAnalysisTitle(result.type)}
          </h3>
        </div>
        <div className="flex items-center space-x-1 text-xs text-gray-500">
          <Clock className="w-3 h-3" />
          <span>{formatTimestamp(result.timestamp)}</span>
        </div>
      </div>
      
      {renderResultContent()}
    </div>
  )
}

export default AnalysisResult 