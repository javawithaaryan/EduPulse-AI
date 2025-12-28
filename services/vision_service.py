import time
from config import Config

class VisionService:
    @staticmethod
    def extract_text(file_url):
        """
        Extracts text from an image/PDF using Azure AI Vision or Mock.
        """
        if Config.USE_MOCK_AI:
            time.sleep(1.5)
            # Return some dummy student handwriting text
            # Return varied student handwriting text for different mock scenarios
            text_samples = [
                "The Water Cycle involves evaporation, condensation, and precipitation. Heat from the sun is the main driver.",
                "To solve quadratic equations, we can use the formula x = (-b ± √(b² - 4ac)) / 2a.",
                "Shakespeare's Macbeth explores the themes of ambition, guilt, and the corrupting nature of power."
            ]
            return random.choice(text_samples)
        
        # Real implementation would use azure-ai-vision-imageanalysis
        return "Simulated OCR Text from Azure Vision"
