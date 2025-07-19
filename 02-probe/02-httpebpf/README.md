# HTTP Traffic Monitoring with eBPF

This example demonstrates how to use eBPF to monitor HTTP traffic in a Kubernetes cluster. The probe attaches to network-related syscalls to capture and analyze HTTP requests and responses.

## Overview

The HTTP eBPF probe:

1. Monitors network-related system calls using eBPF
2. Captures HTTP traffic data (headers, payloads, etc.)
3. Provides visibility into HTTP requests and responses across the cluster
4. Can detect sensitive information in HTTP traffic

## Prerequisites

- Docker installed for building the container image
- Access to a Kubernetes cluster (K3s with Vagrant in this setup)
- `kubectl` configured to communicate with your cluster

## Build and Push the Container Image

```bash
# Replace <username> with your Docker Hub username
docker build -t <username>/ebpf-httpebpf .
docker push <username>/ebpf-httpebpf
```

## Deploy to Kubernetes

The DaemonSet ensures the eBPF probe runs on every node in the cluster:

```bash
# Update the image name in daemonset.yaml if needed
kubectl apply -f daemonset.yaml
```

## Testing the HTTP Monitoring

SSH into one of the worker nodes and generate HTTP traffic:

```bash
# Connect to a worker node
vagrant ssh k3s-worker1

# Generate HTTP traffic with curl
curl --header "Content-Type: application/json" \
     --request POST \
     --data '{"username":"xyrv","password":"xyzd"}' \
     http://httpbin.org/post?q=123 -v
```

## Monitoring the Probe Output

View the logs from the eBPF probe pods to see captured HTTP traffic:

```bash
# View all HTTP traffic logs
kubectl logs -l name=ebpf-httpebpf -f

# Filter for specific processes (e.g., curl)
kubectl logs -l name=ebpf-httpebpf -f | grep curl

# Filter for specific content (e.g., username)
kubectl logs -l name=ebpf-httpebpf -f | grep username
```

## How It Works

The probe uses eBPF to attach to network-related syscalls like `send`, `recv`, `write`, and `read`. When these syscalls are used for HTTP traffic, the probe captures the data, analyzes it to identify HTTP patterns, and logs the relevant information.

## Security Considerations

- This probe can see sensitive information in HTTP traffic (passwords, tokens, etc.)
- In production environments, consider implementing filtering for sensitive data
- HTTPS/TLS traffic would require additional configuration to decrypt

## Troubleshooting

If you don't see any HTTP traffic in the logs:

1. Verify the pods are running: `kubectl get pods -l name=ebpf-httpebpf`
2. Check for errors: `kubectl describe pods -l name=ebpf-httpebpf`
3. Ensure the traffic is actually HTTP (not HTTPS/TLS)
4. Try generating more traffic or using different HTTP clients

## Cleanup

```bash
kubectl delete -f daemonset.yaml
```
