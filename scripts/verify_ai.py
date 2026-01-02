import os
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load env variables explicitly
load_dotenv()

from services.openai_service import OpenAIService
from config import Config

def test_integration():
    print("--- Verifying Azure AI Integration ---")
    print(f"Endpoint: {Config.AZURE_OPENAI_ENDPOINT}")
    print(f"Deployment: {Config.AZURE_OPENAI_DEPLOYMENT_NAME}")
    print(f"Mock Mode: {Config.USE_MOCK_AI}")
    
    if Config.USE_MOCK_AI:
        print("WARNING: System is running in MOCK mode. Set USE_MOCK_AI=False in .env to test real API.")
        
    print("\n1. Testing 'ask_ai'...")
    try:
        response = OpenAIService.ask_ai("What is the capital of France?", context="Geography Test")
        print(f"Response: {response}")
        if "mock" in response.lower() and not Config.USE_MOCK_AI:
            print("FAILURE: Got mock response but expected real.")
        elif "error" in response.lower():
            print("FAILURE: AI Service returned an error.")
        else:
            print("SUCCESS: Received valid AI response.")
    except Exception as e:
        print(f"CRITICAL FAILURE: {e}")

if __name__ == "__main__":
    test_integration()
