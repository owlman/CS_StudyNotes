---
title: Zsh 使用笔记
date: 2025-12-04
tags: 命令行工具
categories: 待整理笔记
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

在上述界面中，如果我们输入`q`会直接退出配置引导，下一次运行 zsh 时会再次进入配置引导。如果输入`0`，也会退出配置引导，但是会在当前用户目录生成一个空白的文件`.zshrc`（路径为`~/.zshrc`），并且不会再进入配置引导界面。换言之，Zsh 会不会在启动时进入配置引导界面取决于当前用户目录下是否存在`.zshrc`文件，该文件是 Zsh 的默认配置文件，人们可以使用 vim 编辑器打开它并进行源码级别的手动配置。而如果我们在这里输入`1`，就会开始进行一系列自定义的配置。但通常情况下，考虑到`.zshrc`文件的复杂性，我们在这里并不推荐读者直接进行手动配置，使用 oh-my-zsh 来进行配置会是更好的选择。

## Oh-my-zsh

zsh 配置提示

未经配置的 zsh，看起来很朴素：

默认 zsh 主题样式

由于 zsh 配置较为复杂，推荐大家使用配置管理工具来配置 zsh，花很少时间就可以得到一个称手的 zsh。下面介绍如何使用 oh-my-zsh 来修改 zsh 的主题和安装常用的插件。

## oh-my-zsh

安装 oh-my-zsh 之前，需要确保本地已经安装了 git。

使用 curl 下载脚本并安装：

sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
或者使用 wget 下载脚本并安装：

sh -c "$(wget https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)"
然后同意使用 Oh-my-zsh 的配置模板覆盖已有的 .zshrc：


安装 oh-my-zsh
在配置过程中，脚本会提示将 zsh 设为默认的 shell:


设置 zsh 为默认shell
这样就安装好 oh-my-zsh 了，下面我们开始通过 oh-my-zsh 来配置 zsh 。

配置 zsh
修改主题
在 https://github.com/ohmyzsh/ohmyzsh/wiki/Themes 中查看内置的主题样式和对应的主题名。这些内置主题已经放在 ～/.oh-my-zsh/themes 目录下，不需要再下载。


oh-my-zsh 内置主题
除了内置主题外，还可以选择其他开源的主题，强烈推荐尝试一下 powerlevel10k 主题，一个顶十个，项目地址为：https://github.com/romkatv/powerlevel10k

oh-my-zsh 安装这个款主题的方法：使用 git 将文件 clone 只指定文件夹 ～/.oh-my-zsh/custom/themes/powerlevel10k ，命令如下：

git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
使用 vim 编辑 .zshrc，键入以下内容并保存：

ZSH_THEME="powerlevel10k/powerlevel10k"
最后，执行 source ~/.zshrc 配置生效，这时会提示对主题进行配置，按照提示进行即可。

安装插件

oh-my-zsh 已经内置了 git 插件，内置插件可以在 ～/.oh-my-zsh/plugins 中查看 ，下面介绍一下我常用的三个插件，更多插件可以在 awesome-zsh-plugins 里查看。

zsh-autosuggestions
zsh-autosuggestions 是一个命令提示插件，，当你输入命令时，会自动推测你可能需要输入的命令，按下右键可以快速采用建议。效果如下：


zsh-autosuggestions 插件效果

安装步骤：

把插件下载到本地的 ~/.oh-my-zsh/custom/plugins 目录：

git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

2. 在 .zshrc 中，把 zsh-autosuggestions 加入插件列表：

plugins=(
    # other plugins...
    zsh-autosuggestions  # 插件之间使用空格隔开
)
3. 开启新的 Shell 或执行 source ~/.zshrc，就可以开始体验插件。

zsh-syntax-highlighting
zsh-syntax-highlighting 是一个命令语法校验插件，在输入命令的过程中，若指令不合法，则指令显示为红色，若指令合法就会显示为绿色。效果如下：


zsh-syntax-highlighting 插件效果
安装步骤：

把插件下载到本地的 ~/.oh-my-zsh/custom/plugins 目录:
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting 
2. 在 .zshrc 中，把 `zsh-syntax-highlighting` 加入插件列表：

plugins=(
    # other plugins...
    zsh-autosuggestions
    zsh-syntax-highlighting
)
3. 开启新的 Shell 或执行 source ~/.zshrc，就可以开始体验插件了。

z
z 是一个文件夹快捷跳转插件，对于曾经跳转过的目录，只需要输入最终目标文件夹名称，就可以快速跳转，避免再输入长串路径，提高切换文件夹的效率。效果如下：


z 插件效果
安装步骤：

由于 oh-my-zsh 内置了 z 插件，所以只需要在 .zshrc 中，把 z 加入插件列表：
plugins=(
     # other plugins...
     zsh-autosuggestions
     zsh-syntax-highlighting
     z
)
2. 开启新的 Shell 或执行 source ~/.zshrc，就可以开始体验插件了。

设置 alias
zsh 支持为较长命令设置一个别名，这样在使用时可以快捷输入。

这里以 cd ~/projects/alicode/blog 这个命令来举例：

在 .zshrc 中键入：
alias cdblog="cd ~/projects/alicode/blog" 
2. 开启新的 Shell 或 source ~/.zshrc，以使配置生效。生效后就可以使用 cdblog 进行跳转了。

除了自己设置 alias 之外，一些插件也内置内很多 alias。最常用的是 git 插件内置的 alias。例如，ga 就代表 git add，更多 git 插件内置 alias 可以在 git plugin alias 中查看。

其他

遇事不决，多敲 Tab。

原文地址：zsh 安装与配置：9步打造高效命令行

在 https://www.alicode.pro从零件开始组装自己的开发机、安装环境，开发自己的软件，欢迎关注。

<!-- 以下来自Wikipedia -->


[![](https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Zsh-agnoster.png/250px-Zsh-agnoster.png)](https://zh.wikipedia.org/wiki/File:Zsh-agnoster.png)

运行于[Konsole](https://zh.wikipedia.org/wiki/Konsole "Konsole")终端模拟器上使用Agnoster主题的Zsh

用户社区网站"Oh My Zsh"收集Z shell的第三方插件及主题。<sup id="cite_ref-8"><a href="https://zh.wikipedia.org/wiki/Z_shell#cite_note-8"><span>[</span>8<span>]</span></a></sup>截止于2018年，其[GitHub](https://zh.wikipedia.org/wiki/GitHub "GitHub")源共有超过1000位贡献者、200多款插件和超过140款主题。同时也带有更新已安装插件及主题的自动更新工具。<sup id="cite_ref-9"><a href="https://zh.wikipedia.org/wiki/Z_shell#cite_note-9"><span>[</span>9<span>]</span></a></sup>

-   [Shell对比](https://zh.wikipedia.org/w/index.php?title=Shell%E5%AF%B9%E6%AF%94&action=edit&redlink=1 "Shell对比（页面不存在）")
