# PowerShell 研究笔记

## scoop 包管理器

### 安装与配置

首先打开 PowerShell，并输入`Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`命令，以便赋予当前用户相关的操作权限。然后，我们就可以根据自身所在的网络环境来选择执行下面的某一条命令来安装 scoop 包管理器。

1. 如果想基于 scoop 的官方网站来安装，可执行下面这条命令：

    ```bash
    irm get.scoop.sh | iex
    ```

2. 如果因某些众所周知的原因连不上 scoop 的官方网站，那么可以试试下面的某一个命令，通过镜像链接来安装该包管理器：

    ```bash
    iwr -useb get.glimmer.ltd | iex
    # 或者
    irm https://ghproxy.com/raw.githubusercontent.com/duzyn/scoop-cn/master/install.ps1 | iex
    # 或者
    irm https://cdn.jsdelivr.net/gh/duzyn/scoop-cn/install.ps1 | iex
    ```

对scoop_repo进行更改

scoop config SCOOP_REPO https://gitee.com/scoop-bucket/scoop

执行以下命令订阅软件仓库

scoop bucket rm main

scoop bucket add main https://mirror.nju.edu.cn/git/scoop-main.git

scoop bucket add extras https://mirror.nju.edu.cn/git/scoop-extras.git

以上两个是官方bucket的国内镜像，所有软件建议优先从这里下载。

scoop bucket add dorado https://gitee.com/scoop-bucket/dorado.git

推荐添加dorado这个bucket镜像，里面很多中文软件，但是部分国外的软件下载地址在github，可能无法下载。
每次添加完仓库记得更新一下！


### 使用方式

执行以下命令安装必装软件

scoop install aria2 git 7zip

反正你肯定要用到！
或者

scoop install https://ghproxy.com/raw.githubusercontent.com/duzyn/scoop-cn/master/bucket/7zip.json
scoop install https://ghproxy.com/raw.githubusercontent.com/duzyn/scoop-cn/master/bucket/git.json
scoop install https://ghproxy.com/raw.githubusercontent.com/duzyn/scoop-cn/master/bucket/aria2.json

或者

scoop install https://cdn.jsdelivr.net/gh/duzyn/scoop-cn/bucket/7zip.json
scoop install https://cdn.jsdelivr.net/gh/duzyn/scoop-cn/bucket/git.json
scoop install https://cdn.jsdelivr.net/gh/duzyn/scoop-cn/bucket/aria2.json

对aria2进行设置

scoop config aria2-split 3 
scoop config aria2-max-connection-per-server 3 
scoop config aria2-min-split-size 1M

scoop update

最后说一句：可以登录https://scoop.sh/#/buckets
上面可以看到很多bucket以及软件数
然后就开始愉快的玩耍scoop吧

执行以下命令安装仓库中的软件：

scoop install <仓库名>/<软件名> -s

这个-s是取消hash校验，建议加上

另外附上常用命令

scoop update #更新仓库
scoop update * #更新所有软件
scoop list #列出已安装的软件
scoop bucket list #列出已订阅的仓库

后记

选择scoop纯属意外，也是无奈，因为电脑用户被锁了管理员权限，所有exe安装程序都无法安装，只可以用绿色软件，最后被我发现scoop，省去了到处下载XXX绿色版的烦恼，当然scoop里需要管理员权限的软件也跟我无缘了（譬如everything）。
自用软件

| 软件         | 简介           | 来源             |
| ------------ | -------------- | ---------------- |
| Inkscape     | 矢量图制作     | extras           |
| xyplorer     | 资源管理器     | extras           |
| wechat       | 微信pc版       | 自制             |
| neteasemusic | 网易云音乐     | 自制             |
| jianyingpro  | 剪映pc版       | 自制             |
| Eudic        | 欧路词典       | 自制             |
| baidunetdisk | 百度网盘       | 自制             |
| XunLei       | 迅雷11         | 自制             |
| TIM          | 企业QQ         | 自制             |
| dfcf         | 东方财富       | 自制             |
| QQ           | QQ             | DEV-tools        |
| VLC          | 视频播放器     | TUNA镜像站绿色版 |
| vscodium     | vscode开源版   | TUNA镜像站绿色版 |
| OBS-studio   | 录屏软件       | TUNA镜像站绿色版 |
| snipaste     | 截图软件       | 官网绿色版       |
| xdown        | 下载软件       | 官网绿色版       |
| sumatraPDF   | 阅读软件       | 官网绿色版       |
| everything   | 搜索软件       | 官网绿色版       |
| yu-writer    | markdown编辑器 | 官网绿色版       |
| WinPython    | python集成软件 | 官网绿色版       |