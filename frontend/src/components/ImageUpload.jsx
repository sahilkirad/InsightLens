import React, { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, Image, FileText, AlertCircle } from 'lucide-react'
import { useInsightLens } from '../contexts/InsightLensContext'
import { textExtractionAPI, handleAPIError } from '../services/api'

const ImageUpload = () => {
  const { state, actions } = useInsightLens()
  const { uploadedImage, isExtracting, error } = state

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0]
    if (!file) return

    // Validate file type
    if (!file.type.startsWith('image/')) {
      actions.setError('Please upload an image file (JPEG, PNG, etc.)')
      return
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      actions.setError('File size too large. Maximum size is 10MB.')
      return
    }

    try {
      actions.clearError()
      actions.setUploadedImage(file)
      actions.setExtracting(true)

      // Extract text from image
      const response = await textExtractionAPI.extractText(file)
      
      if (response.success) {
        actions.setExtractedText(response.text)
      } else {
        actions.setError(response.message || 'Failed to extract text from image')
      }
    } catch (error) {
      const errorInfo = handleAPIError(error)
      actions.setError(errorInfo.message)
    } finally {
      actions.setExtracting(false)
    }
  }, [actions])

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.tiff']
    },
    maxFiles: 1,
    disabled: isExtracting
  })

  return (
    <div className="space-y-6">
      {/* Upload Area */}
      <div className="card">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Upload Image
        </h2>
        
        <div
          {...getRootProps()}
          className={`
            relative border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all duration-200
            ${isDragActive && !isDragReject
              ? 'border-primary-500 bg-primary-50'
              : isDragReject
              ? 'border-red-500 bg-red-50'
              : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
            }
            ${isExtracting ? 'opacity-50 cursor-not-allowed' : ''}
          `}
        >
          <input {...getInputProps()} />
          
          {isExtracting ? (
            <div className="space-y-4">
              <div className="loading-spinner mx-auto"></div>
              <p className="text-gray-600">Extracting text from image...</p>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center">
                {isDragActive ? (
                  <Upload className="w-8 h-8 text-primary-600" />
                ) : (
                  <Image className="w-8 h-8 text-gray-400" />
                )}
              </div>
              
              <div>
                <p className="text-lg font-medium text-gray-900">
                  {isDragActive
                    ? isDragReject
                      ? 'Invalid file type'
                      : 'Drop your image here'
                    : 'Drag & drop an image here'
                  }
                </p>
                <p className="text-gray-500 mt-1">
                  or click to browse files
                </p>
              </div>
              
              <div className="text-sm text-gray-400">
                <p>Supports: JPEG, PNG, GIF, BMP, TIFF</p>
                <p>Maximum size: 10MB</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="card border-red-200 bg-red-50">
          <div className="flex items-start space-x-3">
            <AlertCircle className="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" />
            <div>
              <h3 className="text-sm font-medium text-red-800">Error</h3>
              <p className="text-sm text-red-700 mt-1">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Image Preview */}
      {uploadedImage && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Image Preview
          </h3>
          
          <div className="space-y-4">
            <div className="relative">
              <img
                src={URL.createObjectURL(uploadedImage)}
                alt="Uploaded"
                className="w-full h-64 object-contain rounded-lg border border-gray-200"
              />
            </div>
            
            <div className="flex items-center justify-between text-sm text-gray-600">
              <span>{uploadedImage.name}</span>
              <span>{(uploadedImage.size / 1024 / 1024).toFixed(2)} MB</span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ImageUpload 