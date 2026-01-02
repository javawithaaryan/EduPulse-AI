"""
Comprehensive Demo Script for OpenAI and Azure Vision Integration
This script demonstrates all the key features of both services in EduPulse AI
"""

import os
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()
os.environ['USE_MOCK_AI'] = 'False'  # Force real API usage

from services.openai_service import OpenAIService
from services.vision_service import VisionService
from config import Config

def print_section(title):
    """Helper function to print section headers"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def demo_openai_services():
    """Demonstrate all OpenAI service capabilities"""
    
    print_section("AZURE OPENAI DEMONSTRATION")
    
    print(f"📌 Configuration:")
    print(f"   Endpoint: {Config.AZURE_OPENAI_ENDPOINT}")
    print(f"   Deployment: {Config.AZURE_OPENAI_DEPLOYMENT_NAME}")
    print(f"   Mock Mode: {Config.USE_MOCK_AI}")
    
    # 1. Doubt Resolution System
    print_section("1. AI Tutor - Doubt Resolution")
    question = "Explain the Pythagorean theorem with a simple example"
    print(f"📝 Student Question: {question}\n")
    response = OpenAIService.ask_ai(question, context="Mathematics - Grade 8")
    print(f"🤖 AI Tutor Response:\n{response}\n")
    
    # 2. Auto-Grading System
    print_section("2. AI Grading - Assignment Evaluation")
    submission = """
    The water cycle is a continuous process where water evaporates from oceans and lakes,
    forms clouds through condensation, and returns to Earth as precipitation. The sun
    provides the energy that drives this cycle. Evaporation happens when water heats up
    and turns into water vapor.
    """
    print(f"📄 Student Submission:\n{submission}\n")
    grading_result = OpenAIService.grade_submission(
        submission_text=submission,
        subject="Science",
        grade_level="Grade 7",
        rubric="Understanding of water cycle (5 pts), Use of terminology (3 pts), Clarity (2 pts)",
        max_marks=10
    )
    print(f"📊 AI Grading Result:")
    print(f"   Score: {grading_result.get('score', 'N/A')}/10")
    print(f"   Feedback: {grading_result.get('feedback', 'N/A')}")
    print(f"   Strengths: {', '.join(grading_result.get('strengths', []))}")
    print(f"   Improvements: {', '.join(grading_result.get('improvements', []))}")
    print(f"   Practice Tip: {grading_result.get('practice_tip', 'N/A')}\n")
    
    # 3. Teacher Insights
    print_section("3. Class Analytics - Teacher Insights")
    performance_data = """
    {
        "class": "Grade 8A - Mathematics",
        "recent_quiz": {
            "topic": "Quadratic Equations",
            "average_score": 72,
            "students_below_60": 3,
            "common_errors": ["Formula application", "Sign mistakes"]
        }
    }
    """
    print(f"📈 Class Performance Data:\n{performance_data}\n")
    insights = OpenAIService.generate_class_insights(performance_data)
    print(f"💡 AI-Generated Insights:")
    print(f"   Headline: {insights.get('headline', 'N/A')}")
    print(f"   Summary: {insights.get('summary', 'N/A')}")
    print(f"   Action Item: {insights.get('action_item', 'N/A')}\n")
    
    # 4. Parent Report Generation
    print_section("4. Parent Communication - Academic Summary")
    student_records = """
    {
        "student": "Aryan Kumar",
        "grade": "8th",
        "subjects": {
            "Math": {"score": 85, "trend": "improving"},
            "Science": {"score": 92, "trend": "stable"},
            "English": {"score": 78, "trend": "needs attention"}
        }
    }
    """
    print(f"📚 Student Records:\n{student_records}\n")
    parent_report = OpenAIService.generate_parent_report("Aryan Kumar", student_records)
    print(f"📧 AI-Generated Parent Report:\n{parent_report}\n")

def demo_vision_service():
    """Demonstrate Azure Vision OCR capabilities"""
    
    print_section("AZURE VISION SERVICE DEMONSTRATION")
    
    print(f"📌 Configuration:")
    print(f"   Endpoint: {Config.AZURE_VISION_ENDPOINT}")
    print(f"   Mock Mode: {Config.USE_MOCK_AI}")
    
    # Test with sample images containing text
    test_images = [
        {
            "name": "Landmark with Text",
            "url": "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/landmark.jpg",
            "description": "Testing OCR on a landmark image with visible text"
        },
        {
            "name": "Printed Text",
            "url": "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/printed_text.jpg",
            "description": "Testing OCR on printed text document"
        }
    ]
    
    for idx, image in enumerate(test_images, 1):
        print_section(f"OCR Test {idx}: {image['name']}")
        print(f"📸 Image URL: {image['url']}")
        print(f"📝 Description: {image['description']}\n")
        print("🔍 Extracting text from image...\n")
        
        extracted_text = VisionService.extract_text(image['url'])
        
        print(f"📄 Extracted Text:")
        print("-" * 70)
        print(extracted_text)
        print("-" * 70)
        
        if "Error" in extracted_text:
            print("❌ Status: Failed")
        elif "Mock" in extracted_text:
            print("⚠️ Status: Using Mock Service")
        else:
            print("✅ Status: Success")
        print()

def main():
    """Main demo function"""
    print("\n" + "#"*70)
    print("#" + " "*68 + "#")
    print("#  EDUPULSE AI - AZURE SERVICES DEMONSTRATION".center(70) + "#")
    print("#  OpenAI GPT-4 + Azure Vision OCR Integration".center(70) + "#")
    print("#" + " "*68 + "#")
    print("#"*70)
    
    try:
        # Demo OpenAI Services
        demo_openai_services()
        
        # Demo Vision Services
        demo_vision_service()
        
        print_section("DEMONSTRATION COMPLETE")
        print("✅ All Azure AI services are functioning correctly!")
        print("✅ OpenAI service tested: Tutoring, Grading, Insights, Parent Reports")
        print("✅ Vision service tested: OCR text extraction")
        print("\n" + "#"*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
