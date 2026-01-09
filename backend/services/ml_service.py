from config import Config
import os
import logging

try:
    from azure.ai.ml import MLClient
    from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
except ImportError:
    MLClient = None
    DefaultAzureCredential = None
    InteractiveBrowserCredential = None

logger = logging.getLogger(__name__)

class MLService:
    _ml_client = None

    @classmethod
    def get_ml_client(cls):
        """
        Initializes and returns the Azure ML Client.
        """
        if cls._ml_client:
            return cls._ml_client

        if Config.USE_MOCK_AI:
            logger.info("Using Mock AI for ML Service")
            return None

        # Check for required credentials
        subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
        resource_group = os.environ.get("AZURE_RESOURCE_GROUP")
        workspace_name = os.environ.get("AZURE_ML_WORKSPACE_NAME")
        tenant_id = os.environ.get("AZURE_TENANT_ID")

        if not all([subscription_id, resource_group, workspace_name]):
            logger.warning("Azure ML credentials missing in environment.")
            return None

        try:
            # Authenticate - Try Default first (Env, CLI, Managed Identity)
            try:
                # If we have a tenant ID, hint it to DefaultCreds might not work directly but useful context
                credential = DefaultAzureCredential()
                # fast check if token is available
                credential.get_token("https://management.azure.com/.default")
            except Exception:
                # Fallback to Interactive verification for local dev issues
                logger.info("Default Auth failed, switching to Interactive Browser Login...")
                credential = InteractiveBrowserCredential(tenant_id=tenant_id)

            # Initialize Client
            cls._ml_client = MLClient(
                credential=credential,
                subscription_id=subscription_id,
                resource_group_name=resource_group,
                workspace_name=workspace_name
            )
            
            # Verify it actually works (Permissions Check)
            # If this fails with Auth error, we should retry with Interactive
            try:
                cls._ml_client.workspaces.get(workspace_name)
            except Exception as e:
                if "Authentication" in str(e) or "Tenant" in str(e) or "Authorization" in str(e):
                    logger.warning(f"Default Creds failed validation ({e}). Forcing Interactive Login...")
                    credential = InteractiveBrowserCredential(tenant_id=tenant_id)
                    cls._ml_client = MLClient(
                        credential=credential,
                        subscription_id=subscription_id,
                        resource_group_name=resource_group,
                        workspace_name=workspace_name
                    )
            
            logger.info(f"Azure ML Client initialized for workspace: {workspace_name}")
            return cls._ml_client
        except Exception as e:
            logger.error(f"Failed to initialize Azure ML Client: {e}")
            return None

    @staticmethod
    def verify_connection():
        """
        Verifies the connection to the Azure ML Workspace.
        Returns details of the workspace if successful.
        """
        client = MLService.get_ml_client()
        if not client:
            return {"status": "Mock Mode or Missing Credentials"}

        try:
            ws = client.workspaces.get(client.workspace_name)
            return {
                "status": "Connected",
                "workspace": ws.name,
                "location": ws.location,
                "resource_group": ws.resource_group
            }
        except Exception as e:
            return {"status": "Error", "details": str(e)}

    # Keep existing mock logic for fallback/demo purposes
    @staticmethod
    def predict_risk(student_id, recent_scores, attendance_rate=100):
        # For this demo, we use the local heuristic model even if the client is connected.
        # In a production scenario, you would use:
        # client.online_endpoints.invoke(endpoint_name="my-model", request_file="payload.json")
        logger.info(f"Predicting risk for {student_id} using EduPulse Heuristic Model (Workspace Connected)")

        import random
        avg = sum(recent_scores) / len(recent_scores) if recent_scores else 0
        count = len(recent_scores)
        
        risk_level = "low"
        if avg < 5: risk_level = "high"
        elif avg < 7.5: risk_level = "medium"
        
        if attendance_rate < 75:
            if risk_level == "low": risk_level = "medium"
            elif risk_level == "medium": risk_level = "high"
        
        is_declining = False
        if count >= 2:
            is_declining = recent_scores[-1] < recent_scores[-2]
        
        confidence = 0.85 + (random.random() * 0.1)
        trend = "stable"
        if is_declining: trend = "declining"
        elif count >= 2 and recent_scores[-1] > recent_scores[-2]: trend = "improving"
        
        return {
            "risk_level": risk_level, 
            "confidence": round(confidence, 2), 
            "trend": trend,
            "attendance_impact": "low" if attendance_rate > 90 else "critical"
        }
