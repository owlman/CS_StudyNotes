---
title: zsh 使用笔记
date: 2025-12-04
tags: 软件使用
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

## 安装与配置

每个操作系统安装方式不一 ，这里只介绍我用过的操作系统的安装方法。

macOS：

brew install zsh
ubuntu：

sudo apt-get install zsh
ArchLinux/Manjaro：

sudo pacman -S zsh
若你使用的是其他发行版本，则使用对应的包管理器安装即可。

安装好后，使用 cat /etc/shells 查看系统可以用的 shell：

系统内可用的shell
使用 chsh -s /bin/zsh 命令将 zsh 设置为系统默认 shell。新开一个 Shell Session，就可以开始使用 zsh 了。

第一次运行 zsh 时会进入如下的配置引导页面：

zsh 配置引导页面
输入 q 会直接退出配置引导，下一次运行 zsh 时会再次进入配置引导。

输入 0，也会退出配置引导，但是会在当前用户目录生成一个空白的文件 .zshrc，下一次运行时就不会再进入配置引导。下一次运行时是否再进入配置引导，取决于用户目录下是否存在.zshrc 文件。

输入输入 1 后，就开始进行配置，如下：


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

1.  ^ [跳转到： <sup><b>1.0</b></sup>](https://zh.wikipedia.org/wiki/Z_shell#cite_ref-ZshManual_1-0) [<sup><b>1.1</b></sup>](https://zh.wikipedia.org/wiki/Z_shell#cite_ref-ZshManual_1-1) [The Z Shell Manual](http://zsh.sourceforge.net/Doc/Release/Introduction.html#Author) (Version 5.0.0). Sourceforge.net. July 21, 2012 \[September 18, 2012\]. （原始内容[存档](https://web.archive.org/web/20180220011558/http://zsh.sourceforge.net/Doc/Release/Introduction.html#Author)于2018-02-20）.
2.  ^ [跳转到： <sup><b>2.0</b></sup>](https://zh.wikipedia.org/wiki/Z_shell#cite_ref-wikidata-6a09ee00ad86b0d9690112bdc4da420046938ba0-v3_2-0) [<sup><b>2.1</b></sup>](https://zh.wikipedia.org/wiki/Z_shell#cite_ref-wikidata-6a09ee00ad86b0d9690112bdc4da420046938ba0-v3_2-1) [zsh 5.9 released](https://www.zsh.org/mla/announce/msg00134.html).
3.  **[^](https://zh.wikipedia.org/wiki/Z_shell#cite_ref-3 "跳转")** [zsh / Code / \[281031\] /LICENCE](http://sourceforge.net/p/zsh/code/ci/master/tree/LICENCE). Paul Falstad. \[February 7, 2015\]. （原始内容[存档](https://web.archive.org/web/20210302213122/https://sourceforge.net/p/zsh/code/ci/master/tree/LICENCE)于2021-03-02）.
4.  **[^](https://zh.wikipedia.org/wiki/Z_shell#cite_ref-4 "跳转")** [zsh - a ksh/tcsh-like shell (part 1 of 8)](https://groups.google.com/group/alt.sources/msg/936c7876941058ed). alt.sources. December 14, 1990 \[September 18, 2012\].
5.  **[^](https://zh.wikipedia.org/wiki/Z_shell#cite_ref-5 "跳转")** [Z-Shell Frequently-Asked Questions](http://zsh.sourceforge.net/FAQ/zshfaq01.html#l3). Sourceforge.net. February 15, 2010 \[September 18, 2012\]. （原始内容[存档](https://web.archive.org/web/20210302213122/http://zsh.sourceforge.net/FAQ/zshfaq01.html#l3)于2021-03-02）.
6.  **[^](https://zh.wikipedia.org/wiki/Z_shell#cite_ref-6 "跳转")** [The Z-Shell (ZSH) Lovers' Page](http://www.guckes.net/zsh/lover.html). Guckes.net. c. 2004 \[October 2, 2012\]. （原始内容[存档](https://web.archive.org/web/20170517213919/http://www.guckes.net/zsh/lover.html)于2017-05-17）.
7.  **[^](https://zh.wikipedia.org/wiki/Z_shell#cite_ref-7 "跳转")** [Zsh Mailing List Archive](http://www.zsh.org/mla/users/2005/msg00951.html). Zsh.org. August 8, 2005 \[October 2, 2012\]. （原始内容[存档](https://web.archive.org/web/20210302213117/https://www.zsh.org/mla/users/2005/msg00951.html)于2021-03-02）.
8.  **[^](https://zh.wikipedia.org/wiki/Z_shell#cite_ref-8 "跳转")** [Oh My ZSH - Community driven framework with 150+ plugins and 100+ themes](https://ohmyz.sh/). \[May 7, 2014\]. （原始内容[存档](https://web.archive.org/web/20220320201812/https://ohmyz.sh/)于2022-03-20）.
9.  **[^](https://zh.wikipedia.org/wiki/Z_shell#cite_ref-9 "跳转")** [robbyrussell/oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh). \[2018-10-17\]. （原始内容[存档](https://web.archive.org/web/20210302213118/https://github.com/ohmyzsh/ohmyzsh)于2021-03-02）. A delightful community-driven (with 1,000+ contributors) framework for managing your zsh configuration. Includes 200+ optional plugins (rails, git, OSX, hub, capistrano, brew, ant, php, python, etc), over 140 themes to spice up your morning, and an auto-update tool so that makes it easy to keep up with the latest updates from the community.

-   [主要网站](https://www.zsh.org/) （[页面存档备份](https://web.archive.org/web/20220401133343/https://www.zsh.org/)，存于[互联网档案馆](https://zh.wikipedia.org/wiki/%E4%BA%92%E8%81%94%E7%BD%91%E6%A1%A3%E6%A1%88%E9%A6%86 "互联网档案馆")）
-   [Sourceforge 项目页](https://sourceforge.net/projects/zsh/) （[页面存档备份](https://web.archive.org/web/20220401051958/https://sourceforge.net/projects/zsh/)，存于[互联网档案馆](https://zh.wikipedia.org/wiki/%E4%BA%92%E8%81%94%E7%BD%91%E6%A1%A3%E6%A1%88%E9%A6%86 "互联网档案馆")）
-   [邮件列表存档](https://www.zsh.org/mla/) （[页面存档备份](https://web.archive.org/web/20220330215106/https://www.zsh.org/mla/)，存于[互联网档案馆](https://zh.wikipedia.org/wiki/%E4%BA%92%E8%81%94%E7%BD%91%E6%A1%A3%E6%A1%88%E9%A6%86 "互联网档案馆")）
-   [ZSH维基](http://zshwiki.org/) （[页面存档备份](https://web.archive.org/web/20090106034724/http://zshwiki.org/)，存于[互联网档案馆](https://zh.wikipedia.org/wiki/%E4%BA%92%E8%81%94%E7%BD%91%E6%A1%A3%E6%A1%88%E9%A6%86 "互联网档案馆")）

-   [Zzapper的ZSH小技巧](http://www.zzapper.co.uk/zshtips.html) （[页面存档备份](https://web.archive.org/web/20220212184448/http://www.zzapper.co.uk/zshtips.html)，存于[互联网档案馆](https://zh.wikipedia.org/wiki/%E4%BA%92%E8%81%94%E7%BD%91%E6%A1%A3%E6%A1%88%E9%A6%86 "互联网档案馆")）
-   [TuxRadar：轻松上手Z Shell](http://www.tuxradar.com/content/z-shell-made-easy) （[页面存档备份](https://web.archive.org/web/20170512140142/http://www.tuxradar.com/content/z-shell-made-easy)，存于[互联网档案馆](https://zh.wikipedia.org/wiki/%E4%BA%92%E8%81%94%E7%BD%91%E6%A1%A3%E6%A1%88%E9%A6%86 "互联网档案馆")）
-   [用户指南](http://zsh.sourceforge.net/Guide/zshguide.html) （[页面存档备份](https://web.archive.org/web/20210426213352/http://zsh.sourceforge.net/Guide/zshguide.html)，存于[互联网档案馆](https://zh.wikipedia.org/wiki/%E4%BA%92%E8%81%94%E7%BD%91%E6%A1%A3%E6%A1%88%E9%A6%86 "互联网档案馆")）

-   [开放目录项目](https://zh.wikipedia.org/wiki/%E5%BC%80%E6%94%BE%E5%BC%8F%E7%9B%AE%E5%BD%95 "开放式目录")中的“[zsh](https://curlie.org/Computers/Software/Operating_Systems/Unix/Shell/zsh/)”