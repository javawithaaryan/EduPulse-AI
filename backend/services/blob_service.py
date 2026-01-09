import os
from config import Config
from werkzeug.utils import secure_filename

class BlobService:
    @staticmethod
    def upload_file(file):
        """
        Uploads file to Azure Blob Storage or saves locally (Mock).
        Returns the public URL (or local path).
        """
        filename = secure_filename(file.filename)
        
        if Config.USE_MOCK_AI:
            # Save locally to static/uploads for demo
            upload_dir = os.path.join(os.getcwd(), 'static', 'uploads')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)
            return f"/static/uploads/{filename}"

        # Real Azure Blob Upload Code
        # blob_service_client = BlobServiceClient.from_connection_string(Config.AZURE_STORAGE_CONNECTION_STRING)
        # ...
        return f"https://mockaccount.blob.core.windows.net/uploads/{filename}"
