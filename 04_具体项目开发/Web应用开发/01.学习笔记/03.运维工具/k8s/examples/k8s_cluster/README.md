# 项目说明

本项目演示如何使用 Vagrant+VirtualBox 搭建 Kubernetes 集群，并针对国内的网络环境做了优化。

## 使用方法

### 准备工作

在使用本项目之前，需先在当前操作系统中安装以下软件：

- [OpenSSH](https://www.openssh.com/)
- [Git](https://git-scm.com/)
- [kubectl](https://kubernetes.io/zh-cn/docs/tasks/tools/#kubectl)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- [Vagrant](https://www.vagrantup.com/docs/installation)

### 搭建集群

请打开 Powershell/Bash 等命令行终端环境并执行以下命令：

```bash
git clone https://github.com/owlman/vagrant-ubuntu-k8s-cluster.git
cd vagrant-ubuntu-k8s-cluster
vagrant up
```

以上命令会自动构建出以下三台虚拟的服务器主机：

|   主机名    |     IP地址     | 内存 | 处理器数量 |   操作系统   |
| :---------: | :------------: | :--: | :--------: | :----------: |
| k8s-master  | 192.168.100.21 |  2G  |     2      | Ubuntu 20.04 |
| k8s-worker1 | 192.168.100.22 |  2G  |     2      | Ubuntu 20.04 |
| k8s-worker2 | 192.168.100.23 |  2G  |     2      | Ubuntu 20.04 |

根据在`vagrantfile`中的定义，Vagrant 在构建上述虚拟机的同时还会自动执行`scripts`目录中的脚本，这些脚本将会自动为虚拟机配置、安装 Docker 与 Kubernetes 环境，以下是其安装软件的版本信息：

```bash
Docker-CE:  20.10.17
Kubernetes: 1.21.1
    kube-apiserver: v1.21.1
    kube-proxy: v1.21.1
    kube-controller-manager: v1.21.1
    kube-scheduler: v1.21.1
    pause: 3.4.1
    coredns: v1.8.0
    etcd: 3.4.13-0  
```

### 基本操作

1. 启动、重启与关闭虚拟机：

    ```bash
    # 启动所有虚拟机
    vagrant up
    # 启动指定的虚拟机
    vagrant up <主机名>
    # 重启所有虚拟机
    vagrant reload
    # 重启指定的虚拟机
    vagrant reload <主机名>
    # 关闭所有虚拟机
    vagrant halt
    # 关闭指定的虚拟机
    vagrant halt <主机名>
    ```

2. 使用 SSH 的方式进入指定虚拟机：

    ```bash
    vagrant ssh  <主机名>
    ```

3. 销毁虚拟机

    ```bash
    # 销毁所有虚拟机
    vagrant destroy -f
    # 销毁指定的虚拟机
    vagrant destroy <主机名> -f
    ```

### 使用 Kubectl

如果想使用 kubectl 命令行工具在本地远程操作这个虚拟的 Kubernetes 集群，可打开 Powershell/Bash 等命令行终端环境并进入到`vagrant-ubuntu-k8s-cluster`目录中，然后执行以下命令：

```bash
mkdir ~/.kube
cp ./configs/config  ~/.kube/
```

如果一切顺利，当我们在本地的命令行终端中输入`kubectl get nodes`命令时，就能看到如下输出了：

```bash
NAME          STATUS     ROLES                  AGE   VERSION
k8s-master    Ready      control-plane,master   22h   v1.21.1
k8s-worker1   Ready      <none>                 20h   v1.21.1
k8s-worker2   Ready      <none>                 21h   v1.21.1
```
