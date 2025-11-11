# LaTeX 学习笔记：专业文档排版

在撰写学术论文、技术报告或专业著作时，排版的质量往往决定了作品给人的第一印象。对于计算机科学、工程技术、数理化等领域而言，文档中不仅包含大量数学公式，还常常涉及图表、参考文献等复杂结构。正如我们在《[[LaTeX学习笔记：开场白与索引]]》一文中所提到的那样，计算机科学家们正是为了应对这些复杂的排版需求而开发了 $\LaTeX$。

在本篇笔记中，我们将重点介绍 $\LaTeX$ 在专业排版中的使用技巧，帮助你提升学术文档的可读性与专业气质。下面，就让我们先从文档结构的定义开始吧。

## 文档的结构定义

在 $\LaTeX$ 中，文档的整体结构是通过一系列**结构性命令**（structural commands）来定义的。这些命令用于指定文档的基本类型、加载所需的宏包、设置标题信息，并生成文档的开篇部分。最常用的命令包括：

- `\documentclass`：用于指定文档所属的基本类型；
- `\usepackage`：用于通过加载宏包的方式来获得扩展功能；
- `\title`、`\author`、`\date`：用于定义文档的基本元信息；
- `\maketitle`：用于在正文中生成标题页。

接下来，我将会按照功能逐一介绍这些命令的使用方法。

### 定义文档的基本类型

在 $\LaTeX$ 中，文档类型决定的是文档的基本排版结构，例如，是单栏排版还是双栏排版，是书籍还是文章。较为常见的文档类型包括：

- `article`：用于撰写短篇文章，如论文、报告等；
- `report`：用于撰写较长的报告，如毕业论文、技术文档等；
- `book`：用于撰写书籍；
- `letter`：用于撰写信件。
- `ctexart`：用于中文的`article`类型扩展；
- `ctexrep`：用于中文的`report`类型扩展；
- `ctexbook`：用于中文的`book`类型扩展。
- `ctexletter`：用于中文的`letter`类型扩展。

这些文档类型通常需要使用`\documentclass`命令在文档的开头进行指定。例如，如果我们想要创建一篇支持中文的短篇文章，可以使用以下命令：

```tex
\documentclass{ctexart}
```

当然，该命令除了指定文档的类型之外，还可以通过一些选项参数来指定文档的格式。例如，我们可以使用以下命令来创建一篇单面打印、12号字体的短篇文章：

```tex
\documentclass[12pt,oneside]{ctexart}
```

在上述命令的中括号里，`12pt`表示字体大小为12号，`oneside`表示单面打印。

## 加载所需的宏包

为了达到专业排版效果，推荐加载以下宏包（可根据实际需求增减）：

```tex
\usepackage[utf8]{inputenc}     % 设定源文件编码
\usepackage[T1]{fontenc}        % 使用 T1 字体编码
\usepackage{lmodern}            % 使用 Latin Modern 字体
\usepackage{geometry}           % 设置页面尺寸与边距
\usepackage{amsmath,amssymb}    % 数学公式支持
\usepackage{graphicx}           % 插入图形支持
\usepackage{booktabs}           % 专业表格线支持
\usepackage{hyperref}           % 超链接支持（目录、引用、书签）
\usepackage{cleveref}           % 智能引用宏包
\usepackage{biblatex}           % 参考文献管理（可选）
```

在加载宏包时，建议遵循“少而精”原则：只加载必要宏包，避免发生冲突或冗余。

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

## 标题、目录与分节结构

### 分节结构

专业文献通常采用三层或四层标题结构：

* \section{}（一级）
* \subsection{}（二级）
* \subsubsection{}（三级）
* \paragraph{}（可选四级）
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

* 行间公式（使用 `\[ … \]` 或 `\begin{equation}…\end{equation}`）适合重要公式；
* 行内公式（使用 `$…$`）适合文本相关符号；
* 对于多行推导，推荐使用 `amsmath` 提供的 `align` 环境，保持对齐，利于阅读；
* 公式编号应统一使用 `(1)`, `(2)`, … 样式，并在文中引用公式使用 `\eqref{}` 或 `\ref{}`。
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

* 列对齐符号（如 `l`、`c`、`r`）应根据内容选择；
* 表格中避免竖线（`|`）分隔，视觉更干净；
* 给 \caption 与 \label 排序如上，确保标签引用正确。

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

* 文中引用应简洁明了，如 “Smith 等人在 \cite{smith2022deep} 中提出…”；
* 避免 “作者在其论文中” 而不注明文献编号；
* 多篇引用可用 `\cite{ref1,ref2,ref3}`；
* 保持与正文、表格、图中的引用一致；即使文献量大，也应通过自动化工具统一管理。

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

* **误区一**：导入过多宏包造成冲突。建议先理解每个宏包的作用，按需加载。
* **误区二**：公式、图表未编号或编号混乱。建议坚持统一编号格式，必要时使用 \label + \ref。
* **误区三**：图表位置混乱，影响阅读体验。建议合理使用 [htbp] 参数，并在正文中引用它们。
* **误区四**：参考文献格式不规范且手工编辑。建议使用 biblatex 或 natbib 等工具自动管理。
* **建议**：每完成一节内容，编译一次 PDF，浏览排版效果。早期发现问题比后期大规模修修改容易。

## 结语

通过以上各章内容，我们系统介绍了 LaTeX 在“专业文档排版”中的关键要素：从文档框架与宏包选择、标题结构、定理环境、图表插入、参考文献管理，到排版优化与细节建议。掌握这些技巧，能极大提升你的稿件专业性与排版质量。
接下来，建议你选择一个实际写作项目（如论文、技术报告或学位论文）作为练习对象，逐步应用本文所述方法。与此同时，多查看优秀已发表文献的排版风格，从中吸收灵感与规范。祝你排版顺利、文稿精彩！
