# PowerShell 研究笔记

## scoop 包管理器

scoop 是一款基于 Windows 系统的命令行界面的包管理工具，类似 Ubuntu 系统中的 Apt 或 CentOS 中的 yum，可被视为是一款专门为程序员开发的软件管家，你不需要再一个一个的访问官网，然后找软件的安装包，而只需要一个命令，全部搞定。它不同于普通软件管家，其最大的特点是可以自动配置环境变量，自动解决依赖冲突。也就是说如果你是一个java开发者，你只需要用Scoop下载jdk就可以直接使用java命令查看版本等，而不需要再自己配置JAVA_HOME等环境变量，Scoop已经为你做好了；如果你有使用不同的版本需求，也可以下载两个不同版本的jdk，然后使用命令 scoop reset xxx 来切换版本，方便的“布哒鸟”。同理，Python等也可以进行管理。删除、更新也全部是命令搞定（下面会介绍）。更为舒服的是，如果你想换电脑或者重装系统的话（相同操作系统），可以直接将安装位置复制走，然后稍加操作就OK了，完全不用在一个一个的下载，你的数据也不会丢失。

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

3. 接下来需要安装一些使用 scoop 包管理器必备的软件，为此我们需要执行`scoop install aria2 git 7zip`命令，该命令会陆续安装 Aria2 下载工具，Git 版本控制工具以及 7-zip 压缩工具。同样的，如果默认的 scoop 下载源不给力，我们也可以指定要使用的软件源，例如：

    ```bash
    scoop install https://ghproxy.com/raw.githubusercontent.com/duzyn/scoop-cn/master/bucket/7zip.json
    scoop install https://ghproxy.com/raw.githubusercontent.com/duzyn/scoop-cn/master/bucket/git.json
    scoop install https://ghproxy.com/raw.githubusercontent.com/duzyn/scoop-cn/master/bucket/aria2.json

    # 或者
    scoop install https://cdn.jsdelivr.net/gh/duzyn/scoop-cn/bucket/7zip.json
    scoop install https://cdn.jsdelivr.net/gh/duzyn/scoop-cn/bucket/git.json
    scoop install https://cdn.jsdelivr.net/gh/duzyn/scoop-cn/bucket/aria2.json
    ```

4. 接下来要做的就是对 Aria2 下载工具进行一些配置，为此我们需要执行以下命令：

    ```bash
    scoop config aria2-split 3 
    scoop config aria2-max-connection-per-server 3 
    scoop config aria2-min-split-size 1M
    ```

5. 最后要做的是对 scoop 本身使用的软件源进行一些配置，为此我们需要执行以下命令：

    ```bash
    # 首先对scoop_repo进行更改
    scoop config SCOOP_REPO https://gitee.com/scoop-bucket/scoop

    # 然后再执行以下命令要订阅的软件源
    scoop bucket rm main
    scoop bucket add main https://mirror.nju.edu.cn/git/scoop-main.git
    scoop bucket add extras https://mirror.nju.edu.cn/git/scoop-extras.git

    # 以上两个是官方软件源在国内的镜像，所有软件建议优先从这里下载。
    scoop bucket add dorado https://gitee.com/scoop-bucket/dorado.git
    ```

在这里，我个人会强烈建议要添加上面这个名为 dorado 的软件源镜像。原因是除了其中包含了许多中文软件之外，更重要的是，部分国外的软件下载地址都在 Github 上，它们随时都有可能因为一些不可抗力的因素而无法下载。另外，请务必记得每次添加完软件源之后都应该执行`scoop update`命令，以便更新一下该包管理器的索引。

### 使用方式

<!-- 以下为待整理的资料 -->

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

    1、安装要求

    用户名文件夹不含中文（我的不是中文，不清楚如果是中文会发生什么，修改用户名文件夹为英文请看我的另一篇文章 传送门）
    Windows 7 SP1+ / Windows Server 2008+
    Powershell 5 及以上，.NET Framework 4.5 及以上

    $PSVersionTable.PSVersion.Major  # 查看Powershell版本 
    $PSVersionTable.CLRVersion.Major  # 查看.NET Framework版本
        1
        2

    这些要求一般情况下都是满足的

2、开始安装

1）安装到默认位置的话（C:\Users\scoop），什么都不用改；如果想安装到其他位置，Powershell执行以下命令（请全部阅读后在自行决定是否要用命令行改位置）：

 设置用户软件安装位置
$env:SCOOP='D:\Applications\Scoop' # 自己改你的位置，下同
[Environment]::SetEnvironmentVariable('SCOOP', $env:SCOOP, 'User')

 设置全局软件安装位置
$env:SCOOP_GLOBAL='F:\GlobalScoopApps'
[Environment]::SetEnvironmentVariable('SCOOP_GLOBAL', $env:SCOOP_GLOBAL, 'Machine')

1.这些命令其实就是添加了一个用户环境变量，和一个系统环境变量，如果嫌麻烦，可以自己直接打开环境变量自行添加（完全可以全部添加到系统环境变量），比这方便点儿，变量名分别是SCOOP和SCOOP_GLOBAL，对应的变量值分别为你的 用户软件安装位置 和 全局软件安装位置（打个比方，图二，本人的环境变量）
    2.不懂用户软件和全局软件的可以单纯的理解为，一个是给当前用户装的，一个是给所有用户装的，如果你的电脑只是自己使用，那就没啥区别了，但是使用命令行时有不同，全局安装必须有管理员权限

在这里插入图片描述
图二

2）以管理员身份打开PowerShell，输入以下命令

Set-ExecutionPolicy RemoteSigned -scope CurrentUser
#然后输入 Y 或 A 回车

3）执行安装命令

Invoke-Expression (New-Object System.Net.WebClient).DownloadString('https://get.scoop.sh')

 或者
iwr -useb get.scoop.sh | iex

  需要注意的是，这里可能会安装失败，因为访问外网会很慢

    方案一：添加报错信息中的网站到hosts（任有失败可能），具体方法百度

    方案二：使用 “科学上网” 方式（这个最直接）

    如果安装失败，删除安装位置下的文件，重新安装

三、基本使用
1、注意事项

1）先安装 7zip ，很多软件需要它才能安装。

2）添加bucket前，需要安装git 。

3）aria2 是一个下载加速工具，但有时视乎不太好用，自行体验并决定是否使用。

scoop install aria2  # 安装
scoop config aria2-max-connection-per-server 16 # 修改配置，不改也行
scoop config aria2-split 16
scoop config aria2-min-split-size 1M

 如果不想使用了，除了直接删除，还可以
scoop config aria2-enabled false
 想用的时候，把false改为true
2、软件安装命令

 scoop instal 软件名

scoop install 7zip
scoop install git

 可以使用 scoop search 软件名  查找是否有你需要的软件
 可以使用 scoop info 软件名 查看软件介绍
 如果第一次安装失败，需要先卸载，然后再次安装（自行探索即可知）
 如果某个软件有依赖它会自行安装，或安装完毕后提示你

 如果想要全局安装，以管理员身份打开PowerShell
scoop install -g xxxx

 或者可以安装 sudo ，然后在普通身份时也可以对全局进行操作：
scoop install -g sudo # 此时以管理员身份打开的Powershell

sudo scoop install -g git # 此时普通身份亦可

 使用 scoop list 可以查看已安装的所有软件

3、软件更新命令

# scoop update 软件名

scoop update git 

# 可以使用 scoop update * 一次性更新所有软件（必须在安装目录下使用）
# 使用 scoop update 更新scoop，有时当你安装或其他操作时scoop会自行更新自己，由于软件数量和版本极多，更新频率会有点高

 使用 scoop status 查看可更新的软件

4、卸载命令

 scoop uninstall 软件名

scoop uninstall git


5、添加bucket

1）什么是bucket？

可以理解为一个软件库，里面有很多的软件，当你所需要的软件没有时，你需要添加其所在的bucket

2）都有哪些bucket？

scoop bucket known # 列出已知所有官方bucket
-----------------------------------------------------
main         # 默认的bucket，大多数常用软件 
extras
versions	 # 一些软件的旧版本，比如mysql5.6
nightlies
nirsoft
php 		 
nerd-fonts
nonportable
java		 # java JDK，好多版本
games
jetbrains	 # jetbrains公司的所有软件

 自行探索要添加的bucket，当然，你可以全部添加。

    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    13
    14
    15

3）添加bucket

 scoop bucket add bucket名

scoop bucket add java

 使用 scoop bucket rm bucket名 移除不想要的bucket

 还可以添加别人（或组织）创建的bucket如：

 微信、QQ、钉钉、网易云音乐等国内常用
scoop bucket add dorado https://github.com/chawyehsu/dorado

国外常用
scoop bucket add dodorz https://github.com/dodorz/scoop-bucket

当你的多个bucket出现相同名字的软件，你可以指定bucket
scoop install main/git
当然你也可以自己创建一个，自行百度，此处不介绍

如果还不够，到官方给出的列表中查看https://github.com/rasa/scoop-directory/blob/master/by-score.md
这是一个md文件，由于较大，无法在线查看，可以下载后自行查看（英语不好的可要头疼了）


好了，scoop的基本使用就是这些了，希望对大家有用。使用时可以输入scoop help ，查看帮助文档自行研究。
