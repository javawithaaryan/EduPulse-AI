import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

def verify_search():
    print("Loading environment variables...")
    load_dotenv()
    
    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    key = os.getenv("AZURE_SEARCH_KEY")
    index_name = os.getenv("AZURE_SEARCH_INDEX")
    
    print(f"Endpoint: {endpoint}")
    print(f"Index: {index_name}")
    print(f"Key Present: {'Yes' if key else 'No'}")
    
    if not all([endpoint, key, index_name]):
        print("ERROR: Missing configuration variables.")
        return

    try:
        print(f"Connecting to Azure Search index '{index_name}'...")
        credential = AzureKeyCredential(key)
        client = SearchClient(endpoint=endpoint,
                            index_name=index_name,
                            credential=credential)
        
        print("Running test query '*' (limit 1)...")
        results = client.search(search_text="*", top=1)
        
        count = 0
        for result in results:
            count += 1
            print(f"Success! Found document with ID: {result.get('id', 'Unknown')}")
            # Print a few keys to verify content
            keys = list(result.keys())[:3]
            print(f"Document keys sample: {keys}")
            
        if count == 0:
            print("Connection successful, but no documents found in index.")
        else:
            print("Verification PASSED: Successfully connected and retrieved data.")
            
    except Exception as e:
        print(f"Verification FAILED: {str(e)}")

if __name__ == "__main__":
    verify_search()
