
import os

file_path = "config.py"
with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    if "AZURE_OPENAI_DEPLOYMENT_NAME =" in line:
        new_lines.append("    AZURE_OPENAI_API_VERSION = os.environ.get('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')\n")

with open(file_path, "w") as f:
    f.writelines(new_lines)

print("✅ config.py updated.")
