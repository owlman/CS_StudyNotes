# Rust 学习笔记（持续更新中）

这篇学习笔记将用于记录本人在学习 Rust 编程语言过程中所编写的学习心得与代码。为此，我会在`https://github.com/owlman/study_note`项目的`Programming/LanguageStudy/`目录下创建一个名为的`Rust`目录，并在该目录下设置以下两个子目录：

- `QuickStart`目录用于存放 Markdown 格式的笔记。
- `Examples`目录则用于存放笔记中所记录的代码示例。

## 学习资料

- 参考书籍：
  - [《Rust 实战》](https://book.douban.com/subject/35081743/)
  - [《精通 Rust》](https://book.douban.com/subject/35290878/)
- 视频教程：
  - [Rust 编程语言入门教程](https://www.bilibili.com/video/BV1hp4y1k7SV?spm_id_from=333.999.0.0)

## 学习准备阶段

Rust 是一门由 Mozilla 基金会主导开发的通用、编译型程序设计语言。这门语言的设计准则为“安全、并发、实用”，它支持函数式、并发式、命令式等多种编程范式，目前被认为是自 C++ 以来最全能的系统级程序设计语言。它为系统编程领域提供了一种更安全、更快速且原生支持并发的现代化解决方案，具有相当的学习价值。当然了，在具体学习这门语言之前，我需要先了解一些背景知识。

### 语言的起源故事

Rust 语言最初只是 Mozilla 公司员工 Graydon Hoare 在 2006 年开发的一个私人项目，而 Mozilla 基金会本身则是到了 2009 年才开始正式赞助这个项目 ，并于 2010 年首次向公众发布。第一个有版本号的 Rust 编译器于 2012 年 1 月发布，这是一个基于 LLVM 编译器框架开发的、可自我编译的编译器。Rust 1.0 是它的第一个稳定版本，于 2015 年 5 月 15 日发布。

Rust 项目是完全开源的，并且相当欢迎社区的反馈。在 1.0 稳定版之前，语言设计也因为透过撰写 Servo 网页浏览器排版引擎和 rustc 编译器本身，而有进一步的改善。虽然它由 Mozilla 资助，但它其实是一个开源项目，有很大部分的代码是来自于社区的贡献者。

### 语言的优势分析

Rust 语言的设计目标是希望帮助人们以更简单明了的方式来设计高度可靠且快速的软件系统，它既可用于底层机器操作的具体实现，也可用于高层抽象逻辑的应用设计，因此成为了时下最热门的程序设计语言之一。具体来说，Rust 语言相较于其他程序设计语言具有以下独特优势：

- **更安全的内存管理**：与 C/C++ 语言相比，使用 Rust 语言来进行程序设计可以从源头上去预防出现诸如空指针，缓存溢出和内存泄漏等问题带来的困扰。
- **更好的运行性能**：与 Java/C# 等语言相比，Rust 语言的内存管理不是依靠垃圾回收器机制（ GC ）来实现的。这个设计提高了程序运行的性能。
- **原生支持多线程开发**：Rust 语言的所有权机制和内存安全的特性为没有数据竞争的并发提供了语言层面上的原生支持。
- **支持 WebAssembly**：WebAssembly 语言的出现解决了人们希望在 Web 浏览器、嵌入式设备等环境中执行计算密集型操作的需求。而用 Rust 语言编写的代码可以被直接编译成 WebAssembly 程序，这样就能确保程序在上述执行环境中拥有与本地代码相似的执行速度。

下面来看一看 Rust 语言的主要使用场景：

- **学术研究**：Rust 语言在计算机专业领域中是一个很好的学术研究工具。例如，人们可以学习如何使用 Rust 语言开发操作系统，这个学习过程将帮助他们更好地理解操作系统中的各种概念。
- **团队合作**：对于开发者团队来说， Rust 语言是非常实用的工具。众所周知，低水平的程序代码会包含很多 bug，需要测试人员进行覆盖测试广泛验证。然而在 Rust 语言中，如果程序代码中包含 bug，编译器将拒绝编译代码，这样一来，开发者就可以更专注于程序的业务逻辑了。
- **商业开发**：到目前为止，已经有不少大大小小的公司选择使用 Rust 语言来完成各种商业开发的任务。这些任务包括命令行工具，Web 服务，DevOps 工具，嵌入式设备，音频和视频的分析和转码，加密货币，生物信息学，搜索引擎，物联网应用，机器学习，甚至是火狐浏览器的重要组成部分。
- **开源运动**：Rust 本身就是一门遵守 Apache 和 MIT 开源许可证的程序设计语言，这意味人们可以按照这些许可证赋予的权益参与各种 Rust 语言设计与推广的公益活动。

### 语言环境的配置

由于 Rust 的语言环境是基于 C/C++ 编译工具来构建的，这意味着在安装语言环境之前，我们的计算机上至少需要先安装一个 C/C++ 编译工具。换句话说，如果该计算机上使用的是类 Linux 系统，它就需要先安装 GCC 或 clang。如果是 macOS 系统，则就需要先安装 Xcode。如果是 Windows，则需要先安装 Visual Studio 2013 或 MinGW 之类的 C/C++ 编译工具。

#### 下载并执行安装脚本

到目前为止，Rust 语言环境大体上都是通过安装脚本的形式来安装的。所以在确定安装了 C/C++ 编译工具之后，` 接下来要做的就是根据自己所在的操作系统来下载并执行 Rust 语言环境的安装脚本了。

- 如果想要在 Windows 系统下学习 Rust，我们只需在搜索引擎中搜索“rust”关键字或直接在 Web 浏览器的地址栏中输入`https://www.rust-lang.org/`这个 URL 即可进入到 Rust 语言的官方网站，然后通过点击首页中的“install”链接，就会看到如下页面：

  ![rust_install](img/rust_install.png)

  在该页面中，我们可以根据自己所在的平台来下载 32 位或 64 位版本的安装脚本（通常是一个名为`rustup-init.exe`的二进制文件）。待下载完成之后，我们就可以双击执行该安装脚本，并遵循屏幕上的指示来安装（对于初学者，只需一路选择默认选项即可）。

- 如果想在类 UNIX 系统（包括 WSL)下学习 Rust，我们只需直接终端环境中执行下面的 shell 代码，并遵循终端返回的指示信息来安装（对于初学者，只需一路选择默认选项即可）。

  ```bash
  # 可选步骤：设置国内下载镜像
  echo "export RUSTUP_DIST_SERVER=https://mirrors.ustc.edu.cn/rust-static" >> ~/.bashrc
  echo "export RUSTUP_UPDATE_ROOT=https://mirrors.ustc.edu.cn/rust-static/rustup" >> ~/.bashrc
  source .bashrc

  # 下载并执行安装脚本
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

  # 安装完毕后刷新环境变量
  source ~/.cargo/env
  ```

#### 管理语言环境的版本

默认情况下，我们安装的语言环境是属于 stable 这一版本系列的，这一系列的版本迭代周期大约是每六周一次，它在各方面的配备都会偏向于确保生产环境的稳定性。但如果我们想使用类似 racer 这一类组件的部分功能，就必须切换到配置方案更偏向于学习、实验性质的 nightly 版本（这一系列的版本迭代周期是每天一次）。在 Rust 语言环境中，人们通常是利用 rustup 这一命令工具来实现版本管理的，其具体使用方式如下：

```bash
# 安装指定版本的语言环境
rustup install <版本号>
# 安装语言环境的 nightly 版本
rustup install nightly
# 将语言环境的默认版本设置为 nightly
rustup default nightly
# 更新当前系列版本的语言环境
rustup update
# 删除当前版本的语言环境
rustup self uninstall
```

待上述命令执行完成之后，我们可通过在终端中执行`rustc -V` 和`cargo -V`来查看是否能输出相应的版本信息。如果这两个命令输出了相应的版本信息，就证明 Rust 语言环境的安装和配置工作已经成功了一半了，接下来的任务是配置 Cargo 并安装相关插件。

#### 使用 Cargo 包管理器

Cargo 是一个内置在 Rust 语言环境中的包管理器及项目构建工具，其作用类似于 Node.js 运行环境中的 NPM。也就是说，在开发 Rust 项目的过程中，我们可以使用 Cargo 包管理器来下载并管理当前项目所依赖的第三方程序库，以及完成项目的构建工作。

和 NPM 一样，Cargo 在默认情况下链接的是`https://crates.io/`这个官方的程序仓库。由于众所周知的原因，这个服务器位于国外的官方仓库的可用性非常容易受到各种不可抗力的影响，很多时候是不确定的，我们最好还是将其设置为国内的代理仓库。为此，我们需要将代理仓库的服务器地址写到 cargo 的配置文件中（该配置文件就叫“config”，没有扩展名，通常情况下位于`${HOME}/.cargo/`目录中）。在这里，我将其具体配置如下：

```bash
[source.crates-io]
registry = "https://github.com/rust-lang/crates.io-index"
# 指定镜像
replace-with = 'sjtu'

# 清华大学
[source.tuna]
registry = "https://mirrors.tuna.tsinghua.edu.cn/git/crates.io-index.git"

# 中国科学技术大学
[source.ustc]
registry = "git://mirrors.ustc.edu.cn/crates.io-index"

# 上海交通大学
[source.sjtu]
registry = "https://mirrors.sjtug.sjtu.edu.cn/git/crates.io-index"

# rustcc 社区
[source.rustcc]
registry = "https://code.aliyun.com/rustcc/crates.io-index.git"
```

在配置完上述内容之后，可以通过执行`rustup update`命令来验证代理仓库是否可用。如果一切正常，该命令会将当前语言环境中的所有组件更新到最新版本。

安装 rust-analyzer 组件

```bash
rustup component add rust-analyzer --toolchain stable
```

#### 构建开发环境

推荐使用 VSCode：`https://code.visualstudio.com/`
安装好 VSCode后，Ctrl + Shift + X 打开应用商店
搜索chinese安装中文语言包，搜索Rust (rls)官方的插件，基本上就OK可以撸代码了。

## 语言基础学习阶段

### 使用 Cargo 构建并运行项目

## 第 2 部分：编写本地应用程序

## 第 3 部分：编写网络应用程序
