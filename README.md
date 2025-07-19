# Kubernetes eBPF Monitoring and DDoS Protection Demo

## 🌟 KCD Lima 2025 Workshop Project

This repository contains a complete demonstration environment for showcasing eBPF-based monitoring and DDoS protection in Kubernetes. It was created for the Kubernetes Community Days (KCD) Lima 2025 workshop.

## 📋 Overview

This project demonstrates how to:

1. Set up a local Kubernetes cluster using K3s and Vagrant
2. Deploy and use Cilium as a CNI for advanced networking capabilities
3. Implement various eBPF probes for monitoring system and network activity
4. Simulate and detect DDoS attacks using eBPF-based protection

## 🗂️ Repository Structure

The repository is organized into the following modules, each with its own detailed README:

### [01-vm](./01-vm/)

Contains Vagrant configuration and scripts to set up a 3-node K3s cluster (1 master, 2 workers) with Cilium CNI.

### [02-probe](./02-probe/)

Collection of eBPF probes for different monitoring scenarios:

- [01-simple-kprobe](./02-probe/01-simple-kprobe/): Basic kernel probe example for monitoring file operations
- [02-httpebpf](./02-probe/02-httpebpf/): HTTP traffic monitoring using eBPF
- [03-sslebpf](./02-probe/03-sslebpf/): SSL/TLS traffic monitoring using eBPF uprobes

### [03-ddos](./03-ddos/)

Tools and examples for DDoS attack simulation and protection:

- [01-ebpf](./03-ddos/01-ebpf/): eBPF-based DDoS detection and mitigation
- [02-deploy](./03-ddos/02-deploy/): Deployment configurations for testing DDoS scenarios

### [04-cilium](./04-cilium/)

Cilium-specific configurations, Hubble observability setup, and network policy examples.

## 🚀 Getting Started

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/vagrant-k3s.git
   cd vagrant-k3s
   ```

2. **Set up the K3s cluster**
   ```bash
   cd 01-vm
   vagrant up
   ```

3. **Configure kubectl**
   ```bash
   export KUBECONFIG=$(pwd)/kube.config
   kubectl get nodes
   ```

4. **Follow module-specific instructions**
   Each module has its own README with detailed instructions.

## 📊 Workshop Modules

1. **Cluster Setup**: Learn how to set up a Kubernetes cluster with Cilium CNI
2. **Basic eBPF Monitoring**: Explore simple kprobes for system call monitoring
3. **Advanced Network Monitoring**: Implement HTTP and SSL/TLS traffic monitoring
4. **DDoS Protection**: Simulate attacks and implement eBPF-based protection
5. **Network Observability**: Use Hubble for advanced network visibility

## 🛠️ Prerequisites

- [Vagrant](https://www.vagrantup.com/downloads) (2.2.x or later)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads) (6.1.x or later)
- At least 8GB RAM available for VMs
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) for cluster interaction
- [Docker](https://docs.docker.com/get-docker/) for building container images

## 📝 Notes

- This environment is designed for educational purposes
- Resource requirements can be adjusted in the Vagrantfile
- All examples include cleanup instructions to reset your environment

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

*Created for Kubernetes Community Days Lima 2025*