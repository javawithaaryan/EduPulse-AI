
import os
import sys

# New values provided by user
# NOTE: Replace these with your actual Azure credentials
NEW_CONF = {
    "AZURE_OPENAI_KEY": "your_azure_openai_key_here",
    "AZURE_OPENAI_ENDPOINT": "your_azure_endpoint_here",
    "AZURE_OPENAI_DEPLOYMENT_NAME": "your_deployment_name_here",
    "AZURE_OPENAI_API_VERSION": "2025-04-01-preview"
}

env_path = ".env"
new_lines = []

# Read existing lines and filter out OpenAI keys
if os.path.exists(env_path):
    with open(env_path, "r") as f:
        for line in f:
            key = line.split("=")[0].strip()
            # Keep line if it's NOT one of the keys we are updating
            if key not in NEW_CONF:
                new_lines.append(line.strip())

# Add new keys
for key, value in NEW_CONF.items():
    new_lines.append(f"{key}={value}")

# Write back
with open(env_path, "w") as f:
    f.write("\n".join(new_lines))
    f.write("\n")

print("✅ .env file updated successfully.")
