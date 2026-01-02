import time
import logging
import os
import requests
from config import Config

logger = logging.getLogger(__name__)

class VisionService:
    @staticmethod
    def extract_text(file_url):
        """
        Extracts text from an image/PDF using Azure AI Vision REST API or Mock.
        """
        try:
            # Check if Mock Mode is enabled
            if Config.USE_MOCK_AI:
                logger.info("Using Mock Vision Service")
                time.sleep(1.0)
                if "math" in file_url.lower():
                    return "To solve quadratic equations, we can use the formula x = (-b ± √(b² - 4ac)) / 2a."
                elif "science" in file_url.lower():
                    return "The Water Cycle involves evaporation, condensation, and precipitation. Heat from the sun is the main driver."
                else:
                    return "Shakespeare's Macbeth explores the themes of ambition, guilt, and the corrupting nature of power."
            
            # Validate Credentials
            if not Config.AZURE_VISION_KEY or not Config.AZURE_VISION_ENDPOINT:
                logger.error("Azure Vision credentials missing.")
                return "Error: Vision credentials not configured in .env"

            # Prepare REST API request
            endpoint = Config.AZURE_VISION_ENDPOINT.rstrip('/')
            api_url = f"{endpoint}/computervision/imageanalysis:analyze?api-version=2023-10-01&features=read"
            
            headers = {
                'Ocp-Apim-Subscription-Key': Config.AZURE_VISION_KEY,
                'Content-Type': 'application/json'
            }
            
            data = {'url': file_url}
            
            response = requests.post(api_url, headers=headers, json=data)
            
            if response.status_code != 200:
                logger.error(f"Azure Vision API Error: {response.status_code} - {response.text}")
                return f"Error: Azure Vision API returned {response.status_code}"

            result = response.json()
            
            # Extract Text from READ result
            if 'readResult' in result:
                # Structure for 2023-10-01 usually: readResult -> blocks -> lines -> text
                # Or sometimes at top level 'read' depending on version. 
                # Let's check 'readResult' first (common in newer API)
                lines = [line['text'] for block in result['readResult']['blocks'] for line in block['lines']]
                return "\n".join(lines)
            
            if 'read' in result:
                # Alternative structure
                lines = [line['text'] for block in result['read']['blocks'] for line in block['lines']]
                return "\n".join(lines)

            return "No text detected."

        except Exception as e:
            logger.error(f"Error in extract_text: {str(e)}")
            return f"Error extracting text: {str(e)}"
