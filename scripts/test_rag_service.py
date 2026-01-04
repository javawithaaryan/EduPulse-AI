import sys
import os
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv()

from services.openai_service import OpenAIService
from config import Config

# Enable logging
logging.basicConfig(level=logging.INFO)

def test_rag():
    print("\n=== Testing OpenAIService.ask_ai_rag ===")
    
    # Ensure Mock AI is FALSE for this test
    Config.USE_MOCK_AI = False
    print(f"USE_MOCK_AI: {Config.USE_MOCK_AI}")
    print(f"Azure Endpoint Configured: {bool(Config.AZURE_OPENAI_ENDPOINT)}")
    print(f"Azure Search Endpoint Configured: {bool(os.getenv('AZURE_SEARCH_ENDPOINT'))}")

    query = "What is the content of the uploaded documents?"
    print(f"\nSending Query: '{query}'")
    
    try:
        response = OpenAIService.ask_ai_rag(query, history=[], subject="General")
        
        with open("test_output.txt", "w") as f:
            f.write("--- Response Content ---\n")
            f.write(response.get('content', 'No content'))
            f.write("\n\n--- Citations ---\n")
            f.write(str(response.get('citations', [])))
        
        print("\n--- Response Received ---")
        print(f"Content written to test_output.txt")
        print(f"Content Preview: {response.get('content')[:100]}...") 
        print(f"Citations: {len(response.get('citations', []))}")
        
        if "Error" in response.get('content', ''):
            print("\n❌ TEST FAILED: Error in response.")
        elif response.get('citations'):
            print("\n✅ TEST PASSED: Response received with citations.")
        else:
            print("\n⚠️ TEST PARTIAL: Response received but NO citations (Index might be empty or query mismatch).")
            
    except Exception as e:
        print(f"\n❌ TEST FAILED with Exception: {str(e)}")

if __name__ == "__main__":
    test_rag()
