---
title: NeoVim 使用笔记
author: 凌杰
date: 2020-07-15
updated: 2026-09-10
tags: [文本编辑器, NeoVim, LSP, lazy.nvim]
categories: [命令行工具]
---

> [!NOTE] 笔记说明
>
> 这篇笔记用于记录本人在使用 NeoVim 这款文本编辑器过程中的心得体会，存储于个人的[计算机专业笔记库](https://github.com/owlman/CS_Studynotes) 中并长期维护。

> [!IMPORTANT] 2026-05 大更新
>
> 自 2020 年首次撰写以来，本文涉及的工具链已经迭代了好几代，本轮一次性同步下列依赖：
>
> | 旧 | 新 | 主要变化 |
> | --- | --- | --- |
> | Node.js 17 | Node.js 20 LTS | Node 17 已 EOL；现以 20.x 长期支持版为基准 |
> | `registry.npm.taobao.org` | `registry.npmmirror.com` | 淘宝镜像整体迁移到 npmmirror |
> | NeoVim 0.4.3 | NeoVim 0.11+ | 内置 LSP / Treesitter / Lua 配置成熟 |
> | vim-plug | lazy.nvim | 主流从 vimscript 插件管理器迁移到 Lua |
> | Coc.nvim + coc-pyls | 内置 LSP + Pyright | 用 NeoVim 0.11 内置 `vim.lsp.*` 替代 Coc 中间层，Pyright 替代停更的 pyls |
> | ranger + rnvimr | yazi + yazi.nvim | ranger 已基本停更，yazi 是当前社区主流 |
> | vim-airline | lualine.nvim | 纯 Lua 实现的状态栏，主题生态更现代 |
>
> 版本基线：本文以 **NeoVim 0.11 / 0.12+**（撰写时最新稳定版 v0.12.5，2026-08 发布）为基准；Node.js 20 LTS；lazy.nvim v11+；yazi v26+。
>
> 图片方面：旧版本中的博客园 CDN 图片已在历次 commit 中统一迁移至本地 `img/` 目录，本文不再保留任何外链图片。
>
> 2026-09 实战微调：按本文 §3-§7 实际在 Windows 11 + Scoop 环境配置一轮后回写，修正了 7 处与现行社区规范不符的写法（详见 §6 常见问题 Q9-Q15）。

## 目录

- [1. 学习规划](#1-学习规划)
- [2. 背景知识](#2-背景知识)
  - [2.1 NeoVim 起源](#21-neovim-起源)
  - [2.2 NeoVim 现状](#22-neovim-现状)
- [3. 安装与配置](#3-安装与配置)
  - [3.1 基础环境准备](#31-基础环境准备)
  - [3.2 安装 NeoVim](#32-安装-neovim)
  - [3.3 配置文件结构](#33-配置文件结构)
- [4. 插件管理：lazy.nvim](#4-插件管理lazynvim)
  - [4.1 安装 lazy.nvim](#41-安装-lazynvim)
  - [4.2 插件目录约定](#42-插件目录约定)
- [5. 常用插件推荐](#5-常用插件推荐)
  - [5.1 编辑器基础：Treesitter + 补全 + 模糊搜索](#51-编辑器基础treesitter--补全--模糊搜索)
  - [5.2 LSP：内置 LSP + Pyright](#52-lsp内置-lsp--pyright)
  - [5.3 状态栏：lualine](#53-状态栏lualine)
  - [5.4 文件管理器：yazi](#54-文件管理器yazi)
  - [5.5 Markdown 预览：markdown-preview.nvim](#55-markdown-预览markdown-previewnvim)
  - [5.6 启动页：alpha-nvim](#56-启动页alpha-nvim)
  - [5.7 主题：catppuccin](#57-主题catppuccin)
- [6. 常见问题](#6-常见问题)
- [7. 附录：完整配置骨架](#7-附录完整配置骨架)

## 1. 学习规划

- 学习基础：
  - 掌握 Linux shell 命令的基本使用。
  - 掌握 Vim 编辑器的基本操作方法。
  - 有一两门编程语言的使用经验。
- 学习环境：
  - Ubuntu Linux 24.04+（其他主流发行版 / macOS / Windows 同样可行，本文以 Ubuntu 为示例）。
- 学习资料：
  - NeoVim 官方网站：[neovim.io](https://neovim.io/)
  - NeoVim 项目仓库：[GitHub - neovim/neovim](https://github.com/neovim/neovim)
  - NeoVim 内置文档：`:help`，配合 `:help lua-guide` / `:help lsp` / `:help treesitter` 起步。

## 2. 背景知识

### 2.1 NeoVim 起源

2014 年，巴西程序员 Thiago de Arruda Padilha（aka tarruda）曾经向 Vim 开源编辑器项目递交了两大补丁，其中包含了对 Vim 的架构进行大幅调整的建议，结果遭到了 Vim 作者 Bram Moolenaar 的拒绝。因为后者认为对于 Vim 这样一个成熟的项目进行如此大的改变风险太高。但或许在 tarruda 看来，Vim 这个上个世纪 90 年代初的产物，至今已经 20 多年了，该项目中不仅遗留了大量的历史痕迹，而且该项目的管理层如今在程序的维护、Bug 的修复、以及新特性的添加等问题上的态度都在变得越来越僵化，且难以与时俱进。

总而言之，基于对 Vim 项目的不满，并致力于打造一款面向 21 世纪的代码编辑器，tarruda 先生以众筹资金的方式发起了 Vim 的这个 fork 项目：NeoVim。在这里，Neo 这个单词表达的是其作者对 Vim 编辑器在这个新时代的重生期待。

### 2.2 NeoVim 现状

从 NeoVim 项目的提交记录可以看出，tarruda 先生是个非常有项目维护经验的人，其有条不紊的管理让 NeoVim 的版本迭代相当快速，基本上几天就会推送一个新的版本。目前来说，NeoVim 已经实现 Vim 大部分功能，并兼容了 Vim 百分之九十以上的配置。

NeoVim 项目逐步成为成熟项目，并率先提供了多个 8.0 之前 Vim 所没有的新特性：

- 支持在 Vim 中打开命令行终端窗口，使用户不必退出编辑器就能执行 shell 命令。
- 为 vimscript 提供异步任务支持，之前的 vimscript 只能以同步方式执行任务。
- 重构 Vim 部分代码，实现多平台兼容，并使用更现代化的代码编译工具链。

NeoVim 的成功也反过来唤起了 Vim 项目组的危机意识，加快了 Vim 8.0/8.1 的迭代；Vim 现在也支持异步任务、内置终端等特性。

到 2026 年前后，NeoVim 已经稳定进入了 **0.11 / 0.12 时代**：

- **内置 LSP**：`vim.lsp.config / vim.lsp.enable` 已经覆盖了 server 注册、filetype 关联、capabilities 等核心场景；Coc 这种 Node.js 中间层已不再是必需品。
- **内置 Treesitter**：高亮、缩进、跳转都走 `vim.treesitter.*`，从 0.11 开始官方也提供了内建 parser 安装机制（`:checkhealth vim.treesitter`）。
- **Lua 作为一等公民**：`init.lua` 与 `lua/` 模块成为推荐配置方式，vimscript 配置被逐步淘汰；lazy.nvim 这类 Lua 插件管理器随之成为主流。
- **稳定与 nightly 双轨发布**：每夜构建与稳定版均可通过 GitHub Releases 直接下载 AppImage，不再受发行版仓库拖累。

## 3. 安装与配置

本文以 Ubuntu Linux 24.04 为示例，其他发行版 / macOS / Windows 思路一致。

### 3.1 基础环境准备

#### Node.js 20 LTS

部分 LSP 客户端、Treesitter parser 的远程同步、以及 markdown-preview.nvim 仍依赖 Node.js。Node 17 已 EOL，本文以 20.x LTS 为基准（Node 22 LTS 也已可用，但生态适配目标仍以 20 为主）：

```bash
# Ubuntu / Debian
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# 验证
node -v   # v20.x.x
npm -v    # 10.x.x
```

国内用户顺手把 NPM 默认仓库切到 npmmirror（旧的 `registry.npm.taobao.org` 已经停止服务，整个镜像站迁到了 `registry.npmmirror.com`）：

```bash
npm config set registry https://registry.npmmirror.com
npm config get registry # 应输出：https://registry.npmmirror.com
```

#### Python、ripgrep、fd

Pyright LSP、Treesitter 解析器以及若干 formatter 都依赖 Python 与一些 CLI 工具：

```bash
sudo apt install -y python3 python3-pip python3-venv \
                    ripgrep fd-find unzip
pip install --user pynvim
```

> 如果你用 venv 管理 Python 项目，记得在每个 venv 里再装一次 `pynvim` 和 `pyright`，否则 LSP 会读到全局 site-packages。

#### Git / curl

后续装 lazy.nvim、克隆插件必备：

```bash
sudo apt install -y curl git
```

### 3.2 安装 NeoVim

在这里，我会建议读者**不要直接用 Ubuntu 仓库的 `apt install neovim`**，发行版仓库里通常还停留在 0.9 甚至 0.7，缺少内置 LSP / Treesitter 关键改动。推荐以下三种方式之一：

#### AppImage（最简单，跨发行版通用）

```bash
curl -L -o /tmp/nvim.appimage \
  https://github.com/neovim/neovim/releases/download/stable/nvim-linux-x86_64.appimage
chmod +x /tmp/nvim.appimage
sudo mv /tmp/nvim.appimage /usr/local/bin/nvim
```

如果想跟踪 nightly：

```bash
curl -L -o /tmp/nvim.appimage \
  https://github.com/neovim/neovim/releases/download/nightly/nvim-linux-x86_64.appimage
```

#### Ubuntu PPA

```bash
sudo add-apt-repository ppa:neovim-ppa/stable
sudo apt update
sudo apt install -y neovim
```

#### 源码编译

适合追求最新 commit 或自己改源码的场景：

```bash
git clone https://github.com/neovim/neovim.git
cd neovim && make CMAKE_BUILD_TYPE=Release
sudo make install
```

#### 验证

```bash
nvim -v   # NVIM v0.12.x（撰写时最新稳定版 v0.12.5）
nvim --headless +checkhealth +q
```

### 3.3 配置文件结构

NeoVim 0.11+ 的标准做法是把所有配置放进 `~/.config/nvim/`，把 Lua 模块放进 `lua/<user>/`，推荐结构如下：

```Bash
~/.config/nvim/
├── init.lua                 # 入口
├── lua/
│   └── user/
│       ├── lazy.lua         # lazy.nvim bootstrap + setup
│       └── plugins/         # 各插件 spec
│           ├── init.lua
│           ├── edit.lua
│           ├── lsp.lua
│           ├── lualine.lua
│           ├── yazi.lua
│           ├── markdown.lua
│           ├── alpha.lua
│           └── colorscheme.lua
├── after/
└── spell/
```

入口 `init.lua` 一般只需要做两件事：bootstrap lazy、import 各插件 spec：

```lua
-- ~/.config/nvim/init.lua
require("user.lazy")
require("user.options")
```

## 4. 插件管理：lazy.nvim

### 4.1 安装 lazy.nvim

lazy.nvim 的安装脚本会自动判断 `stdpath('data')` 并写入 `lazy.lua`：

```bash
mkdir -p ~/.config/nvim/lua/user
```

然后新建 `~/.config/nvim/lua/user/lazy.lua`（见 §7 模板）。首次启动 NeoVim 时 lazy 会自动 clone 自己到 `~/.local/share/nvim/lazy/lazy.nvim`。

国内网络拉 GitHub 不稳的常见解决：

- 给 git 设代理：`git config --global http.proxy http://127.0.0.1:<port>`
- 把 lazy 的 git 源改成 ghproxy：

  ```lua
  require("lazy").setup({
    git = { url_format = "https://ghproxy.com/https://github.com/%s.git" },
  })
  ```

### 4.2 插件目录约定

lazy.nvim 推荐每个插件一个 spec 文件，由 `lua/user/plugins/init.lua` 统一 import：

```lua
-- lua/user/plugins/init.lua
return {
  require("user.plugins.edit"),
  require("user.plugins.lsp"),
  require("user.plugins.lualine"),
  require("user.plugins.yazi"),
  require("user.plugins.markdown"),
  require("user.plugins.alpha"),
  require("user.plugins.colorscheme"),
}
```

每个 `*.lua` 文件以 `return { ... }` 形式声明该分类下的全部插件 spec：

```lua
-- lua/user/plugins/lualine.lua
return {
  {
    "nvim-lualine/lualine.nvim",
    event = "VeryLazy",
    dependencies = { "nvim-tree/nvim-web-devicons" },
    config = function()
      require("lualine").setup({
        options = { theme = "catppuccin" },
      })
    end,
  },
}
```

> 相比旧文里每加一个插件就把整个 `init.vim` 重新粘贴一遍的写法，lazy 的 spec 文件天然去重，新增/移除插件只动一行。

## 5. 常用插件推荐

> 旧版每节都重复整段 `init.vim`，本节按"按职责分组"的写法，每个 spec 文件只关注自己分类下的插件，不再粘贴重复配置。

### 5.1 编辑器基础：Treesitter + 补全 + 模糊搜索

```lua
-- lua/user/plugins/edit.lua
return {
  -- 语法高亮 / 缩进 / 跳转
  -- 注意：0.12+ 必须切 main 分支（master 冻结不兼容 0.12）、且不能 lazy-load
  {
    "nvim-treesitter/nvim-treesitter",
    branch = "main",
    lazy = false,           -- nvim-treesitter main 分支明确说"This plugin does not support lazy-loading"
    build = ":TSUpdate",
    config = function()
      require("nvim-treesitter").setup({
        install_dir = vim.fn.stdpath("data") .. "/site",
      })
      -- 装常用 parser（新 API 是 nvim-treesitter.install，不是 ensure_installed）
      pcall(function()
        require("nvim-treesitter").install({
          "lua", "python", "cpp", "c", "json", "markdown",
          "bash", "yaml", "toml", "vim", "vimdoc",
        })
      end)
    end,
  },

  -- 自动补全括号 / 引号
  {
    "echasnovski/mini.pairs",
    event = "InsertEnter",
    config = function() require("mini.pairs").setup() end,
  },

  -- 模糊搜索
  {
    "nvim-telescope/telescope.nvim",
    cmd = "Telescope",
    dependencies = { "nvim-lua/plenary.nvim" },
    config = function()
      local telescope = require("telescope.builtin")
      vim.keymap.set("n", "<leader>ff", telescope.find_files, { desc = "查找文件" })
      vim.keymap.set("n", "<leader>fg", telescope.live_grep, { desc = "全局搜索" })
      vim.keymap.set("n", "<leader>fb", telescope.buffers, { desc = "切换 buffer" })
    end,
  },
}
```

> 旧版用 `ervandew/supertab` 做 tab 补全，本节换成了 Treesitter + mini.pairs + Telescope 的现代组合。
>
> [!NOTE] Treesitter 的两条路
>
> NeoVim 0.11+ **已经内置** `vim.treesitter.*` + `:checkhealth vim.treesitter`，外部 `nvim-treesitter` 插件的角色被弱化为"提供大量 parser 与 query 模板"。如果你只用 lua/python/json 等几个语言，可以**完全不装** nvim-treesitter，跳过本节第一个 spec，只保留 mini.pairs + Telescope，启动更快。

### 5.2 LSP：内置 LSP + Pyright

NeoVim 0.11 内置 `vim.lsp.*`，配合各语言官方 LSP server 即可获得跳转、引用、重命名、code action 等能力，**无需任何 Node.js 中间层**（这正是替代 Coc 的关键动机）。

```lua
-- lua/user/plugins/lsp.lua
return {
  -- nvim-cmp 必须是顶层 spec：所有 cmp-* 的 after/plugin/*.lua 会第一时间 require("cmp")，
  -- 所以 cmp 要先于它们装好；cmp-* 全列在 cmp 的 dependencies 里。
  {
    "hrsh7th/nvim-cmp",
    event = "InsertEnter",
    dependencies = {
      "hrsh7th/cmp-nvim-lsp",
      "L3MON4D3/LuaSnip",
      "saadparwaiz1/cmp_luasnip",
      "hrsh7th/cmp-path",
      "rafamadriz/friendly-snippets",
    },
    config = function()
      local cmp = require("cmp")
      cmp.setup({
        snippet = require("luasnip").lazy_snippet,
        mapping = cmp.mapping.preset.insert({
          ["<CR>"]   = cmp.mapping.confirm({ select = true }),
          ["<Tab>"]  = cmp.mapping.select_next_item(),
          ["<S-Tab>"] = cmp.mapping.select_prev_item(),
        }),
        sources = cmp.config.sources(
          { { name = "nvim_lsp" }, { name = "luasnip" } },
          { { name = "path" } }
        ),
      })

      -- 诊断显示
      vim.diagnostic.config({
        virtual_text = true,
        signs        = true,
        underline    = true,
        update_in_insert = false,
      })
    end,
  },

  -- nvim-lspconfig 现在退化为"提供 server 默认配置 + capabilities"的角色，
  -- 真正的启用/挂载走 NeoVim 0.11+ 内置 vim.lsp.config / vim.lsp.enable
  {
    "neovim/nvim-lspconfig",
    event = { "BufReadPre", "BufNewFile" },
    config = function()
      local servers = { "pyright", "clangd", "lua_ls", "bashls", "jsonls", "yamlls" }

      -- jsonls 的 lspconfig 默认 cmd 写的是复数 `vscode-json-languageserver`，
      -- 但 `vscode-langservers-extracted` npm 包实际 shim 是单数 `vscode-json-language-server`。
      -- 这里显式覆盖，否则 :LspInfo 会报 `spawn: not found`。
      vim.lsp.config("jsonls", {
        cmd = { "vscode-json-language-server", "--stdio" },
      })

      for _, name in ipairs(servers) do
        if name ~= "jsonls" then
          vim.lsp.config(name, {})
        end
      end
      vim.lsp.enable(servers)
    end,
  },

  -- 诊断列表 / LSP 动作面板
  -- 旧名 nvim-web-devicon（单数）仓库已删，要写复数 nvim-web-devicons
  {
    "folke/trouble.nvim",
    cmd = { "Trouble", "TroubleToggle" },
    dependencies = { "nvim-tree/nvim-web-devicons" },
  },
}
```

**LSP server 本身不是 Vim 插件，要在系统 / 虚拟环境里装**：

```bash
# Pyright：替代停更的 coc-pyls
pip install --user pyright

# clangd：替代 coc-clangd
sudo apt install -y clangd

# 其他几个 server 一般走 npm
npm i -g bash-language-server yaml-language-server vscode-langservers-extracted
```

> Coc 时代用 `coc-pyls` 提供 Python 补全；现 Pyright 由微软维护，已是 Python 静态分析的事实标准。如果你更习惯 Coc 生态，也可以装 `coc-pyright`（只是 Coc 扩展的 Pyright 集成），整段 LSP 配置可以无缝替换为 Coc 配置——这是用户友好度的双轨选择。

### 5.3 状态栏：lualine

替代 vim-airline 的纯 Lua 状态栏，主题生态更现代。

```lua
-- lua/user/plugins/lualine.lua
return {
  {
    "nvim-lualine/lualine.nvim",
    event = "VeryLazy",
    -- 旧名 nvim-web-devicon（单数）仓库已删；改用复数 nvim-web-devicons
    dependencies = { "nvim-tree/nvim-web-devicons" },
    config = function()
      require("lualine").setup({
        options = {
          theme = "catppuccin",
          section_separators = { "", "" },
          component_separators = { "", "" },
          icons_enabled = true,
        },
      })
    end,
  },
}
```

效果：

![img](img/vim-airline.png)

> 旧图保留以便对比 lualine 与 vim-airline 的视觉差异；当前默认主题为 catppuccin。

### 5.4 文件管理器：yazi

ranger 多年未发版，社区已切换到 Rust 写的 [yazi](https://github.com/sxyazi/yazi)。NeoVim 集成用 `mikavilpas/yazi.nvim`：

```bash
# 安装 yazi 本体
cargo install --locked yazi-fm yazi-cli
# 或用包管理器（Ubuntu 24.04+ 仓库已有）
sudo apt install -y yazi
```

```lua
-- lua/user/plugins/yazi.lua
-- 严格按 mikavilpas/yazi.nvim 官方 README 的 spec 写法
return {
  {
    "mikavilpas/yazi.nvim",
    version = "*", -- 锁定到最新稳定 tag
    event = "VeryLazy",
    enabled = function()
      -- 没装 yazi 二进制就整个 spec 跳过，不影响其它插件
      return vim.fn.executable("yazi") == 1
    end,
    dependencies = {
      { "nvim-lua/plenary.nvim", lazy = true },
      -- 注意：之前有人写过 "yazi-org/yazi.nvim"，那个仓库根本不存在（404），
      -- yazi.nvim 真正的依赖只有 plenary.nvim。
    },
    keys = {
      -- 把 keymap 放进去：lazy 看到对应键被按下才加载，更省启动时间
      { "<M-o>",  "<cmd>Yazi toggle<CR>",       desc = "Yazi 切换",   mode = "n" },
      { "<M-+>",  "<cmd>BufferNext<CR>",        desc = "下一标签",   mode = "n" },
      { "<M-->",  "<cmd>BufferPrevious<CR>",    desc = "上一标签",   mode = "n" },
    },
    opts = {
      open_for_directories = true,
      keymaps = { show_help = "<f1>" },
    },
    init = function()
      -- 关掉 netrw，让 yazi.nvim 接管目录浏览
      vim.g.loaded_netrwPlugin = 1
    end,
  },
}
```

效果：

![img](img/ranger.png)

> 旧图保留以便对比 yazi 与 ranger 的视觉差异；`<M-o>` / `<M-+>` / `<M-->` 快捷键沿用。

### 5.5 Markdown 预览：markdown-preview.nvim

`iamcco/markdown-preview.nvim` 在社区里仍是事实标准，迁移到 lazy 之后配置无大变化：

```lua
-- lua/user/plugins/markdown.lua
return {
  {
    "iamcco/markdown-preview.nvim",
    cmd = { "MarkdownPreview", "MarkdownPreviewStop" },
    ft = "markdown",
    -- 注意：原来用 `build = function() vim.fn["mkdp#util#install"]() end`
    -- 会在 lazy 还在 clone 阶段（runtimepath 还没设置）就调用，必报
    -- `Vim:E117: Unknown function: mkdp#util#install`。
    -- 改用 `init` + `vim.schedule` 推迟到插件 source 完成后再装。
    init = function()
      vim.schedule(function()
        pcall(vim.fn["mkdp#util#install"])
      end)
    end,
  },
}
```

使用：

```vim
:MarkdownPreview       " 打开预览
:MarkdownPreviewStop   " 关闭预览
```

> [!WARNING] 维护停滞风险
>
> `iamcco/markdown-preview.nvim` 自 2024-07 之后未再发布新版本（撰写时已 2 年），目前仍可正常使用但已缺乏新功能与适配。如果你不想开浏览器、想在 NeoVim buffer 里直接渲染 Markdown（带加粗、斜体、代码块等格式高亮），可以用 `MeanderingProgrammer/render-markdown.nvim`（与 markdown-preview 是不同范式，二选一即可）；否则继续用 iamcco 的版本问题不大。

### 5.6 启动页：alpha-nvim

旧版的 `mhinz/vim-startify` 已多年未维护，社区主流切换到 alpha-nvim：

```lua
-- lua/user/plugins/alpha.lua
return {
  {
    "goolord/alpha-nvim",
    event = "VimEnter",
    config = function()
      require("alpha").setup(require("alpha.themes.startify").config)
    end,
  },
}
```

效果：

![img](img/vim-startify.png)

### 5.7 主题：catppuccin

旧版用的 `connorholyday/vim-snazzy` 已停止更新，替换为社区最常用的 `catppuccin/nvim`：

```lua
-- lua/user/plugins/colorscheme.lua
return {
  {
    "catppuccin/nvim",
    name = "catppuccin",
    priority = 1000,
    config = function()
      vim.cmd.colorscheme("catppuccin-mocha")
    end,
  },
}
```

效果：

![img](img/vim-snazzy.png)

> 旧图保留以便对比主题切换前后的视觉变化；当前默认主题为 catppuccin-mocha。

## 6. 常见问题

### Q1. `:LspInfo` 显示 `No client` / 跳不到定义

大概率是 LSP server 没装到 PATH 里。先 `which pyright`、`which clangd` 确认；没装就按 §5.2 装。Python 项目尤其要确认打开的是 **项目虚拟环境**里的 pyright，否则会读到全局 site-packages。

### Q2. `:checkhealth` 报 Python provider 缺失

```bash
pip install --user pynvim
# 如果用 venv，必须在 venv 里再装一次
.venv/bin/pip install pynvim
```

### Q3. lazy.nvim 安装时报 `failed to clone`

国内网络环境拉 GitHub 不稳。两种解决：

- 临时给 git 设代理：`git config --global http.proxy http://127.0.0.1:7890`
- 把 lazy 的 git 源改成 ghproxy（见 §4.1）。

### Q4. LSP 启动太慢

- 把 LSP 的触发时机从 `BufReadPre` 收紧到具体文件类型：

  ```lua
  { "neovim/nvim-lspconfig", ft = { "python", "cpp", "lua" } }
  ```

- 或直接用 NeoVim 0.11 的 `vim.lsp.enable({ "pyright", "clangd" })` 配合 `lazy = false` 的 server 配置，跳过 nvim-lspconfig。

### Q5. yazi 启动报 `command not found: yazi`

```bash
which yazi
# 没装就用 cargo 或包管理器
cargo install --locked yazi-fm yazi-cli
# 或者 Ubuntu 24.04+
sudo apt install -y yazi
```

### Q6. markdown 预览空白 / 中文乱码

`iamcco/markdown-preview.nvim` 需要 Node.js 18+，且国内网络下要装 markdown-it 等 npm 依赖：

```bash
npm config set registry https://registry.npmmirror.com
:checkhealth markdown-preview
```

### Q7. NeoVim 如何升级到 0.11/0.12+

不要用系统包管理器升级——会卡在发行版仓库的老版本。推荐下载 AppImage 替换 `/usr/local/bin/nvim`，或者直接用社区脚本：

```bash
curl -sL https://raw.githubusercontent.com/neovim/neovim-releases/latest/run.sh | bash
```

### Q8. `:Lazy` 提示某插件加载报错

最常见的是 `dependencies` 写错或 spec 写法不兼容当前 lazy 版本。先 `:Lazy update` 一次；如果还报错，删 `~/.local/share/nvim/lazy/<plugin>` 重装：

```bash
:Lazy clean   # 清掉不用的插件
:Lazy sync    # 重装 + 更新
```

### Q9. `lazy.nvim` clone 报 `Repository not found: .../nvim-web-devicon.git`

仓库 `nvim-tree/nvim-web-devicon`（单数）已删除 / 重命名为 `nvim-tree/nvim-web-devicons`（复数）。把所有依赖里的旧名换成新名：

```diff
- dependencies = { "nvim-tree/nvim-web-devicon" }
+ dependencies = { "nvim-tree/nvim-web-devicons" }
```

同样的坑在 `yazi-org/yazi.nvim` 上也踩过——那个仓库**根本不存在**，`mikavilpas/yazi.nvim` 的真正依赖只有 `nvim-lua/plenary.nvim`。

### Q10. `require('nvim-treesitter.configs') not found`

装了 NeoVim 0.12+ 才会遇到。`nvim-treesitter` 的 `master` 分支已经被冻结只做向后兼容，**不支持 0.12**；所有新功能在 `main` 分支，且 main 是**重大不兼容重写**：

```diff
  {
    "nvim-treesitter/nvim-treesitter",
+   branch = "main",
+   lazy = false,  -- main 分支明确说"This plugin does not support lazy-loading"
    build = ":TSUpdate",
-   event = { "BufReadPost", "BufNewFile" },
    config = function()
-     require("nvim-treesitter.configs").setup({ ... })
+     require("nvim-treesitter").setup({
+       install_dir = vim.fn.stdpath("data") .. "/site",
+     })
+     pcall(function()
+       require("nvim-treesitter").install({ "lua", "python", "json", ... })
+     end)
    end,
  }
```

另外 main 分支要求 `tree-sitter-cli` 0.26.1+，**且不能通过 npm 装**：

```bash
# macOS
brew install tree-sitter
# Ubuntu（scoop / cargo 也行）
cargo install tree-sitter-cli --locked
```

Windows 上 Scoop main bucket 有 `tree-sitter`：

```powershell
scoop install tree-sitter
```

### Q11. `options.lua:35: '=' expected near 'plugin'`

`filetype plugin indent on` 是 vimscript 命令，不能直接写在 `.lua` 文件里。要么用 `vim.cmd(...)` 包装，要么换成 Lua 等价写法：

```lua
-- 错误：vimscript 命令混进 Lua 文件
filetype plugin indent on

-- 正确做法 1
vim.cmd("filetype plugin indent on")

-- 正确做法 2（更显式）
vim.cmd([[
  filetype plugin indent on
]])
```

### Q12. `:LspStart` 报 `module 'cmp' not found` / `cmp_luasnip` after/plugin 失败

`hrsh7th/cmp-nvim-lsp`、`saadparwaiz1/cmp_luasnip`、`hrsh7th/cmp-path` 这类 cmp-* 的 `after/plugin/*.lua` 会在 lazy 加载它们时**第一时间** `require("cmp")`，但 `nvim-cmp` 本身没在 dependencies 顶层。

修法是把 `nvim-cmp` 拆成独立 spec，cmp-* 全列在它的 dependencies 里（参见 §5.2 改写后的代码）：

```lua
{
  "hrsh7th/nvim-cmp",  -- 先
  event = "InsertEnter",
  dependencies = {
    "hrsh7th/cmp-nvim-lsp", "L3MON4D3/LuaSnip",
    "saadparwaiz1/cmp_luasnip", "hrsh7th/cmp-path",
    "rafamadriz/friendly-snippets",
  },
  config = function() require("cmp").setup({ ... }) end,
},
```

### Q13. `:LspInfo` 报 `jsonls: spawn: not found`

`vscode-langservers-extracted` 这个 npm 包实际可执行文件是单数 `vscode-json-language-server.cmd`，但 `nvim-lspconfig` 内置的 jsonls 默认 cmd 写的是复数 `vscode-json-languageserver`（已过时）。在 spec 里显式覆盖 cmd：

```lua
vim.lsp.config("jsonls", {
  cmd = { "vscode-json-language-server", "--stdio" },
})
```

同理 `vscode-html-language-server` / `vscode-css-language-server` / `vscode-eslint-language-server` 都是单数。

### Q14. `mkdp#util#install` 不存在 / `Vim:E117`

`markdown-preview.nvim` 的 `mkdp#util#install` 函数只在插件 source 之后才存在，lazy 的 `build` 字段在 clone 完成**立即**执行（runtimepath 还没 prepend），必报 `Unknown function`。

改用 `init` + `vim.schedule` 推迟：

```lua
{
  "iamcco/markdown-preview.nvim",
  cmd = { "MarkdownPreview", "MarkdownPreviewStop" },
  ft = "markdown",
- build = function() vim.fn["mkdp#util#install"]() end,
+ init = function()
+   vim.schedule(function() pcall(vim.fn["mkdp#util#install"]) end)
+ end,
}
```

### Q15. Windows / Scoop 上跑本笔记配置要做的额外步骤

| 笔记里的命令 | Windows / Scoop 等价 |
| --- | --- |
| `sudo apt install -y ripgrep fd-find unzip` | `scoop install ripgrep fd unzip` |
| `pip install --user pyright` | `pip install pyright`（全局 venv 用） |
| `npm i -g bash-language-server yaml-language-server vscode-langservers-extracted` | 同左（scoop nvm 下的 npm） |
| `sudo apt install -y clangd` | `scoop install llvm`（自带 clangd） |
| `lua-language-server` 没有 npm 包 | `scoop install lua-language-server`（main bucket 里有 v3.19+） |
| `cargo install --locked yazi-fm yazi-cli` | `scoop bucket add extras && scoop install yazi` |
| `~/.config/nvim/` 路径 | `%LOCALAPPDATA%\nvim\`（即 `C:\Users\<u>\AppData\Local\nvim`），**不用建 `~/.config/nvim` 软链** |

> 笔记里 §5 的 spec 文件**跨平台通用**，仅上述几条命令需要换写法；配置文件结构（`init.lua` / `lua/user/*.lua`）在 Windows 上由 NeoVim 的 `stdpath('config')` 自动解析到 `%LOCALAPPDATA%\nvim\`，所以你只要把文件放对地方即可。

## 7. 附录：完整配置骨架

下面给出最小可用的全套配置，把它们按路径放好后，第一次启动 NeoVim 就会进入 lazy.nvim 的安装界面，按提示完成即可。

```lua
-- ~/.config/nvim/init.lua
require("user.lazy")
require("user.options")
```

```lua
-- ~/.config/nvim/lua/user/options.lua
vim.g.mapleader = " "
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.expandtab = true
vim.opt.shiftwidth = 2
vim.opt.clipboard = "unnamedplus"
vim.opt.signcolumn = "yes"
vim.opt.updatetime = 300
```

```lua
-- ~/.config/nvim/lua/user/lazy.lua
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not (vim.uv or vim.loop).fs_stat(lazypath) then
  vim.fn.system({
    "git", "clone", "--filter=blob:none", "--branch=stable",
    "https://github.com/folke/lazy.nvim.git", lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
  spec = { { import = "user.plugins" } },
  install_missing_modules = true,
  checker = { enabled = true },
})
```

```lua
-- ~/.config/nvim/lua/user/plugins/init.lua
return {
  require("user.plugins.edit"),
  require("user.plugins.lsp"),
  require("user.plugins.lualine"),
  require("user.plugins.yazi"),
  require("user.plugins.markdown"),
  require("user.plugins.alpha"),
  require("user.plugins.colorscheme"),
}
```

`edit.lua` / `lsp.lua` / `lualine.lua` / `yazi.lua` / `markdown.lua` / `alpha.lua` / `colorscheme.lua` 的内容见 §5 各小节。
