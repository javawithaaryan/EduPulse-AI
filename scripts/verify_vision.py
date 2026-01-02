import os
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Logging to file
import logging
logging.basicConfig(filename='vision_debug.log', level=logging.DEBUG, filemode='w')

# Load env variables and FORCE disable mock for this test
load_dotenv()
os.environ['USE_MOCK_AI'] = 'False'

from services.vision_service import VisionService
from config import Config

def test_vision():
    print("--- Verifying Azure Vision Integration ---")
    print(f"Endpoint: {Config.AZURE_VISION_ENDPOINT}")
    
    # Use a simple image with clear text
    test_image_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/landmark.jpg"
    
    print(f"\nTarget Image: {test_image_url}")
    print("Sending request to Azure Vision...")
    
    # Reload Config to ensure it picks up the os.environ change if it was already loaded
    import importlib
    import config
    importlib.reload(config)
    
    try:
        text = VisionService.extract_text(test_image_url)
        print(f"\n--- Extracted Text Result ---\n{text}")
        
        if "Error" in text:
            print("\nFAILURE: Vision Service returned an error.")
        elif "Mock" in text:
            print("\nFAILURE: Service is still using Mock mode.")
        else:
            print("\nSUCCESS: Text extraction completed.")
            
    except Exception as e:
        print(f"\nCRITICAL FAILURE")
        print(f"Type: {type(e).__name__}")
        print(f"Msg: {str(e)[:300]}")

if __name__ == "__main__":
    test_vision()
