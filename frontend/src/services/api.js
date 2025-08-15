import axios from 'axios'

// Create axios instance with base configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('API Request Error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message)
    
    // Log more detailed error information for debugging
    if (error.response) {
      console.error('Error Status:', error.response.status)
      console.error('Error Data:', error.response.data)
      console.error('Error Headers:', error.response.headers)
    } else if (error.request) {
      console.error('No response received:', error.request)
    } else {
      console.error('Error setting up request:', error.message)
    }
    
    return Promise.reject(error)
  }
)

// Text extraction API
export const textExtractionAPI = {
  /**
   * Extract text from uploaded image
   * @param {File} imageFile - The image file to process
   * @returns {Promise<Object>} Response with extracted text
   */
  extractText: async (imageFile) => {
    const formData = new FormData()
    formData.append('file', imageFile)
    
    const response = await api.post('/api/extract-text', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    
    return response.data
  },
}

// Text analysis API
export const analysisAPI = {
  /**
   * Analyze text using AI models
   * @param {Object} params - Analysis parameters
   * @param {string} params.text - Text to analyze
   * @param {string} params.analysis_type - Type of analysis (summarize, sentiment, question)
   * @param {string} [params.prompt] - Optional prompt for question analysis
   * @returns {Promise<Object>} Analysis results
   */
  analyzeText: async ({ text, analysis_type, prompt }) => {
    const payload = {
      text,
      analysis_type,
      ...(prompt && { prompt }),
    }
    
    const response = await api.post('/api/analyze', payload)
    return response.data
  },

  /**
   * Get available analysis types
   * @returns {Promise<Object>} Available analysis types
   */
  getAnalysisTypes: async () => {
    const response = await api.get('/api/analysis-types')
    return response.data
  },
}

// Health check API
export const healthAPI = {
  /**
   * Check API health status
   * @returns {Promise<Object>} Health status
   */
  checkHealth: async () => {
    const response = await api.get('/health')
    return response.data
  },
}

// Error handling utilities
export const handleAPIError = (error) => {
  if (error.response) {
    // Server responded with error status
    const { status, data } = error.response
    return {
      message: data.detail || data.message || `HTTP ${status}: ${error.response.statusText}`,
      status,
      data,
    }
  } else if (error.request) {
    // Request was made but no response received
    return {
      message: 'No response from server. Please check your connection.',
      status: 0,
    }
  } else {
    // Something else happened
    return {
      message: error.message || 'An unexpected error occurred.',
      status: 0,
    }
  }
}

export default api 