# Cilium Network Observability and Security

This directory contains configurations and tools for monitoring and securing your Kubernetes cluster using Cilium's advanced networking features.

## 🚀 Features

- **Network Policy Enforcement**: Secure your cluster with L3-L7 network policies
- **Hubble Observability**: Real-time network traffic monitoring
- **DDoS Protection**: Monitor and mitigate potential DDoS attacks
- **Service Mesh**: Built-in service mesh capabilities

## 📋 Prerequisites

- A running Kubernetes cluster with Cilium CNI installed
- `kubectl` configured to communicate with your cluster
- `cilium` CLI installed on your local machine

## 🛠 Installation & Setup

### 1. Install Cilium CLI

```bash
# Download and install the Cilium CLI
CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/main/stable.txt)
curl -L --remote-name-all https://github.com/cilium/cilium-cli/releases/download/${CILIUM_CLI_VERSION}/cilium-darwin-arm64.tar.gz{,.sha256sum}
shasum -a 256 -c cilium-darwin-arm64.tar.gz.sha256sum
sudo tar xzvfC cilium-darwin-arm64.tar.gz /usr/local/bin
rm cilium-darwin-arm64.tar.gz cilium-darwin-arm64.tar.gz.sha256sum
```

### 2. Install Cilium in the Cluster

```bash
# Install Cilium with custom IPAM settings
cilium install --version 1.17.6 --set=ipam.operator.clusterPoolIPv4PodCIDRList="10.42.0.0/16"

# Verify installation
cilium status
```

## 🔭 Enabling Hubble for Network Observability

### Basic Hubble Setup

```bash
# Enable Hubble with the default configuration
cilium hubble enable
```

### Enable Hubble UI (Optional)

```bash
# Enable Hubble UI components
cilium hubble enable --ui

# Port-forward the Hubble UI to localhost
cilium hubble ui
```

> The UI will be available at http://localhost:12000

## 🛡 DDoS Testing

To test DDoS protection capabilities, you can use the included test script:

```bash
# Make the script executable
chmod +x ddos-test.sh

# Run the DDoS test
./ddos-test.sh
```

### Test Script Details

The `ddos-test.sh` script simulates a DDoS attack using `wrk` with the following parameters:
- `-t10`: 10 threads
- `-c100`: 100 concurrent connections
- `-d30s`: 30 seconds duration
- Target: `http://10.0.0.11:31084`

## 📊 Monitoring with Hubble

While the DDoS test is running, you can observe the traffic in Hubble:

1. Open the Hubble UI: `cilium hubble ui`
2. Navigate to the "Flows" section
3. Apply filters to monitor the test traffic

## 🔍 Useful Commands

```bash
# Check Cilium status
cilium status

# View Cilium system pods
kubectl get pods -n kube-system -l k8s-app=cilium

# View Hubble pods
kubectl get pods -n kube-system -l k8s-app=hubble
```

## 🧹 Cleanup

To completely remove Cilium from your cluster:

```bash
cilium uninstall
```

## 📚 Resources

- [Cilium Documentation](https://docs.cilium.io/)
- [Hubble Documentation](https://docs.cilium.io/en/stable/overview/intro/#hubble)
- [Cilium GitHub](https://github.com/cilium/cilium)

## ⚠️ Note

This setup is for testing and educational purposes. For production environments, please refer to the official Cilium documentation for recommended configurations and security practices.
```