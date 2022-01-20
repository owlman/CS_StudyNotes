# NeoVim 学习笔记

## 研究资源

- NeoVim 官方网站：[NeoVim.io](https://NeoVim.io/)
- NeoVim 项目仓库：[GitHub - NeoVim/NeoVim](https://github.com/NeoVim/NeoVim)

## 背景知识

### NeoVim 起源

2014 年，巴西程序员 Thiago de Arruda Padilha（aka tarruda）曾经向 Vim 开源编辑器项目递交了两大补丁，其中包含了对 Vim 的架构进行大幅调整的建议，结果遭到了 Vim 作者 Bram Moolenaar 的拒绝。因为后者认为对于 Vim 这样一个成熟的项目进行如此大的改变风险太高。但或许在 tarruda 看来，Vim 这个上个世纪 90 年代初的产物，至今已经 20 多年了，该项目中不仅遗留了大量的历史痕迹，而且该项目的管理层如今在程序的维护、Bug 的修复、以及新特性的添加等问题上的态度都在变得越来越僵化，且难以与时俱进。

总而言之，基于对 Vim 项目的不满，并致力于打造一款面向 21 世纪的代码编辑器，tarruda 先生以众筹资金的方式发起了 Vim 的这个 fork 项目：NeoVim。在这里，Neo 这个单词表达的是其作者对 Vim 编辑器在这个新时代的重生期待。

### NeoVim 现状

从 NeoVim 项目的提交记录可以看出，tarruda 先生是个非常有项目维护经验的人，其有条不紊的管理让 NeoVim 的版本迭代相当快速，基本上几天就会推送一个新的版本。目前来说， NeoVim 已经实现 Vim 大部分功能，并兼容了 Vim 百分之九十以上的配置。根据该项目的自述说明，它最终想实现以下目标 :

- 通过简化项目的维护工作来改进 Bug 修复及特性添加的速度；
- 在实现新的、现代化的用户界面时不必修改编辑器的核心源码；
- 可利用新的、基于协同进程的新插件架构改善编辑器的扩展性；
- 支持使用 Python 等多种第三方编程语言与 NeoVim 进行交互；

随着时间的推移，NeoVim 项目逐渐发展成为一个成熟的项目，并率先提供了多个 8.0 版本之前的 Vim 所没有的新特性：

- 支持在 Vim 中打开命令行终端窗口，使用户不必退出编辑器就能执行 bash 命令；
- 为 vimscript 提供了异步任务的支持，之前的 vimscirpt 只能以同步的方式执行任务；
- 重构了 Vim 的部分代码，实现了多平台兼容，并可使用更加现代化的代码编译工具链；

但与此同时，NeoVim 项目的成功也反过来唤起了 Vim 项目组的危机意识，重新激发了他们的开发热情，促使 Vim 在 7.0 之后加快了新功能开发进度，很快发布了 Vim 8.0/8.1，把 NeoVim 实现的大部分新特性在 Vim 中也实现了一遍。Vim 现在也支持异步任务，内置终端等特性了。所以目前来看 NeoVim 与 Vim 的差异已经很小，大部分第三方插件都能兼容 NeoVim/Vim。

## 安装与配置

本文将以 Ubuntu Linux 发行版为系统环境来研究 NeoVim 的安装与环境配置方法，并学习使用它的具体功能。

### 基础环境配置

因为在为 NeoVim 安装 coc.nVim 等插件时会需要用到 Node.js，所以在正式安装 NeoVim 之前，我们首先要在操作系统中安装一个 12.0.0 以上版本的 Node.js 运行时环境，它可以通过以下 Bash 命令序列来安装：

```bash
curl -fsSL https://deb.nodesource.com/setup_17.x | sudo -E bash -
sudo apt install -y nodejs
```

如果一切顺利，我们通过`node -v`和`npm -v`命令就可以查看到相应的版本，例如像这样：

```bash
$ node -v
v17.4.0
$ npm· -v
8.3.1
```

在这里，为了后续操作的顺利，我们需要将 NPM 所连接的默认仓库换成在国内的镜像：

```bash
$ npm config set registry https://registry.npm.taobao.org
$ npm config get registry
https://registry.npm.taobao.org
```

接着，我们需要安装 Python3 环境，它可以通过以下 Bash 命令序列来安装：

```bash
sudo apt install  -y  python3 python3-pip
pip install pynVim
```

最后，我们需要安装 curl 和 git，它们可以通过以下 Bash 命令序列来安装：

```bash
sudo apt install -y curl git
```

### 安装 NeoVim

<!-- 以下内容尚未整理 -->

安装NeoVim

和安装nodejs一样，NeoVim下载地址：NeoVim

sudo ln -s /home/ykh/软件/nVim-linux64/bin/nVim nVim

创建环境变量（第二个deepin没有，需要自己创建，不然安装coc.nVim会出错）：

sudo Vim /etc/profile


环境变量加入：

export PATH="/home/ykh/软件/nVim-linux64/bin:$PATH"
export TMPDIR="/tmp"

让环境变量生效：

source /etc/profile

    1

这时候就可以直接用nVim来打开NeoVim了
安装插件管理器

参看一下raw.githubusercontent.com的IP，有时候会连不上：IP查询
在这里插入图片描述
修改下host：

sudo nVim /etc/hosts

    1

加入：

199.232.96.133 raw.githubusercontent.com

    1

安装Vim-plug

sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nVim/site/autoload/plug.Vim --create-dirs \
       https://raw.githubusercontent.com/junegunn/Vim-plug/master/plug.Vim'


创建配置文件：

mkdir ~/.config/nVim/
nVim ~/.config/nVim/init.Vim

输入（设置行号）

set nu

    1

保存退出，再次进入，显示行号了就成功了
安装插件
tab补全

编辑配置文件init.Vim

  set nu

  call plug#begin('~/.Vim/plugged')
                 
  Plug 'ervandew/supertab'
                 
  call plug#end()

保存退出，进入NeoVim命令模式下输入PlugInstall自动安装，重启进入NeoVim,按下tab键就会有提示了，其他插件安装类似
安装coc.nVim

coc.nVim 是集代码补全、静态检测、函数跳转等功能的一个引擎

npm install -g NeoVim

init.Vim加入：

Plug 'neoclide/coc.nVim', {'branch': 'release'}

然后进行自动安装，安装完成后可以输入命令 checkhealth 检查是否有错误
配置C++环境：

nVim命令模式输入：

:CocInstall coc-clangd # C++环境插件
:CocInstall coc-cmake  # Cmake 支持

打开一个.cpp文件

nVim test.cpp

会出现提示：

[coc.nVim] clangd was not found on your PATH. :CocCommand clangd.install will install 11.0.0.

C++ 需要安装clangd，输入:CocCommand clangd.install安装clangd，但我的失败了，另一个方法：

 sudo apt-get install clang-tools

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
:CocInstall coc-Vimlsp # lsp
:CocInstall coc-yaml   # yaml

配色

这里配色使用monokai，把monokai.Vim下载下来，放到/root/.config/nVim/colors/目录下，没有就自己创建
monokai

修改init.Vim，加入colorscheme monokai再次打开：
在这里插入图片描述
其他配置和插件
插件：

首先要安装ranger：sudo apt install ranger

Plug 'junegunn/Vim-easy-align'
"ranger文件浏览器                                                                              
Plug 'kevinhwang91/rnVimr'
"更好看的标签栏                                                                                  
Plug 'Vim-airline/Vim-airline'                                                                              
Plug 'Vim-airline/Vim-airline-themes' "airline 的主题 


配置：

```Vim
let g:airline#extensions#tabline#enabled = 1                                                                
let g:rnVimr_ex_enable = 1   
" Alt+o打开ranger                                                                                                                                                                                  
nnoremap <silent> <M-o> :RnVimrToggle<CR>                                                                   
"Alt+加号切换下一个标签，-号上一个                                                       
nnoremap <M-+> :bp<CR>                                                                                      
nnoremap <M--> :bn<CR>
```


随着 nVim/Vim 对异步任务的支持，很多原先 Vim 中被大量使用的插件已经逐渐变得过时，这里列举一些更加「先进」的插件，可以作为古老 Vim 插件的替代品。
文件管理

使用 Shougo/defx.nVim 替代 scrooloose/nerdtree，defx.nVim 使用 NeoVim 的 Remote plugin，通过 python3 开发，支持异步，在文件多的情况下打开文件浏览器的速度更加快速。作者 Shougo 是一个高产的 Vim 插件作者，同时开发了 denite 等著名插件。但是他写的插件特点就是并不开箱即用，需要大量的配置。这里我列出了我的 defx 配置，同时使用了 kristijanhusak/defx-git 和 kristijanhusak/defx-icons（需要安装 nerd font）来显示 git 修改和图标。

配置：

Plug 'Shougo/defx.nVim', { 'do': ':UpdateRemotePlugins' }
map <silent> - :Defx<CR>
" Avoid the white space highting issue
autocmd FileType defx match ExtraWhitespace /^^/
" Keymap in defx
autocmd FileType defx call s:defx_my_settings()
function! s:defx_my_settings() abort
  IndentLinesDisable
  setl nospell
  setl signcolumn=no
  setl nonumber
  nnoremap <silent><buffer><expr> <CR>
  \ defx#is_directory() ?
  \ defx#do_action('open_or_close_tree') :
  \ defx#do_action('drop',)
  nmap <silent><buffer><expr> <2-LeftMouse>
  \ defx#is_directory() ?
  \ defx#do_action('open_or_close_tree') :
  \ defx#do_action('drop',)
  nnoremap <silent><buffer><expr> s defx#do_action('drop', 'split')
  nnoremap <silent><buffer><expr> v defx#do_action('drop', 'vsplit')
  nnoremap <silent><buffer><expr> t defx#do_action('drop', 'tabe')
  nnoremap <silent><buffer><expr> o defx#do_action('open_tree')
  nnoremap <silent><buffer><expr> O defx#do_action('open_tree_recursive')
  nnoremap <silent><buffer><expr> C defx#do_action('copy')
  nnoremap <silent><buffer><expr> P defx#do_action('paste')
  nnoremap <silent><buffer><expr> M defx#do_action('rename')
  nnoremap <silent><buffer><expr> D defx#do_action('remove_trash')
  nnoremap <silent><buffer><expr> A defx#do_action('new_multiple_files')
  nnoremap <silent><buffer><expr> U defx#do_action('cd', ['..'])
  nnoremap <silent><buffer><expr> . defx#do_action('toggle_ignored_files')
  nnoremap <silent><buffer><expr> <Space> defx#do_action('toggle_select')
  nnoremap <silent><buffer><expr> R defx#do_action('redraw')
endfunction

" Defx git
Plug 'kristijanhusak/defx-git'
let g:defx_git#indicators = {
  \ 'Modified'  : '✹',
  \ 'Staged'    : '✚',
  \ 'Untracked' : '✭',
  \ 'Renamed'   : '➜',
  \ 'Unmerged'  : '═',
  \ 'Ignored'   : '☒',
  \ 'Deleted'   : '✖',
  \ 'Unknown'   : '?'
  \ }
let g:defx_git#column_length = 0
hi def link Defx_filename_directory NERDTreeDirSlash
hi def link Defx_git_Modified Special
hi def link Defx_git_Staged Function
hi def link Defx_git_Renamed Title
hi def link Defx_git_Unmerged Label
hi def link Defx_git_Untracked Tag
hi def link Defx_git_Ignored Comment

" Defx icons
" Requires nerd-font, install at https://github.com/ryanoasis/nerd-fonts or
" brew cask install font-hack-nerd-font
" Then set non-ascii font to Driod sans mono for powerline in iTerm2
Plug 'kristijanhusak/defx-icons'
" disbale syntax highlighting to prevent performence issue
let g:defx_icons_enable_syntax_highlight = 1

显示效果如下：

defx
fzf

https://github.com/junegunn/fzf.Vim

fzf 是一个 fuzzy search 工具，相比与 ctrlp，它能提供更好的性能，并且扩展性更好，可以集成到其他插件中。类似与 ctrlp 它能提供文件搜索功能，同时还能提供 ctags 代码 symbol 搜索，代码内容搜索等功能。 fzf 的配置相对简单，这里只贴一些的效果图：

文件模糊搜索：

fzf-file

fzf 使用了 terminal + command 的实现方式，可以对其功能进行扩展，例如结合 Vim-go 插件搜索代码中的 code symbol：

fzf-btags

除了fzf， Shougo 开发的 denite.nVim 也是一个非常流行的 fuzzy search 插件，但是 denite 的配置就更加复杂，这里就进行赘述了。
代码补全

在过去，比较流行的补全插件有 ycm-core/YouCompleteMe 和 Shougo/deoplete.nVim，但是这些插件对不同语言的支持程度都不尽相同，每个语言的补全可能都需要单独配置。其中 YCM 采用 C++ 开发了额外程序，每次更新还需要进行编译。配置，使用，调试都是非常费力且折腾的事情。

随着微软发力开发开源代码编辑器 vscode，同时发布了 Language Server Protocol，这种混乱的局面正在逐渐变得标准化和统一。现在每个语言基本都有对应的 LSP Server 实现。使用 LSP 协议的好处在于，编辑器是需要实现 LSP Client 就可以和 LSP Server 交互，而不需要 care 具体是什么语言。

coc.nVim 就是这样一个采用 LSP 实现的 Vim 插件。同时他还利用了 NeoVim 的 Remote plugin 功能，使用 typescript 开发，能够最小成本的将已有的 vscode 插件进行少量修改适配，即可移植到 Vim 中来。

coc.nVim 同时是一个插件化的系统，通过很多众多的插件，还能提供代码补全之外的额外功能。而且 coc.nVim 的开发速度非常快，已经支持了 NeoVim 刚刚 master 分支上实现的 floating window 功能（这个功能未来也会在 Vim 中进行对应实现）。

这里列举一些常用功能：

快速查看函数签名，支持 floating window 展示：

coc-k

这个功能直接映射一个快捷键即可，这里映射为 K：

" Use K to show documentation in preview window
function! s:show_documentation()
  if (index(['Vim','help'], &filetype) >= 0)
    execute 'h '.expand('<cword>')
  else
    call CocAction('doHover')
  endif
endfunction
nnoremap <silent> K :call <SID>show_documentation()<CR>

在补全中提示函数的参数列表：

coc-func-param

执行代码检查，并将结果通过 flaoting window 展示：

coc-diag

coc.nVim 还能够安装扩展支持很多额外功能，例如 git 信息显示，括号自动补全，调用第三方 sinppets 等功能。具体的安装配置文档可以参考：coc wiki
配置参考

由于篇幅限制，这里只列出一些我常用的一些插件，我所有的 Vim 配置文件都在 github 上可以查看，完整的插件和配置可以参考：https://github.com/paco0x/dotfiles/tree/master/Vim

