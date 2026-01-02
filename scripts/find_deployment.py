
import os
import sys
import requests
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load env variables
load_dotenv()

def test_deployment(deployment_name):
    print(f"Testing deployment name: '{deployment_name}'", end="... ")
    
    endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT')
    api_key = os.environ.get('AZURE_OPENAI_KEY')
    api_version = "2024-02-15-preview"
    
    if not endpoint or not api_key:
        print("Missing credentials.")
        return False
        
    url = f"{endpoint}/openai/deployments/{deployment_name}/chat/completions?api-version={api_version}"
    
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
    
    payload = {
        "messages": [{"role": "user", "content": "Ping"}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            print("✅ SUCCESS!")
            return True
        elif response.status_code == 404:
            print("❌ Not Found")
        elif response.status_code == 401:
            print("❌ Unauthorized (Check Key)")
            return False # Key issue, stop trying
        else:
            print(f"⚠️ Error {response.status_code}: {response.text[:50]}...")
            
    except Exception as e:
        print(f"Connection Error: {e}")
        
    return False

if __name__ == "__main__":
    print("--- Probing Azure OpenAI Deployments ---")
    current = os.environ.get('AZURE_OPENAI_DEPLOYMENT_NAME')
    print(f"Current Configured Name: {current}\n")
    
    common_names = [
        "gpt-4",
        "gpt-4-turbo",
        "gpt-4o",
        "gpt-35-turbo", 
        "gpt-3.5-turbo",
        "gpt-35-turbo-16k",
        "text-davinci-003",
        "edupulse-gpt4",
        "edupulse-model",
        "chat"
    ]
    
    found = False
    for name in common_names:
        if test_deployment(name):
            print(f"\n🎉 FOUND VALID DEPLOYMENT: {name}")
            print(f"Please update your .env file: AZURE_OPENAI_DEPLOYMENT_NAME={name}")
            found = True
            break
            
    if not found:
        print("\n❌ Could not guess the deployment name.")
        print("Please check your Azure AI Studio > Deployments tab.")
