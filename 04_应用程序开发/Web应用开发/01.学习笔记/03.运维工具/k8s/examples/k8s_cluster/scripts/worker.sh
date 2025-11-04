#! /bin/bash

# 执行之前保存的，用于往K8s集群中添加工作节点的脚本
/bin/bash /vagrant/configs/join.sh -v

# 如果希望在工作节点中也能使用kubectl，可执行以下命令
sudo -i -u vagrant bash << EOF
mkdir -p /home/vagrant/.kube
sudo cp -i /vagrant/configs/config /home/vagrant/.kube/
sudo chown 1000:1000 /home/vagrant/.kube/config
EOF
