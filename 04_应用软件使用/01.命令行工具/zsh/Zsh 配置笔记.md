---
title: Zsh 配置笔记
date: 2025-12-04
tags: 命令行工具
categories: 应用软件使用
---

## Zsh 简介

Z shell（以下简称 Zsh）是保罗·弗斯塔德（Paul Falstad）于 1990 年在普林斯顿大学求学时编写的、一款可用作交互式登录的 Shell 及脚本编写的命令解释器。Zsh 对 [Bourne shell](https://zh.wikipedia.org/wiki/Bourne_shell)做出了大量改进，同时加入了 [Bash](https://zh.wikipedia.org/wiki/Bash)、[ksh](https://zh.wikipedia.org/wiki/Korn_shell) 及 [tcsh](https://zh.wikipedia.org/wiki/Tcsh) 的某些功能。

2019 年，由于 Bash 的版本已經很旧，而新版本的 Bash v5 改采 GPLv3 授权，这是 Apple 公司无法接受的。于是自从那时起，macOS 系统上的预置 Shell 就已从 Bash 改为了 Zsh。另外，[Kali Linux](https://zh.wikipedia.org/wiki/Kali_Linux) 也使用 Zsh 作为预置 Shell。其主要特性包括：

- 提供可编程的命令行补全功能，该功能可帮助用户键入常用命令选项及参数；
- 提供可编程的命令行界面，包括将提示行信息显示在屏幕右侧，以及自动隐藏过长指令等功能；
- 提供可与任意 Shell 共享的命令行历史记录；
- 可在不借助外部程序的情况下实现文件的查找；
- 改进了针对变量/数组的处理方式；
- 允许在单缓冲区内编辑多行命令；
- 支持针对命令的拼写检查；
- 支持多种兼容模式（例如，Zsh 可在运行为`/bin/sh`的情况下伪装成 Bourne shell）
- 支持以加载模块的方式引入额外的功能，包括支持 Unix 域套接字控制、FTP 客户端等；
- 提供有`where`命令，该命令的使用方法与`which`命令类似，但返回的是指定指令在`$PATH`中的全部位置，而不是它当前最优先匹配的位置；
- 允许用户为指定目录设置别名，例如，用户可以为`/usr/bin`设置别名`/u`，这样在输入`/u`时，Zsh 会自动将其替换为`/usr/bin`；

## 安装步骤

在安装之前，我希望读者确定自己是在类 UNIX 系统下，因为 Zsh 是在类 UNIX 系统下运行的 Shell 程序，如果您使用的是 Windows 系统，推荐使用 Windows Subsystem for Linux（WSL）。下面书归正传，Zsh 在每个操作系统中的安装方式并不完全相同，下面是其在几种常见 Linux/UNIX 系统下的安装命令：

```bash
# macOS 系统下的安装命令：
brew install zsh

# ubuntu/debian 系统下的安装命令：
sudo apt install zsh

# CentOS 系统下的安装命令：
sudo yum install zsh

# ArchLinux/Manjaro 系统下的安装命令：
sudo pacman -S zsh
```

如果您使用的是上述操作系统之一，在执行完相应的安装命令之后，就可以使用`cat /etc/shells`命令查看当前系统可以用的 Shell 了。然后，只要在该命令返回的结果中看到`/bin/zsh`，就说明 Zsh 已经安装好了，如图 1 所示。

![图 1：当前可用的 Shell](./img/show_shell.png)

**图 1**：当前可用的 Shell

接下来，我们可以使用`chsh -s /bin/zsh`命令将 Zsh 设置为系统默认 Shell 了。如果到目前为止的操作一切顺利，现在只需要重新启动一个 Shell 会话（通常是一个命令行终端窗口），就会看到 Zsh 的初始配置了，如图 2 所示。

![图 2：Zsh 的配置引导界面](./img/initial.png)

**图 2**：Zsh 的配置引导界面

在上述界面中，如果我们输入`q`会直接退出配置引导，下一次运行 zsh 时会再次进入配置引导。如果输入`0`，也会退出配置引导，但是会在当前用户目录生成一个空白的文件`.zshrc`（路径为`~/.zshrc`），并且不会再进入配置引导界面。换言之，Zsh 会不会在启动时进入配置引导界面取决于当前用户目录下是否存在`.zshrc`文件，该文件是 Zsh 的默认配置文件，人们可以使用 vim 编辑器打开它并进行源码级别的手动配置。而如果我们在这里输入`1`，就会开始进行一系列自定义的配置。但通常情况下，考虑到`.zshrc`文件中各项配置的复杂性，我们在这里并不推荐读者直接进行手动配置，使用 Oh-My-Zsh 来进行配置会是更好的选择。

## Oh-My-Zsh

Oh-My-Zsh 是一款 Zsh 的配置管理工具，它提供了丰富的主题和插件，可以极大地美化命令行界面，并提高工作效率。我们需要这项工具的原因在于：原生的 Zsh 虽然很强大，但存在着以下几个问题：

- 稍复杂一些的配置就需要使用编码的方式修改`.zshrc`文件；
- 命令的自动补全和提示需要手动调教；
- 引入第三方主题与插件的相关配置就更为复杂了。

而 Oh-My-Zsh 的作用就是把这些复杂的配置一次性打包好，确保开箱即用，它相对于 Bash、原生 Zsh 的优势如表 1 所示：

| 项目     | Bash   | 原生 Zsh | Oh My Zsh    |
| -------- | ------ | -------- | ------------ |
| 自动补全 | 基础   | 强       | **非常强**   |
| 配置难度 | 低     | 高       | **低**       |
| 插件系统 | 无     | 无       | **有**       |
| 主题     | 基本无 | 有       | **大量现成** |
| 上手速度 | 快     | 慢       | **最快**     |

**表 1**：Bash、原生 Zsh 与 Oh My Zsh 的对比

在了解 Oh-My-Zsh 的基本信息以及所能发挥的功能之后，我们现在就来演示一下它的安装步骤：

- 在安装 Oh-My-Zsh 之前，需要确保本地已经安装了 Git，关于 Git 的安装与配置步骤，读者可参考我在《[[Git 使用笔记]]》中的记录；

- 打开 Zsh 终端窗口，并在用户目录下使用 curl 或 wget 命令下载 Oh-My-Zsh 的安装脚本，并执行它：

    ```bash
    # 使用 curl 下载脚本并安装：
    sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

    # 使用 wget 下载脚本并安装：
    sh -c "$(wget https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)"
    ```

- 在执行上述命令过程中，我们需要同意 Oh-My-Zsh 使用自身的配置模板覆盖已有的`.zshrc`文件，如图 3 所示（由于我已完成配置，不便截图，此处引用来自[网络的截图](https://www.haoyep.com/posts/zsh-config-oh-my-zsh/)）：

    ![图 3：Oh-My-Zsh 的安装界面](./img/install_OMZ.png)

    **图 3**：Oh-My-Zsh 的安装过程

待安装顺利完成之后，用户的`home`目录下会出现一个名为`.oh-my-zsh`的目录，该目录中存储的就是 Oh-My-Zsh 框架本身，及其主题和插件的实现代码。下面，我们从功能插件和外观配置两个方面来介绍 Oh-My-Zsh 的主要配置方法。

### 功能插件

Oh-My-Zsh 的核心竞争力主要来自于它所提供的那套极具开放性的，高度可定制的插件系统，这让我们可以根据自己的喜好进行选择和配置，打造一个富有个性的命令行终端界面。下面，先让我们来介绍一些常见的功能性插件：

| 插件                           | 功能                           |
| ------------------------------ | ------------------------------ |
| `z`                            | 可实现智能目录跳转。           |
| `git`                          | Git 相关增强。                 |
| `sudo`                         | 可通过双击`Esc`添加 sudo 权限。|
| `docker`                       | Docker 相关增强。              |
| `python`                       | Python 相关增强。              |
| `extract`                      | 提供`x`压缩包解压命令。        |
| `you-should-use`               | 命令行错误提示功能。           |
| `zsh-completions`              | 命令行自动补齐功能。           |
| `zsh-autosuggestions`          | 命令行自动提示功能。           |
| `zsh-syntax-highlighting`      | 命令行语法高亮功能。           |
| `zsh-history-substring-search` | 命令行历史记录搜索功能。       |

在 Oh-My-Zsh 中安装和启用插件通常可按照以下三个步骤来进行（如果是自带插件，则可跳过第一步）：

1. 如果我们要启用的不是 Oh-My-Zsh 自带的插件，那该插件通常会在 github 上有独立的仓库，人们需要先使用`git clone`命令将其下载到 Oh-My-Zsh 安装目录下的`custom/plugins`目录中，例如，我们要启用`zsh-autosuggestions`插件，就需要执行以下命令：

    ```bash
    git clone https://github.com/zsh-users/zsh-autosuggestions $ZSH_CUSTOM/plugins/zsh-autosuggestions
    ```

2. 使用 vim 这样的文本编辑器打开`.zshrc`文件，并在其中找到`plugins`字段，并将要启用的插件名称添加到该字段中（该字段的值是一个用空白符分隔的字符串），例如，如果我们现在要启用的插件包括`z`、`git`、`extract`、`you-should-use`、`zsh-completions`、`zsh-autosuggestions`、`zsh-syntax-highlighting`、`zsh-history-substring-search`，那么`.zshrc`文件中`plugins`字段的值就该被设置如下：

    ```bash
    plugins=(
        z 
        git
        extract
        you-should-use 
        zsh-completions 
        zsh-autosuggestions 
        zsh-syntax-highlighting 
        zsh-history-substring-search
    )
    ```

3. 保存并关闭`.zshrc`文件，然后执行`source ~/.zshrc`命令使配置生效。例如，图 4 所示的是启用`extract`插件之后，使用`x`命令解压文件的效果：

    ![图 4：extract 插件的效果](./img/extract.png)

    **图 4**：extract 插件的效果

### 外观配置

在 Oh-My-Zsh 中，我们可以通过一种被称之为“主题”的特殊插件来配置 Zsh 界面所呈现的外观，目的是通过各种特定的颜色和提示信息让命令行界面的易用性和美观性达到一个平衡。Oh-My-Zsh 内置了大量的主题，它们都位于 Oh-My-Zsh 安装目录下的`custom/themes`目录中（也可以前往 [Oh-My-Zsh 官方文档](https://github.com/ohmyzsh/ohmyzsh/wiki/Themes)查看），如图 5 所示：

![图 5：Oh-My-Zsh 内置的主题](./img/themes.png)

**图 5**：Oh-My-Zsh 内置的主题

如果我们想启用上述任意一个 Oh-My-Zsh 的内置主题，就只需将`.zshrc`文件中的`ZSH_THEME`变量值修改为该主题的名称即可，例如，假设现在要启用的是`agnoster`主题，我们就只需要执行以下步骤：

- 先使用 vim 这样的文本编辑器打开`.zshrc`文件；

- 找到`ZSH_THEME`变量，并将它的值设置如下即可：

    ```bash
    ZSH_THEME="agnoster" # 默认主题为 robbyrussell
    ```

- 保存并关闭`.zshrc`文件，然后执行`source ~/.zshrc`命令使配置生效，其效果如图 6 所示：
  
    ![图 6：agnoster 主题的效果](./img/agnoster.png)

    **图 6**：agnoster 主题的效果

当然，除了 Oh-My-Zsh 自带的这些主题之外，我们还可以选择安装其他开源的主题，例如，[powerlevel10k](https://github.com/romkatv/powerlevel10k)就是一个非常受欢迎的，功能强大的主题，它提供了丰富的配置选项，可以让我们打造出各种个性化的命令行界面，其安装与配置步骤如下：

1. 使用`git clone`命令将主题下载到 Oh-My-Zsh 安装目录下的`custom/themes`目录中：

    ```bash
    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
    ```

2. 使用 vim 这样的文本编辑器打开`.zshrc`文件，并在其中找到`ZSH_THEME`变量，并将它的值设置为我们刚刚下载的主题名称即可：

    ```bash
    ZSH_THEME="powerlevel10k/powerlevel10k"
    ```

3. 保存并关闭`.zshrc`文件，然后执行`source ~/.zshrc`命令使配置生效。在该主题配置首次生效时会启动一个配置向导（之后也可以通过执行`p10k configure`命令来启动该向导），引导我们完成主题的配置，如图 7 所示：

    ![图 7：powerlevel10k 主题的配置向导](./img/powerlevel10k.png)

    **图 7**：powerlevel10k 主题的配置向导

4. 接下来，我们只需要根据上述配置向导的提示，按照自己的喜欢一步一步地做出选择，就可以完成主题的配置，我个人的配置效果如图 8 所示：

    ![图 8：powerlevel10k 主题的配置效果](./img/powerlevel10k2.png)

    **图 8**：powerlevel10k 主题的配置效果

<!-- 以下待整理 -->
## 快捷命令

zsh 支持为较长命令设置一个别名，这样在使用时可以快捷输入。

这里以 cd ~/projects/alicode/blog 这个命令来举例：

在 .zshrc 中键入：
alias cdblog="cd ~/projects/alicode/blog" 
2. 开启新的 Shell 或 source ~/.zshrc，以使配置生效。生效后就可以使用 cdblog 进行跳转了。

除了自己设置 alias 之外，一些插件也内置内很多 alias。最常用的是 git 插件内置的 alias。例如，ga 就代表 git add，更多 git 插件内置 alias 可以在 git plugin alias 中查看。

其他

遇事不决，多敲 Tab。
