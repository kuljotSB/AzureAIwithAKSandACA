# AKS + Istio Labs

Welcome! Pick a Lab:

## Infrastructure
- [Infrastructure Deployment](infra/infra_deployment.md)

## Lab 1: Getting Started
- [Lab 1: Getting Started With AKS](lab1_Getting_Started_With_AKS/lab1.md)

## Lab 2: Deploying AI App
- [Build and Push Docker Image (Docker Desktop to ACR)](lab2_deploying_AI_app/docker_desktop_to_acr.md)
- [Deploy AI App from ACR to AKS](lab2_deploying_AI_app/acr_to_aks.md)
- [Pod Anti-Affinity](lab2_deploying_AI_app/pod_anti_affinity.md)
- [Resource Limits](lab2_deploying_AI_app/resource_limits.md)
- [StatefulSet Deployments](lab2_deploying_AI_app/StatefulSet.md)

## Lab 3: Exposing AI App
- [Exposing ACR Image](lab3_exposing_AI_app_external_IP/exposing_acr_image.md)

## Lab 4: ConfigMap and Azure Key Vault
- [ConfigMaps](lab4_configMap_and_AKV/configMaps.md)
- [Secrets and ConfigMaps](lab4_configMap_and_AKV/secrets_and_configMaps.md)
- [Azure Key Vault Integration](lab4_configMap_and_AKV/azure_key_vault.md)

## Lab 5: Multi-Container Patterns
- [Simple Frontend Backend Chat App (Sidecar)](lab5_Multi_Container_Patterns/Simple_Frontend_Backend_Chat_App/simple-fb-sidecar.md)
- [ClusterIP Service Pattern](lab5_Multi_Container_Patterns/Simple_Frontend_Backend_Chat_App/ClusterIP-svc.md)
- [RAG Patterns: Helm Charts](lab5_Multi_Container_Patterns/RAG_Patterns/Helm_Charts.md)
- [RAG Patterns: Helm Charts to ACR](lab5_Multi_Container_Patterns/RAG_Patterns/Helm_Charts_to_ACR.md)
- [RAG Patterns: NGINX Ingress](lab5_Multi_Container_Patterns/RAG_Patterns/NGINX_Ingress.md)
- [RAG Patterns: Preloading Vectors with Sidecar](lab5_Multi_Container_Patterns/RAG_Patterns/Sidecar_Container_for_vectors.md)
- [RAG Patterns: With PVC](lab5_Multi_Container_Patterns/RAG_Patterns/RAG_with_PVC.md)

## Lab 6: Deployment Strategies
- [Rolling Updates](lab6_Deployment_Strategies/Rolling_Updates.md)
- [Canary (Blue/Green) Deployment](lab6_Deployment_Strategies/Canary_Deployment.md)

## Lab 7: Observability and Maintenance
- [Copilot Workbooks and Logs](lab7_Observability_and_Maintenance/copilot_workbooks_and_logs.md)

## Lab 8: KEDA on AKS
- [KEDA with Cron Scaled Object](lab8_KEDA_on_AKS/cron_scaled_object.md)
- [Vertical Pod Autoscaler (VPA)](lab8_KEDA_on_AKS/k8s_vpa.md)

## Lab 9: Istio Service Mesh
- [Istio mTLS Encryption](lab9_Istio_Service_Mesh/istio_encryption_mTLS.md)
- [Istio Ingress Gateway](lab9_Istio_Service_Mesh/istio_ingress_gateway.md)
- [Istio Canary Deployment](lab9_Istio_Service_Mesh/istio_canary_depoyment.md)