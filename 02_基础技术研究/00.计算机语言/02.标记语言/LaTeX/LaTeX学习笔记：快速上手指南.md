# LaTeX 学习笔记：快速上手指南

众所周知，$\LaTeX$ 语言本质上是一套封装了 $\TeX$ 处理细节的宏，其中使用的每一个标记实际上都是一个宏。下面，让我们先来简单了解一下 $\LaTeX$ 标记的基本使用，因为这种形式也会出现在复杂的公式中。这种形态的 $\LaTeX$ 标记通常会以一个反斜杠开头，后面紧接着该命令的名称，这个名称既可能是个单一符号，也可能是一个字符串。命令名称之后还可以有一些指定参数，我们通常会用花括号将它们括起来（如果该参数只有一个字符，花括号可以省略）。除此之外，如果有可选参数，则用方括号括起来，具体如下：

- 无参数形式：`\command`。
- 有参数形式：`\command{参数1}{参数2}……{参数N}`。
- 带可选参数形式：`\command[可选参数]{参数1}{参数2}……{参数N}`。

例如，我们现在这里所显示的“$\LaTeX$”字样，使用的就是一个无参数形式的标记`\LaTeX`。再例如，我们之前所使用开方标记`\sqrt`，就需要有一个指定参数来表示被开方数。另外，我们还可以用该标记的可选参数来指定开方的次数。当然，关于这些标记的具体应用，我们稍后会开辟专题讨论。眼下，先让我们来初步了解一下 $\LaTeX$ 的基本使用方式，以便实现对这门语言的快速上手。

## 在第三方文档中的使用

或许对许多人来说，有些反直觉的是：尽管 $\LaTeX$ 的设计初衷是服务于学术文献的专业排版，但从实际使用的角度来看，它被应用得最广泛的场景，反而不是在专门的排版系统中，而是以公式编辑功能的形式，嵌入于 Word、Markdown 等第三方文档编辑器之中。下面，让我们从最简单的情况开始，分别介绍 $\LaTeX$ 标记在 Word 与 Markdown 文档中的具体用法。

### 在 Word 中的使用

从 Word 2016 开始，微软在其内置的公式编辑器中加入了对 $\LaTeX$ 语法的直接支持，这使得用户无需借助第三方插件（如 MathType），就能在 Word 文档中使用 $\LaTeX$ 标记来编写数学公式[^1]。换句话说，Word 自身已经具备了将 $\LaTeX$ 语法解析为数学公式的能力。

要在 Word 中插入 $\LaTeX$ 公式，可以按照以下步骤进行操作：

1. 将光标放在希望插入公式的位置；
2. 在菜单栏中依次选择 **“插入 → 公式（Insert → Equation）”**；
3. 在弹出的公式编辑框中，点击右上角的下拉箭头，在“公式选项（Equation Options）”中找到 **“公式输入模式（Input Mode）”**；
4. 将输入模式切换为 **“LaTeX”**；
5. 现在就可以直接输入 $\LaTeX$ 语法了。输入完成后按下 **空格键** 或 **Enter 键**，Word 会自动将其渲染为格式化的数学公式。

例如：

```LaTeX
\int_{0}^{\infty} e^{-x^2} \, dx = \frac{\sqrt{\pi}}{2}
```

在 Word 的 LaTeX 模式中会自动被渲染为：

$$
\int_{0}^{\infty} e^{-x^2} \, dx = \frac{\sqrt{\pi}}{2}
$$

值得注意的是，Word 对 $\LaTeX$ 的支持并不是完全的，它仅实现了 $\LaTeX$ 数学语法的一个子集。例如，某些高级宏命令、宏包功能以及自定义命令（如 `\newcommand`）在 Word 中是无法使用的。此外，Word 对排版细节的控制能力远不及原生的 $\LaTeX$ 系统，因此这种模式更适合于**公式较简单的文档场景**，而不适合进行大规模的学术论文或书籍排版。

总的来说，如果你的目标只是为了在 Word 文档中插入数学公式，而不需要完全掌握 $\LaTeX$ 的宏包体系与版面控制，那么利用 Word 的内置 $\LaTeX$ 模式是一种非常便捷且低门槛的选择。

### 在 Markdown 中的使用

在如今这个时代，当我们需要在本地计算机上对文件进行编辑时，往往就意味着要做一些较为复杂的事，这就需要编辑器具有完善的编辑功能，就 Markdown 来说，用来编辑本地文件的编辑器如果只支持基本语法，显然就不够用了。我们得根据自己的编辑需要来选择支持某部分扩展特性的 Markdown 编辑器，例如要支持编辑数学公式、流程图、UML图以及代码高亮显示，那么选择的编辑器就必须要能支持 $\LaTeX$、`Mermaid`等扩展以及文件预览功能。当然，符合这些要求的 Markdown 编辑器也不少，我在这里主要推荐如下这两款目前最具有代表性的。

- **Typora**：​ Typora 是一款轻便简洁的 Markdown 编辑器，它通过内置的 MathJax 渲染引擎实现了对 $\LaTeX$ 标记的即时预览。这种即时渲染技术让它可以和 Word、Pages 一样提供”所见即所得“的写作体验。这也是它与其他 Markdown 编辑器最显着的区别，不再需要分栏显示编写区和预览区了。除此之外，Typora也是一款支持多平台的 Markdown 编辑器，我们在 Linux、MacOS 和 Windows 中都可以使用这款软件。
 
- **VS Code**：VS Code是 Visual Studio Code 的缩写，这是一款通用的代码编辑器，它同样在 Linux、MacOS 和 Windows 下都可以使用。正是由于这是一款通用的代码编辑器，主要的作用是编写程序代码，因此其自身集成了强大的文件管理和版本控制模块，这些模块可以帮助我们轻松地实现工程级的项目管理。更为重要的是，VSCode具有非常强大的插件体系，以便它可以胜任几乎所有编程语言和标记语言的编辑。譬如对于 Markdown，我们只需要在 VS Code 编辑器的插件管理系统中搜索并安装一款名为 Markdown Extension Pack 的插件包装即可，该插件包通过对 Markdown Preview Enhanced 插件的依赖，或内置的 Markdown-it + KaTeX 机制实现了对 $\LaTeX$ 标记的渲染。

需要注意的是，Markdown 编辑器中的 $\LaTeX$ 渲染通常并非真正调用 TeX 引擎，而是通过 MathJax 或 KaTeX 等 JavaScript 数学排版引擎实现的。这种方式虽然不具备完整的宏包功能，但足以满足一般的公式显示需求。

在设置好 Markdown 的编辑环境之后，我们就可以在 Markdown 文档中插入 $\LaTeX$ 标记了。具体来说，$\LaTeX$ 标记的引用方式主要有以下两种：

- **行内引用**：采用行内引用方式的 $\LaTeX$ 标记通常与正常文本处于同一逻辑行中（软件界面导致的自动换行不算），具体语法就是*在待引用标记的前后各加一个美元符号*。例如，如果我们想显示“我正在使用 $\LaTeX$ 来排版论文。”这句话，只需进行如下编码即可：  
  
  ```Markdown
  我正在使用$\LaTeX$来排版论文。
  ```

- **单独引用**：采用单独引用方式的 $\LaTeX$ 标记通常会独立于正常文本，自成一行，具体语法就是*在待引用标记的前后各加两个美元符号*。例如，如果我们想在 Markdown 文档中讨论勾股定理，就可以使用如下编码来描述该定理：

  ```Markdown
  在平面上的一个直角三角形中，如果设直角三角形的两条直角边长度分别是a和b，斜边长度是c，那么按照勾股定理，这三边的关系如下：
  
  $$ a^{2} + b^{2} = c^{2} $$
  
  这也就意味着：
  
  $$ a = \sqrt{c^{2} - b^{2}} $$
  $$ b = \sqrt{c^{2} - a^{2}} $$
  $$ c = \sqrt{a^{2} + b^{2}} $$
  ```

  其渲染效果如下

    > 在平面上的一个直角三角形中，如果设直角三角形的两条直角边长度分别是a和b，斜边长度是c，那么按照勾股定理，这三边的关系如下：
    >
    > $$ a^{2} + b^{2} = c^{2} $$
    >
    > 这也就意味着：
    >
    > $$ a = \sqrt{c^{2} - b^{2}} $$  
    > $$ b = \sqrt{c^{2} - a^{2}} $$  
    > $$ c = \sqrt{a^{2} + b^{2}} $$

请注意，读者暂时不用担心看不懂上面这些数学公式中使用的 $\LaTeX$ 标记，因为我稍后会在《[[LaTeX学习笔记：数学公式编辑]]》这篇笔记中开专题讨论这些标记的具体使用。在这里，我们只需要对 $\LaTeX$ 标记的引用方式有清楚的认知就可以了。

## 在专业排版软件中的使用

如果我们使用 $\LaTeX$ 的目的并不局限于编辑数学公式，而是希望更充分地发挥它在学术文档排版方面的专业能力，那么就需要使用像 TeX Live、MiKTeX 这样的 $\LaTeX$ 专用软件。在专业术语中，这类软件被称为 **$\TeX$ 发行版（distribution）**，它们能够提供完整的 $\LaTeX$ 编译环境，支持从命令行到图形化界面的多种使用方式。

在简体中文写作环境中，为了简化排版配置，我们通常会选择安装 CTeX 套装（基于 MiKTeX 的发行版），或在 TeX Live 中添加 ctex 宏包，以搭建专用的 $\LaTeX$ 编译与编辑环境。下面，让我们来介绍一下 $\LaTeX$ 专用环境的搭建及其使用方法。

### 基于 CTeX 套装的使用

CTeX 套装是在 Windows 系统中最为常见的中文 $\LaTeX$ 发行版之一。它以 MiKTeX 为核心发行版，集成了常用的中文宏包（如 `ctex`、`xeCJK` 等）和若干常用编辑器（如 WinEdt、TeXworks 等），从而为用户提供了一个**即装即用**的中文 $\LaTeX$ 编译与编辑环境。与手动配置相比，CTeX 套装最大的优点在于安装简单、中文支持完善，提供有独立的 Windows 安装包。虽然该项目已多年未更新，但其稳定性和兼容性仍然能够满足一般的中文排版需求，非常适合以 Windows 系统为主要工作环境的初级用户。下面，让我们来介绍一下安装和使用 CTeX 套装的具体步骤。

1. 在网页浏览器中打开 CTeX 套件在[清华大学的镜像站](https://mirrors.tuna.tsinghua.edu.cn/ctex/legacy/)。[^2]

2. 根据自己所在的操作系统（例如 64 位的 Windows）下载最新版本的安装包，例如`CTeX_3.0.215.2.exe`。

3. 双击下载好的安装包文件，启动 CTeX 的图形化安装界面，并根据界面的提示执行如下设置：

   1. 在下面的界面中选择[简体中文]，并点击“下一步”按钮。

      ![选择安装语言](./img/ctex1.png)

   2. 勾选下面界面中所有的组件以确保安装 CTeX 所有的功能，然后点击“下一步”按钮。

      ![选择要安装的组件](./img/ctex2.png)

   3. 在下面界面中设置安装路径（我在这里将其设置为`D:\CTeX`），然后点击“安装”按钮。

      ![选择安装路径](./img/ctex3.png)

   4. 安装过程可能持续数分钟，请耐心等待安装完成。

      ![安装过程的进度条](img/ctex4.png)

   5. 待安装完成之后，我们将会看到如下界面，现在只需点击“完成”按钮即可结束安装。

      ![安装完成](./img/ctex5.png)

4. 待安装完成之后，系统会自动将 CTeX 的可执行文件路径加入到 Windows 的环境变量中。若在命令行终端环境（例如 Bash 或 Powershell）中运行 `latex`、`xelatex` 或 `pdflatex` 时出现“命令未找到”等提示，可以手动检查路径设置：

   1. 打开“系统属性 → 高级 → 环境变量”。

   2. 在“系统变量”中找到`Path`，根据自己安装时的设置确保其中包含类似以下路径：

      ```text
      D:\CTeX\MiKTeX\miktex\bin\
      D:\CTeX\CTeX\bin\
      ```

5. 现在，如果问你想要在 VS Code 编辑器中编写 $\LaTeX$ 文档，就可以通过如下步骤来实现（这也可用于验证 CTeX 是否安装成功）：

   1. 打开 VS Code 编辑器，并安装 LaTeX Workshop 和 LaTeX 这两个插件。

      ![安装 VS Code 编辑器的 LaTeX 插件](./img/ctex6.png)

   2. 在 VS Code 编辑器的命令面板中执行`[首选项：打开工作区设置（JSON）]`命令。

      ![打开 VS Code 编辑器的工作区配置文件](./img/ctex7.png)

   3. 在`settings.json`文件中添加如下内容，完成插件的配置工作：

        ```json
        {
            //---------LaTeX Workshop 配置开始-----------
            // 设置是否自动编译,可选："never", "onSave", "onFileChange"
            "latex-workshop.latex.autoBuild.run":"never",
            //文件输出路径，会自动创建temp文件
            //"latex-workshop.latex.outDir": "./temp",
            //右键菜单
            "latex-workshop.showContextMenu":true,
            //从使用的包中自动补全命令和环境
            "latex-workshop.intellisense.package.enabled": true,
            //编译出错时设置是否弹出气泡设置
            "latex-workshop.message.error.show": false,
            "latex-workshop.message.warning.show": false,
            // 编译工具和命令
            "latex-workshop.latex.tools": [
                {
                    "name": "xelatex",
                    "command": "xelatex",
                    "args": [
                        "-synctex=1",
                        "-interaction=nonstopmode",
                        "-file-line-error",
                        //"-output-directory=temp", //自定义辅助文件输出路径
                        //"-outdir=%OUTDIR%", //辅助文件输出路径
                        "%DOCFILE%"
                    ]
                },
                {
                    "name": "pdflatex",
                    "command": "pdflatex",
                    "args": [
                        "-synctex=1",
                        "-interaction=nonstopmode",
                        "-file-line-error",
                        //"-output-directory=temp", //自定义辅助文件输出路径
                        //"-outdir=%OUTDIR%", //辅助文件输出路径
                        "%DOCFILE%"
                    ]
                },
                {
                    "name": "latexmk",
                    "command": "latexmk",
                    "args": [
                        "-synctex=1",
                        "-interaction=nonstopmode",
                        "-file-line-error",
                        "-pdf",
                        "-outdir=%OUTDIR%",
                        "%DOCFILE%"
                    ]
                },
                {
                    "name": "bibtex",
                    "command": "bibtex",
                    "args": [
                        "%DOCFILE%"
                    ]
                }
            ],
            // 用于配置编译链
            "latex-workshop.latex.recipes": [
                {
                    "name": "XeLaTeX",
                    "tools": [
                        "xelatex"
                    ]
                },
                {
                    "name": "XeLaTeX*2",
                    "tools": [
                        "xelatex",
                        "xelatex"
                    ]
                },
                {
                    "name": "PDFLaTeX",
                    "tools": [
                        "pdflatex"
                    ]
                },
                {
                    "name": "PDFLaTeX*2",
                    "tools": [
                        "pdflatex",
                        "pdflatex"
                    ]
                },
                {
                    "name": "BibTeX",
                    "tools": [
                        "bibtex"
                    ]
                },
                {
                    "name": "LaTeXmk",
                    "tools": [
                        "latexmk"
                    ]
                },
                {
                    "name": "xelatex -> bibtex -> xelatex*2",
                    "tools": [
                        "xelatex",
                        "bibtex",
                        "xelatex",
                        "xelatex"
                    ]
                },
                {
                    "name": "pdflatex -> bibtex -> pdflatex*2",
                    "tools": [
                        "pdflatex",
                        "bibtex",
                        "pdflatex",
                        "pdflatex"
                    ]
                }
            ],
            //文件清理。此属性必须是字符串数组
            "latex-workshop.latex.clean.fileTypes": [
                "*.aux",
                "*.bbl",
                "*.blg",
                "*.idx",
                "*.ind",
                "*.lof",
                "*.lot",
                "*.out",
                "*.toc",
                "*.acn",
                "*.acr",
                "*.alg",
                "*.glg",
                "*.glo",
                "*.gls",
                "*.ist",
                "*.fls",
                "*.log",
                "*.fdb_latexmk"
            ],
            //设置为onFaild 在构建失败后清除辅助文件
            "latex-workshop.latex.autoClean.run": "onFailed",
            // 使用上次的recipe编译组合
            "latex-workshop.latex.recipe.default": "lastUsed",
            // 用于反向同步的内部查看器的键绑定。ctrl/cmd +点击(默认)或双击
            "latex-workshop.view.pdf.internal.synctex.keybinding": "double-click",
            //设置查看PDF的工具，可选"browser","tab","external"
            "latex-workshop.view.pdf.viewer": "tab", 
            //---------LaTeX Workshop 配置结束-----------
        }
        ```

   4. 在用于演示的`example/hello_latex`目录中新建一个名为`hello_latex.tex`的文件，并在其中输入以下内容：

        ```latex
        \documentclass{ctexart}
        \begin{document}
            \title{您好！\LaTeX}
            \author{张三}
            \date{\today}
            \maketitle
            这是我的第一个\LaTeX 文档，仅用于学习专业文档的排版。    
            \section{第一部分}
            \subsection{第一小节}
            \subsubsection{第一小小节}
            \paragraph{第一小段} 这是一个段落。
            \subparagraph{第一小段} 这是一个子段落。
            \section{第二部分}
            \subsection{第二小节}
            \subsubsection{第二小小节}
            \paragraph{第二小段} 这是一个段落。
            \subparagraph{第二小段} 这是一个子段落。
        \end{document}
        ```

   5. 在 VS Code 编辑器的命令面板中执行`[LaTeX workshop: 构建 LaTeX 项目]`命令。

      ![执行构建 LaTeX 项目的命令](./img/ctex8.png)

   6. 如果一切顺利，我们就会在`example`目录中一个文件名为`hello_latex.pdf`，内容包含“你好，LaTeX！”字样的 PDF 文件，这表明基于 CTeX 套件的中文排版环境已配置成功。

      ![构建 LaTeX 项目的结果](./img/ctex9.png)

这里需要提醒读者注意的是：CTeX 套装自带的宏包版本是比较老旧的，如果在使用过程中遇到了兼容性问题，我们可通过 **MiKTeX Console** 进行在线更新来修复问题，该程序界面如下所示：

![更新 MiKTeX 宏包](./img/ctex10.png)

如果 MiKTeX Console 启动失败，通常会看到类似“this application failed to start because no Qt platform plugin could be initialized”的错误信息。这通常是由于缺少或损坏的 Qt 插件导致的。该问题可通过执行`miktex --admin packages update`命令升级 MiKTeX 的版本来解决。

另外，如果读者计划编写大型文档或需要使用现代字体与宏包，我会更建议大家使用 **TeX Live + ctex 宏包** 的方案，以获得更好的可维护性和长期支持。 总而言之，CTeX 套装为中文用户提供了一个开箱即用的 $\LaTeX$ 工作环境，它简化了复杂的配置过程，使用户能够专注于内容创作与排版逻辑的学习。虽然其更新频率较低，但作为入门与教学用途，依然具有较高的实用价值。

同样的，读者现在暂时也不用担心看不懂`hello_latex.tex`文件中所用到的这些 $\LaTeX$ 标记，因为我稍后也会在《[[LaTeX学习笔记：专业文献排版]]这篇笔记中开专题介绍这些标记，目前只需知道如何搭建 $\LaTeX$ 的中文排版环境即可。

<!-- 以下是注释区 -->

[^1]:部分早期Word2016版本可能需要更新至Office365才能完整启用LaTeX模式。
[^2]:CTeX的官方网站已经停止维护多年，但我们可以通过它在国内的各种镜像站点下载到CTeX套装。
