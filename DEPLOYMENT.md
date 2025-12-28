# Deployment Guide: EduPulse AI

This guide covers deploying EduPulse AI to Azure App Service with GitHub Actions for continuous deployment.

## Prerequisites

- Azure Account with active subscription
- Azure CLI installed
- GitHub account
- Git configured locally

## Azure Resources Setup

### 1. Create Azure Resources

```bash
# Login to Azure
az login

# Create resource group
az group create --name edupulse-rg --location eastus

# Create App Service Plan (Free tier for testing, upgrade for production)
az appservice plan create --name edupulse-plan --resource-group edupulse-rg --sku B1 --is-linux

# Create Web App
az webapp create --resource-group edupulse-rg --plan edupulse-plan --name edupulse-ai --runtime "PYTHON:3.10"
```

### 2. Configure Azure SQL Database

```bash
# Create SQL Server
az sql server create --name edupulse-sql --resource-group edupulse-rg --location eastus --admin-user sqladmin --admin-password YourPassword123!

# Create Database
az sql db create --resource-group edupulse-rg --server edupulse-sql --name edupulse-db --service-objective S0

# Configure firewall (Allow Azure services)
az sql server firewall-rule create --resource-group edupulse-rg --server edupulse-sql --name AllowAzureServices --start-ip-address 0.0.0.0 --end-ip-address 0.0.0.0
```

### 3. Create Azure Storage Account

```bash
# Create storage account
az storage account create --name edupulsestorage --resource-group edupulse-rg --location eastus --sku Standard_LRS

# Get connection string
az storage account show-connection-string --name edupulsestorage --resource-group edupulse-rg
```

### 4. Set Up Azure OpenAI

1. Go to Azure Portal → Create Resource → Azure OpenAI
2. Deploy GPT-4 model with deployment name: `gpt-4`
3. Note the endpoint and API key

## Environment Configuration

### Set App Service Environment Variables

```bash
# Set environment variables in Azure App Service
az webapp config appsettings set --resource-group edupulse-rg --name edupulse-ai --settings \
  SECRET_KEY="your-strong-secret-key" \
  AZURE_OPENAI_ENDPOINT="https://your-openai.openai.azure.com/" \
  AZURE_OPENAI_KEY="your-openai-key" \
  AZURE_OPENAI_DEPLOYMENT="gpt-4" \
  DATABASE_URL="mssql+pyodbc://sqladmin:YourPassword123!@edupulse-sql.database.windows.net/edupulse-db?driver=ODBC+Driver+18+for+SQL+Server" \
  AZURE_STORAGE_CONNECTION_STRING="your-storage-connection-string" \
  FLASK_ENV="production"
```

## GitHub Actions CI/CD

### 1. Get Azure Publish Profile

```bash
az webapp deployment list-publishing-profiles --name edupulse-ai --resource-group edupulse-rg --xml
```

### 2. Add GitHub Secret

1. Go to GitHub repository → Settings → Secrets and variables → Actions
2. Create new secret: `AZURE_WEBAPP_PUBLISH_PROFILE`
3. Paste the XML content from step 1

### 3. GitHub Actions Workflow

Create `.github/workflows/azure-deploy.yml`:

```yaml
name: Deploy to Azure App Service

on:
  push:
    branches:
      - main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Deploy to Azure Web App
      uses: azure/webapps-deploy@v2
      with:
        app-name: 'edupulse-ai'
        publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
```

## Database Initialization

After first deployment, initialize database tables:

```bash
# SSH into Azure App Service or use Azure CLI
az webapp ssh --resource-group edupulse-rg --name edupulse-ai

# Run Python shell
python

# Initialize database
>>> from app import app, db
>>> with app.app_context():
>>>     db.create_all()
>>> exit()
```

## Post-Deployment Verification

1. **Test Application**: Visit `https://edupulse-ai.azurewebsites.net`
2. **Check Logs**: 
   ```bash
   az webapp log tail --resource-group edupulse-rg --name edupulse-ai
   ```
3. **Monitor Performance**: Use Azure Monitor in Azure Portal

## Auto-Commit Setup (Local Development)

For automatic commits on file changes (development only):

### Option 1: VS Code Extension
Install "Git Auto Commit" extension from VS Code Marketplace

### Option 2: Git Hooks
Create `.git/hooks/post-save` (requires additional tooling)

### ⚠️ Recommended Approach
Instead of auto-commits, use proper Git workflow:

```bash
# After making changes
git add .
git commit -m "Descriptive commit message"
git push

# GitHub Actions will automatically deploy to Azure
```

## Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure Azure SQL with production tier
- [ ] Enable HTTPS only
- [ ] Set up Azure Application Insights
- [ ] Configure custom domain
- [ ] Enable Azure CDN for static files
- [ ] Set up backup strategy
- [ ] Configure auto-scaling rules

## Troubleshooting

### Database Connection Issues
- Verify firewall rules allow Azure services
- Check connection string format
- Ensure SQL Server is accessible

### Deployment Failures
- Check GitHub Actions logs
- Verify `requirements.txt` is up to date
- Check Azure App Service logs

### Performance Issues
- Upgrade App Service Plan (from B1 to S1 or higher)
- Enable Application Insights for monitoring
- Consider Azure Redis Cache for sessions

## Support

For issues or questions:
- GitHub Issues: https://github.com/javawithaaryan/EduPulse-AI/issues
- Azure Support: https://azure.microsoft.com/support/

---

**Live URL**: `https://edupulse-ai.azurewebsites.net` (after deployment)
