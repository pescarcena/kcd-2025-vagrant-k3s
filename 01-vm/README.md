# K3s Cluster with Cilium CNI

This project sets up a local Kubernetes cluster using K3s with Cilium as the Container Network Interface (CNI). The cluster consists of one master and two worker nodes running in Vagrant VMs.

## 🚀 Quick Start

1. **Start the Cluster**
   ```bash
   cd 01-vm
   vagrant up
   ```

2. **Configure kubectl**
   ```bash
   export KUBECONFIG=$(pwd)/kube.config
   ```

3. **Update Hosts File**
   Add the following line to your `/etc/hosts` file to avoid certificate issues:
   ```bash
   echo "10.0.0.11 k3s-master" | sudo tee -a /etc/hosts
   ```
   > This ensures proper hostname resolution for the Kubernetes API server

4. **Verify Cluster Status**
   ```bash
   kubectl get nodes
   ```
   > Note: Nodes will initially show as `NotReady` until we install Cilium.

## 🔧 Network Configuration

K3s is installed without the default Flannel CNI. Instead, we'll use Cilium for advanced networking features:

1. **Install Cilium**
   ```bash
   # Install Cilium CLI
   curl -L --remote-name-all https://github.com/cilium/cilium-cli/releases/latest/download/cilium-linux-amd64.tar.gz{,.sha256sum}
   sha256sum --check cilium-linux-amd64.tar.gz.sha256sum
   sudo tar xzvfC cilium-linux-amd64.tar.gz /usr/local/bin
   rm cilium-linux-amd64.tar.gz{,.sha256sum}

   # Install Cilium in the cluster
   cilium install --version 1.17.6 \
     --set=ipam.operator.clusterPoolIPv4PodCIDRList="10.42.0.0/16"
   ```

2. **Verify Cilium Installation**
   ```bash
   cilium status
   kubectl -n kube-system get pods -l k8s-app=cilium
   ```

3. **Check Node Status**
   ```bash
   kubectl get nodes
   ```
   > Nodes should now show as `Ready`

## 🌐 Accessing the Cluster

- **Kubernetes Dashboard**: Not installed by default
- **kubectl**: Configured to use the local `kube.config`
- **Node IPs**:
  - Master: `10.0.0.11`
  - Worker1: `10.0.0.12`
  - Worker2: `10.0.0.13`

## 🛠 Management

- **Start all VMs**: `vagrant up`
- **Stop all VMs**: `vagrant halt`
- **Destroy all VMs**: `vagrant destroy -f`
- **SSH into a node**: `vagrant ssh k3s-master` (or `k3s-worker1`, `k3s-worker2`)

## 🔍 Troubleshooting

### Common Issues

1. **Nodes Not Ready**
   - Ensure Cilium is installed and all pods are running:
     ```bash
     kubectl -n kube-system get pods
     ```

2. **Network Issues**
   - Check Cilium status:
     ```bash
     cilium status
     ```
   - View Cilium logs:
     ```bash
     kubectl -n kube-system logs -l k8s-app=cilium
     ```

3. **Vagrant Issues**
   - If VMs fail to start, try:
     ```bash
     vagrant plugin repair
     vagrant up
     ```

## 📚 Resources

- [K3s Documentation](https://rancher.com/docs/k3s/latest/en/)
- [Cilium Documentation](https://docs.cilium.io/)
- [Vagrant Documentation](https://www.vagrantup.com/docs)

## 📄 License

This project is provided as-is with no warranties. Use at your own risk.
