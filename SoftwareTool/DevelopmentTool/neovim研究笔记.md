# NeoVim 研究笔记

本文将以 Ubuntu Linux 发行版为系统环境来研究 NeoVim 的安装与环境配置方法，并学习使用它的具体功能。

- NeoVim 项目地址：[GitHub - neovim/neovim](https://github.com/neovim/neovim)
- Vim 原项目地址：[GitHub - vim/vim](https://github.com/vim/vim)

## 背景知识介绍

### NeoVim 起源

2014 年，巴西程序员 Thiago de Arruda Padilha（aka tarruda）曾经向 Vim 开源编辑器项目递交了两大补丁，其中对 Vim 的架构进行了大幅调整，结果遭到了 Vim 作者 Bram Moolenaar 的拒绝，因为后者认为对于 Vim 这样一个成熟的项目进行如此大的改变风险太高。于是 tarruda 发起了 Vim fork 项目 NeoVim，集资 1 万美元打造出 21 世纪的编辑器，提供更好的脚本、插件支持，整合现代的图形界面。

Bram Moolenaar 在写 Vim 时还是 90 年代初，至今已经 20 多年 过去了。其中，不仅包含了大量的遗留代码，而且程序的维护、Bug 的修复、以及新特性的添加都变得越来越困难。为了解决这些问题，NeoVim 项目应运而生。Neo 即“新”之意，它是 Vim 在这个新时代的重生。

### NeoVim 现状

根据 NeoVim 的自述说明，在总体上，它将达到下列目的 :

- 通过简化维护以改进 Bug 修复及特性添加的速度；
- 分派各个开发人员的工作；
- 实现新的、现代化的用户界面，而不必修改核心源代码；
- 利用新的、基于协同进程的新插件架构改善扩展性，并支持使用任何语言 编写插件

NeoVim 目前在 Mac 和 Linux 上运作的很好，而且从项目的 Commit 上来看，项目发起人（PM）是个非常有经验的人，管理有条不紊， 不过项目迭代也是相当快，几天一个版本。Ubuntu 有现成的 PPA 源方便及时更新。目前来说， NeoVim 已经实现 Vim 大部分功能，兼容Vim 90%+以上的配置。 小部分没有实现和兼容.

### 和 Vim 的差异

- NeoVim 只有终端版本. 没有 GUI 版本，但是Vim 有 GUI 版本；
- NeoVim 目前的剪贴板功能（寄存器） 和原生 Vim 实现不一 ；
- NeoVim 配置文件入口和 Vim 不同，可以通过 `:version`命令来查看；
- NeoVim 目前对外部语言的支持并不友好，目前只对 Python 支持比较完善，而 Vim 则支持比较全面；

## 基础环境配置

首先安装 Node.js，这里需要 12.0.0 以上的版本，因为我们之后在为其安装 coc.nvim 等插件时会用到它。为此，我们需要在 bash shell 环境中输入以下命令序列：

```bash
curl -fsSL https://deb.nodesource.com/setup_17.x | sudo -E bash -
sudo apt install -y nodejs
```

如果一切顺利，通过`node -v`和`npm -v`命令就会看到相应的版本。接下来，为了后续操作的顺利，我们需要将 NPM 所连接的默认仓库换成在国内的镜像：

```bash
npm config set registry https://registry.npm.taobao.org
```

接着，我们需要安装 Python3 环境，为此可以继续在 bash shell 环境中输入以下命令序列：

```bash
sudo apt install python3
sudo apt install python3-pip
pip install pynvim
```

最后，我们需要安装 curl 和 git，为此可以继续在 bash shell 环境中输入以下命令：

```bash
sudo apt install curl git
```

<!-- 以下内容尚未整理 -->

安装配置NeoVim
安装NeoVim

和安装nodejs一样，NeoVim下载地址：NeoVim

sudo ln -s /home/ykh/软件/nvim-linux64/bin/nvim nvim

    1

创建环境变量（第二个deepin没有，需要自己创建，不然安装coc.nvim会出错）：

sudo vim /etc/profile

    1

环境变量加入：

export PATH="/home/ykh/软件/nvim-linux64/bin:$PATH"
export TMPDIR="/tmp"

    1
    2

让环境变量生效：

source /etc/profile

    1

这时候就可以直接用nvim来打开NeoVim了
安装插件管理器

参看一下raw.githubusercontent.com的IP，有时候会连不上：IP查询
在这里插入图片描述
修改下host：

sudo nvim /etc/hosts

    1

加入：

199.232.96.133 raw.githubusercontent.com

    1

安装vim-plug

sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs \
       https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'


创建配置文件：

mkdir ~/.config/nvim/
nvim ~/.config/nvim/init.vim

输入（设置行号）

set nu

    1

保存退出，再次进入，显示行号了就成功了
安装插件
tab补全

编辑配置文件init.vim

  set nu

  call plug#begin('~/.vim/plugged')
                 
  Plug 'ervandew/supertab'
                 
  call plug#end()

    1
    2
    3
    4
    5
    6
    7

保存退出，进入NeoVim命令模式下输入PlugInstall自动安装，重启进入NeoVim,按下tab键就会有提示了，其他插件安装类似
安装coc.nvim

coc.nvim 是集代码补全、静态检测、函数跳转等功能的一个引擎

npm install -g NeoVim

    1

init.vim加入：

Plug 'neoclide/coc.nvim', {'branch': 'release'}

    1

然后进行自动安装，安装完成后可以输入命令 checkhealth 检查是否有错误
配置C++环境：

nvim命令模式输入：

:CocInstall coc-clangd # C++环境插件
:CocInstall coc-cmake  # Cmake 支持

    1
    2

打开一个.cpp文件

nvim test.cpp

    1

会出现提示：

[coc.nvim] clangd was not found on your PATH. :CocCommand clangd.install will install 11.0.0.

    1

C++ 需要安装clangd，输入:CocCommand clangd.install安装clangd，但我的失败了，另一个方法：

 sudo apt-get install clang-tools

    1

然后编写c++就有提示了
在这里插入图片描述
其他语言配置

:CocInstall coc-git    # git 支持
:CocInstall coc-highlight  # 高亮支持
:CocInstall coc-jedi   # jedi
:CocInstall coc-json   # json 文件支持
:CocInstall coc-python # python 环境支持
:CocInstall coc-sh     # bash 环境支持
:CocInstall coc-snippets # python提供 snippets
:CocInstall coc-vimlsp # lsp
:CocInstall coc-yaml   # yaml

配色

这里配色使用monokai，把monokai.vim下载下来，放到/root/.config/nvim/colors/目录下，没有就自己创建
monokai

修改init.vim，加入colorscheme monokai再次打开：
在这里插入图片描述
其他配置和插件
插件：

首先要安装ranger：sudo apt install ranger

Plug 'junegunn/vim-easy-align'
"ranger文件浏览器                                                                              
Plug 'kevinhwang91/rnvimr'
"更好看的标签栏                                                                                  
Plug 'vim-airline/vim-airline'                                                                              
Plug 'vim-airline/vim-airline-themes' "airline 的主题 


配置：

```vim
let g:airline#extensions#tabline#enabled = 1                                                                
let g:rnvimr_ex_enable = 1   
" Alt+o打开ranger                                                                                                                                                                                  
nnoremap <silent> <M-o> :RnvimrToggle<CR>                                                                   
"Alt+加号切换下一个标签，-号上一个                                                       
nnoremap <M-+> :bp<CR>                                                                                      
nnoremap <M--> :bn<CR>
```