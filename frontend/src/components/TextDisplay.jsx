import React from 'react'
import { FileText, Copy, Check } from 'lucide-react'
import { useInsightLens } from '../contexts/InsightLensContext'

const TextDisplay = () => {
  const { state } = useInsightLens()
  const { extractedText, isExtracting } = state
  const [copied, setCopied] = React.useState(false)

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(extractedText)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (error) {
      console.error('Failed to copy text:', error)
    }
  }

  if (!extractedText && !isExtracting) {
    return (
      <div className="card">
        <div className="text-center py-12">
          <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            No Text Extracted
          </h3>
          <p className="text-gray-500">
            Upload an image to extract text and see it here
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold text-gray-900">
          Extracted Text
        </h2>
        
        {extractedText && (
          <button
            onClick={handleCopy}
            className="flex items-center space-x-2 px-3 py-1.5 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors duration-200"
            title="Copy to clipboard"
          >
            {copied ? (
              <>
                <Check className="w-4 h-4 text-green-600" />
                <span className="text-green-600">Copied!</span>
              </>
            ) : (
              <>
                <Copy className="w-4 h-4 text-gray-600" />
                <span className="text-gray-600">Copy</span>
              </>
            )}
          </button>
        )}
      </div>

      {isExtracting ? (
        <div className="space-y-4">
          <div className="loading-spinner mx-auto"></div>
          <p className="text-center text-gray-600">
            Extracting text from image...
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {/* Text Statistics */}
          <div className="flex items-center justify-between text-sm text-gray-600 bg-gray-50 rounded-lg p-3">
            <span>
              Characters: {extractedText.length.toLocaleString()}
            </span>
            <span>
              Words: {extractedText.split(/\s+/).filter(word => word.length > 0).length.toLocaleString()}
            </span>
            <span>
              Lines: {extractedText.split('\n').length.toLocaleString()}
            </span>
          </div>

          {/* Text Content */}
          <div className="relative">
            <textarea
              value={extractedText}
              readOnly
              className="w-full h-64 p-4 text-sm text-gray-900 bg-white border border-gray-200 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent custom-scrollbar"
              placeholder="Extracted text will appear here..."
            />
          </div>

          {/* Text Actions */}
          {extractedText && (
            <div className="flex items-center justify-between text-sm text-gray-600">
              <span>
                Text extracted successfully
              </span>
              <span>
                Ready for analysis
              </span>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default TextDisplay 