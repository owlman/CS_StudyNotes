#! /bin/bash

KUBERNETES_VERSION="1.21.1-00"

# disable swap 
sudo swapoff -a
sudo sed -ri 's/.*swap.*/#&/' /etc/fstab 

echo "Swap diasbled..."

# disable firewall
sudo ufw disable

# install dependencies
sudo apt-get update -y
sudo apt-get install -y apt-transport-https ca-certificates curl wget software-properties-common
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update -y
sudo apt-get install -y docker-ce

echo "Dependencies installed..."

# configure docker
cat <<EOF | sudo tee /etc/docker/daemon.json
{
  "registry-mirrors": ["https://registry.cn-hangzhou.aliyuncs.com"],
  "exec-opts":["native.cgroupdriver=systemd"]
}
EOF

# start docker
sudo systemctl enable docker
sudo systemctl daemon-reload
sudo systemctl restart docker

echo "Docker installed and configured..."

# install kubelet, kubectl, kubeadm
curl https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg | sudo apt-key add -
cat <<EOF | sudo tee /etc/apt/sources.list.d/kubenetes.list
deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main
EOF

sudo apt-get update -y
sudo apt-get install -y kubelet=$KUBERNETES_VERSION kubectl=$KUBERNETES_VERSION kubeadm=$KUBERNETES_VERSION

sudo systemctl start kubelet  
sudo systemctl enable kubelet   

echo "Installation done..."
