# eBPF DDoS Detection Example

A practical example demonstrating how to use eBPF (Extended Berkeley Packet Filter) for detecting potential DDoS attacks by tracing network traffic patterns.

## Overview

This project showcases the power of eBPF for network security monitoring, specifically focusing on DDoS attack detection. It includes a simple eBPF program that monitors network traffic and identifies potential DDoS patterns.

## Features

- Real-time network traffic monitoring using eBPF
- Basic DDoS attack detection mechanisms
- Lightweight and efficient implementation
- Easy-to-understand example for educational purposes

## Prerequisites

- Linux kernel 4.9 or later (with eBPF support)
- Docker
- `bpftool` and kernel headers (for local development)
- Basic understanding of eBPF and network security concepts

## Building the Project

Build the Docker image:

```bash
docker build -t pescarcena/ebpf-trace-example .
```

## Acknowledgments

- The eBPF community for their amazing work
- Cilium and BCC projects for inspiration
- All open-source contributors who made eBPF accessible