import inspect
from azure.ai.vision.imageanalysis import ImageAnalysisClient

print(f"Has analyze_from_url: {hasattr(ImageAnalysisClient, 'analyze_from_url')}")

sig = inspect.signature(ImageAnalysisClient.analyze)
print("Analyze Params:")
for i, (name, param) in enumerate(sig.parameters.items()):
    print(f"{i}: {name} ({param.kind})")
