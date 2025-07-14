## RAG Application with Azure OpenAI, QDrantDB and Azure File Share CSI

![RAG_with_PVC](./Assets/RAG_with_PVC.png)

### Overview
In this lab, you will set up a Retrieval-Augmented Generation (RAG) application using Azure OpenAI, QDrantDB, and Azure File Share with Persistent Volume Claims (PVC). The RAG pattern allows you to enhance the capabilities of your AI applications by combining the power of large language models with external data sources.

>**What is QDrantDB?**
> QDrantDB is an open-source vector database that allows you to store and query high-dimensional vectors, making it suitable for applications like semantic search and recommendation systems.

>**What is Azure File Share CSI?**
> Azure File Share CSI (Container Storage Interface) allows you to use Azure File Shares as persistent storage for your Kubernetes applications. This is useful for storing large datasets or files that need to be accessed by multiple pods.

### Applications we will use
The applications that we will use in this lab include:

- **ChatBackend**: A backend service that handles chat interactions and integrates with Azure OpenAI.
- **QDrantDB**: A vector database for storing and querying embeddings.
- **ChatFrontend**: A web-based frontend for interacting with the chat backend.
- **VectorLoader**: A service that loads data into QDrantDB and prepares it for querying.

All of these applications are contained in the `/lab5_Multi_Container_Patterns/RAG_Patterns/` directory, and they are designed to work together to provide a complete RAG solution. We will be containerizing these applications using Docker and deploying them on a Kubernetes cluster.

### Setting Export Variables in the Bash Shell
Before you start, you need to set some environment variables in your bash shell. These variables will be used in some of the commands and scripts throughout this lab. Open your terminal and run the following commands:

```bash
export ACR_NAME="YOUR_ACR_NAME" # The name of your Azure Container Registry
export QDRANT_CLIENT_URL="http://localhost:6333" # The port where the QDrantDB instance listens
export AZURE_API_URL="YOUR_AZURE_OPENAI_ENDPOINT" # The Azure OpenAI endpoint
export AZURE_API_KEY="YOUR_AZURE_API_KEY" # The Azure OpenAI API key
export AZURE_MODEL_NAME="YOUR_AZURE_MODEL_NAME" # The Azure OpenAI model name
export EMBEDDING_MODEL_NAME="YOUR_EMBEDDING_MODEL_NAME" # The embedding model name
```

### Preparing the VectorLoader Application
Before we can deploy the RAG application, we need to ensure that the `VectorLoader` application is ready to preload vectors into QDrantDB. This involves containerizing the application and pushing it to an Azure Container Registry (ACR). The `VectorLoader` application is responsible for reading data from a JSON file and uploading it to QDrantDB. This will now be run as a sidecar container alongside the QDrantDB instance to ensure that the vectors are loaded before the main application starts serving requests. But this can also be run as a `Job` in Kubernetes if you prefer to make incremental updates to your vector database on a scheduled or ad-hoc basis.

Make sure you are in the `lab5_Multi_Container_Patterns/RAG_Patterns/VectorLoader` directory, and follow the steps below to containerize the `VectorLoader` application.

Run the following command to build the Docker image:
```bash
docker build -t vector-loader .
```

Now we must push the image to Azure Container Registry.
Login to your Azure Container Registry:
```bash
az acr login --name $ACR_NAME
```

```bash
docker tag vector-loader $ACR_NAME.azurecr.io/vector-loader
docker push $ACR_NAME.azurecr.io/vector-loader
```

### Preparing the ChatBackend Application
The `ChatBackend` application is a backend service that handles chat interactions and integrates with Azure OpenAI. It exposes a `/chat` endpoint for processing chat messages in the RAG pipeline. It will be containerized and deployed in the Kubernetes cluster alongside QDrantDB.

Make sure you are in the `lab5_Multi_Container_Patterns/RAG_Patterns/ChatBackend` directory, and follow the steps below to containerize the `ChatBackend` application.

```bash
docker build -t chat-backend .
```

Now we must push the image to Azure Container Registry.
```bash
docker tag chat-backend $ACR_NAME.azurecr.io/chat-backend
docker push $ACR_NAME.azurecr.io/chat-backend
```

### Preparing the ChatFrontend Application
The `ChatFrontend` application is a web-based frontend for interacting with the chat backend. It provides a user interface for sending messages and receiving responses from the RAG pipeline. This application will also be containerized and deployed in the Kubernetes cluster.

Make sure you are in the `lab5_Multi_Container_Patterns/RAG_Patterns/ChatFrontend/chat-frontend` directory, and follow the steps below to containerize the `ChatFrontend` application.

```bash
docker build -t chat-frontend .
```
Now we must push the image to Azure Container Registry.
```bash
docker tag chat-frontend $ACR_NAME.azurecr.io/chat-frontend
docker push $ACR_NAME.azurecr.io/chat-frontend
```

### Creating a ConfigMap for the VectorLoader Application
We will have to set up a ConfigMap to store the configuration for the `VectorLoader` application. This will include the QDrantDB URL which is going to be `http://localhost:6333` when running in the Kubernetes cluster. We will reference the export variable `QDRANT_CLIENT_URL` that we set earlier in the bash shell while creating the configMap.

Run the following command to create a ConfigMap for the `VectorLoader` application:
```bash
kubectl create configmap vectorloader-config --from-literal=QDRANT_CLIENT_URL=$QDRANT_CLIENT_URL
```

To view the contents of the ConfigMap resource, you can run the following command:
```bash
kubectl get configmap vectorloader-config -o yaml
```

### Creating a ConfigMap for the ChatBackend Application
We will now create a ConfigMap for the `ChatBackend` application to store the Azure OpenAI API configuration. This will include the following:
- `AZURE_API_URL`: The Azure OpenAI endpoint.
- `AZURE_API_KEY`: The Azure OpenAI API key.
- `AZURE_MODEL_NAME`: The Azure OpenAI model name.
- `EMBEDDING_MODEL_NAME`: The embedding model name.

Run the following command to create a ConfigMap for the `ChatBackend` application:
```bash
kubectl create configmap chatbackend-configs \
--from-literal=AZURE_API_URL=$AZURE_API_URL \
--from-literal=AZURE_API_KEY=$AZURE_API_KEY \
--from-literal=AZURE_MODEL_NAME=$AZURE_MODEL_NAME \
--from-literal=EMBEDDING_MODEL_NAME=$EMBEDDING_MODEL_NAME
```

To view the contents of the ConfigMap resource, you can run the following command:
```bash
kubectl get configmap chatbackend-configs -o yaml
```

### Writing the Kubernetes Manifests
Now that we have containerized the applications and created the necessary ConfigMaps, we will write the Kubernetes manifests to deploy the `VectorLoader`, `QDrantDB`, and `ChatBackend` applications in a Kubernetes cluster.

We will be creating a `statefulset` for all the applications combined. The reason(s) for this are:
- **StatefulSet**: We will use a StatefulSet to manage the deployment of the `QDrantDB` instance, ensuring that it has a stable network identity and persistent storage. Moreoever, we need one single pod that houses these application containers.

- **PVC**: We will use a Persistent Volume Claim (PVC) to provide persistent storage for the `QDrantDB` instance. This will allow the database to retain its data even if the pod is restarted or rescheduled. Here defining and deploying a `StatefulSet` with a PVC is essential for the `QDrantDB` instance to ensure data persistence.

Make sure you are in the `lab5_Multi_Container_Patterns/RAG_Patterns/` directory.

Create a `manifests` directory if it does not already exist:
```bash
mkdir manifests
```

First we will create a Persistent Volume Claim (PVC) for the QDrantDB instance. This will allow us to store the data persistently in Azure File Share.
Create a file named `qdrant-pvc.yaml` in the `manifests` directory with the following content:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: qdrant-pvc
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
  storageClassName: azurefile-csi
```

Next, we will create a `StatefulSet` definition for the entire RAG application. Create a file named `rag-app.yaml` in the `manifests` directory with the following content:

```yaml 
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: rag-app
spec:
  serviceName: "rag-app-headless"
  replicas: 2
  selector:
    matchLabels:
      app: rag-app
  template:
    metadata:
      labels:
        app: rag-app
    spec:
      containers:
        - name: qdrant
          image: qdrant/qdrant:latest
          ports:
            - containerPort: 6333
          volumeMounts:
            - name: qdrant-storage
              mountPath: /qdrant/storage/$(HOSTNAME)

        - name: vector-loader
          image: $ACR_NAME.azurecr.io/vector-loader
          ports:
            - containerPort: 5173
          command: ["/bin/sh", "-c"]
          args:
            - |
              echo "Waiting for Qdrant...";
              until curl -s http://localhost:6333; do
                sleep 2;
              done;
              echo "Running embedding upsert script...";
              python /app/app.py
          envFrom:
            - configMapRef:
                name: vectorloader-config

        - name: chat-backend
          image: $ACR_NAME.azurecr.io/chat-backend
          ports:
            - containerPort: 5000
          envFrom:
            - configMapRef:
                name: chatbackend-configs

        - name: chat-frontend
          image: $ACR_NAME.azurecr.io/chat-frontend
          ports:
            - containerPort: 80
      volumes:
        - name: qdrant-storage
          persistentVolumeClaim:
            claimName: qdrant-pvc
```