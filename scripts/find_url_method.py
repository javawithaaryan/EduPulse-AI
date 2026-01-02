import inspect
from azure.ai.vision.imageanalysis import ImageAnalysisClient

print("Looking for URL methods...")
for m in dir(ImageAnalysisClient):
    if "url" in m.lower():
        print(f"Found: {m}")

print("\nDocstring for analyze:")
if ImageAnalysisClient.analyze.__doc__:
    print(ImageAnalysisClient.analyze.__doc__[:300])
else:
    print("No docstring")
