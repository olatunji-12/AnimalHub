# Deploying Pet Adoption Hub to Azure

This guide demonstrates how to deploy the Pet Adoption Hub Flask application to Azure App Service.

## Prerequisites

1. Install Azure CLI
2. Have an Azure account
3. Install Git

## Deployment Steps

### 1. Login to Azure

```bash
az login
```

### 2. Create Azure Resources

```bash
# Create a resource group
az group create --name pet-adoption-hub --location eastus

# Create an App Service plan
az appservice plan create --name pet-adoption-plan --resource-group pet-adoption-hub --sku B1 --is-linux

# Create a web app
az webapp create --name pet-adoption-hub --resource-group pet-adoption-hub --plan pet-adoption-plan --runtime "PYTHON:3.11"
```

### 3. Configure Environment Variables

```bash
# Set the necessary environment variables
az webapp config appsettings set --name pet-adoption-hub --resource-group pet-adoption-hub --settings \
    FLASK_APP=main.py \
    FLASK_ENV=production \
    DATABASE_URL=<your-database-url>
```

### 4. Deploy the Application

```bash
# Initialize Git repository (if not already done)
git init
git add .
git commit -m "Initial commit for Azure deployment"

# Add Azure remote
az webapp deployment source config-local-git --name pet-adoption-hub --resource-group pet-adoption-hub

# Get the deployment URL
az webapp deployment list-publishing-credentials --name pet-adoption-hub --resource-group pet-adoption-hub

# Add Azure as a remote and push
git remote add azure <deployment-url-from-previous-command>
git push azure master
```

### 5. Verify Deployment

1. Visit your application at: `https://pet-adoption-hub.azurewebsites.net`
2. Check the application logs:
```bash
az webapp log tail --name pet-adoption-hub --resource-group pet-adoption-hub
```

## Troubleshooting

1. If the application fails to start, check the logs:
```bash
az webapp log tail --name pet-adoption-hub --resource-group pet-adoption-hub
```

2. Verify environment variables:
```bash
az webapp config appsettings list --name pet-adoption-hub --resource-group pet-adoption-hub
```

3. Restart the web app if needed:
```bash
az webapp restart --name pet-adoption-hub --resource-group pet-adoption-hub
```

## Important Notes

- The application uses Gunicorn as the WSGI server
- Environment variables must be properly configured
- Database connection string should be updated to match your production database
- Static files are served through Azure's web server

## Clean Up Resources

When you're done with the demo, clean up the resources:

```bash
az group delete --name pet-adoption-hub --yes
```

This will delete all resources created for this deployment.
