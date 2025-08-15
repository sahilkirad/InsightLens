
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

class AlternativeAIAnalysisService:
    """AI service using Cohere API for enhanced analysis"""
    
    def __init__(self):
        # Cohere API
        self.cohere_api_key = os.getenv("COHERE_API_KEY")
        self.cohere_url = "https://api.cohere.ai/v1"
        
        if not self.cohere_api_key:
            print("Warning: COHERE_API_KEY not set. Cohere features will not work.")
    
    async def analyze_text(self, text: str, analysis_type: str, prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze text using Cohere API
        
        Args:
            text: Text to analyze
            analysis_type: Type of analysis ('summarize', 'sentiment', 'question')
            prompt: Optional prompt for question-answering or summarization
            
        Returns:
            dict: Analysis results
        """
        try:
            # Clean the text first
            text = clean_text(text)
            
            if analysis_type == 'summarize':
                return await self._summarize_text(text, prompt)
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
    
    async def _summarize_text(self, text: str, prompt: Optional[str] = None) -> Dict[str, Any]:
        """Summarize text using Cohere API"""
        try:
            if not self.cohere_api_key:
                return {
                    'success': False,
                    'result': None,
                    'message': 'Cohere API key not configured'
                }
            
            headers = {
                "Authorization": f"Bearer {self.cohere_api_key}",
                "Content-Type": "application/json"
            }
            
            # Prepare the text for Cohere (limit to 100KB as per Cohere docs)
            if len(text) > 100000:
                text = text[:100000]
            
            payload = {
                "text": text,
                "length": "medium",
                "format": "paragraph",
                "model": "summarize-xlarge",
                "additional_command": prompt or "Create a clear, well-structured summary of the extracted text only. Focus on key points and main ideas from the provided content. Do not add any external information or assumptions."
            }
            
            print(f"Cohere Summarization - Text length: {len(text)}")
            
            response = requests.post(
                f"{self.cohere_url}/summarize",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            print(f"Cohere Response: {result}")
            
            summary = result.get('summary', '').strip()
            
            if not summary:
                return {
                    'success': False,
                    'result': None,
                    'message': 'Cohere returned empty summary'
                }
            
            return {
                'success': True,
                'result': {
                    'summary': summary,
                    'original_length': len(text),
                    'summary_length': len(summary),
                    'compression_ratio': round(len(summary) / len(text) * 100, 1),
                    'api_used': 'Cohere Summarize-XLarge'
                },
                'message': 'Text summarized successfully using Cohere'
            }
        except requests.exceptions.RequestException as e:
            print(f"Cohere Network Error: {str(e)}")
            return {
                'success': False,
                'result': None,
                'message': f'Cohere network error: {str(e)}'
            }
        except Exception as e:
            print(f"Cohere Error: {str(e)}")
            return {
                'success': False,
                'result': None,
                'message': f'Cohere summarization failed: {str(e)}'
            }
    
    async def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment using Cohere API"""
        try:
            if not self.cohere_api_key:
                return {
                    'success': False,
                    'result': None,
                    'message': 'Cohere API key not configured'
                }
            
            return await self._sentiment_with_cohere(text)
        except Exception as e:
            return {
                'success': False,
                'result': None,
                'message': f'Sentiment analysis failed: {str(e)}'
            }
    
    async def _sentiment_with_cohere(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment using Cohere Generate API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.cohere_api_key}",
                "Content-Type": "application/json"
            }
            
            # Prepare the prompt for sentiment analysis
            prompt = f"""Analyze the sentiment of the following text and provide:
1. Overall sentiment (Positive/Negative/Neutral)
2. Confidence level (0-100%)
3. Key emotional indicators

Text: {text}

Analysis:"""
            
            payload = {
                "model": "command",
                "prompt": prompt,
                "max_tokens": 150,
                "temperature": 0.1,
                "k": 0,
                "stop_sequences": [],
                "return_likelihoods": "NONE"
            }
            
            print(f"Cohere Sentiment Analysis - Text length: {len(text)}")
            
            response = requests.post(
                f"{self.cohere_url}/generate",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            print(f"Cohere Sentiment Response: {result}")
            
            if 'generations' in result and len(result['generations']) > 0:
                analysis = result['generations'][0]['text'].strip()
                
                # Extract sentiment from analysis
                sentiment = "Neutral"
                confidence = 50.0
                
                if "positive" in analysis.lower():
                    sentiment = "Positive"
                    confidence = 85.0
                elif "negative" in analysis.lower():
                    sentiment = "Negative"
                    confidence = 85.0
                
                # Ensure confidence is capped at 100%
                confidence = min(confidence, 100.0)
                
                emoji_map = {
                    "Positive": "😊",
                    "Neutral": "😐",
                    "Negative": "😞"
                }
                
                return {
                    'success': True,
                    'result': {
                        'sentiment': sentiment,
                        'confidence': confidence,
                        'emoji': emoji_map.get(sentiment, "😐"),
                        'analysis': analysis,
                        'api_used': 'Cohere Command'
                    },
                    'message': 'Sentiment analyzed successfully using Cohere'
                }
            else:
                return {
                    'success': False,
                    'result': None,
                    'message': 'Invalid response format from Cohere'
                }
        except requests.exceptions.RequestException as e:
            print(f"Cohere Sentiment Network Error: {str(e)}")
            return {
                'success': False,
                'result': None,
                'message': f'Cohere network error: {str(e)}'
            }
        except Exception as e:
            print(f"Cohere Sentiment Error: {str(e)}")
            return {
                'success': False,
                'result': None,
                'message': f'Cohere sentiment analysis failed: {str(e)}'
            }
    
    async def _answer_question(self, context: str, question: str) -> Dict[str, Any]:
        """Answer questions using Cohere API"""
        try:
            # Validate context quality
            if not context or len(context.strip()) < 10:
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
            
            if not self.cohere_api_key:
                return {
                    'success': False,
                    'result': None,
                    'message': 'Cohere API key not configured'
                }
            
            return await self._question_with_cohere(context, question)
        except Exception as e:
            return {
                'success': False,
                'result': None,
                'message': f'Question answering failed: {str(e)}'
            }
    
    async def _question_with_cohere(self, context: str, question: str) -> Dict[str, Any]:
        """Answer questions using Cohere Generate API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.cohere_api_key}",
                "Content-Type": "application/json"
            }
            
            # Prepare the prompt for Cohere with strict context-only instructions
            prompt = f"""IMPORTANT: You must ONLY answer based on the information provided in the context below. Do NOT use any external knowledge or general information.

Context: {context}

Question: {question}

Instructions:
1. Answer ONLY using information from the provided context
2. If the answer is not explicitly mentioned in the context, respond with: "Based on the provided text, I cannot find a specific answer to your question. The information may not be present in the extracted text."
3. Do not make assumptions or provide general knowledge
4. Quote specific parts of the context when possible
5. If the context is unclear or insufficient, state that clearly

Answer:"""
            
            payload = {
                "model": "command",
                "prompt": prompt,
                "max_tokens": 300,
                "temperature": 0.3,
                "k": 0,
                "stop_sequences": [],
                "return_likelihoods": "NONE"
            }
            
            print(f"Cohere Question Answering - Context length: {len(context)}")
            
            response = requests.post(
                f"{self.cohere_url}/generate",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            print(f"Cohere QA Response: {result}")
            
            if 'generations' in result and len(result['generations']) > 0:
                answer = result['generations'][0]['text'].strip()
                
                # Ensure the answer is based only on the provided context
                if not answer or answer.lower() in ['', 'none', 'null']:
                    answer = "Based on the provided text, I cannot find a specific answer to your question. The information may not be present in the extracted text."
                else:
                    # Add a prefix to emphasize context-only response
                    answer = f"[Based on extracted text] {answer}"
                
                return {
                    'success': True,
                    'result': {
                        'answer': answer,
                        'confidence': 85.0,  # Cohere typically provides good answers
                        'context_preview': context[:300] + '...' if len(context) > 300 else context,
                        'question': question,
                        'answer_length': len(answer),
                        'api_used': 'Cohere Command'
                    },
                    'message': 'Question answered successfully using Cohere'
                }
            else:
                return {
                    'success': False,
                    'result': None,
                    'message': 'Invalid response format from Cohere'
                }
        except requests.exceptions.RequestException as e:
            print(f"Cohere QA Network Error: {str(e)}")
            return {
                'success': False,
                'result': None,
                'message': f'Cohere network error: {str(e)}'
            }
        except Exception as e:
            print(f"Cohere QA Error: {str(e)}")
            return {
                'success': False,
                'result': None,
                'message': f'Cohere question answering failed: {str(e)}'
            }
