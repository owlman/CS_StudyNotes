#! /bin/bash

# 指定要安装哪一个版本的K8s
KUBERNETES_VERSION="1.21.1-00"

# 关闭swap分区
sudo swapoff -a
sudo sed -ri 's/.*swap.*/#&/' /etc/fstab 

echo "Swap diasbled..."

# 关闭防火墙功能
sudo ufw disable

# 安装一些 Docker+k8s 环境的依赖项
sudo mv /etc/apt/sources.list /etc/apt/sources.list-backup
sudo cp -i /vagrant/scripts/apt/sources.list /etc/apt/ 
sudo apt update -y
sudo apt install -y apt-transport-https ca-certificates curl wget software-properties-common build-essential

echo "Dependencies installed..."

# 安装并配置 Docker CE
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update -y
sudo apt install -y docker-ce

cat <<EOF | sudo tee /etc/docker/daemon.json
{
  "registry-mirrors": ["https://registry.cn-hangzhou.aliyuncs.com"],
  "exec-opts":["native.cgroupdriver=systemd"]
}
EOF

# 启动 Docker
sudo systemctl enable docker
sudo systemctl daemon-reload
sudo systemctl restart docker

echo "Docker installed and configured..."

# 安装 k8s 组件：kubelet, kubectl, kubeadm
curl https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg | sudo apt-key add -
cat <<EOF | sudo tee /etc/apt/sources.list.d/kubenetes.list
deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main
EOF
sudo apt update -y
sudo apt install -y kubelet=$KUBERNETES_VERSION kubectl=$KUBERNETES_VERSION kubeadm=$KUBERNETES_VERSION

# 如果想阻止自动更新，可以选择锁住相关软件的版本
sudo apt-mark hold kubeadm kubectl kubelet

# 启动 K8s 的服务组件：kubelet
sudo systemctl start kubelet  
sudo systemctl enable kubelet   

echo "K8s installed and configured..."
