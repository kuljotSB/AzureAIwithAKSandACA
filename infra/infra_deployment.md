### Scripts to Deploy Kubernetes Cluster Workload

Start by logging in to the Azure CLI (make sure you have the Azure CLI installed):
```sh
az login
```

To keep the resource names unique, we will use a random number as a suffix for the resource names. This will also help you to avoid naming conflicts with other resources in your Azure subscription.

Run the following command to generate a random number.
```bash
RAND=$RANDOM
export RAND
echo "Random resource identifier will be: ${RAND}"
```

Set the location to a region of your choice. For example, eastus or westeurope. (eastus is used in this example.)
```bash
export LOCATION=eastus
```

Create a resource group name using the random number.
```bash
export RG_NAME=myresourcegroup$RAND
```

Create a resource group in Azure.
```bash
az group create \
--name $RG_NAME \
--location $LOCATION
```

Deploy the Azure resources needed for the workshop.
```bash
az deployment group create \
--resource-group $RG_NAME \
--name "${RG_NAME}-deployment" \
--template-uri https://raw.githubusercontent.com/kuljotSB/AzureAIwithAKSandACA/refs/heads/main/infra/main.json \
--parameters randomSeed=$RAND userObjectId=$(az ad signed-in-user show --query id -o tsv)
```

The deployment will provision the following Azure resources in your resource group:

- **Azure Kubernetes Service (AKS)**: A managed Kubernetes cluster for running your workloads.
- **Azure Container Registry (ACR)**: Stores and manages your container images.
- **Azure Managed Prometheus**: Provides monitoring and metrics collection for AKS.
- **Azure Managed Grafana**: Visualizes Prometheus metrics with customizable dashboards.
- **Azure Log Analytics Workspace**: Centralizes and stores application and infrastructure logs.
- **Azure Key Vault**: Secures and manages secrets, keys, and certificates.
- **Azure App Configuration**: Centralizes application configuration management.
- **Azure Cosmos DB**: Globally distributed database for demo application data storage.
- **Azure User-Assigned Managed Identities**: Enables secure authentication to Azure services without credentials.

These resources form the foundation for deploying, monitoring, and managing your Kubernetes workloads in Azure.

> **Note:**  
> The `Azure Cosmos DB` and `Azure App Configuration` resources are **not required** for this workshop.  
> You can safely delete them using the Azure Portal or the Azure CLI:
>
> ```bash
> az cosmosdb delete --name <cosmosdb-account-name> --resource-group $RG_NAME
> az appconfig delete --name <app-config-name> --resource-group $RG_NAME
> ```

### Clean Up Resources
To clean up the resources created during the workshop, you can delete the entire resource group. This will remove all resources within it, including the AKS cluster, ACR, and other associated services.
```bash
az group delete --name $RG_NAME --yes --no-wait
```

