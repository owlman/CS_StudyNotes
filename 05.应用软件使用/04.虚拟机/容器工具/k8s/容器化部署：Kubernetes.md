# 容器化部署：Kubernetes

在接下来的这篇笔记中，我将会介绍 Kubernetes 这一强大的容器编排工具，并学习其基本使用方法。该笔记将会被存储在`https://github.com/owlman/study_note`项目的`Software/Container`目录下一个名为`K8s`的子目录中。其具体内容将包含：

- 了解 Kubernetes 的核心设计理念和它的基本组成结构；
- 掌握使用 Kubernetes 构建服务器集群的基本工作流程；
- 掌握如何在服务器集群中实现应用程序的容器化运维；

## 学习规划

- 学习基础：
  - 有一两门编程语言的使用经验。
  - 有一定的 Web 开发及维护经验。
- 视频资料：
  - [麦兜搞IT的K8s系列](https://space.bilibili.com/364122352/channel/collectiondetail?sid=588615)：哔哩哔哩上的视频教程。
- 阅读资料：
  - [《深入剖析Kubernetes》](https://book.douban.com/subject/35424872/)：本人学习所用书籍。
- 学习目标：
  - 使用 Docker+Kubernetes 发布并维护自己的私人项目。

## Kubernetes 简介

在实际生产环境中，许多企业级规模的应用程序为了获得更好的执行性能和负载能力，经常会选择在多台设备组成的服务器集群上进行分布式部署，其中涉及到的容器数量可能会多达上百个。如果我们需要在这种服务器集群环境中实现应用程序的自动化部署与维护，容器编排工作的难度将会得到进一步增加。为了更好地应对这项工作，我们在这里会更新于推荐读者使用 Kubernetes（以下简称为 K8s [^1]）这个更为强大的容器编排工具。

K8s 是 Google 公司于 2014 年推出的一个开源的容器编排工具，它近年来一直被公认为是在服务器集群环境中对应用程序进行容器化部署的最佳解决方案。该工具最核心的功能是能实现容器的自主管理，这可以保证我们在服务器集群环境中部署的应用程序能按照指定的容器编排规则来实现自动化的部署和维护。换而言之，如果我们想部署一个名为“线上简历”的应用程序，就只需要在容器编排文件中定义好部署该应用程序中各项微服务时所需要创建的容器，以及这些容器之间通信方案、数据持久化方案、负载均衡方案等规则。然后，K8s、就会和 Docker Compose 一样自动去实例化并启动这些容器以及相关网络、数据存储等基础设施，并持续确保这些容器的运行状态，以及按照预定方式对其进行负载均衡，但不同的是，K8s还会根据应用程序中各项微服务的具体负载状态自动调整相关容器实例在服务器集群中的具体运行节点。总而言之，K8s更着重于为应用程序的用户提供不间断的服务状态。

为了更好地实现基于微服务架构的应用程序部署方案，K8s的开发者在设计上对服务器设备上计算资源的调度单元进行了一系列高层次的抽象。正是因为有了这些抽象化的资源调度对象，运维人员才能得以像管理单一主机的不同部件一样管理一个服务器集群，因为他们只需要基于一些抽象的资源调度对象来定义应用程序的部署和维护方案，然后交由k8s自行决定如何在物理层面上执行这些方案。所以在具体学习K8s的使用方法之前，我们有必要先了解一下该工具的核心组成结构及其背后的软件架构。

### 核心组成结构

K8s 相较于其他容器编排工具的独到之处在于，它同时在物理组织和软件架构这两个层面上对服务器集群环境进行了抽象化设计。首先，在面对服务器集群中的多台物理主机时，K8s将应用程序的部署环境抽象化成了一个分布式的软件管理系统，它在逻辑上将服务器集群中的所有物理主机定义为一个主控节点和若干个工作节点。其中，主控节点（Master）用于调度并管理部署在 K8s 系统中的应用程序，而工作节点（Worker）则用于运行具体的容器实例，可被视为供K8s系统调度的计算资源。其具体组成结构如下图所示。

![K8s组成结构](https://img2023.cnblogs.com/blog/691082/202305/691082-20230529103945956-1660848197.png)

从上述结构图中，我们可以看出 K8s 被设计成了一个与 Linux 有几分相似的分层系统，其核心层包含了以下一系列功能组件。

- kubelet 组件，用于管理部署在服务器集群环境中的所有容器及其镜像，同时也负责数据卷和内部网络的管理；
- proxy 组件：用于对 K8s 中的调度单元执行反向代理、内部通信、负载均衡等作业；
- etcd 组件：用于保存整个服务器集群的运行状态，这些数据通常存储于主控节点中；
- API Server 组件：用于负责对外提供服务器集群中各类计算资源的操作接口，它同时也是集群中各组件数据交互和通信的枢纽，主要用于处理 REST 操作，并在 etcd 组件中验证、更新相关资源对象的状态（并存储）；
- Scheduler 组件：用于负责服务器集群中计算资源的调度，其基本原理是先通过监听 API Server 组件来获取可调度的计算资源，然后再基于一系列筛选和评优算法来对这些资源进行任务分配；
- Controller Manager 组件： 该组件会基于一种被称为 Controller 的资源调度概念（我们稍后会详细介绍它）来实现对服务器集群中所有容器的编排作业；
- Container Runtime 组件：用于管理容器的镜像及它们在 K8s 调度单元中的实例化与运行；

除了上述核心组件之外，K8s 在外层还设计有一个开放性的插件体系，我们还可以根据自己的需要为其安装不同的插件。例如：kube-dns 可以用于为整个服务器集群提供域名解析服务、Ingress Controller 可为应用程序提供外网入口、coredns 插件可用于建立服务器集群内部网络等。通过利用该插件系统带来的可扩展性，运维人员就能实现在逻辑层面上像操作一台主机中的不同组件一样对服务器集群进行管理，任意为其新增相关的功能。

总而言之，为了给运维人员提供一个可以在多台服务器设备上部署、维护和扩展应用程序的自动化机制，K8s 被定义成了一系列松耦合的构建模块和具有高度可扩展性的分布式系统。但从某种程度上来说，如果我们想用 K8s 灵活地应对各种工作场景对应用程序负载能力的要求，还必须要要在上述组成结构的基础上理解 K8s 的软件架构。也就是说，在具体介绍如何在跨服务器环境中进行应用程序的部署和维护之前，我们还需要先来了解一下 K8s 在软件层面上的架构设计。

### 软件架构设计

在软件的架构设计上，K8s 的设计者也针对服务器集群中可调度的计算资源进行了抽象。换而言之，我们在 K8s 中所进行的所有运维工作实际上都需要通过以下一系列基于这些抽象的资源对象来完成。

- **Pod**：这是在 K8s 中部署应用程序时可调度的最小资源对象，它本质上是针对容器分组部署工作所进行的一种抽象。在K8s的设计中，被部署在同一个 Pod 中的容器将会始终被部署到同一个物理服务器上，并且每个 Pod 都将会被整个集群的内部网络自动分配一个唯一的 IP 地址，这样就可以允许应用程中的不同组件序使用同一端口，不必担心会发生端口冲突的问题。另外，某些 Pod 还可以被定义成一个独立的数据卷，并将其映射到某个本地磁盘目录或网络磁盘，以供其他Pod中的容器访问。

- **ReplicationController**：这是一种针对 Pod 的运行状态进行抽象的资源对象。该对象是早期版本的 K8s 中 ReplicaSet 对象的升级，这两种对象主要用于确保在任何时候都有特定数量的 Pod 实例处于运行状态。和 Pod 一样，我们通常不会直接手动创建和管理这一级的抽象对象，而是直接通过 deployment 等 Controller 对象来对它们进行自动化管理、

- **Controller**：在通常情况下，我们虽然也可以通过定义基于 Pod 的容器编排规则和相关的 K8s 客户端命令来实现对 Pod 的手动调度，但如果想最大限度地发挥 K8s 的优势，运维人员更多时候会选择使用更高层次的抽象机制来实现自动化调度。其中，Controller 是一种针对 Pod 或 ReplicationController 的运行状态进行控制的资源对象。在 K8s 中，内置的 Controller 对象主要有以下五种。
  - deployment：适合用于部署无状态的服务，例如 HTTP 服务；
  - StatefullSet：适合用于部署有状态的服务，例如数据库服务；
  - DaemonSet：适合需要在服务器集群的所有节点上部署相同实例的服务，例如分布式存储服务。
  - Job：适合用于执行一次性的任务，例如离线数据处理、视频解码等任务；
  - Cronjob：适合用于执行周期性的任务，例如信息通知、数据备份等任务；

- **Service**：它可以被视为是一种以微服务架构的视角来组织和调度 Pod 的资源对象，K8s 会通过给 Service 分配静态 IP 地址和域名，并且以轮循调度的方式对应用程序的流量执行负载均衡作业。在默认情况下，Service 既可以被暴露在服务器集群的内部网络中，也可以被暴露给服务器集群的外部外部网络。

- **namespace**：如果我们希望将一个物理意义上的服务器集群划分成若干个虚拟的集群环境，用于部署不同的应用程序，就可以使用 namespace 这一抽象概念对物理层面上的计算资源加以划分。

正如之前所说，有了上面介绍的这些资源调度对象，运维人员就可以根据具体的需求来定义应用程序的部署和维护方案了，k8s 将会自行决定如何在物理层面上执行这些方案。接下来，我们的任务就是要带领大家构建一个基于 K8s 的服务器集群，然后演示如何在该集群环境中定义容器编排规则，并实际部署应用程序。

## 构建 K8s 服务器集群

接下来，我们要为大家演示如何构建一个用于部署“线上简历”示例程序的K8s三机集群。为此，我们需要准备三台安装了 Ubuntu 20.04 系统的计算机设备。在实际生产环境中，我们通常会选择去实际购买相应的物理设备或者云主机。但即使对于一些企业级用户来说，采用这种方案也会是一笔不小的开销，用来本书所需要的演示环境就显得更不经济了，因此使用虚拟机软件可能是一个更具有可行性的选择。于是，我们使用 Vagrant+VirtualBox 工具构建出了一个以下配置的服务器集群。

|   主机名    |     IP地址     | 内存 | 处理器数量 |   操作系统   |
| :---------: | :------------: | :--: | :--------: | :----------: |
| k8s-master  | 192.168.100.21 |  4G  |     2      | Ubuntu 20.04 |
| k8s-worker1 | 192.168.100.22 |  2G  |     2      | Ubuntu 20.04 |
| k8s-worker2 | 192.168.100.23 |  2G  |     2      | Ubuntu 20.04 |

在完成设备方面的准备之后，我们接下来的工作是要在上述三台设备上安装与配置 Docker+K8s 环境，并将名为 k8s-master 的主机设置成服务器集群的主控节点，而 k8s-worker1 和 k8s-worker2 这两台主机则设置为工作节点。为此，我们需要执行以下步骤的操作。

### 安装 Docker+K8s 环境

为了让 K8s 服务器集群的搭建过程成为一个可重复的自动化工作流程，我决定使用 Shell 脚本的方式来完成相关的安装与配置工作。为此，我们首先需要分别进入到上述三台主机中，并通过执行以下脚本文件来完成 Docker+K8s 环境的安装与基本配置。

```bash
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
sudo apt update -y
sudo apt install -y apt-transport-https ca-certificates curl wget software-properties-common

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

# 如果想禁止K8s的自动更新，可以锁住上述组件的版本
sudo apt-mark hold kubeadm kubectl kubelet

# 启动 K8s 的服务组件：kubelet
sudo systemctl start kubelet  
sudo systemctl enable kubelet   

echo "K8s installed and configured..."
```

在上述脚本执行完成之后，用户可以通过执行`kubeadm version` 和`kubectl version`这两个命令来确认一下安装成果，如果这些命令正常输出了相应的版本信息，就说明 K8s 已经可以正常使用了。另外在该脚本文件中，我们可以看到除了之前已经熟悉了的、用于安装和配置 Docker CE 的操作之外，它执行的主要操作就是安装 kubeadm、kubectl 和 kubelet 三个软件包。其中，kubeadm 是 K8s 集群的后台管理工具，主要用于快速构建 k8s 集群并管理该集群中的所有设备，kubectl 是 K8s 集群的客户端工具，主要用于在 K8s 集群中对应用程序进行具体的部署与维护工作，而 kubelet 则是 K8s 集群部署在其每一台主机上的服务端组件，主要用于响应客户端的操作并维持应用程序在集群上的运行状态。

### 设置主控节点与工作节点

接下来的工作是为 K8s 集群设置主控节点与工作节点。为此，我们需要先单独进入到名为 k8s-master 的主机中，并通过执行以下脚本文件来将其设置成集群的主控节点。

```bash
#! /bin/bash

# 指定主控节点的IP地址
MASTER_IP="192.168.100.21"
# 指定主控节点的主机名
NODENAME=$(hostname -s)
# 指定当前 K8s 集群中 Pod 所使用的 CIDR
POD_CIDR="10.244.0.0/16"
# 指定当前 K8s 集群中 Service 所使用的 CIDR
SERVICE_CIDR="10.96.0.0/12"
# 指定当前使用的 K8s 版本
KUBE_VERSION=v1.21.1

# 特别预先加载 coredns 插件
COREDNS_VERSION=1.8.0
sudo docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/coredns:$COREDNS_VERSION
sudo docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/coredns:$COREDNS_VERSION registry.cn-hangzhou.aliyuncs.com/google_containers/coredns/coredns:v$COREDNS_VERSION

# 使用 kubeadm 工具初始化 K8s 集群
sudo kubeadm init \
--kubernetes-version=$KUBE_VERSION \
--apiserver-advertise-address=$MASTER_IP \
--image-repository=registry.cn-hangzhou.aliyuncs.com/google_containers \
--service-cidr=$SERVICE_CIDR \
--pod-network-cidr=$POD_CIDR \
--node-name=$NODENAME \
--ignore-preflight-errors=Swap

# 生成主控节点的配置文件
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# 将主控节点的配置文件备份到别处
config_path="/vagrant/configs"

if [ -d $config_path ]; then
sudo rm -f $config_path/*
else
sudo mkdir -p $config_path
fi

sudo cp -i /etc/kubernetes/admin.conf $config_path/config
sudo touch $config_path/join.sh
sudo chmod +x $config_path/join.sh       

# 将往 K8s 集群中添加工作节点的命令保存为脚本文件
kubeadm token create --print-join-command > $config_path/join.sh

# 安装名为 flannel 的网路插件
sudo wget https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
sudo kubectl apply -f kube-flannel.yml

# 针对 Vagrant+VirtualBox 虚拟机环境的一些特定处理
sudo -i -u vagrant bash << EOF
mkdir -p /home/vagrant/.kube
sudo cp -i /vagrant/configs/config /home/vagrant/.kube/
sudo chown 1000:1000 /home/vagrant/.kube/config
EOF
```

在上述脚本中，除了因国内网络环境而使用了基于阿里云的镜像来对 coredns 插件进行的预加载操作之外，我们的主要工作就是使用 kubeadm 工具对 K8s 集群进行初始化。在这里，`kubeadm init`命令会自动将当前主机设置为整个集群的主控节点，我们在执行该命令时需提供以下参数。

- `kubernetes-version`参数：该参数用于指定当前使用的K8s版本。
- `apiserver-advertise-address`参数：该参数用于指定访问当前K8s集群的API Server时需要使用的IP地址，通常就是主控节点所在主机的IP地址。
- `image-repository`参数：该参数用于指定当前K8s集群所使用的远程容器镜像仓库，在这里，我们使用的是位于中国境内的阿里云镜像仓库。
- `service-cidr`参数：该参数用于指定当前K8s集群中Service对象的CIDR，这决定了这些Service对象在该集群内部网络中可被分配的IP地址段。
- `pod-network-cidr`参数：该参数用于指定当前K8s集群中Pod对象的CIDR，这决定了这些Pod对象在该集群内部网络中可被分配的IP地址段。
- `node-name`参数：该参数用于指定当前节点在K8s集群中的名称，通常情况下，我们会将其设置为当前主机的名称。
- `ignore-preflight-errors`参数：该参数用于指定要忽略的预检错误。

如果一切顺利的话，在`kubeadm init`命令执行完成之后，当前主机就成功地被设置成为了当前 K8s 集群的主控节点。接下来，我们需要继续执行两项善后工作。首先要做的是将当前 K8s 集群的配置文件备份至别处，并复制一份到我们在主控节点的`$HOME/.kube/`目录下，这样一来，我们就可以在主控节点中使用 kubectl 客户端工具操作整个集群了。

其次，我们将用于往当前K8s集群中添加工作节点的命令保存成为了一个名为`join.sh`的 Shell 脚本文件，并将其备份至别处（在这里，就是将其备份至`/vagrant/configs/`目录中）。然后，我们就只需要再分别进入到 k8s-worker1 和 k8s-worker2 这两台主机中，并通过执行以下脚本文件来将其设置成 K8s 服务器集群的工作节点。

```bash
#! /bin/bash

# 执行之前保存的，用于往K8s集群中添加工作节点的脚本
/bin/bash /vagrant/configs/join.sh -v

# 如果希望在工作节点中也能使用kubectl，可执行以下命令
sudo -i -u vagrant bash << EOF
mkdir -p /home/vagrant/.kube
sudo cp -i /vagrant/configs/config /home/vagrant/.kube/
sudo chown 1000:1000 /home/vagrant/.kube/config
EOF
```

如果读者仔细查看一下`join.sh`文件的内容，就会看到往当前 K8s 集群中添加工作节点的操作是通过`kubeadm join`命令来实现的，该命令在当前 K8s 集群中的使用方式，会在`kubeadm init`命令执行成功之后，以返回信息的形式提供给用户，其大致形式如下。

```bash
kubeadm join 192.168.100.21:6443 --token 6e2oxk.affn2w8jqe4vkr0p --discovery-token-ca-cert-hash sha256:c6c928b4f4e6403b9d05bde57511aa1742e0254344219c7ca94848175bbab1fe 
```

正如读者所见，我们在执行`kubeadm join`命令时通常需要提供以下参数。

- `[K8s API Server]`：在该参数中，我们会指定当前 K8s 集群的 API Server 所使用的 IP 地址和端口号，通常情况下就是主控节点的 IP 地址，默认端口为`6443`。
- `token`参数：该参数用于指定加入当前 K8s 集群所需要使用的令牌，该令牌会在`kubeadm init`命令执行成功之后，以返回信息的形式提供给用户。
- `discovery-token-ca-cert-hash`参数：该参数是一个 hash 类型的值，主要用于验证加入令牌的 CA 公钥，该 hash 值也会在`kubeadm init`命令执行成功之后，以返回信息的形式提供给用户。

### 使用 kubectl 远程操作集群

到目前为止，我们在操作 K8s 集群的时候，都需要先进入到该集群的主控节点中，然后使用 kubectl 等工具对其进行操作。但在现实生产环境中，我们能直接进入到主控节点的机会并不多，因为该服务器设备大概率位于十万八千里之外的某个机房里，我们甚至都不知道它是一台实体设备还是虚拟云主机。当然，我们也可以在以 Windows 或 macOS 为操作系统的个人工作机上先使用 SSH 等远程登录的方式进入到集群的主控节点中，然后再执行 K8s 的相关操作，但更为专业的做法是直接在工作机上使用 kubectl 客户端工具远程操作 K8s 集群，为此，我们需要在工作机上进行如下配置。

1. 通过在搜索引擎中搜索“kubectl”找到该客户端工具的官方下载页面，然后根据自己工作机使用的操作系统下载相应的安装包，并将 kubectl 安装到工作机中。

2. 进入到 Windows 或 macOS 的系统用户目录中。如果读者使用的是 Windows 10/11 系统，该目录就是`C:\Users\<你的用户名>`；如果使用的是 macOS 系统，该目录就是`/user/<你的用户名>`；如果使用的是 Ubuntu 这样的 Linux 系统，该目录就是`/home/<你的用户名>`。

3. 在系统目录中创建一个名为`.kube`目录，并将之前保存的、名为`config`的K8s集群配置文件复制到其中。

4. 在个人工作机上打开 Powershell 或 Bash 这样的命令行终端环境，并执行`kubectl get nodes`命令，如果得到如下输出，就说明我们已经可以在当前设备上对之前创建的 K8s 集群进行操作了。

```bash
$ kubectl get nodes

NAME          STATUS     ROLES                  AGE   VERSION
k8s-master    Ready      control-plane,master   22h   v1.21.1
k8s-worker1   Ready      <none>                 20h   v1.21.1
k8s-worker2   Ready      <none>                 21h   v1.21.1
```

## 项目实践

在完成了 K8s 集群的环境构建之后，我们就可以正式地在该服务器集群中开展应用程序的运维工作了。下面，就让我们来具体介绍一下在使用 K8s 对“线上简历”应用程序进行部署的基本步骤、容器编排文件的编写规则、运维工作时会遇到的使用场景，以及在这些场景中会使用到的相关命令吧。

### 部署应用的基本步骤

现在，让我们先来演示一下如何将应用程序部署到 K8s 集群中，并将其运行起来。正如之前所说，K8s 的核心设计目标就将物理上由多台主机组成的服务器集群抽象成一台逻辑层面上的单机环境，以便用户可以像管理一台主机中的不同组件一样管理服务器集群中的计算资源。因此，使用 K8s 部署应用程序的步骤其实和我们之前使用 Docker Compose 在单一服务器环境中部署应用程序的步骤是大同小异的。接下来，我们就来具体演示一下如何使用 K8s 来完成“线上简历”应用程序的部署。

1. 在 K8s 集群的主控节点上创建一个名为`online_resumes`的目录，并使用 Git 或 FTP 等工具将我们之前已经编写好了的、“线上简历”应用程序的源码复制到该目录中。

2. 进入到`online_resumes`目录中，并根据已有的`Dockerfile`文件来执行`sudo docker image build -t online_resumes .`命令。该命令会将应用程序的核心业务模块打包成一个新的Docker镜像。待命令执行完成之后，我们就可以在`docker image ls`命令返回的本地镜像列表中看到这个名为`online_resumes`的镜像了。

3. 由于我们使用的是一个三机组成的集群环境，所以还需要继续在主控节点中使用`docker image save -o /vagrant/k8s_yml/resumes.img online_resumes`命令将刚才创建的镜像以文件的形式导出并保存到别处（这里的`/vagrant`目录是Vagrant设置的虚拟机共享目录）。然后分别进入到另外两个工作节点中，通过执行`docker image load -i /vagrant/k8s_yml/resumes.img`命令将该镜像加载到 Docker 镜像列表中。当然，如果读者注册了 Docker Hub 这样的远程仓库服务，也可以使用`docker push`命令将镜像推送到远程仓库中，让 K8s 自动拉取它们。

4. 在K8s集群的主控节点上执行`sudo kubectl create namespace online-resumes`命令，以便在该集群中单独创建一个用于部署“线上简历”应用程序的namespace。

5. 由于“线上简历”应用程序的核心业务模块是一个基于 HTTP 协议的无状态服务，所以我们打算使用 Deployment 类型的控制器编排容器，并将其部署成 K8s 集群的一个 Service。为此，我们需要在`online_resumes`目录下创建一个名为`express-deployment.yml`的资源定义文件，其具体内容如下。

    ```yaml
    apiVersion: apps/v1 # 指定Deployment API的版本，
                                    # 可用kubectl api-versions命令查看
    kind: Deployment   # 定义资源对象的类型为Deployment
    metadata:              # 定义Deploynent对象的元数据信息
    name: express-deployment # 定义Deploynent对象的名称
    namespace: online-resumes # 定义Deploynent对象所属的命名空间
    spec:    # 定义Deploynent对象的具体特征
    replicas: 3 # 定义Deploynent对象要部署的数量
    selector: # 定义Deploynent对象的选择器，以便其他对象引用
        matchLabels: # 定义该选择器用于匹配的标签
        app: resumes-web # 定义该选择器的app标签
    template:  # 定义Deploynent对象中的Pod对象模板
        metadata: # 定义该Pod对象模板的元数据
        labels: # 定义Pod对象模板的标签信息
            app: resumes-web # 定义Pod对象模板的app标签
        spec:      # 定义Pod对象模板的具体特征
        containers: # 定义Pod对象模板中要部署的容器列表
        - name: resumes-web # 定义第一个容器的名称
            image: online_resumes:latest # 定义该容器使用的镜像
            imagePullPolicy: Never # 定义拉取容器的方式，主要有：
                                                # Always：始终从远程仓库中拉取
                                                # Never：始终使用本地镜像
                                                # IfNotPresent：优先使用本地镜像，
                                                #      镜像不存在时从远程仓库拉取
            ports:               # 定义容器的端口映射
            - containerPort: 3000 # 定义容器对外开放的端口

    ---
    apiVersion: v1 # 指定Service API的版本
                            # 可用kubectl api-versions命令查看
    kind: Service    # 定义资源对象的类型为Service
    metadata:        # 定义Service对象的元数据信息
    name: express-service # 定义Service对象的名称
    namespace: online-resumes # 定义Service对象所属的命名空间
    labels:             # 定义Service对象的标签信息
        app: resumes-web # 定义Service对象的app标签
    spec:                  # 定义Service对象的具体属性
    type: ClusterIP # 定义Service对象的类型为 ClusterIP，这也是其默认类型
    ports:              # 定义Service对象的端口映射
        - port: 80    # 定义Service对象对外开放的端口
        targetPort: 3000 # 定义Service对象要转发的内部端口
    selector:         # 使用选择器定义Service对象要部署的资源对象
        app: resumes-web # 该app标匹配的是稍后定义的Deployment对象
    ```

6. 由于“线上简历”应用程序的数据库模块是一个有状态的 MongoDB 服务，所以它适合用 StatefullSet 类型的控制器编排容器，并用 StorageClass 对象定义一个数据持久化方案，最后再将其部署成 K8s 集群的另一个 Service。为此，我们需要在`online_resumes`目录下创建一个名为`mongodb-statefulset.yml`的资源定义文件，其具体内容如下。

    ```yaml
    # 用StorageClass对象定义一个数据持久化方案
    apiVersion: storage.k8s.io/v1 # 指定StorageClass API的版本
    kind: StorageClass  # 定义资源对象的类型为StorageClass
    metadata:               # 定义StorageClass对象的元数据信息
    name: cluster-mongo # 定义StorageClass对象的名称
    provisioner: fuseim.pri/ifs # 定义StorageClass对象采用nfs文件系统

    ---
    # 用StatefulSet对象来组织用于部署MongoDB数据库的Pod对象
    apiVersion: apps/v1  # 指定StatefulSet API的版本
    kind: StatefulSet   # 定义资源对象的类型为StatefulSet
    metadata:              # 定义StatefulSet对象的元数据信息
    name: mongodb-statefulset # 定义StatefulSet对象的名称
    namespace: online-resumes # 定义StatefulSet对象所属的命名空间
    spec:                     # 定义StatefulSet对象的具体属性
    selector  :            # 定义StatefulSet对象的选择器，以便其他对象引用
        matchLabels: # 定义该选择器用于匹配的标签
        role: mongo # 定义该选择器的role标签，用于匹配相应的认证规则
        environment: test # 定义该选择器的环境标签为test
    serviceName: mongo-service
    replicas: 2  # 定义StatefulSet对象要部署的数量
    template:  # 定义StatefulSet对象中的Pod对象模板
        metadata: # 定义该Pod对象模板的元数据
        labels: # 定义该Pod对象模板的标签信息
            role: mongo
            environment: test
        spec: # 定义Pod对象模板的具体属性
        containers: # 定义Pod对象模板中要部署的容器列表
        - name: mongo  # 定义第一个容器的名称
            image: mongo:latest # 定义第一个容器使用的镜像
            command: # 设置启动该容器的命令参数
            - mongod
            - "--replSet"
            - rs0
            - "--bind_ip"
            - 0.0.0.0
            - "--smallfiles"
            - "--noprealloc"
            ports:   # 定义该容器对外开放的端口
            - containerPort: 27017
            volumeMounts: # 定义该容器所要挂载的数据卷
            - name: mongo-storage
                mountPath: /data/db
        - name: mongo-sidecar  # 定义第二个容器的名称及相关参数
            image: cvallance/mongo-k8s-sidecar:latest # 定义第二个容器使用的镜像
            env:
            - name: MONGO_SIDECAR_POD_LABELS
                value: "role=mongo,environment=test"
    volumeClaimTemplates: # 定义StatefulSet对象所要使用的数据卷模板
        - metadata:
            name: mongo-storage
        spec:
            storageClassName: cluster-mongo # 采用之前已定义的StorageClass
            accessModes: ["ReadWriteOnce"] # 定义数据卷的读写模式
            resources: # 定义该模板要申请的存储资源
            requests:
                storage: 10Gi # 数据卷的容量

    ---
    # 将上述StatefulSet控制器对象组织的Pod导出为本地服务
    apiVersion: v1
    kind: Service
    metadata:
    name: mongo-service
    namespace: online-resumes
    labels:
        name: mongo-service
    spec:
    clusterIP: None # 定义该Service对象的网络类型为本地访问
    ports:
        - port: 27017
        targetPort: 27017
    selector:
        role: mongo

    ---
    # 将上述StatefulSet控制器对象组织的Pod导出为外部服务
    apiVersion: v1
    kind: Service
    metadata:
    name: mongo-cs
    namespace: online-resumes
    labels:
        name: mongo
    spec:
    type: NodePort # 定义该Service对象的网络类型为NodePort
    ports:
        - port: 27017
        targetPort: 27017
        nodePort: 30717
    selector:
        role: mongo
    ```

7. 将上面定义的两个容器编排文件复制到 K8s 集群的主控节点中，并分别执行`kubectl create -f express-deployment.yml`命令和`kubectl create -f mongodb-statefulset.yml`命令创建相关的 Pod 实例和 Service 实例，并启动它们。如果一切顺利，我们就可以通过以下操作来确认应用程序的部署情况。

    ```bash
    $ sudo kubectl get services -n online-resumes
    NAME              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)     AGE
    express-service   ClusterIP   10.104.174.250   <none>        80/TCP      18m
    mongo-cs          NodePort    10.109.1.28      <none>        27017:30717/TCP   88s
    mongo-service     ClusterIP   None             <none>        27017/TCP         88s
    
    $ sudo kubectl get deployments -n online-resumes
    NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
    express-deployment   3/3     3            3           18m
    
    $ sudo kubectl get statefulsets -n online-resumes
    NAME                  READY   AGE
    mongodb-statefulset   2/2     46m

    $ sudo kubectl get pods -n online-resumes
    NAME                                  READY   STATUS    RESTARTS   AGE 
    express-deployment-75d7c69766-266hq   1/1     Running   0          23m
    express-deployment-75d7c69766-kxfhr   1/1     Running   0          23m
    express-deployment-75d7c69766-lh5kr   1/1     Running   0          23m
    mongodb-statefulset-0                 2/2     Running   0          46m
    ```

只要看到了与上面类似的输出，就说明我们已经成功完成了“线上简历”应用程序在 K8s 集群环境中的容器化部署。接下来就可以利用 kubectl 这一 K8s 集群的客户端工具对应用程序进行日常维护工作了。

### 编写资源定义文件

和使用 Docker Compose 时一样，我们在 K8s 中部署一个应用程序的主要任务也是编写用于定义各类资源对象的 YAML 文件。而 YAML 文件的格式可以被视为是 JSON 的一种子集格式，由于它只需凭借简单的缩进和键/值对格式就可以描述出一个内容颇为复杂的分层数据结构，因而相对于 JSON 而言更适用于执行软件的配置与管理工作。下面，就让我们来简单介绍一下使用 YAML 文件在 K8s 中定义资源对象的基本规则。

在 K8s 中，资源对象在本质上就是服务器集群状态在软件系统中的抽象化表述，它们会以运行时内存实体的形式始终存在于 K8s 系统的整个生命周期中，并用于描述如下信息：

- 在服务器集群中运行的应用程序（以及它们所在的服务器节点）；
- 上述应用程序可以使用的计算资源，例如网络、数据卷等；
- 上述应用程序所采用的的运维策略，比如重启策略、升级策略以及容错策略；

因此和软件在运行时管理的其他内存实体一样，K8s 中的这些资源对象的创建、修改、删除等操作也都需要通过调用 K8s API 来完成。也就是说，我们在编写定义资源对象的 YAML 文件时实际上在做的就是拟定 K8s API 的调用方法及其调用参数，因此所有的 K8s 资源对象定义文件中应该都至少会包含以下四个必须字段：

- `apiVersion`字段：用于声明当前文件创建资源对象时所需要使用的 K8s API 的版本，当前系统中可用的 K8s API 版本可用`kubectl api-versions`命令进行查询；
- `kind`字段：用于声明当前文件要创建的资源对象所属的类型，例如 Pod、Deployment、StatefulSet 等；
- `metadata`字段：用于声明当前资源对象的元数据，以便唯一标识被创建的对象，该元数据中通常会包括一个名为`name`的子字段，用于声明该资源对象的名称，有时候还会加上一个`namespace`子字段，用于声明该资源对象所属的命名空间；
- `spec`字段：用于声明当前资源对象的具体属性，用于具体描述被创建对象的各种细节信息；

需要特别注意的是，K8s中 不同类型的资源对象在`spec`字段中可配置的子字段是不尽相同的，我们需要在 K8s API 参考文档中根据要创建的资源类型来了解其`spec`字段可配置的具体选项，例如，Pod 对象的`spec`字段中可配置的是我们在该对象中所要创建的各个容器及其要使用的镜像等信息；在 Deployment、StatefulSet 这一类控制器对象中，`spec`字段中配置的通常是它在组织相关资源对象时所需要使用的 Pod 对象模板；而 Service 对象的`spec`字段中可配置的则是被导出为服务的资源对象，及其使用网络类型、端口映射关系等信息。

对于上述资源对象的定义细节，我们在上一节中就已经以“线上简历”应用程序为例、分别针对无状态的 Web 服务和有状态的数据库服务在 K8s 中的部署做了具体的示范，并在定义这些对象的 YAML 文件中添加了详细的注释信息，以供读者参考。当然了，同样基于篇幅方面的考虑，我们在本书中介绍的依然只是在编写K8s资源定义文件时可能会用到的最基本写法。如果读者希望更全面地了解在使用这类 YAML 文件定义 K8s 中各种类型的资源对象时所有可配置的内容及其配置方法，可以自行在 Google 等搜索引擎中搜索“Kubernetes API”关键字，然后查看更为详尽的文献资料。[^2]

### 使用kubectl客户端

在 K8s 集群中，对应用程序的日常维护工作大部分都是通过 kubectl 这个客户端命令行工具来完成的。在接下来的内容中，我们就结合维护工作中常见的使用场景来介绍一下该命令行工具的具体使用方法。

首先是基于 YAML 格式的资源定义文件的操作，我们在执行这一类操作时经常会用到以下命令。

- `kubectl create -f <YAML文件名>`命令：该命令会根据`<YAML文件名>`参数指定的资源定义文件创建相关的资源对象，并将其部署到K8s集群中。
- `kubectl apply -f <YAML文件名>`命令：该命令会根据`<YAML文件名>`参数指定的资源定义文件修改相关的资源对象，并将其重新部署到K8s集群中。
- `kubectl delete -f <YAML文件名>`命令：该命令会根据`<YAML文件名>`参数指定的资源定义文件删除相关的资源对象，并解除其K8s集群中的部署。

在上述命令中，`kubectl create` 和`kubectl apply`命令都可以用于根据指定的资源定义文件来创建资源对象（利用`-f`参数），区别在于：`kubectl apply`命令可以根据目标资源的存在情况来调整要执行的操作。如果资源对象已经存在，则根据资源定义文件创建该对象；如果资源对象已经存在，但资源定义文件已经被修改，就将修改应用于该对象中，如果资源定义文件没有变化，则什么也不做。简而言之，`kubectl apply`命令是一个可在运维工作中反复使用的命令，而`kubectl create`命令通常只能用于一次性地创建不存在的资源对象。

接下来，我们需要了解的是对已经部署到K8s集群中的资源对象可以自行的常用操作，在执行这一类操作时经常会用到以下命令。

- `kubectl get <资源类型> <参数列表>`命令：该命令用于列出部署在K8s集群中的所有资源对象及其相关信息。在该命令中，`<资源类型>`可以是`pods`、`deployments`、`statefulsets`、`services`等我们之前介绍过的资源对象类型；而`<参数列表>`中则可以为该命令指定一些具体条件，例如`-n`参数可用于指定资源对象所属的命名空间，默认情况下使用的是`default`命名空间，而`-o`参数则可以指定返回信息的呈现样式。

- `kubectl describe <资源对象> <参数列表>`命令：该命令用于查看K8s集群中指定资源对象的信息。在该命令中，`<资源对象>`需指定资源对象的名称及其所属的资源类型，例如，如果想查看一个名为`express-pod`的 Pod 对象。该命令就该是`kubectl describe pod express-pod`。同样的，我们也可以在`<参数列表>`中使用`-n`参数来指定资源对象所属的命名空间，默认情况下使用的是`default`命名空间。

- `kubectl delete <资源对象> <参数列表>`命令：该命令用于删除部署在 K8s 集群中的资源对象。在该命令中，`<资源对象>`和`<参数列表>`部分的编写语法与`kubectl describe`命令相同。

- `kubectl edit <资源对象> <参数列表>`命令：该命令用于修改部署在 K8s 集群中的资源对象，它会使用 VIM 编辑器打开指定资源对象的 YAML 文件，以便我们修改该对象的定义。在该命令中，`<资源对象>`和`<参数列表>`部分的编写语法也与`kubectl describe`命令相同。

- `kubectl exec <Pod对象> <参数列表>`命令：该命令用于进入到指定`<Pod对象>`的容器中，它的编写语法与`docker exec`命令基本相同，默认情况下会进入到Pod对象中的第一个容器中，如果需要进入其他容器，就需要使用`-c`参数指定容器名称。例如`kubectl exec -it express-pod -c resumes-web /bin/bash`命令的作用就是进入名为`express-pod`的Pod对象中的`resumes-web`容器中，并执行`/bin/bash`程序。

- `kubectl scale <资源对象> <参数列表>`命令：该命令用于对指定`<资源对象>`的数量进行动态伸缩，它的编写语法与`docker-compose scale`命令基本相同，例如`kubectl scale deployment express-deployment --replicas=5`命令的作用就是名为`express-deployment`的Deployment控制器对象在 K8s 集群中的运行实例数量修改为五个。

- `kubectl set image <资源类型/资源对象名称> <镜像名称="版本标签">`命令：该命令用于更改指定容器镜像的版本，例如，如果我们想将“线上简历”应用程序中使用的`mongo`镜像的版本改为`3.4.22`，就可以通过执行`kubectl set image statefulset/mongodb-statefulset mongo="mongo:3.4.22"`命令来实现。

- `kubectl rollout undo <资源类型/资源对象名称>`命令：该命令用于回滚被修改的资源对象，将其恢复到被修改之前的状态。例如，如果我们在更新了上述`mongo`镜像之后除了问题，就可以通过执行`kubectl rollout undo statefulset/mongodb-statefulset`命令来将其回滚到之前的版本。

最后，再来了解一下可对 K8s 集群本身执行的执行的操作，我们在执行这一类操作时经常会用到以下命令。

- `kubectl get nodes <参数列表>`命令：该命令用于列出当前 K8s 集群中的所有节点，其`<参数列表>`部分的编写语法与之前用于查看资源对象的`kubectl get`命令相同。

- `kubectl api-versions`命令：该命令用于查看当前系统所支持的 K8s API 及其版本，我们可以根据其返回的信息来编写资源定义文件。

- `kubectl cluster-info`命令：该命令用于查看当前 K8s 集群的相关信息。

<!-- 以下为注释区 -->

[^1]: 在这里，“K8s”这个简称是由将kubernetes中间的“ubernete”八个字母缩写为“8”而来。
[^2]: 在搜索参考文献时最好不要使用“K8s”这样的缩写形式，这会让我们错过一些正式的官方文档。

----
#已完成
