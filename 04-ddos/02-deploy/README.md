# NGINX Deployment for DDoS Testing

This directory contains Kubernetes manifests for deploying a sample NGINX web server that will be used for DDoS testing and mitigation demonstrations.

## 📋 Overview

The deployment consists of:
- A Kubernetes Deployment with 2 NGINX replicas
- A NodePort Service exposing the NGINX instances on port 31084

## 🚀 Quick Start

### Prerequisites

- A running Kubernetes cluster
- `kubectl` configured to communicate with your cluster

### Deploy NGINX

1. **Deploy the application**:
   ```bash
   # Deploy NGINX
   kubectl apply -f deployment.yaml
   
   # Create the service
   kubectl apply -f service.yaml
   ```

2. **Verify the deployment**:
   ```bash
   # Check deployment status
   kubectl get deployments
   
   # Check pod status
   kubectl get pods -l app=nginx
   
   # Check service status
   kubectl get svc nginx-service
   ```

## 🌐 Accessing the Application

Once deployed, you can access the NGINX service using any of the following methods:

### Via NodePort
```bash
# Get cluster nodes
kubectl get nodes -o wide

# Access using any node's IP on port 31084
curl http://10.0.0.11:31084
```

## 📊 Monitoring

To monitor the deployment:

```bash
# View pod logs
kubectl logs -l app=nginx --tail=50 -f

# View pod metrics
kubectl top pods -l app=nginx

# View service endpoints
kubectl describe svc nginx-service
```

## 🧪 Testing the Deployment

You can test the deployment using various tools:

### Simple HTTP Test
```bash
# Basic connectivity test
curl -I http://10.0.0.11:31084
```

### Load Test with `wrk`
```bash
# Install wrk if not already installed
# On macOS: brew install wrk
# On Ubuntu/Debian: sudo apt-get install wrk

# Run a basic load test
wrk -t2 -c100 -d30s http://10.0.0.11:31084
```

## 🧹 Cleanup

To remove the deployment and service:

```bash
kubectl delete -f service.yaml -f deployment.yaml
```

Or delete everything in the current directory:

```bash
kubectl delete -f .
```

## 📚 Resources

- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)
- [NGINX Documentation](https://docs.nginx.com/)

## ⚠️ Security Note

This deployment is for testing purposes only. For production use:
- Implement proper security policies
- Configure resource limits
- Enable authentication/authorization
- Use Ingress with TLS termination