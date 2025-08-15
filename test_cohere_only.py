#!/usr/bin/env python3
"""
Simple test script to verify Cohere API integration
"""

import asyncio
import os
from dotenv import load_dotenv
from backend.app.services.alternative_ai_service import AlternativeAIAnalysisService

# Load environment variables
load_dotenv()

async def test_cohere_integration():
    """Test Cohere API integration"""
    
    print("🧪 Testing Cohere API Integration...")
    print("=" * 50)
    
    # Check if Cohere API key is set
    cohere_key = os.getenv("COHERE_API_KEY")
    if not cohere_key:
        print("❌ COHERE_API_KEY not found in environment variables")
        print("Please add your Cohere API key to the .env file")
        return
    
    print(f"🔑 Cohere API Key: {cohere_key[:10]}...")
    print()
    
    # Initialize the service
    service = AlternativeAIAnalysisService()
    
    # Test text
    test_text = """
    The company XYZ Corp was founded in 2010 by John Smith. 
    Their main product is a mobile app called "TechHelper" which helps users organize their daily tasks.
    The app costs $9.99 per month and has over 50,000 active users.
    The company is headquartered in San Francisco, California.
    """
    
    print("📝 Test Text:")
    print(test_text.strip())
    print()
    
    # Test 1: Summarization
    print("1️⃣ Testing Summarization...")
    try:
        result = await service._summarize_text(test_text)
        if result['success']:
            print(f"✅ Summary: {result['result']['summary']}")
            print(f"📊 Compression: {result['result']['compression_ratio']}%")
        else:
            print(f"❌ Failed: {result['message']}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    print()
    
    # Test 2: Sentiment Analysis
    print("2️⃣ Testing Sentiment Analysis...")
    try:
        result = await service._analyze_sentiment(test_text)
        if result['success']:
            print(f"✅ Sentiment: {result['result']['sentiment']}")
            print(f"📊 Confidence: {result['result']['confidence']}%")
            print(f"😊 Emoji: {result['result']['emoji']}")
        else:
            print(f"❌ Failed: {result['message']}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    print()
    
    # Test 3: Question Answering
    print("3️⃣ Testing Question Answering...")
    try:
        result = await service._answer_question(test_text, "Who founded XYZ Corp?")
        if result['success']:
            print(f"✅ Answer: {result['result']['answer']}")
            print(f"📊 Confidence: {result['result']['confidence']}%")
        else:
            print(f"❌ Failed: {result['message']}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    print()
    
    print("=" * 50)
    print("🎉 Cohere API Integration Test Complete!")

if __name__ == "__main__":
    asyncio.run(test_cohere_integration())
