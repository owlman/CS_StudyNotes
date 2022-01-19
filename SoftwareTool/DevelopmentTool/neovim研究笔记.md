# neovim 研究笔记

本文将以 Ubuntu Linux 发行版为例来介绍 neovim 的安装与环境配置方法，并研究它的具体功能使用。

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

安装配置neovim
安装neovim

和安装nodejs一样，neovim下载地址：neovim

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

这时候就可以直接用nvim来打开neovim了
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

保存退出，进入neovim命令模式下输入PlugInstall自动安装，重启进入neovim,按下tab键就会有提示了，其他插件安装类似
安装coc.nvim

coc.nvim 是集代码补全、静态检测、函数跳转等功能的一个引擎

npm install -g neovim

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