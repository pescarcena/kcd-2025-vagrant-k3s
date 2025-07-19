# Simple kprobe eBPF Example

This example demonstrates how to use eBPF kprobes to monitor system calls in a Kubernetes cluster. The probe attaches to the `openat` syscall to detect when files are opened by processes.

## Overview

The `simple_kprobe.py` script uses BCC (BPF Compiler Collection) to:

1. Attach to the `openat` syscall using a kprobe
2. Capture process information when files are opened
3. Report the process name and PID for monitoring purposes

## Prerequisites

- Docker installed for building the container image
- Access to a Kubernetes cluster (K3s with Vagrant in this setup)
- `kubectl` configured to communicate with your cluster

## Build and Push the Container Image

```bash
# Replace <username> with your Docker Hub username
docker build -t <username>/ebpf-simple-kprobe .
docker push <username>/ebpf-simple-kprobe
```

## Deploy to Kubernetes

The DaemonSet ensures the eBPF probe runs on every node in the cluster:

```bash
# Update the image name in daemonset.yaml if needed
kubectl apply -f daemonset.yaml
```

## Testing the Probe

SSH into one of the worker nodes and perform file operations:

```bash
# Connect to a worker node
vagrant ssh k3s-worker1

# Run commands that open files
cat /etc/hosts
ls -la /etc
```

## Monitoring the Probe Output

View the logs from the eBPF probe pods:

```bash
# View all logs
kubectl logs -l name=ebpf-simple-kprobe -f

# Filter for specific processes (e.g., cat)
kubectl logs -l name=ebpf-simple-kprobe -f | grep cat
```

## How It Works

The probe attaches to the kernel's `openat` syscall, which is called whenever a process opens a file. When triggered, it captures the process ID and name, then sends this data to userspace where it's displayed in the pod logs.

## Troubleshooting

If you don't see any output:

1. Verify the pods are running: `kubectl get pods -l name=ebpf-simple-kprobe`
2. Check for errors: `kubectl describe pods -l name=ebpf-simple-kprobe`
3. Ensure the host has the proper kernel headers installed

## Cleanup

```bash
kubectl delete -f daemonset.yaml
```
