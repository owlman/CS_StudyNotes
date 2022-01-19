# NeoVim 研究笔记

本文将以 Ubuntu Linux 发行版为系统环境来研究 NeoVim 的安装与环境配置方法，并学习使用它的具体功能。

- NeoVim 项目地址：[GitHub - neovim/neovim](https://github.com/neovim/neovim)
- Vim 原项目地址：[GitHub - vim/vim](https://github.com/vim/vim)

## 背景知识介绍

### NeoVim 起源

2014 年，巴西程序员 Thiago de Arruda Padilha（aka tarruda）曾经向 Vim 开源编辑器项目递交了两大补丁，其中包含了对 Vim 的架构进行大幅调整的建议，结果遭到了 Vim 作者 Bram Moolenaar 的拒绝。因为后者认为对于 Vim 这样一个成熟的项目进行如此大的改变风险太高。但或许在 tarruda 看来，Vim 这个上个世纪 90 年代初的产物，至今已经 20 多年了，该项目中不仅遗留了大量的历史痕迹，而且该项目的管理层如今在程序的维护、Bug 的修复、以及新特性的添加等问题上的态度都在变得越来越僵化，且难以与时俱进。

总而言之，基于对 Vim 项目的不满，并致力于打造一款面向 21 世纪的代码编辑器，tarruda 先生以众筹资金的方式发起了 Vim 的这个 fork 项目：NeoVim。在这里，Neo 这个单词取“新”之意，表达的是其作者对 Vim 编辑器在这个新时代的重生期待。

### NeoVim 现状

根据 NeoVim 项目的自述说明，它在总体上想实现以下目标 :

- 通过简化维护以改进 Bug 修复及特性添加的速度；
- 分派各个开发人员的工作；
- 实现新的、现代化的用户界面，而不必修改核心源代码；
- 利用新的、基于协同进程的新插件架构改善扩展性，并支持使用任何语言编写插件；

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


但是随着时间的推移，neovim 项目逐渐发展成为一个成熟的项目，并率先提供了多个当时 vim 不支持的新特性：

    remote plugin，支持使用 python 等第三方语言编写的程序与 nvim 交互，开发插件
    为 vimscript 提供了异步任务的支持，在此之前 vimscirpt 只能以同步的方式工作，任务卡住会导致 vim 前台卡住
    支持在 vim 中打开 terminal window
    重构了 vim 的部分代码，如使用 libuv 库来做多平台兼容，而不是像 vim 那样手动维护，并且使用更加现代化的代码编译工具链

neovim 项目的成功也激发了 bram 对 vim 项目开发的激情，促使 vim 在 7.0 之后极大的加快了新功能开发进度，很快发布了 vim8.0/8.1，把 neovim 实现的大部分新特性在 vim 中也实现了一遍。vim 现在也支持异步任务，terminal 等特性了。所以目前来看 neovim 与 vim 的差异已经很小，大部分第三方插件都能兼容 nvim/vim。

但是在这里还是强烈推荐使用 neovim：

    我从 neovim 0.17 版本开始使用（macOS），使用下来，nvim 的稳定性和 vim 基本相当
    neovim 始终保持先进性，由于社区开发进度更高效，各种新功能仍然还是先在 neovim 中实现，vim 才会有对应实现，并且现在 neovim 还被 google summer of code 支持，为其添加新特性
    neovim 还有一些未被 vim 实现的特性，例如 Remote plugin, virtual text 等..

关于 vim/neovim 的更多比较，各位还可以查阅更多网上的资料。这里还有一篇文章讲述 vim codebase 的问题供参考：链接
利用 nvim/vim 新特性，打造更现代化的编辑器

随着 nvim/vim 对异步任务的支持，很多原先 vim 中被大量使用的插件已经逐渐变得过时，这里列举一些更加「先进」的插件，可以作为古老 vim 插件的替代品。
文件管理

使用 Shougo/defx.nvim 替代 scrooloose/nerdtree，defx.nvim 使用 neovim 的 Remote plugin，通过 python3 开发，支持异步，在文件多的情况下打开文件浏览器的速度更加快速。作者 Shougo 是一个高产的 vim 插件作者，同时开发了 denite 等著名插件。但是他写的插件特点就是并不开箱即用，需要大量的配置。这里我列出了我的 defx 配置，同时使用了 kristijanhusak/defx-git 和 kristijanhusak/defx-icons（需要安装 nerd font）来显示 git 修改和图标。

配置：

Plug 'Shougo/defx.nvim', { 'do': ':UpdateRemotePlugins' }
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

https://github.com/junegunn/fzf.vim

fzf 是一个 fuzzy search 工具，相比与 ctrlp，它能提供更好的性能，并且扩展性更好，可以集成到其他插件中。类似与 ctrlp 它能提供文件搜索功能，同时还能提供 ctags 代码 symbol 搜索，代码内容搜索等功能。 fzf 的配置相对简单，这里只贴一些的效果图：

文件模糊搜索：

fzf-file

fzf 使用了 terminal + command 的实现方式，可以对其功能进行扩展，例如结合 vim-go 插件搜索代码中的 code symbol：

fzf-btags

除了fzf， Shougo 开发的 denite.nvim 也是一个非常流行的 fuzzy search 插件，但是 denite 的配置就更加复杂，这里就进行赘述了。
代码补全

在过去，比较流行的补全插件有 ycm-core/YouCompleteMe 和 Shougo/deoplete.nvim，但是这些插件对不同语言的支持程度都不尽相同，每个语言的补全可能都需要单独配置。其中 YCM 采用 C++ 开发了额外程序，每次更新还需要进行编译。配置，使用，调试都是非常费力且折腾的事情。

随着微软发力开发开源代码编辑器 vscode，同时发布了 Language Server Protocol，这种混乱的局面正在逐渐变得标准化和统一。现在每个语言基本都有对应的 LSP Server 实现。使用 LSP 协议的好处在于，编辑器是需要实现 LSP Client 就可以和 LSP Server 交互，而不需要 care 具体是什么语言。

coc.nvim 就是这样一个采用 LSP 实现的 vim 插件。同时他还利用了 neovim 的 Remote plugin 功能，使用 typescript 开发，能够最小成本的将已有的 vscode 插件进行少量修改适配，即可移植到 vim 中来。

coc.nvim 同时是一个插件化的系统，通过很多众多的插件，还能提供代码补全之外的额外功能。而且 coc.nvim 的开发速度非常快，已经支持了 neovim 刚刚 master 分支上实现的 floating window 功能（这个功能未来也会在 vim 中进行对应实现）。

这里列举一些常用功能：

快速查看函数签名，支持 floating window 展示：

coc-k

这个功能直接映射一个快捷键即可，这里映射为 K：

" Use K to show documentation in preview window
function! s:show_documentation()
  if (index(['vim','help'], &filetype) >= 0)
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

coc.nvim 还能够安装扩展支持很多额外功能，例如 git 信息显示，括号自动补全，调用第三方 sinppets 等功能。具体的安装配置文档可以参考：coc wiki
配置参考

由于篇幅限制，这里只列出一些我常用的一些插件，我所有的 vim 配置文件都在 github 上可以查看，完整的插件和配置可以参考：https://github.com/paco0x/dotfiles/tree/master/vim

    Previous
    SR-IOV 虚拟化
    Next
    Uniswap v3 详解（一）：设计原理


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