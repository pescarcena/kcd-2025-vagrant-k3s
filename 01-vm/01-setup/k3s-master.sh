#!/bin/bash
# Install K3s on the master node
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC='--write-kubeconfig-mode=644 --flannel-backend=none --disable-network-policy' sh -

# Make sure kubectl is set up for the vagrant user
sudo mkdir -p /home/vagrant/.kube
sudo cp /etc/rancher/k3s/k3s.yaml /home/vagrant/.kube/config
sudo chown -R vagrant:vagrant /home/vagrant/.kube/config

# Get the token for the worker nodes
TOKEN=$(sudo cat /var/lib/rancher/k3s/server/node-token)

# Store the token for the workers to use
echo $TOKEN > /vagrant/token

# Copy the kubeconfig file directly to avoid YAML formatting issues
sudo cp /home/vagrant/.kube/config /vagrant/kube.config

# Update the server URL in the kubeconfig
sudo sed -i 's|server: https://.*|server: https://k3s-master:6443|' /vagrant/kube.config