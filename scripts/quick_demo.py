"""Quick Demo - OpenAI and Azure Vision Services"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()
os.environ['USE_MOCK_AI'] = 'False'

from services.openai_service import OpenAIService
from services.vision_service import VisionService

print("=" * 60)
print("OPENAI SERVICE DEMO")
print("=" * 60)

print("\n1. AI Tutor Test:")
response = OpenAIService.ask_ai("What is 2+2?", "Math")
print(f"Question: What is 2+2?")
print(f"Answer: {response[:200]}...")

print("\n" + "=" * 60)
print("AZURE VISION SERVICE DEMO")
print("=" * 60)

print("\n2. OCR Text Extraction Test:")
test_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/landmark.jpg"
print(f"Image: {test_url}")
text = VisionService.extract_text(test_url)
print(f"Extracted Text:\n{text}")

print("\n" + "=" * 60)
print("DEMO COMPLETE!")
print("=" * 60)
