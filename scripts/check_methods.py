import inspect
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

print("Methods:")
print([m for m in dir(ImageAnalysisClient) if not m.startswith("_")])

print("\nSignature of analyze:")
sig = inspect.signature(ImageAnalysisClient.analyze)
for name, param in sig.parameters.items():
    print(f"{name}: {param.default}")
