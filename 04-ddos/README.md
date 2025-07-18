# DDoS Simulation and Protection Demo

This directory contains tools and examples for simulating DDoS attacks and demonstrating protection mechanisms using eBPF (Extended Berkeley Packet Filter) technology.

## 📋 Overview

This project demonstrates how to simulate DDoS attacks for testing and educational purposes, along with an eBPF-based detection system that can identify and mitigate such attacks in real-time.

## 🚀 Features

- DDoS attack simulation using `wrk`
- Real-time attack detection with eBPF
- Educational example of network security monitoring
- Configurable attack parameters

## 🛠 Prerequisites

- Linux system with kernel 4.9+ (for eBPF support)
- Docker installed and running
- `wrk` HTTP benchmarking tool
- Basic understanding of network protocols and DDoS attacks

## 🚀 Quick Start

### Install wrk (if not already installed)

On Debian/Ubuntu:
```bash
sudo apt-get update
sudo apt-get install -y wrk
```

On RHEL/CentOS:
```bash
sudo yum install -y wrk
```

### Simulate a Basic DDoS Attack

Run a simple HTTP load test to simulate a DDoS attack:

```bash
# Basic usage: wrk -t<threads> -c<connections> -d<duration> <URL>
wrk -t10 -c100 -d30s http://10.0.0.11:31084
```

### Parameters Explained

- `-t10`: Use 10 threads to generate load
- `-c100`: Maintain 100 concurrent connections
- `-d30s`: Run the test for 30 seconds
- `--timeout 2s`: Set request timeout (optional)
- `--latency`: Print latency statistics (optional)

## 🎯 Advanced Simulation Scenarios

### Simulate Different Attack Patterns

1. **High Connection Rate Attack**
   ```bash
   wrk -t20 -c500 -d60s --timeout 1s http://10.0.0.11:31084
   ```

2. **Long-running Attack**
   ```bash
   wrk -t5 -c50 -d300s http://10.0.0.11:31084
   ```

3. **With Custom Headers**
   ```bash
   wrk -t10 -c100 -d30s -H "User-Agent: DDoS-Simulation" http://10.0.0.11:31084
   ```

## 🔍 Monitoring the Attack

While the attack is running, you can monitor system resources and network traffic:

```bash
kubectl get pods -n default | grep ebpf

kubectl logs -n default <pod-name> -f
```

## 🛡 eBPF Protection

This repository includes an eBPF-based DDoS detection system in the `01-ebpf` directory. The system can detect and mitigate DDoS attacks in real-time.

To learn more about the protection mechanisms, see the [eBPF DDoS Protection Guide](./01-ebpf/README.md).

## ⚠️ Important Notes

- Only run these simulations in controlled environments
- Ensure you have permission to perform load testing
- Be aware of your network's terms of service
- Monitor system resources to prevent system instability
