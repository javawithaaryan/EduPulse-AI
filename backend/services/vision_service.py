import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

class VisionService:
    def __init__(self):
        # Support both standard AZURE_ prefix and simplified names
        self.endpoint = os.environ.get("AZURE_VISION_ENDPOINT") or os.environ.get("VISION_ENDPOINT")
        self.key = os.environ.get("AZURE_VISION_KEY") or os.environ.get("VISION_KEY")
        self.client = None

        if self.endpoint and self.key:
            try:
                self.client = ImageAnalysisClient(
                    endpoint=self.endpoint,
                    credential=AzureKeyCredential(self.key)
                )
            except Exception as e:
                print(f"Failed to initialize Azure Vision Client: {e}")

    def analyze_image(self, image_data, features=None):
        """
        Analyzes an image using Azure AI Vision.
        
        :param image_data: Raw bytes of the image file
        :param features: List of VisualFeatures enum to extract (defaults to all safe ones)
        :return: Structured JSON dictionary with results
        """
        if not self.client:
            return {"error": "Azure Vision Service not configured properly (Missing credentials)"}

        if features is None:
            features = [
                VisualFeatures.CAPTION,
                VisualFeatures.READ,
                VisualFeatures.OBJECTS, # Objects
                VisualFeatures.TAGS,
                VisualFeatures.PEOPLE,
                VisualFeatures.SMART_CROPS
            ]

        try:
            result = self.client.analyze(
                image_data=image_data,
                visual_features=features
            )

            # Format Response
            response = {
                "caption": result.caption.text if result.caption else None,
                "text_extracted": [line.text for block in result.read.blocks for line in block.lines] if result.read else [],
                "objects": [obj.tags[0].name for obj in result.objects.list] if result.objects else [],
                "tags": [tag.name for tag in result.tags.list] if result.tags else [],
                "people_count": len(result.people.list) if result.people else 0,
                "metadata": {
                    "width": result.metadata.width,
                    "height": result.metadata.height
                }
            }

            # Safety: Remove bounding boxes or identity info if present (People feature only gives bounding box and confidence)
            # We strictly return count only for people as per requirements.

            return response

        except Exception as e:
            return {"error": str(e)}
