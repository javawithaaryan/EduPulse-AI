import importlib.metadata
import inspect
try:
    from azure.ai.vision.imageanalysis import ImageAnalysisClient
    print(f"Version: {importlib.metadata.version('azure-ai-vision-imageanalysis')}")
    print("Inspect analyze:")
    print(inspect.signature(ImageAnalysisClient.analyze))
except Exception as e:
    print(e)
