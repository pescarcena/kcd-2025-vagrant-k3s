# SSL/TLS Traffic Monitoring with eBPF Uprobes

This example demonstrates how to use eBPF uprobes to monitor encrypted SSL/TLS traffic in a Kubernetes cluster. Unlike kprobes which attach to kernel functions, uprobes attach to user-space library functions, allowing us to capture SSL/TLS data before encryption or after decryption.

## Overview

The SSL eBPF uprobe:

1. Attaches to OpenSSL library functions (`SSL_read` and `SSL_write`)
2. Captures plaintext data before encryption or after decryption
3. Provides visibility into encrypted HTTPS traffic
4. Can detect sensitive information in encrypted communications

## How It Works

This probe uses uprobes to instrument the OpenSSL library's `SSL_read` and `SSL_write` functions:

- `SSL_write`: Captures data before it's encrypted and sent over the network
- `SSL_read`: Captures data after it's received and decrypted

This approach allows us to see the plaintext content of HTTPS communications without breaking encryption.

## Prerequisites

- Docker installed for building the container image
- Access to a Kubernetes cluster (K3s with Vagrant in this setup)
- `kubectl` configured to communicate with your cluster
- Applications using OpenSSL for SSL/TLS (most Linux applications do)

## Build and Push the Container Image

```bash
# Replace <username> with your Docker Hub username
docker build -t <username>/ebpf-ssl-uprobe .
docker push <username>/ebpf-ssl-uprobe
```

## Deploy to Kubernetes

The DaemonSet ensures the eBPF probe runs on every node in the cluster:

```bash
# Update the image name in daemonset.yaml if needed
kubectl apply -f daemonset.yaml
```

## Testing the SSL/TLS Monitoring

SSH into one of the worker nodes and generate HTTPS traffic:

```bash
# Connect to a worker node
vagrant ssh k3s-worker1

# Generate HTTPS traffic with curl
curl --header "Content-Type: application/json" \
     --request POST \
     --data '{"username":"xyrv","password":"xyzd"}' \
     https://httpbin.org/post?q=123 -v
```

## Monitoring the Probe Output

View the logs from the eBPF probe pods to see captured SSL/TLS traffic:

```bash
# View all SSL/TLS traffic logs
kubectl logs -l name=ebpf-ssl-uprobe -f

# Filter for specific content (e.g., username)
kubectl logs -l name=ebpf-ssl-uprobe -f | grep username

# Filter for specific SSL operations
kubectl logs -l name=ebpf-ssl-uprobe -f | grep "SSL_read"
kubectl logs -l name=ebpf-ssl-uprobe -f | grep "SSL_write"
```

## Security and Privacy Considerations

- This probe can see sensitive information in encrypted traffic (passwords, tokens, etc.)
- Use only in development/testing environments or with proper authorization
- In production, implement strict filtering for sensitive data
- Consider legal and privacy implications before deploying

## Troubleshooting

If you don't see any SSL/TLS traffic in the logs:

1. Verify the pods are running: `kubectl get pods -l name=ebpf-ssl-uprobe`
2. Check for errors: `kubectl describe pods -l name=ebpf-ssl-uprobe`
3. Ensure the application is using OpenSSL (not other TLS libraries)
4. Check if the OpenSSL version matches what the uprobe is targeting
5. Try using different SSL/TLS clients or applications

## Limitations

- Only works with applications using OpenSSL (not other TLS libraries like GnuTLS, NSS, etc.)
- May need adjustments for different OpenSSL versions
- Cannot capture traffic from applications using statically linked OpenSSL
- Performance impact on SSL/TLS operations

## Cleanup

```bash
kubectl delete -f daemonset.yaml
```
