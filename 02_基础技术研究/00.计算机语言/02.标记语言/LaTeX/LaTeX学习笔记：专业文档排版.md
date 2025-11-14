# LaTeX 学习笔记：专业文档排版

在撰写学术论文、技术报告或专业著作时，排版的质量往往决定了作品给人的第一印象。对于计算机科学、工程技术、数理化等领域而言，文档中不仅包含大量数学公式，还常常涉及图表、参考文献等复杂结构。正如我们在《[[LaTeX学习笔记：开场白与索引]]》一文中所提到的那样，计算机科学家们正是为了应对这些复杂的排版需求而开发了 $\LaTeX$。

在本篇笔记中，我们将重点介绍 $\LaTeX$ 在专业排版中的使用技巧，帮助你提升学术文档的可读性与专业气质。下面，就让我们先从文档结构的定义开始吧。

## 定义文档的结构

在 $\LaTeX$ 中，文档的整体结构是通过一系列**结构性命令**（structural commands）来定义的。这些命令用于指定文档所属的类型、加载所需的宏包、设置标题、作者等元信息，并生成文档的开篇部分。最常用的命令包括：

- `\documentclass`：用于指定文档所属的类型；
- `\usepackage`：用于通过加载宏包的方式来获得扩展功能；
- `\title`、`\author`、`\date`：用于定义文档的标题、作者等元信息；
- `\maketitle`：用于在正文中生成标题页。

接下来，我将会按照功能逐一介绍这些命令的使用方法。

### 指定文档的类型

在使用 $\LaTeX$ 定义一个文档的排版结构时，我们通常首先需要其源文件的第一行使用`\documentclass`命令指定要采用的文档类型。具体来说就是，我们需要先指定该文档的排版规格属于短篇文章、学术报告还是书籍等。在日常工作中，我们较为常用的文档类型主要如下：

1. **标准文档类**，由 $\LaTeX$ 核心包提供，主要包括以下四个类：

   - `article`：用于排版短篇文章，包括期刊投稿、技术文档等；
   - `report`：用于排版学术报告，包括毕业论文、技术报告等；
   - `book`：用于排版书籍类文档，例如专着、教材等；
   - `letter`：用于排版信件类文档，包括个人书信、商务信函等；

2. **扩展文档类**，类由`extsizes`宏包提供，提供有`extarticle`、`extreport`、`extbook`三个类，分别对应上述三个标准文档类的扩展版，主要支持更大的字号选项（如 `14pt`、`17pt`、`20pt`），其余行为与原类一致。

3.**中文文档类**，这些类由`ctex`宏包提供，提供有`ctexart`、`ctexrep`、`ctexbook`、`ctexletter`四个类，分别对应上述四个标准文档类的中文增强版本，自动配置中文字体、字号、段落间距与标题格式，更适合中文排版。另外，其中的`ctexletter`类在新版 CTeX 宏集中（自 2.0 以后），ctexletter 仍存在但默认未随发行版编译安装，可通过 texdoc ctex 查阅详细信息。

例如，如果想要对目标文档按照`ctexart`类型来排版，就需要在其 $\LaTeX$ 源文件的开头添加以下命令：

```tex
\documentclass{ctexart}
```

值得一提的是，该命令除了指定文档的类型之外，还可以通过一些可选参数来指定文档的某些排版细节。例如像下面这样：

```tex
\documentclass[12pt,oneside]{ctexart}
```

在上述命令的中括号里，参数`12pt`用于将文档的字体大小设置为 12 磅（point），而参数`oneside`则用于指定该文档将采用单面打印的方式输出。总体来说，`\documentclass`命令的可选参数主要可分为以下几大类：

1. **字体与字号参数**：用于设置文档的字体大小，除了之前提到的 `12pt` 外，还包括如下常见选项：

   - `10pt`（默认值）：适用于一般文档；
   - `11pt`：适用于需要稍大字体的论文或报告；
   - `14pt`, `17pt`, `20pt`：部分扩展类支持更大的字号；

   需要再次强调的是：`14pt`、`17pt`、`20pt`等较大字号仅在`extarticle`等扩展类中可用。另外，对于中文类文档（如 `ctexart`），也可通过 `zihao` 参数控制字号，例如：

   ```tex
   \documentclass[zihao=-4]{ctexart} % 设置中文字号
   ```

   这会根据中文字号标准（初号、四号等）调整排版比例，更符合中文出版规范。

2. **页面尺寸参数**：用于设置文档的页面尺寸，常见选项主要包括：

   - `a4paper`：适用于 A4 纸；
   - `letterpaper`：适用于 US Letter 纸；
   - `a5paper`：适用于 A5 纸；
   - `b5paper`：适用于 B5 纸；
   - `executivepaper`：适用于 Executive 纸；
   - `legalpaper`：适用于 Legal 纸；

3. **页面布局参数**：用于设置文档的页面布局，常见选项主要包括：

   - `titlepage/notitlepage`：控制是否生成独立标题页（`report`和`book`这两个类默认采用`titlepage`，`article`类默认则不是）；
   - `openright/openany`：控制章节起始页是否必须在奇数页（书籍排版常用）；
   - `twocolumn/onecolumn`：双栏或单栏排版；
   - `draft/final`：在草稿模式下，LaTeX 会标出溢出行、图片留空；
   - `fleqn/leqno`：左对齐公式或在左侧编号；

4. **打印与装订参数**：用于设置文档的打印与装订方式，常见选项主要包括：

   - `oneside` / `twoside`：控制单双面排版（`book`类默认采用`twoside`）；
   - `bindingoffset`：配合 `geometry` 设置装订空白；
   - `landscape`：横向排版（与 PDF 输出相配合时尤其有用）。

这些可选参数共同决定了文档的版式与打印方式，是掌握专业排版的基础。接下来，我们将介绍如何通过 \usepackage 命令加载宏包，以进一步扩展 $\LaTeX$ 的功能。

当然，除了上面列出的常用文档类型之外，一些特定的学术期刊或机构可能会要求我们按照特定的文档类型来排版，例如`IEEEtran`、`acm_proc_article-sp`等。虽然在通常情况下，这些文档类型也只需使用`\documentclass`命令来指定即可，但在某些特定情况下，如果想让这些第三方文档类型充分发挥作用，还需通过`\usepackage`命令来加载这些第三方文档类型指定的宏包，以扩展 $\LaTeX$ 的排版功能，下面就让我们继续来看这个命令的使用方法吧。

### 加载所需的宏包

从程序员的角度，我们可以将 $\LaTeX$ 中的`\usepackage`命令理解成 Python 中的`import`语句，C/C++ 语言中的`#include`语句，它们的作用都是在当前源文件中引入 $\LaTeX$ 自带或者第三方提供的扩展包，以便获得特定的功能。在 $\LaTeX$ 中，这些扩展包都是以“宏包（package）”的形式提供的，例如`amsmath`、`graphicx`、`hyperref`等。具体来说，就是我们需要在使用`\documentclass`命令指定了当前文档所要采用的排版类型之后，就紧接着使用`\usepackage`命令来加载我们需要的宏包，以便获得这些宏包提供的扩展功能。例如，如果我们既想使用标准类`article`排版，又想在文档中使用中文，就可以通过`\usepackage`命令加载`ctex`这个宏包来实现，就像下面这样：

```tex
\documentclass{article}
\usepackage{ctex}
% 其他命令 ...
```

除此之外，为了达到专业排版效果，我们通常还会推荐加载以下宏包（可根据实际需求增减）：

```tex
% 基础
\usepackage{ctex}        % 中文支持
\usepackage{geometry}    % 页面设置

% 数学
\usepackage{amsmath,amssymb}   % 数学公式

% 图形
\usepackage{graphicx,float,caption,subcaption}

% 表格
\usepackage{booktabs}

% 超链接与引用
\usepackage{hyperref,cleveref}

% 文献管理
\usepackage{biblatex}

% 微排版
\usepackage{microtype}
```

当然，在加载宏包时，需要注意遵循“少而精”原则：只加载必要宏包即可，以避免发生冲突或冗余。例如，在上述推荐中，如果我们事前已经加载了`ctex`宏包，那么`inputenc`、`fontenc`、`lmodern`这几个宏包就无需再加载了。因为使用`ctex`宏包时，我们采用的排版引擎大概率是 XeLaTeX 或 LuaLaTeX，它们已经内置了 UTF-8 编码、T1 字体编码以及 Latin Modern 字体，无需再额外加载。

另外，加载宏包也需要特别注意一下加载的顺序，因为某些宏包之间存在着特定的依赖关系，对加载的顺序是敏感的，例如，我们通常建议先加载数学宏包（`amsmath`、`amssymb`），再加载`hyperref`；而`cleveref`则必须在`hyperref`之后加载。总而言之，读者最好在具体使用之前查阅一下这些宏包的文档，以了解它们之间的依赖关系。

<!-- 以下待整理 -->
### 定义文档的元信息

版式设置直接影响阅读体验。常见设置示例：

```tex
\geometry{
  a4paper,
  left=3cm,
  right=3cm,
  top=3cm,
  bottom=3cm
}
\linespread{1.2}  % 设置行距为1.2倍
```

此设置适用于 A4 纸、左右边距 3 cm、行距适中。若为 US Letter 纸或双栏排版（two‑column），可相应调整。

### 生成文档的标题页

## 组织文档内容

### 分节结构

专业文献通常采用三层或四层标题结构：

- \section{}（一级）
- \subsection{}（二级）
- \subsubsection{}（三级）
- \paragraph{}（可选四级）

  示例：

```tex
\section{引言}
\subsection{研究背景}
\subsubsection{问题陈述}
\paragraph{本文贡献}
```

建议分节时保持每节内容在合理长度（如 300–600 字）范围内，不宜一节过长或过短。

### 目录生成

加载 `\usepackage{hyperref}` 后，可直接使用：

```tex
\tableofcontents
```

生成目录并自动建立书签。若希望目录自动更新页码，建议在文档编译过程中多运行两次。

### 标题样式微调

若需要调整标题样式，可使用 `titlesec` 宏包。例如：

```tex
\usepackage{titlesec}
\titleformat{\section}{\Large\bfseries}{\thesection}{1em}{}
```

将一级标题设置为大号粗体。请注意，一定要保证标题样式与整体排版风格一致，不宜随意混用多种风格。

## 专业内容排版：定理、证明、算法

### 定理环境

专业文献常用“定理–引理–证明–推论”结构，可用 `amsthm` 宏包定义。例如：

```tex
\usepackage{amsthm}
\newtheorem{theorem}{定理}[section]
\newtheorem{lemma}{引理}[section]
\theoremstyle{definition}
\newtheorem{definition}{定义}[section]
```

然后在文中使用：

```tex
\begin{theorem}
假设 …，则 …
\end{theorem}

\begin{proof}
由 … 及 … 可得 …。
\end{proof}
```

务必保持定理编号方式的一致性，推荐 “章节号+定理号”的编号方式（例如 2.1、2.2…）。

### 算法排版

对于算法伪代码，可使用 `algorithm` 或 `algorithm2e` 宏包。例如：

```tex
\usepackage{algorithm}
\usepackage{algpseudocode}

\begin{algorithm}
\caption{快速排序 (QuickSort)}
\begin{algorithmic}[1]
\Procedure{QuickSort}{$A,p,r$}
  \If{$p<r$}
    \State $q \gets \Call{Partition}{A,p,r}$
    \State \Call{QuickSort}{$A,p,q-1$}
    \State \Call{QuickSort}{$A,q+1,r$}
  \EndIf
\EndProcedure
\end{algorithmic}
\end{algorithm}
```

这样，算法将自动编号、格式清晰、带行号，读者阅读更方便。

### 公式与数学环境

虽然你当前可能已熟悉公式编辑技巧，但在专业文档排版中，需要额外注意以下事项：

- 行间公式（使用 `\[ … \]` 或 `\begin{equation}…\end{equation}`）适合重要公式；
- 行内公式（使用 `$…$`）适合文本相关符号；
- 对于多行推导，推荐使用 `amsmath` 提供的 `align` 环境，保持对齐，利于阅读；
- 公式编号应统一使用 `(1)`, `(2)`, … 样式，并在文中引用公式使用 `\eqref{}` 或 `\ref{}`。
  示例：

```tex
\begin{align}
\label{eq:energy}
E &= mc^2 \\
\label{eq:momentum}
p &= mv
\end{align}
```

并在文中写：“如公式 \eqref{eq:energy} 所示，…”
以上方式保证公式清晰、可引用、结构一致。

## 图表、插图与表格排版

### 插图

插图是文献中增强可视化理解的重要元素。建议使用 `graphicx` 宏包，并按如下方式插入：

```tex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.6\textwidth]{figure1.pdf}
  \caption{系统架构示意图}
  \label{fig:architecture}
\end{figure}
```

注意事项：
- `[htbp]` 表示优先放在此处（here）、顶部（top）、底部（bottom）、独立一页（page）；
- 使用 `\label{}` 和 `\ref{}` 联动引用图；
- 图宽度建议为文档宽度的 0.5–0.8 倍，不宜过大或过小；
- 为保证输出质量，推荐使用矢量图（如 PDF、EPS）而非低分辨率 raster 图。

### 表格

表格应清晰、对齐规范。建议使用 `booktabs` 宏包，避免使用粗 \hline 或密集边框。例如：

```tex
\begin{table}[htbp]
  \centering
  \caption{实验结果对比}
  \label{tab:results}
  \begin{tabular}{lcc}
    \toprule
    方法 & 精度 (%) & 召回率 (%) \\
    \midrule
    方法 A & 92.5 & 88.3 \\
    方法 B & 94.1 & 90.2 \\
    \bottomrule
  \end{tabular}
\end{table}
```

注意：

- 列对齐符号（如 `l`、`c`、`r`）应根据内容选择；
- 表格中避免竖线（`|`）分隔，视觉更干净；
- 给 \caption 与 \label 排序如上，确保标签引用正确。

### 引用与浮动体管理

图与表都属于“浮动体”（float），建议将 `\begin{figure}` / `\begin{table}` 放在能表达相关语义的合适位置，并在文本中引用（如“见图 \ref{fig:architecture}”）。加载 `\usepackage{caption}` 或 `\usepackage{subcaption}` 可进一步增强图注或子图处理能力。

---

## 参考文献与引用管理

### 文献管理工具

专业文献中，参考文献往往篇幅较多、格式规范。推荐使用 `\usepackage{biblatex}` 或经典的 `\usepackage{natbib}`。以 biblatex 为例：

```tex
\usepackage[
  backend=biber,
  style=ieee,     % 或 numeric、alphabetic 等
]{biblatex}
\addbibresource{refs.bib}
```

然后在文中用：

```tex
如文献\cite{smith2022deep}所示，…
```

最后在文末：

```tex
\printbibliography
```

### 参考文献格式

根据期刊或出版社的要求，参考文献可能需要按照 IEEE、ACM、APA、GB/T 7714 等格式排列。biblatex 的 style 参数通常能满足；如需定制，可手动修改 .bbx/.cbx 模块。

### 引用规范建议

- 文中引用应简洁明了，如 “Smith 等人在 \cite{smith2022deep} 中提出…”；
- 避免 “作者在其论文中” 而不注明文献编号；
- 多篇引用可用 `\cite{ref1,ref2,ref3}`；
- 保持与正文、表格、图中的引用一致；即使文献量大，也应通过自动化工具统一管理。

---

## 排版优化与版式细节

### 字体与行距

建议选用适于学术排版的字体，如 Latin Modern、Times New Roman 等。加载 `\linespread{1.2}` 或 `\setlength{\baselineskip}{1.2\baselineskip}` 可提升可读性。

### 边距与页眉页脚

为了论文打印与装订，需要考虑边距、页眉页脚设置。例如：

```tex
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhead[L]{}
\fancyhead[C]{}
\fancyhead[R]{\thepage}
\fancyfoot{}
```

若为双面打印，应使用 `twoside` 选项。

### 链接与文档书签

加载 hyperref 后，建议如下设置：

```tex
\hypersetup{
  colorlinks=true,
  linkcolor=blue,
  citecolor=blue,
  urlcolor=blue,
  pdfauthor={你的名字},
  pdftitle={文档标题}
}
```

这样生成的 PDF 在阅读器中可直接跳转目录、图表、参考文献，提高阅读体验。

### 可重用的模板结构

若你经常撰写论文或报告，建议构建一个个人 LaTeX 模板，包含常用宏包、页眉页脚、定理环境、算法环境、图表样式、参考文献设定等。每次写作时只需复制模板，替换标题、作者、内容即可，使撰写流程更高效。

## 常见误区与建议

- **误区一**：导入过多宏包造成冲突。建议先理解每个宏包的作用，按需加载。
- **误区二**：公式、图表未编号或编号混乱。建议坚持统一编号格式，必要时使用 \label + \ref。
- **误区三**：图表位置混乱，影响阅读体验。建议合理使用 [htbp] 参数，并在正文中引用它们。
- **误区四**：参考文献格式不规范且手工编辑。建议使用 biblatex 或 natbib 等工具自动管理。
- **建议**：每完成一节内容，编译一次 PDF，浏览排版效果。早期发现问题比后期大规模修修改容易。

## 结语

通过以上各章内容，我们系统介绍了 LaTeX 在“专业文档排版”中的关键要素：从文档框架与宏包选择、标题结构、定理环境、图表插入、参考文献管理，到排版优化与细节建议。掌握这些技巧，能极大提升你的稿件专业性与排版质量。
接下来，建议你选择一个实际写作项目（如论文、技术报告或学位论文）作为练习对象，逐步应用本文所述方法。与此同时，多查看优秀已发表文献的排版风格，从中吸收灵感与规范。祝你排版顺利、文稿精彩！
