# Vagrant K3s Cluster for KCD 2025 Lima

This repository contains the setup for a K3s Kubernetes cluster using Vagrant and VirtualBox, designed for the **Kubernetes Community Days (KCD) 2025 Lima** event.

## Overview

This project sets up a lightweight Kubernetes cluster using K3s with the following architecture:

- **1 Master Node** (`k3s-master`) - 2GB RAM, 2 CPUs
- **2 Worker Nodes** (`k3s-worker1`, `k3s-worker2`) - 1GB RAM, 1 CPU each

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- [Vagrant](https://www.vagrantup.com/downloads) (>= 2.0)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads) (>= 6.0)
- At least 4GB of available RAM
- At least 10GB of available disk space

### For Apple Silicon (M1/M2/M3) Macs

This setup uses `bento/ubuntu-22.04` which is compatible with ARM64 architecture.

## Quick Start

1. **Clone this repository:**

   ```bash
   git clone <repository-url>
   cd vagrant-k3s
   ```

2. **Navigate to the VM directory:**

   ```bash
   cd 01-vm
   ```

3. **Start the cluster:**

   ```bash
   vagrant up
   ```

4. **Check the status:**

   ```bash
   vagrant status
   ```

## Project Structure

```text
vagrant-k3s/
├── README.md
├── .gitignore
├── 01-vm/
│   └── Vagrantfile          # Vagrant configuration
└── 02-setup/
    ├── k3s-master.sh        # K3s master setup script
    └── k3s-worker.sh        # K3s worker setup script
```

## Network Configuration

The cluster uses a private network with the following IP addresses:

- **Master Node**: `10.0.0.11`
- **Worker Node 1**: `10.0.0.12`
- **Worker Node 2**: `10.0.0.13`

## Accessing the Cluster

### SSH into nodes

```bash
# Access master node
vagrant ssh k3s-master

# Access worker nodes
vagrant ssh k3s-worker1
vagrant ssh k3s-worker2
```

### Using kubectl

After the cluster is up, you can access it from the master node:

```bash
vagrant ssh k3s-master
sudo kubectl get nodes
```

To access the cluster from your host machine, you'll need to copy the kubeconfig file:

```bash
# From the master node
vagrant ssh k3s-master
sudo cat /etc/rancher/k3s/k3s.yaml

# Copy the content and save it locally, then update the server IP to 10.0.0.11
```

## Useful Commands

### Vagrant Operations

```bash
# Start all VMs
vagrant up

# Start specific VM
vagrant up k3s-master

# Stop all VMs
vagrant halt

# Restart all VMs
vagrant reload

# Destroy and recreate cluster
vagrant destroy -f && vagrant up

# Check VM status
vagrant status

# SSH into master
vagrant ssh k3s-master
```

### Kubernetes Operations

```bash
# Check cluster status
kubectl get nodes

# Check system pods
kubectl get pods -A

# Deploy a test application
kubectl create deployment nginx --image=nginx
kubectl expose deployment nginx --port=80 --type=NodePort
```

## Troubleshooting

### Common Issues

1. **Architecture mismatch on Apple Silicon:**
   - Ensure you're using an ARM64-compatible base box (already configured)

2. **VirtualBox issues:**
   - Make sure VirtualBox is properly installed and your user has permissions
   - Check that virtualization is enabled in BIOS/UEFI

3. **Network connectivity:**
   - Verify that the private network IPs don't conflict with your host network
   - Check firewall settings if nodes can't communicate

4. **Memory issues:**
   - Ensure your host has enough available RAM (at least 4GB free)
   - Reduce VM memory allocation if needed

### Logs and Debugging

```bash
# Check Vagrant logs
vagrant up --debug

# Check K3s service status on nodes
vagrant ssh k3s-master
sudo systemctl status k3s

vagrant ssh k3s-worker1
sudo systemctl status k3s-agent
```

## Workshop Scenarios

This setup is designed for KCD 2025 Lima workshops and supports:

- Basic Kubernetes operations
- Pod scheduling and management
- Service discovery and networking
- ConfigMaps and Secrets
- Persistent volumes (local storage)
- Basic monitoring and logging

## Contributing

This is a workshop repository for KCD 2025 Lima. If you find issues or have improvements:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Resources

- [K3s Documentation](https://docs.k3s.io/)
- [Vagrant Documentation](https://www.vagrantup.com/docs)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [KCD Lima 2025](https://community.cncf.io/events/details/cncf-lima-presents-kubernetes-community-days-lima-2025/)

## License

This project is open source and available under the [MIT License](LICENSE).

---

**KCD 2025 Lima - Building Cloud Native Communities** 🚀
