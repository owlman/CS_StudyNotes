# MongoDB 研究笔记（待整理）

    MongoDB 4.2 Community Edition删除了对x86_64上的Ubuntu 14.04（“ Trusty”）的支持
    MongoDB 4.2 Community Edition删除了对ARM64上的Ubuntu 16.04（“ Xenial”）的支持

MongoDB 4.2 Community Edition 在x86_64体系结构上支持以下 64位 Ubuntu LTS（长期支持）版本 ：

    18.04 LTS（“仿生”）
    16.04 LTS（“ Xenial”）

MongoDB仅支持这些平台的64位版本。

Ubuntu上的MongoDB 4.2社区版还支持某些平台上的 ARM64和 s390x架构。

有关更多信息，请参见支持的平台。

Windows Linux子系统（WSL）-不支持

MongoDB不支持Linux的Windows子系统（WSL）。
生产注意事项

在生产环境中部署MongoDB之前，请考虑 生产说明文档，该文档提供了有关生产MongoDB部署的性能注意事项和配置建议。
官方的MongoDB软件包

要在Ubuntu系统上安装MongoDB社区，这些说明将使用官方mongodb-org软件包，该软件包由MongoDB Inc.维护和支持。该官方mongodb-org 软件包始终包含MongoDB的最新版本，可从其自己的专用存储库中获得。

重要

mongodbUbuntu提供的软件包不受 MongoDB Inc.维护，并且与官方mongodb-org软件包冲突 。如果您已经mongodb 在Ubuntu系统上安装了该软件包，则必须先卸载该mongodb软件包，然后再按照这些说明进行操作。

有关官方软件包的完整列表，请参阅MongoDB社区版软件包。
安装MongoDB社区版

请按照以下步骤使用apt程序包管理器安装MongoDB Community Edition 。
1个
导入包管理系统使用的公钥。

在终端上，发出以下命令以从https://www.mongodb.org/static/pgp/server-4.2.asc导入MongoDB公共GPG密钥：

wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -

该操作应以响应OK。

但是，如果收到指示gnupg未安装的错误，则可以：

    gnupg使用以下命令安装及其所需的库：

    sudo apt-get install gnupg

    安装完成后，重试导入密钥：

    wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -

2
为MongoDB创建一个列表文件。

/etc/apt/sources.list.d/mongodb-org-4.2.list为您的Ubuntu版本创建列表文件 。

单击适合您的Ubuntu版本的选项卡。如果不确定主机正在运行哪个Ubuntu版本，请在主机上打开终端或shell并执行。lsb_release -dc

    Ubuntu 18.04（仿生）
    Ubuntu 16.04（Xenial）

以下说明适用于Ubuntu 18.04（Bionic）。对于Ubuntu 16.04（Xenial），单击相应的选项卡。

/etc/apt/sources.list.d/mongodb-org-4.2.list 为Ubuntu 18.04（Bionic）创建 文件：

echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list

以下说明适用于Ubuntu 16.04（Xenial）。对于Ubuntu 18.04（Bionic），单击相应的选项卡。

/etc/apt/sources.list.d/mongodb-org-4.2.list 为Ubuntu 16.04（Xenial）创建 文件：

echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list

3
重新加载本地软件包数据库。

发出以下命令以重新加载本地软件包数据库：

sudo apt-get update

4
安装MongoDB软件包。

您可以安装最新的稳定版MongoDB或特定版本的MongoDB。

    安装最新版本的MongoDB。
    安装特定版本的MongoDB。

要安装最新的稳定版本，请发出以下命令

sudo apt-get install -y mongodb-org

要安装特定发行版，您必须分别指定每个组件包以及版本号，如以下示例所示：

sudo apt-get install -y mongodb-org=4.2.6 mongodb-org-server=4.2.6 mongodb-org-shell=4.2.6 mongodb-org-mongos=4.2.6 mongodb-org-tools=4.2.6

如果仅安装mongodb-org=4.2.6而不包括组件包，则无论您指定哪个版本，都将安装每个MongoDB包的最新版本。

可选的。尽管您可以指定任何可用的MongoDB版本，但 apt-get将在更新版本可用时升级软件包。为防止意外升级，您可以将软件包固定在当前安装的版本上：

echo "mongodb-org hold" | sudo dpkg --set-selections
echo "mongodb-org-server hold" | sudo dpkg --set-selections
echo "mongodb-org-shell hold" | sudo dpkg --set-selections
echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
echo "mongodb-org-tools hold" | sudo dpkg --set-selections

有关在Ubuntu上安装MongoDB时遇到的故障排除错误的帮助，请参阅我们的 故障排除指南。
运行MongoDB社区版

ulimit注意事项
    大多数类Unix操作系统都限制了会话可能使用的系统资源。这些限制可能会对MongoDB的运行产生负面影响。有关更多信息，请参见UNIX ulimit设置。

目录

    如果通过程序包管理器安装，则在安装过程中将创建数据目录 /var/lib/mongodb和日志目录/var/log/mongodb。

    默认情况下，MongoDB使用mongodb用户帐户运行。如果更改运行MongoDB进程的用户，则还必须修改对数据和日志目录的权限，以使该用户可以访问这些目录。
配置文件
    官方的MongoDB软件包包括一个配置文件（/etc/mongod.conf）。这些设置（例如数据目录和日志目录规范）在启动时生效。也就是说，如果在运行MongoDB实例时更改配置文件，则必须重新启动实例以使更改生效。

程序

请按照以下步骤在系统上运行MongoDB Community Edition。这些说明假定您使用的是官方mongodb-org 软件包，而不是mongodbUbuntu提供的非官方软件包，并且使用的是默认设置。

初始化系统

要运行和管理您的mongod流程，您将使用操作系统的内置init系统。Linux的最新版本倾向于使用systemd（使用systemctl命令），而Linux的较早版本倾向于使用System V init（使用service命令）。

如果不确定平台使用哪个初始化系统，请运行以下命令：

ps --no-headers -o comm 1

然后根据结果在下面选择适当的选项卡：

    systemd-选择下面的systemd（systemctl）标签。
    init-选择下面的System V Init（服务）标签。


    systemd（systemctl）
    系统V初始化（服务）

1个
启动MongoDB。

您可以mongod通过发出以下命令来启动该过程：

sudo systemctl start mongod

如果在启动时收到类似于以下内容的错误 mongod：
Failed to start mongod.service: Unit mongod.service not found.

首先运行以下命令：

sudo systemctl daemon-reload

然后再次运行上面的启动命令。
2
验证MongoDB已成功启动。

sudo systemctl status mongod

您可以有选择地通过发出以下命令来确保MongoDB将在系统重启后启动：

sudo systemctl enable mongod

3
停止MongoDB。

根据需要，可以mongod通过发出以下命令来停止该过程：

sudo systemctl stop mongod

4
重新启动MongoDB。

您可以mongod通过发出以下命令来重新启动该过程：

sudo systemctl restart mongod

您可以通过查看/var/log/mongodb/mongod.log文件中的输出来跟踪错误或重要消息的处理状态。
5
开始使用MongoDB。

mongo在与相同的主机上启动Shell mongod。您可以在mongo不使用任何命令行选项的情况下运行Shell，以mongod使用默认端口27017 连接到在本地主机上运行的shell ：

mongo

有关使用mongo Shell 连接的更多信息，例如连接到mongod在其他主机和/或端口上运行的实例，请参阅mongo Shell。

为了帮助您开始使用MongoDB，MongoDB提供了各种驱动程序版本的入门指南。有关可用版本，请参阅 入门。
1个
启动MongoDB。

发出以下命令以启动mongod：

sudo service mongod start

2
验证MongoDB已成功启动

验证该mongod过程已成功启动：

sudo service mongod status

您还可以在日志文件中查看mongod进程的当前状态， /var/log/mongodb/mongod.log默认情况下位于： 。运行中的 mongod实例将通过以下行表明已准备好进行连接：

[initandlisten] waiting for connections on port 27017
3
停止MongoDB。

根据需要，可以mongod通过发出以下命令来停止该过程：

sudo service mongod stop

4
重新启动MongoDB。

发出以下命令以重新启动mongod：

sudo service mongod restart

5
开始使用MongoDB。

mongo在与相同的主机上启动Shell mongod。您可以在mongo不使用任何命令行选项的情况下运行Shell，以mongod使用默认端口27017 连接到在本地主机上运行的shell ：

mongo

有关使用mongo Shell 连接的更多信息，例如连接到mongod在其他主机和/或端口上运行的实例，请参阅mongo Shell。

为了帮助您开始使用MongoDB，MongoDB提供了各种驱动程序版本的入门指南。有关可用版本，请参阅 入门。
卸载MongoDB社区版

要从系统中完全删除MongoDB，必须删除MongoDB应用程序本身，配置文件以及任何包含数据和日志的目录。以下部分将指导您完成必要的步骤。

警告

此过程将完全删除MongoDB，其配置和所有 数据库。此过程不可逆，因此请确保在继续操作之前备份所有配置和数据。
1个
停止MongoDB。

mongod通过发出以下命令来停止该过程：

sudo service mongod stop

2
删除软件包。

删除以前安装的所有MongoDB软件包。

sudo apt-get purge mongodb-org*

3
删除数据目录。

删除MongoDB数据库和日志文件。

sudo rm -r /var/log/mongodb
sudo rm -r /var/lib/mongodb

其他信息
默认为localhost绑定

默认情况下，MongoDB启动时将其bindIp设置为 127.0.0.1，该绑定到localhost网络接口。这意味着mongod只能接受来自同一计算机上运行的客户端的连接。除非将此值设置为有效的网络接口，否则远程客户端将无法连接到mongod，并且mongod不能初始化副本集。

可以配置此值：

    在MongoDB配置文件中，带有bindIp或
    通过命令行参数 --bind_ip

警告

在绑定到非本地主机（例如，可公共访问）的IP地址之前，请确保已保护群集免受未经授权的访问。有关安全建议的完整列表，请参阅“ 安全清单”。至少应考虑 启用身份验证并 强化网络基础架构。

有关配置的更多信息bindIp，请参见 IP绑定。
MongoDB社区版软件包

MongoDB Community Edition可从其自己的专用存储库中获得，并且包含以下官方支持的软件包：
包裹名字 	描述
mongodb-org 	一metapackage，将自动安装以下四个组件包。
mongodb-org-server 	包含mongod守护程序，关联的初始化脚本和配置文件（/etc/mongod.conf）。您可以使用初始化脚本从mongod 配置文件开始。有关详细信息，请参阅Run MongoDB Community Edition。
mongodb-org-mongos 	包含mongos守护程序。
mongodb-org-shell 	包含mongo外壳。
mongodb-org-tools 	包含以下的MongoDB工具：，，， ， ，，和。mongoimport bsondumpmongodumpmongoexportmongofilesmongorestoremongostatmongotop

MongoDB 中文网

----
#计划中
