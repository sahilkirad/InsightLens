import os
import requests
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def clean_text(text):
    """Clean OCR text by removing duplicate lines, excessive whitespace, and joining into a single paragraph."""
    if not text:
        return ""
    
    # Split into lines and clean each line
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if line and len(line) > 1:  # Only keep lines with meaningful content
            lines.append(line)
    
    # Remove duplicates while preserving order
    unique_lines = []
    seen = set()
    for line in lines:
        if line not in seen:
            unique_lines.append(line)
            seen.add(line)
    
    # Join with proper spacing
    cleaned_text = ' '.join(unique_lines)
    
    # Remove excessive whitespace
    import re
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    
    return cleaned_text.strip()

class AIAnalysisService:
    """Service for AI-powered text analysis using Hugging Face Inference API and TabularisAI for sentiment"""
    
    def __init__(self):
        self.api_token = os.getenv("HUGGING_FACE_API_TOKEN")
        self.api_url = "https://api-inference.huggingface.co/models"
        
        # Allow running without API token for development/testing
        if not self.api_token:
            print("Warning: HUGGING_FACE_API_TOKEN not set. Some features may not work.")
            self.api_token = "demo_token"  # Fallback for development
        
        # Updated model configurations for better performance
        self.models = {
            'summarize': 'facebook/bart-large-cnn',
            'question': 'deepset/roberta-base-squad2',
            'sentiment': 'cardiffnlp/twitter-roberta-base-sentiment-latest'
        }
        
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    async def analyze_text(self, text: str, analysis_type: str, prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze text using the specified analysis type
        
        Args:
            text: Text to analyze
            analysis_type: Type of analysis ('summarize', 'sentiment', 'question')
            prompt: Optional prompt for question-answering or summarization
            
        Returns:
            dict: Analysis results
        """
        try:
            if analysis_type == 'summarize':
                # Use a detailed default prompt if none provided
                if not prompt:
                    prompt = (
                        "Create a concise, well-structured summary of the extracted text only. "
                        "Focus on the key points, main ideas, and important details from the provided content. "
                        "Use clear, simple language and avoid repetition. "
                        "Do not add any external information or assumptions. "
                        "Keep the summary informative but brief."
                    )
                # Clean the text for summarization
                text = clean_text(text)
                return await self._summarize_text(text)
            elif analysis_type == 'sentiment':
                return await self._analyze_sentiment(text)
            elif analysis_type == 'question':
                if not prompt:
                    return {
                        'success': False,
                        'result': None,
                        'message': 'Prompt is required for question analysis'
                    }
                return await self._answer_question(text, prompt)
            else:
                return {
                    'success': False,
                    'result': None,
                    'message': f'Unknown analysis type: {analysis_type}'
                }
        except Exception as e:
            return {
                'success': False,
                'result': None,
                'message': f'Analysis failed: {str(e)}'
            }
    
    async def _summarize_text(self, text: str) -> Dict[str, Any]:
        """Summarize text using the BART model"""
        try:
            model_url = f"{self.api_url}/{self.models['summarize']}"
            
            # Clean and prepare text
            text = clean_text(text)
            if len(text) < 20:
                return {
                    'success': False,
                    'result': None,
                    'message': 'Insufficient text for summarization'
                }
            
            # Limit text length for better performance
            if len(text) > 2000:
                text = text[:2000] + "..."
            
            payload = {
                "inputs": text,
                "parameters": {
                    "max_length": 150,
                    "min_length": 30,
                    "do_sample": False,
                    "num_beams": 4,
                    "early_stopping": True,
                    "length_penalty": 2.0,
                    "no_repeat_ngram_size": 3
                }
            }
            
            print(f"Summarization - Text length: {len(text)}")
            
            response = requests.post(
                model_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            print(f"Summarization Response: {result}")
            
            if isinstance(result, list) and len(result) > 0:
                summary = result[0].get('summary_text', '')
                if not summary or summary.strip() == '':
                    return {
                        'success': False,
                        'result': None,
                        'message': 'Generated summary is empty'
                    }
                
                return {
                    'success': True,
                    'result': {
                        'summary': summary.strip(),
                        'original_length': len(text),
                        'summary_length': len(summary),
                        'compression_ratio': round(len(summary) / len(text) * 100, 1)
                    },
                    'message': 'Text summarized successfully'
                }
            else:
                return {
                    'success': False,
                    'result': None,
                    'message': 'Failed to generate summary - no results returned'
                }
                
        except requests.exceptions.RequestException as e:
            print(f"Summarization Network Error: {str(e)}")
            return {
                'success': False,
                'result': None,
                'message': f'Network error during summarization: {str(e)}'
            }
        except Exception as e:
            print(f"Summarization Error: {str(e)}")
            return {
                'success': False,
                'result': None,
                'message': f'Summarization failed: {str(e)}'
            }
    
   

    async def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment using Hugging Face sentiment analysis model"""
        try:
            # Use the configured sentiment model
            model_url = f"{self.api_url}/{self.models['sentiment']}"
            
            # Clean and prepare text
            text = clean_text(text)
            if len(text) < 5:
                return {
                    'success': False,
                    'result': None,
                    'message': 'Insufficient text for sentiment analysis'
                }
            
            # Limit text length for better performance
            if len(text) > 512:
                text = text[:512]
            
            payload = {
                "inputs": text
            }
            
            print(f"Sentiment Analysis - Text length: {len(text)}")
            
            response = requests.post(
                model_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            print(f"Sentiment Analysis Response: {result}")
            
            if isinstance(result, list) and len(result) > 0:
                # Find the highest scoring sentiment
                best_result = max(result, key=lambda x: x.get('score', 0))
                label = best_result.get('label', 'neutral')
                score = best_result.get('score', 0.0)
                
                # Map labels to user-friendly names
                label_mapping = {
                    'LABEL_0': 'Negative',
                    'LABEL_1': 'Neutral', 
                    'LABEL_2': 'Positive'
                }
                
                sentiment_label = label_mapping.get(label, 'Neutral')
                
                emoji_map = {
                    "Positive": "😊",
                    "Neutral": "😐",
                    "Negative": "😞"
                }
                
                # Ensure confidence is capped at 100%
                confidence_score = min(round(score * 100, 1), 100.0)
                
                return {
                    'success': True,
                    'result': {
                        'sentiment': sentiment_label,
                        'confidence': confidence_score,
                        'emoji': emoji_map.get(sentiment_label, "😐"),
                        'text_analyzed': text[:100] + '...' if len(text) > 100 else text
                    },
                    'message': 'Sentiment analyzed successfully'
                }
            else:
                return {
                    'success': False,
                    'result': None,
                    'message': 'Failed to analyze sentiment - no results returned'
                }
        except requests.exceptions.RequestException as e:
            print(f"Sentiment Analysis Network Error: {str(e)}")
            return {
                'success': False,
                'result': None,
                'message': f'Network error during sentiment analysis: {str(e)}'
            }
        except Exception as e:
            print(f"Sentiment Analysis Error: {str(e)}")
            return {
                'success': False,
                'result': None,
                'message': f'Sentiment analysis failed: {str(e)}'
            }



    
    async def _answer_question(self, context: str, question: str) -> Dict[str, Any]:
        """Answer questions using the roberta model with improved prompting"""
        try:
            model_url = f"{self.api_url}/{self.models['question']}"
            
            # Clean and prepare the context
            context = clean_text(context)
            if len(context) < 10:
                return {
                    'success': False,
                    'result': None,
                    'message': 'Insufficient text extracted from image to answer questions. Please ensure the image contains readable text.'
                }
            
            # Check if context has meaningful content
            meaningful_words = [word for word in context.split() if len(word) > 2]
            if len(meaningful_words) < 5:
                return {
                    'success': False,
                    'result': None,
                    'message': 'Extracted text appears to be insufficient or contains mostly non-meaningful content. Please try with a clearer image.'
                }
            
            # Limit context length for better performance
            if len(context) > 1000:
                context = context[:1000] + "..."
            
            payload = {
                "inputs": {
                    "question": question,
                    "context": context
                }
            }
            
            print(f"Question: {question}")
            print(f"Context length: {len(context)}")
            
            response = requests.post(
                model_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            print(f"Question Answering Response: {result}")
            
            if isinstance(result, dict):
                answer = result.get('answer', '')
                confidence = result.get('score', 0.0)
                
                # Format the answer for better readability and ensure context-only responses
                formatted_answer = answer.strip()
                if not formatted_answer or formatted_answer.lower() in ['', 'none', 'null']:
                    formatted_answer = "Based on the provided text, I cannot find a specific answer to your question. The information may not be present in the extracted text."
                else:
                    # Add a prefix to emphasize context-only response
                    formatted_answer = f"[Based on extracted text] {formatted_answer}"
                
                # Calculate confidence percentage
                confidence_percentage = round(confidence * 100, 1)
                
                # Provide more detailed response
                return {
                    'success': True,
                    'result': {
                        'answer': formatted_answer,
                        'confidence': confidence_percentage,
                        'context_preview': context[:300] + '...' if len(context) > 300 else context,
                        'question': question,
                        'answer_length': len(formatted_answer)
                    },
                    'message': 'Question answered successfully'
                }
            else:
                return {
                    'success': False,
                    'result': None,
                    'message': 'Invalid response format from question answering model'
                }
                
        except requests.exceptions.RequestException as e:
            print(f"Question Answering Network Error: {str(e)}")
            return {
                'success': False,
                'result': None,
                'message': f'Network error during question answering: {str(e)}'
            }
        except Exception as e:
            print(f"Question Answering Error: {str(e)}")
            return {
                'success': False,
                'result': None,
                'message': f'Question answering failed: {str(e)}'
            } 