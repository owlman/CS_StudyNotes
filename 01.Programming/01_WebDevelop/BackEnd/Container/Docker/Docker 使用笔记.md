# Docker 使用笔记

这篇笔记将用于记录本人在学习 Docker 服务端运维工具过程中所记录的心得体会，它将会被存储在`https://github.com/owlman/study_note`项目的`SoftwareTool/Container`目录下一个名为的`Docker`子目录中。

## 学习规划

- 学习基础：
  - 有一两门编程语言的使用经验。
  - 有一定的 Web 开发及维护经验。
- 视频资料：
  - [黑马程序员 Docker 容器化技术](https://www.bilibili.com/video/BV1CJ411T7BK)：哔哩哔哩上的视频教程。
- 阅读资料：
  - [《深入浅出 Docker》](https://book.douban.com/subject/30486354/)：本人学习所用书籍。
- 学习目标：
  - 使用 Docker 发布并维护自己的私人项目.

## Docker 简介

和许多成功的软件项目都有一个无心插柳柳成荫的故事一样，Docker 原本只是一家名为 dotCloud 的 PaaS 服务提供商启动的一个业余项目，该项目在开源之后意外获得了巨大的成功，以至于 dotCloud 公司干脆放弃了原本就不景气的 PaaS 业务，并且将公司改名为 Docker Inc，以便专职维护这个项目。该项目如今的正式名称叫 Moby，读者可以在 GitHub 上找到它。

Docker 这个词在英文中的意思是“码头工人”，这一工种的主要工作是装卸货船上的集装箱，因此该运维工具的核心工作理念就是让应用程序在服务器上的部署像装卸集装箱一样，实现标准化的组件式管理，业界称这种工作理念为容器化部署。从概念上来看，容器的概念和传统的虚拟机比较类似，它们之间主要存在着以下区别：

- 虚拟机依赖的是计算机硬件层面上的技术，而容器是构建在操作系统层面上的，它复用的是操作系统的容器化技术。
- 虚拟机中部署的是一个完整的操作系统，而容器中封装的只是一个与指定应用程序相关的操作系统子集，相对更为轻量化。
- 虚拟机通常是通过快照来保存其运行状态的；而容器则引入了类似于版本控制系统的机制，这种机制可以让运维人员更方便、快速地将应用程序的运行状态切换到其之前的某个历史时间节点上。

以上不同之处也解释了我们为什么需要使用 Docker 这样的工具来对服务端的应用程序进行容器化部署。试想一下，如果我们基于 Vue.js 前端框架、Express.js 后端框架以及 MongoDB 数据库开发了一个 Web 应用程序，而这些应用程序框架和数据库的版本通常是日新月异，不同版本之间内部实现的变化有时也非常剧烈，很多时候基于前一个版本可用的代码，到了下一个版本就运行出错了。这就要求我们在最终部署应用程序的时候在服务器上安装指定版本的框架和数据库，这将是一个非常耗时费力且容易出错的工作。而且一旦遇到服务器故障，应用迁移等问题，这一切工作又得重来一遍，其运维成本可想而知。而容器的作用就是能将应用程序与其所依赖的框架、数据库、操作系统固化下来。

Docker 本质上就是这样一个基于Linux容器（Linux Containers，简称 LXC）技术实现的容器管理引擎。它会通过应用程序及所有程序的依赖环境打包到一个虚拟容器中，这个虚拟容器可以运行在任何一台安装了 Docker 容器引擎的服务器设备上，无论该设备是一台实体的物理设备、还是无实体的云主机或本地虚拟机，都不会影响我们部署容器内的应用程序。这样一来，我们就可以在任何主流的操作系统中对服务端的应用程序进行开发、调试和运行，而不必担心它的可移植性了。

## 安装 Docker

在正式安装 Docker 之前，我们首先要了解一下该产品所发布的各种版本。和所有追求盈利的软件公司一样，随着产品在市场上的不断流行与发展，docker Inc 公司也不能免俗地开启了将产品商业化的道路。于是，Docker 自 17.03 这个版本之后就被分成了 CE（Community Edition，即社区版）和 EE（Enterprise Edition，即企业版）两种不同的版本。其中，Docker CE 是保持免费的版本，它包含了完整的 Docker 平台，非常适合开发人员和运维团队构建用于部署指定应用程序的容器。值得一提的是，Docker CE 本身也还被分成了以下两个版本：

- edge 版本每月发布一次，只提供一个月的支持和维护期，主要面向那些热衷于研究 Docker 本身，喜欢尝试新功能的用户。
- stable 版本每季度发布一次，将提供四个月的支持和维护期，适用于希望在具体工作中对一些实际项目进行维护的用户。

而 Docker EE 的发布节奏则与 Docker CE 的 stable 版本基本保持一致，但每个 Docker EE 版本都享受为期一年的支持与维护期，在此期间接受安全与关键修正。总而言之，Docker CE 并非是功能上的阉割版，而 Docker EE 则只是面前企业用户增加了收费的维护服务以及一些周边产品，以求进一步降低企业运营的风险，但它们在个人的学习体验上不会有太大的区别。

在这里，我们将会主要以 Docker CE 为主来展开针对容器化部署议题的探讨，因此接下来的任务就是要在一个之前配置好的 Ubuntu 系统中安装 Docker CE。为此，我们需要执行以下步骤。

- 首先要做的是将 Docker 所在的 APT 软件源添加到 Ubuntu 的 APT 列表中，为此，我们需要先更新一下当前的软件包索引，并安装一些基础工具：

    ```bash
    sudo apt update
    sudo apt install \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    ```

- 接下来，我们需要使用 curl 工具导入 Docker APT 软件源的 GPG 密钥：

    ```bash
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    ```

- 现在，我们就可以通过以下命令正式地将 Docker APT 软件源添加到 Ubuntu 的 APT 列表中：

    ```bash
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    # `sb_release -cs`变量表达式返回的是Ubuntu的版本代号，在这里是focal。
    ```

- 最后，我们需要再次更新一下系统的软件包索引，然后就可以安装 Docker CE 了，其安装命令如下：

    ```bash
    sudo apt update
    sudo apt install \
       docker-ce \
       docker-ce-cli \
       containerd.io
    ```

当然了，以上命令安装的是 Docker APT 软件源中的最新版本，如果我们想安装的是 Docker 的某个指定版本，需要先执行`apt list -a docker-ce`命令获取到 Docker APT 软件源中所有可用的版本，例如像这样：

```bash
$ apt list -a docker-ce
Listing...
docker-ce/focal,now 5:20.10.12~3-0~ubuntu-focal amd64 [installed]
docker-ce/focal 5:20.10.11~3-0~ubuntu-focal amd64
docker-ce/focal 5:20.10.10~3-0~ubuntu-focal amd64
docker-ce/focal 5:20.10.9~3-0~ubuntu-focal amd64
docker-ce/focal 5:20.10.8~3-0~ubuntu-focal amd64
docker-ce/focal 5:20.10.7~3-0~ubuntu-focal amd64
docker-ce/focal 5:20.10.6~3-0~ubuntu-focal amd64
docker-ce/focal 5:20.10.5~3-0~ubuntu-focal amd64
docker-ce/focal 5:20.10.4~3-0~ubuntu-focal amd64
docker-ce/focal 5:20.10.3~3-0~ubuntu-focal amd64
docker-ce/focal 5:20.10.2~3-0~ubuntu-focal amd64
docker-ce/focal 5:20.10.1~3-0~ubuntu-focal amd64
docker-ce/focal 5:20.10.0~3-0~ubuntu-focal amd64
docker-ce/focal 5:19.03.15~3-0~ubuntu-focal amd64
docker-ce/focal 5:19.03.14~3-0~ubuntu-focal amd64
docker-ce/focal 5:19.03.13~3-0~ubuntu-focal amd64
docker-ce/focal 5:19.03.12~3-0~ubuntu-focal amd64
docker-ce/focal 5:19.03.11~3-0~ubuntu-focal amd64
docker-ce/focal 5:19.03.10~3-0~ubuntu-focal amd64
docker-ce/focal 5:19.03.9~3-0~ubuntu-focal amd64
```

然后根据该命令列出的可用版本，执行以下命令来安装：

```bash
# 通过在软件包名后面添加""=<版本号>"的方式来安装指定版本：
sudo apt install \
    docker-ce=<版本号> \
    docker-ce-cli=<版本号> \
    containerd.io
```

使用APT软件源来安装软件的另一个好处是，当新版本的 Docker CE 发布时，我们可以直接通过`sudo apt update && sudo apt upgrade`命令来进行自动升级。当然了，如果想阻止 Docker 的自动更新，我们也可以通过执行以下命令来锁住它的版本：

```bash
sudo apt-mark hold docker-ce
```

## 配置工作

在基于 Debian 项目的 Linux 发行版上，docker在被安装只会通常会被自动设置为系统的开机启动服务。当然了，如果需要的话，我们也可以通过执行以下命令手动该服务设置为系统的开机启动项。

```bash
sudo systemctl enable docker
```

在一切安装妥当之后，我们可以通过以下这命令来查看 Docker 的版本并确认该服务是否已被启动：

```bash
$ docker version
 Client: Docker Engine - Community
 Version:           20.10.12
 API version:       1.41
 Go version:        go1.16.12
 Git commit:        e91ed57
 Built:             Mon Dec 13 11:45:33 2021
 OS/Arch:           linux/amd64
 Context:           default
 Experimental:      true
$ sudo service docker status
 * Docker is running
```

另外，由于在默认情况下，只有`root`用户或有`sudo`权限的用户可以执行Docker操作，所以如果我们平时使用非`root`用户，但又不想每次执行Docker操作的时候都得在相关命令之前加上`sudo`前缀，也可以选择添加一个`docker`用户组，并将我们使用的非root用户加入到该组中，其具体命令如下：

```bash
$ sudo groupadd docker
$ sudo usermod -aG docker $USER
# 这里的$USER是一个环境变量，代表当前用户名。
```

如果我们想要确认一下 Docker 的容器管理功能是否已经可供使用，可以试着执行以下命令运行一个测试容器：

```bash
$ docker container run hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

上述命令将会从 Docker Hub 中下载一个名为`hello-world`测试镜像，并根据该镜像实例化一个测试容器。而该容器中的应用程序会在运行时打印出带有“Hello from Docker”字样等相关内容的信息之后退出。

## 镜像与容器

正如我们之前所说， Docker 本质上就是一个用于管理容器的服务端工具。而其中用于创建容器的模板，我们就称之为容器的镜像，其作用与我们在使用 Vmware 或 VirtualBox 之类的虚拟机管理器创建虚拟机时选择的模板或快照基本相同（例如我们要创建的是 Linux 系统的虚拟机还是 Windows 系统的虚拟机，抑或是一个安装了 Node.js 的主机），或者如果熟悉面向对象思想的话，也可以将 Docker 中的容器理解为程序在运行过程中存在于内存中的对象实体，而容器就是我们用于创建这些对象的类。

### 理解镜像

简而言之，镜像就是在某一刻停止运行的容器快照。例如我们可以将一个运行了 Ubuntu 系统的容器创建成一个镜像，而将这个容器安装了 Node.js 之后的状态创建为另一个镜像。这样一来，当我们需要一个运行了纯净Ubuntu 环境的容器时，就可以使用第一个镜像来创建它，而当我们需要一个安装在 Ubuntu 上的 Node.js 运行环境时就可以使用第二个镜像来创建容器。同样的，当我们 在Node.js 运行环境中创建了一个引入 Express.js 框架的项目，还可以继续将其创建为一个镜像，以后在需要启动一个 Express 项目的时候，也可以用该镜像快速创建一个项目开发和运维环境。

而基于上述使用镜像的方式，Docker 中镜像在存储上被设计成了分层叠加的结构，并且这些分层是可以在镜像之间共享的，例如在上述三个镜像中，三个镜像之间可以共享 Ubuntu 所在的分层，而后两个镜像也可以共享 Ubuntu 和 Node.js 两个分层。这样一来，这三个镜像在同一主机上整体所占的空间会大幅减少，我们在将它们推送到镜像仓库或者从镜像仓库中拉取它们时，很多时候是不必传输重复的分层的，这也是容器在运维工作上优于虚拟机的原因之一。

而容器相较于虚拟机的另一个优势则在于，即使容器镜像中包含了 Ubuntu 这类操作系统，它通常也只封装了该操作系统的文件系统和一个精简的 Shell 程序，并不包含与任何硬件驱动相关的内核部分。它是与宿主机器共享操作系统内核的。因此与完整的虚拟机相比，显然体积更为轻量化。例如，Docker 官方发布的 Ubuntu 镜像大约只有 80MB 左右的大小，而一个安装了 Ubuntu 系统的虚拟机则通常有 8GB 左右的大小。

### 镜像操作

接下来，让我们来具体介绍一下如何在 Docker 中进行镜像操作。在默认情况下，如果我们是在类 Linux 系统中安装的 Docker，其本地镜像的存储位置通常位于`/var/lib/docker/<storage-driver>`目录中，如果是在 Windows 主机上安装的，本地镜像就应存储在`C:\ProgramData\docker\windowsfilter`目录中。读者可以使用`docker image ls`命令来查看当前本地镜像列表，像这样：

```bash
$ docker image ls 
REPOSITORY    TAG       IMAGE ID       CREATED        SIZE
hello-world   latest    feb5d9fea6a5   6 months ago   13.3kB
```

当然了，我们在刚刚安装完 Docker 时本地应该是没有任何镜像的，但由于之前为了测试安装是否正确，我们已经从 Docker Hub 中下载了一个名为`hello-world`测试镜像，所以读者会在上述镜像列表中看到它。在专业术语中，大家将镜像从远程仓库服务中下载到本地的操作称之为**拉取（pull）**。现在，如果读者想要拉取一个最新版本的 Ubuntu 镜像，就需要执行以下操作将它拉取到本地：

```bash
$ docker image pull ubuntu:latest 
latest: Pulling from library/ubuntu
e0b25ef51634: Pulling fs layer
e0b25ef51634: Download complete
e0b25ef51634: Pull complete
Digest: sha256:9101220a875cee98b016668342c489ff0674f247f6ca20dfc91b91c0f28581ae
Status: Downloaded newer image for ubuntu:latest
docker.io/library/ubuntu:latest

$ docker image ls 
REPOSITORY    TAG       IMAGE ID       CREATED        SIZE
ubuntu        latest    825d55fb6340   6 days ago     72.8MB
hello-world   latest    feb5d9fea6a5   6 months ago   13.3kB
```

如你所见，`docker image pull <远程仓库名>:<版本标签>`命令会负责将指定的镜像从远程镜像仓库服务的仓库中拉取到本地。在默认情况下，Docker 所使用的是其官方的远程镜像仓库服务 Docker Hub。具体到上述操作中，`docker image pull ubuntu:latest`命令的作用就是去 Docker Hub 将 Ubuntu 仓库中标签为 latest 的容器镜像拉取到本地。而通过`docker image ls`命令，我们可以看到，该镜像的大小只有 72.8MB。另外，关于拉取镜像的命令，我们还需要注意以下几点。

- 如果我们在执行拉取命令时没有在仓库名称后指定具体的版本标签，则 Docker 会默认拉取标签为 latest 的镜像。例如，我们之前在拉取 Ubuntu 镜像时，拉取命令也可以简写为`docker image pull ubuntu:latest`，效果是完全一样的。
- 标签为 latest 的镜像是 Docker 默认要拉取的镜像，但并不保证该镜像是仓库中最新版本的镜像。例如，Alpine 仓库中最新镜像的标签通常是 edge。所以，希望读者使用 latest 标签时谨慎行事。

当然了，如果我们不知道远程仓库服务中有哪一些远程仓库可供使用，也可以使用`docker search <关键字>`命令进行查询。例如在下面的操作中，我们对 Docker Hub 中存有的所有与 Ubuntu 相关的远程仓库进行了查询。

```bash
$ docker search ubuntu
NAME                             DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
ubuntu                           Ubuntu is a Debian-based Linux operating sys…   14048     [OK]       
websphere-liberty                WebSphere Liberty multi-architecture images …   283       [OK]       
ubuntu-upstart                   DEPRECATED, as is Upstart (find other proces…   112       [OK]       
neurodebian                      NeuroDebian provides neuroscience research s…   88        [OK]       
open-liberty                     Open Liberty multi-architecture images based…   52        [OK]       
ubuntu-debootstrap               DEPRECATED; use "ubuntu" instead                46        [OK]       
ubuntu/nginx                     Nginx, a high-performance reverse proxy & we…   40                   
ubuntu/mysql                     MySQL open source fast, stable, multi-thread…   29                   
ubuntu/apache2                   Apache, a secure & extensible open-source HT…   26                   
ubuntu/prometheus                Prometheus is a systems and service monitori…   23                   
kasmweb/ubuntu-bionic-desktop    Ubuntu productivity desktop for Kasm Workspa…   22                   
ubuntu/squid                     Squid is a caching proxy for the Web. Long-t…   18                   
ubuntu/postgres                  PostgreSQL is an open source object-relation…   15                   
ubuntu/bind9                     BIND 9 is a very flexible, full-featured DNS…   13                   
ubuntu/redis                     Redis, an open source key-value store. Long-…   9                    
ubuntu/prometheus-alertmanager   Alertmanager handles client alerts from Prom…   5                    
ubuntu/grafana                   Grafana, a feature rich metrics dashboard & …   5                    
ubuntu/memcached                 Memcached, in-memory keyvalue store for smal…   4                    
ubuntu/telegraf                  Telegraf collects, processes, aggregates & w…   3                    
circleci/ubuntu-server           This image is for internal use                  3                    
ubuntu/cortex                    Cortex provides storage for Prometheus. Long…   2                    
ubuntu/cassandra                 Cassandra, an open source NoSQL distributed …   1                    
bitnami/ubuntu-base-buildpack    Ubuntu base compilation image                   0                    [OK]
snyk/ubuntu                      A base ubuntu image for all broker clients t…   0                    
rancher/ubuntuconsole                                                            0              
```

值得注意的是，在默认情况下，`docker search`命令通常只返回 25 条结果。但是，读者可以通过设置`--limit`参数的值来指定该命令返回的条目数，最多可设置为 100 条。

在将镜像拉取到本地之后，我们可以使用`docker image inspect`命令来查看镜像中的各种细节，包括镜像层数据和元数据。例如在下面的操作中，我们使用该命令查看了`hello-world`测试镜像中的细节。

```bash
$ docker image inspect hello-world:latest
[
    {
        "Id": "sha256:feb5d9fea6a5e9606aa995e879d862b825965ba48de054caab5ef356dc6b3412",
        "RepoTags": [
            "hello-world:latest"
        ],
        "RepoDigests": [
            "hello-world@sha256:97a379f4f88575512824f3b352bc03cd75e239179eea0fecc38e597b2209f49a"
        ],
        "Parent": "",
        "Comment": "",
        "Created": "2021-09-23T23:47:57.442225064Z",
        "Container": "8746661ca3c2f215da94e6d3f7dfdcafaff5ec0b21c9aff6af3dc379a82fbc72",
        "ContainerConfig": {
            "Hostname": "8746661ca3c2",
            "Domainname": "",
            "User": "",
            "AttachStdin": false,
            "AttachStdout": false,
            "AttachStderr": false,
            "Tty": false,
            "OpenStdin": false,
            "StdinOnce": false,
            "Env": [
                "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
            ],
            "Cmd": [
                "/bin/sh",
                "-c",
                "#(nop) ",
                "CMD [\"/hello\"]"
            ],
            "Image": "sha256:b9935d4e8431fb1a7f0989304ec86b3329a99a25f5efdc7f09f3f8c41434ca6d",
            "Volumes": null,
            "WorkingDir": "",
            "Entrypoint": null,
            "OnBuild": null,
            "Labels": {}
        },
        "DockerVersion": "20.10.7",
        "Author": "",
        "Config": {
            "Hostname": "",
            "Domainname": "",
            "User": "",
            "AttachStdin": false,
            "AttachStdout": false,
            "AttachStderr": false,
            "Tty": false,
            "OpenStdin": false,
            "StdinOnce": false,
            "Env": [
                "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
            ],
            "Cmd": [
                "/hello"
            ],
            "Image": "sha256:b9935d4e8431fb1a7f0989304ec86b3329a99a25f5efdc7f09f3f8c41434ca6d",
            "Volumes": null,
            "WorkingDir": "",
            "Entrypoint": null,
            "OnBuild": null,
            "Labels": null
        },
        "Architecture": "amd64",
        "Os": "linux",
        "Size": 13256,
        "VirtualSize": 13256,
        "GraphDriver": {
            "Data": {
                "MergedDir": "/var/lib/docker/overlay2/3a0e1e1bea4d0ac0bb55bb22f831cd7b6be43b33d5bb07203e8dc6ab0e5afc40/merged",
                "UpperDir": "/var/lib/docker/overlay2/3a0e1e1bea4d0ac0bb55bb22f831cd7b6be43b33d5bb07203e8dc6ab0e5afc40/diff",
                "WorkDir": "/var/lib/docker/overlay2/3a0e1e1bea4d0ac0bb55bb22f831cd7b6be43b33d5bb07203e8dc6ab0e5afc40/work"
            },
            "Name": "overlay2"
        },
        "RootFS": {
            "Type": "layers",
            "Layers": [
                "sha256:e07ee1baac5fae6a26f30cabfe54a36d3402f96afda318fe0a96cec4ca393359"
            ]
        },
        "Metadata": {
            "LastTagTime": "0001-01-01T00:00:00Z"
        }
    }
]
```

从上述信息中，我们可以看出`hello-world`测试镜像要运行的容器是一个基于 Linux 系统的，运行于 shell 终端环境中的一个 Hello World 程序。

最后，当我们不再需要某个镜像的时候，可以通过`docker image rm`命令将该镜像从本地删除，该操作会在当前主机上删除指定的镜像以及相关的镜像层。这意味着我们之后见无法通过`docker image ls`命令看到被删除的镜像，并且对应镜像分层数据所在的目录也会随之被删除。当然了，如果某个镜像分层被多个镜像共享，那只有当全部依赖该分层的镜像都被删除后，它才会被删除。在下面的示例中，我们将通过镜像ID来删除镜像。

```bash
$ docker image ls 
REPOSITORY    TAG       IMAGE ID       CREATED        SIZE
ubuntu        latest    825d55fb6340   6 days ago     72.8MB
hello-world   latest    feb5d9fea6a5   6 months ago   13.3kB

$ docker image rm feb5d
Untagged: hello-world:latest
Untagged: hello-world@sha256:97a379f4f88575512824f3b352bc03cd75e239179eea0fecc38e597b2209f49a
Deleted: sha256:feb5d9fea6a5e9606aa995e879d862b825965ba48de054caab5ef356dc6b3412
Deleted: sha256:e07ee1baac5fae6a26f30cabfe54a36d3402f96afda318fe0a96cec4ca393359

$ docker image ls 
REPOSITORY    TAG       IMAGE ID       CREATED        SIZE
ubuntu        latest    825d55fb6340   6 days ago     72.8MB
```

需要注意的是，如果被删除的镜像已经在本地实例化出了若干个容器，那么在这些容器被删除之前，该镜像是无法被删除的。接下来，就让我们来具体介绍一下如何使用镜像实例化出具体可运行的容器，并对这些容器进行管理。

### 容器管理

正如我们之前所说，容器是镜像在运行时的实例化。正如基于虚拟机模板可以启动多台虚拟机一样，我们也同样可以基于同一个镜像上启动一个或多个容器。在 Docker 中，启动容器的简便方式是使用`docker container run [参数] <镜像名> [指定应用]`命令。在这里，我们在该命令中使用一下参数：

- `-i`：该参数用于告知该命令以“交互模式”运行容器。
- `-t`：该参数用于告知该命令在容器启动后会进入其命令行终端程序。
- `--name`：该参数用于为创建的容器设置名称。
- `-v`：该参数用于设置容器与其宿主机之间的目录映射关系，它后面通常会紧跟着两个目录参数，第一个是宿主机上的目录，第二个则是映射到容器中目录。另外，我们可以在同一命令中使用多个`-v`参数设置多个目录映射。
- `-d`：该参数用于告知该命令创建一个守护式容器在后台运行，这样创建容器后就不会自动登录容器，如果只加-i -t 两个参数，创建后就会自动进去容器。
- `-p`：该参数用于设置容器与其宿主机之间的端口映射，它后面通常会紧跟着两个端口号参数，第一个设置的是宿主机的端口，第二个设置的是在容器内的映射端口。另外，我们可以在同一命令中使用多个`-p`参数设置多个端口映射。
- `-e`：该参数用于为容器设置环境变量。
- `--network=host`：该参数用于告知该命令将主机的网络环境映射到容器中，容器的网络与主机相同。

例如，我们可以接下来可以通过`docker container run -it --name=myhost ubuntu /bin/bash`这个命令来使用 Ubuntu 镜像实例化并以交互模式启动一个名为`myhost`的容器，该容器在启动之后会自动进入其 Bash Shell 终端中，在完成相关操作后，可以执行`exit`命令退出，该容器也随之停止。

再例如，我们也可以通过`docker container run -dit --name=myhost2 ubuntu`命令来创建一个守护式容器。这类容器在创建时不会立即进入到容器中，并且在容器内执行`exit`命令时，容器本身也不会终止运行。如果对于一个需要长期运行的容器来说，我们可以创建一个守护式容器。

对于已在运行的容器，我们可以通过`docker container exec -it <容器名或容器ID>  [指定应用]`命令进入到该容器中进行相关操作，例如，如果我们想进入之前创建的守护式容器，就可以执行`例如：docker container exec -it myhost2 /bin/bash`命令。如果读者不知道当前宿主机中运行了哪一些容器，也可以通过执行`docker container ls`命令来进行查看。甚至，如果我们还想在其返回的容器列表中包含已经终止运行的容器，还可以在该命令后面加上`--all`或`-a`参数，像这样：

```bash
$ docker container ls --all

CONTAINER ID   IMAGE     COMMAND       CREATED          STATUS                        PORTS     NAMES
1b51ccc03b21   ubuntu    "/bin/bash"   43 minutes ago   Exited (130) 40 minutes ago             myhost
```

对于上述列表中列出的容器，我们既可以执行`docker container stop <容器名或容器ID>`命令停止一个已经在运行的容器，也可以执行`docker container start <容器名或容器ID>`命令启动一个已经停止的容器。甚至还可以执行`docker container kill <容器名或容器ID>`命令杀掉一个已经在运行的容器。最后，如果确定某个容器不再被使用了，我们也可以通过`docker container rm <容器名或容器ID>`命令来删除它。

除此之外，如果我们想将容器的某个运行状态保存下来，以便日后使用，也可以通过执行`docker container commit <容器名或容器ID> <镜像名>`命令将容器重新保存为新的镜像。如果希望将这些镜像传递给别人使用，我们还通过`docker image save -o <文件名> <镜像名>`命令现有的某个镜像打包成文件，然后别人在收到该文件之后，就可以通过执行`docker image load -i <文件名>`命令将该镜像加载到本地。

## 容器化部署实践

在掌握了 Docker 镜像与容器的基本操作之后，我们就可以来具体地来介绍如何使用 Docker 容器来部署应用程序了。我们会以部署一个最简单的 Express.js 项目开始入手，以便让读者先从整体上初步熟悉一下容器化部署的工作流程，并理解它与传统部署方式的不同。

### 基本工作流程

下面，就让我们以SSH的方式远程登录到配置了Docker环境的服务器上，并执行以下步骤来部署项目吧。

1. 先通过执行`docker image pull node:17.5.0`命令从 Docker Hub 中拉取一个与我们开发环境相匹配的 Node.js 镜像。如果一切顺利，待拉取操作完成之后，我们就可以在`docker image ls`命令返回的本地镜像列表中看到这个版本标签为`17.5.0`的 Node.js 镜像了。

    ```bash
    $ docker image ls 
    REPOSITORY    TAG       IMAGE ID       CREATED        SIZE
    node          17.5.0    f8c8d04432c3   4 months ago   994MB
    ubuntu        latest    825d55fb6340   6 days ago     72.8MB
    hello-world   latest    feb5d9fea6a5   6 months ago   13.3kB
    ```

2. 接下来，我们要基于该 Node.js 镜像创建一个用于部署`HelloExpress`应用程序的镜像，具体操作是，先进入应用程序源码目录中（这里假设是一个名为`HelloExpress`的目录），并创建一个名为`Dockerfile`的镜像定义文件，然后在其中写入如下内容。

    ```Dockerfile
    # 声明当前镜像的基础镜像
    FROM node:17.5.0
    # 在当前镜像所实例化的容器中创建一个目录
    RUN mkdir -p /home/Service
    # 将新建的目录设定为容器的工作目录
    WORKDIR /home/Service
    # 设置将当前目录拷贝到容器工作目录
    COPY ./ /home/Service
    # 安装项目依赖与 PM2 进程管理器
    RUN npm install pm2 --global  \
            && npm install
    # 设置应用程序使用的端口
    EXPOSE 3000
    # 设置用于启动应用程序的命令
    CMD pm2 start index.js --no-daemon
    ```

3. 在保存上述文件之后，继续在该文件所在的目录下执行`docker image build -t helloapp:1.0.0 .`命令来为运行`HelloExpress`应用程序的容器创建一个 Docker 镜像。如果一切顺利，待创建操作完成之后，我们就可以在`docker image ls`命令返回的本地镜像列表中看到这个名为`helloapp`的镜像了。

    ```bash
    $ docker image ls 
    REPOSITORY    TAG       IMAGE ID       CREATED        SIZE
    helloapp      1.0.0     5822ce08a2c9   9 seconds ago   1.03GB
    node          17.5.0    f8c8d04432c3   4 months ago   994MB
    ubuntu        latest    825d55fb6340   6 days ago     72.8MB
    hello-world   latest    feb5d9fea6a5   6 months ago   13.3kB
    ```

4. 最后，我们就只需要执行`docker container run -d -p 80:3000 helloapp:1.0.0`命令来实例化这个新建的镜像，并运行用于部署该应用程序的容器了，在该命令中，**`-d`参数**用于将容器设置为后台运行；**`-p`参数**于设置服务器与容器之间的端口映射，在这里，我们将服务器的端口也设置成了`3000`，这样就无需再修改上一章中配置的反向代理了。

5. 如果上述操作过程一切顺利，我们现在就可以在局域网中使用服务器以外的计算机上使用`http://helloexpress.io`这个域名访问`HelloExpress`应用程序了，效果与我们之前在图5-5中看到的完全一致。

在完成了上述步骤之后，我们不仅完成了应用程序的容器化部署，构建了该应用程序的容器镜像。这样一来，如果我们在今后的某一时刻想在升级服务器设备，并重新部署`HelloExpress`应用程序，或者将其另行部署到另一个网络中的某台服务器上，就可以选择通过`docker image save -o hello_image.tar helloapp:1.0.0`命令将这个新建的`helloapp`镜像打包成一个名为`hello_image`文件，然后在目标设备上获取到该文件，并通过执行`docker image load -i hello_image.tar`命令将该镜像加载到本地，然后将它实例化容器并运行即可。当然，如果读者注册了Docker Hub这样的远程镜像仓库服务，也可以直接执行`docker image push helloapp:1.0.0` 命令将镜像文件上传到远程仓库中，然后就可以在其他设备上通过`docker image pull helloapp:1.0.0`命令来获取该镜像了。

### 容器化指令简介

在上述工作流程中，运维人员的核心任务就是要实现应用程序的容器化，而完成这一任务的关键就是要能熟练掌握`Dockerfile`文件的编写方法。从概念上来说，`Dockerfile`是一个由一系列镜像构建指令组成的批处理文件，它的本质就是让我们将部署某一应用程序的步骤以镜像文件的方式固定下来，从而实现应用程序的容器化部署。这种构建容器镜像的方式与我们之前介绍的“先进到某个现有的容器中执行一些手动操作，然后再执行`docker container commit <容器名或容器ID> <镜像名>`命令来将该容器保存为镜像文件”的方式相比，显得更为自动化一些。所以，我们在这里有必要重点学习一下如何编写`Dockerfile`文件，而学习编写`Dockerfile`文件的关键就是要掌握这些镜像构建指令。

首先，作为构建 Docker 镜像的第一步，我们需要先使用`FROM <镜像名>`指令来声明一个用于构建当前镜像的基础镜像。在计算机领域中，很少有工作是真正从零开始的，大多数情况都是基于现有工作成果的进一步扩展，例如，Ubuntu、Android 都是基于 Linux 内核开发的发行版，而 Linux 内核则又是参照 UNIX 系统接口的重新实现。另外在使用 Java 这一类面向对象的编程语言实现某一功能时，我们的第一步通常也是在现有的类库中选择一个父类来进行扩展，以避免重复发明轮子。`FROM <镜像名>`指令的使用思维也是如此，如果我们将 Docker 中镜像与容器类比成面向对象理论中类与对象的关系，那么当前镜像与其基础镜像之间就可以被理解成子类与父类的关系。

在选择基础镜像的时候，运维人员务必要了解接下来部署在容器中的应用程序。在通常情况下，应用程序所依赖的环境越单纯。基础镜像中已完成的工作就可以越多。例如，如果我们要部署的是`HelloExpress`这样的应用程序，那么它只需要一个单纯的 Node,js 运行环境，该环境安装在哪一种 Linux 发行版上并不重要，这时候我们只需要指定一个用于运行 Node.js 环境的容器镜像即可。但如果是要部署“线上简历”这种更为复杂的应用程序，那么除了Node.js运行环境，我们还需要使用APT这样的软件包管理器来安装数据库，这时候选择从一个干净的Ubuntu系统环境开始构建镜像可能是一个更好的选择。

在完成基础镜像的选择之后，我们的第二步就是要使用`RUN <shell命令>`指令来配置应用程序的运行环境了。该指令的作用就设置一系列在镜像被实例化成容器时需要执行的 shell 命令，这些命令通常用于安装一些应用程序的依赖项和相关工具。需要注意点是，由于 Docker 镜像文件被定义成了一种分成结构，而`Dockerfile`文件中的每一条`RUN <shell命令>`指令都会在镜像文件中增加一个新的分层，如果不加节制地使用该指令，可能会造成镜像文件毫无意义地过度膨胀。例如在下面的`Dockerfile`文件中：

```Dockerfile
FROM ubuntu
RUN apt install wget  -y
RUN wget -O redis.tar.gz "http://download.redis.io/releases/redis-5.0.3.tar.gz"
RUN tar -xvf redis.tar.gz
```

以上三条`RUN <shell命令>`指令会在镜像文件中构建三个分层，但这是毫无必要的，因此我们通常会简化成一条`RUN`指令。

```Dockerfile
FROM ubuntu
RUN apt install wget -y \
    && wget -O redis.tar.gz "http://download.redis.io/releases/redis-5.0.3.tar.gz" \
    && tar -xvf redis.tar.gz
```

在某些情况下，我们还需要使用`WORKDIR <目录名>`指令为应用程序在容器中指定一个工作目录（该目录必须是提前创建好的），然后使用`COPY <源文件路径> <容器内路径>`指令将应用程序的源码文件复制到该工作目录中，例如像我们之前所做的：

```Dockerfile
# 此处省略若干指令
RUN mkdir -p /home/Service
WORKDIR /home/Service
COPY ./ /home/Service
RUN npm install pm2 --global \
    && npm install
```

请注意，在指定好工作目录之后，后续的`RUN`指令执行的 shell 命令就会在该目录下执行。除上述指令外，我们还经常会用到以下指令。

- **`ADD <源文件路径> <容器内路径>`指令**：该指令的使用方式与功能和`COPY <源文件路径> <容器内路径>`指令基本相同。不同之处只在于：如果被复制的源文件是一个`tar`压缩文件，该指令会在复制文件时自动将其解压。

- **`CMD <shell命令>`指令**：该指令虽然和`RUN <shell命令>`指令用于执行shell命令，但它们执行命令的时机点不一样，RUN指令执行在构建容器镜像时，而CMD指令执行在容器启动时。后者通常用于为启动的容器指定默认要运行的程序，程序运行结束，容器本身的运行也就随之结束。需要注意的是，如果`Dockerfile`文件中存在多个CMD指令，那么只有最后一条会被真正执行。

- **`ENV <环境变量名> <要设置的变量值>` 指令**：该指令用于在容器内设置环境变量，例如，如果我们想将环境变量`NODE_VERSION`的值设置为`17.5.0`，那么就可以在`Dockerfile`文件中设置一条`ENV NODE_VERSION 17.5.0`指令。另外，我们也可以用该指令一次设置多个环境变量，命令格式为：`ENV <变量1>=<值1> <变量2>=<值2>...`。

- **`VOLUME <路径>` 指令**：该指令用于定义匿名数据卷。在启动容器时忘记挂载数据卷，会自动挂载到匿名卷。定义数据卷有助于避免重要的数据因容器重启而丢失，并可以在一定程度上避免容器的不断膨胀。同样的，我们也可以用该指令一次设置多个数据卷，命令格式为：`VOLUME ["<路径1>", "<路径2>"...]`。

- **`EXPOSE <端口号>` 指令**：如果在容器内运行的应用程序需要该容器向外开放指定的端口号，我们就可以使用该指令来声明要开放的端口号。同样的，我们也可以用该指令一次声明多个端口号，命令格式为：`EXPOSE <端口号1> <端口号2>...`。

- **`USER <用户名>[:<用户组>]` 指令**：该指令主要用于指定执行后续shell命令的用户和用户组（前提是，该用户和用户组必须已经存在）。

在编写完`Dockerfile`文件并将其保存之后，我们就只需要在该文件所在目录上执行`docker image build -t <镜像名> <Dockerfile文件的路径>`命令来构建镜像文件即可。在这里，`-t`参数用于指定`<镜像名>`，该名称中可以包含镜像的版本标签，如果没有特别指定标签，其创建的默认版本标签就是`latest`；而`<Dockerfile文件的路径>`具体在这里就应该是我们执行该命令时所在的当前目录。

基于篇幅方面的考虑，我们在这里记录的只是在使用Docker这一工具容器化 Express.js 应用程序时可能会用到的常用指令。如果读者希望更全面地了解在使用`Dockerfile`文件构建 Docker 镜像文件时所有可用的指令，可以自行前往 Docker 的官方网站查看其提供的文档资料。

----
#已完成
