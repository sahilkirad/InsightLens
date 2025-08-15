import React, { createContext, useContext, useReducer } from 'react'

// Initial state
const initialState = {
  uploadedImage: null,
  extractedText: '',
  isExtracting: false,
  isAnalyzing: false,
  analysisResults: [],
  error: null
}

// Action types
const ACTIONS = {
  SET_UPLOADED_IMAGE: 'SET_UPLOADED_IMAGE',
  SET_EXTRACTED_TEXT: 'SET_EXTRACTED_TEXT',
  SET_EXTRACTING: 'SET_EXTRACTING',
  SET_ANALYZING: 'SET_ANALYZING',
  ADD_ANALYSIS_RESULT: 'ADD_ANALYSIS_RESULT',
  CLEAR_ANALYSIS_RESULTS: 'CLEAR_ANALYSIS_RESULTS',
  SET_ERROR: 'SET_ERROR',
  CLEAR_ERROR: 'CLEAR_ERROR',
  RESET_STATE: 'RESET_STATE'
}

// Reducer function
function insightLensReducer(state, action) {
  switch (action.type) {
    case ACTIONS.SET_UPLOADED_IMAGE:
      return {
        ...state,
        uploadedImage: action.payload,
        error: null
      }
    
    case ACTIONS.SET_EXTRACTED_TEXT:
      return {
        ...state,
        extractedText: action.payload,
        error: null
      }
    
    case ACTIONS.SET_EXTRACTING:
      return {
        ...state,
        isExtracting: action.payload
      }
    
    case ACTIONS.SET_ANALYZING:
      return {
        ...state,
        isAnalyzing: action.payload
      }
    
    case ACTIONS.ADD_ANALYSIS_RESULT:
      return {
        ...state,
        analysisResults: [...state.analysisResults, action.payload],
        error: null
      }
    
    case ACTIONS.CLEAR_ANALYSIS_RESULTS:
      return {
        ...state,
        analysisResults: []
      }
    
    case ACTIONS.SET_ERROR:
      return {
        ...state,
        error: action.payload,
        isExtracting: false,
        isAnalyzing: false
      }
    
    case ACTIONS.CLEAR_ERROR:
      return {
        ...state,
        error: null
      }
    
    case ACTIONS.RESET_STATE:
      return {
        ...initialState
      }
    
    default:
      return state
  }
}

// Create context
const InsightLensContext = createContext()

// Provider component
export function InsightLensProvider({ children }) {
  const [state, dispatch] = useReducer(insightLensReducer, initialState)

  // Action creators
  const actions = {
    setUploadedImage: (image) => {
      dispatch({ type: ACTIONS.SET_UPLOADED_IMAGE, payload: image })
    },
    
    setExtractedText: (text) => {
      dispatch({ type: ACTIONS.SET_EXTRACTED_TEXT, payload: text })
    },
    
    setExtracting: (isExtracting) => {
      dispatch({ type: ACTIONS.SET_EXTRACTING, payload: isExtracting })
    },
    
    setAnalyzing: (isAnalyzing) => {
      dispatch({ type: ACTIONS.SET_ANALYZING, payload: isAnalyzing })
    },
    
    addAnalysisResult: (result) => {
      dispatch({ type: ACTIONS.ADD_ANALYSIS_RESULT, payload: result })
    },
    
    clearAnalysisResults: () => {
      dispatch({ type: ACTIONS.CLEAR_ANALYSIS_RESULTS })
    },
    
    setError: (error) => {
      dispatch({ type: ACTIONS.SET_ERROR, payload: error })
    },
    
    clearError: () => {
      dispatch({ type: ACTIONS.CLEAR_ERROR })
    },
    
    resetState: () => {
      dispatch({ type: ACTIONS.RESET_STATE })
    }
  }

  const value = {
    state,
    actions
  }

  return (
    <InsightLensContext.Provider value={value}>
      {children}
    </InsightLensContext.Provider>
  )
}

// Custom hook to use the context
export function useInsightLens() {
  const context = useContext(InsightLensContext)
  if (!context) {
    throw new Error('useInsightLens must be used within an InsightLensProvider')
  }
  return context
} 