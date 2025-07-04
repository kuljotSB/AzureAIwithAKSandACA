### Getting Started with AKS (Azure Kubernetes Service)

## Connect to Your Kubernetes Cluster

To connect to your Kubernetes cluster, run:

```sh
az aks get-credentials --resource-group $RG_NAME --name $AKS_NAME
```

To view your kubeconfig file, use:

```sh
kubectl config view --raw
```

## Explore Kubernetes Resources

To see details about the `Deployment` resource, run:

```sh
kubectl explain deployment
```

For a complete list of available attributes, use the `--recursive` flag:

```sh
kubectl explain deployment --recursive
```

This outputs a large set of attributes. To focus on a specific part of the resource, such as configuring containers in the Pod template, run:

```sh
kubectl explain deployment.spec.template.spec.containers
```

This command displays the fields available for containers within the Deployment resource, helping you understand how to configure them properly.