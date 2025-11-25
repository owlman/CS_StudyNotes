# LaTex 学习笔记：学术文档排版

在实际应用中，如果我们仅仅需要完成的是《[[LaTeX学习笔记：文档排版基础]]》中所介绍的那些纯文本排版工作，其实并不一定需要用到 $\LaTeX$ 这样复杂的排版系统。毕竟，$\LaTeX$ 的核心优势主要在于其对数学公式、图表、参考文献等复杂文档元素所提供的高质量与高度一致性的支持。因此，当目标是撰写结构严谨、内容复杂的学术文档时，$\LaTeX$ 往往是最稳健，最专业的选择。

在本篇笔记中，我们将沿用之前的示例文稿（即《$\LaTeX$ 排版示例》）继续为读者演示如何使用 $\LaTeX$ 对这些复杂元素进行排版，以帮助读者系统掌握撰写完整学术文档所需的主要技能。

## 图表元素排版

作为以科普宣传、学术研究为目的的专业文档来说，插图与表格都是不可或缺的元素。它们有助于更为直观地展示数据、分析函数、解释概念等，从而帮助读者更好地理解文档内容。在 $\LaTeX$ 排版系统中，插入这些元素通常都需要加载相应的宏包，并按照特定的语法规则执行这些宏包提供的命令。下面，我们从最简单的插图元素开始介绍吧。

### 插入图片

在撰写学术文档时，我们会经常需要在文中插入一些图形，以便用更直观的形式说明学术理论，并提供相关的数据证明。在 $\LaTeX$ 中，图片元素会被视为“浮动体（float）”，因此在执行插入图片的操作时，我们首先需要定义一个名为`figure`的浮动环境，并在其中使用由`graphicx`宏包提供的`\includegraphics`命令插入图片。例如在之前的《$\LaTeX$ 排版示例》文稿中，如果我们想在“插图元素”这个二级标题下面分别添加一段与勾股定理相关的介绍和一张相应的示意图，就可以像下面这样写：

```tex
% 省略之前的文档结构定义部分
\usepackage{graphicx} % 用于插入图片
% 开始组织文档内容
\begin{document}
    % 省略之前的章节
    \section{图表元素示例}
        \subsection{插图元素}
            勾股定理，是一个基本的几何定理，指直角三角形的两条直角边的平方和等于斜边的平方。中国古代称直角三角形为勾股形，并且直角边中较小者为勾，另一长直角边为股，斜边为弦，所以称这个定理为勾股定理，也有人称商高定理，其几何关系如图\ref{fig:勾股定理示意图}所示。
            \begin{figure}[htbp]
                \centering
                \includegraphics[width=0.6\textwidth]{./img/img.png}
                \caption{勾股定理示意图}
                \label{fig:勾股定理示意图}
            \end{figure}
    % 省略之后的章节
\end{document}
```

在上述示例中，我们在定义`figure`环境时使用`[htbp]`参数设置了插图元素在文档中的排版方式，该参数表示我们建议 $\LaTeX$ 依次尝试将浮动体放在当前位置（`h`）、页面顶部（`t`）、页面底部（`b`）或单独成页（`p`）。换而言之，该浮动体的实际位置是由 $\LaTeX$ 自动决定的，并非是严格指定。如果我们想严格指定浮动体的位置，也可以使用`[H]`、`[T]`、`[B]`或`[P]`参数来定义`figure`环境，它们分别会将该浮动体强制放置在“当前位置”、“页面顶部”、“页面底部”和“单独成页”这四个位置上，但这种做法可能会导致文档排版混乱，因此并不推荐使用。

接下来在该浮动体的定义中，我们除了会使用`\includegraphics`命令指定要插入的图片之外，通常还会使用`\label{}`命令为图片添加标签（以便能在文档中使用`\ref`命令对其进行引用）。使用`\caption{}`命令为图片添加了标题，使用`\centering`命令将图片居中显示（如果要让图片左对齐或右对齐，可以使用`\raggedleft`或`\raggedright`命令）。现在，如果我们再次编译这个文档，就可以看到“插图元素”这个二级标题下面已经出现了这个勾股定理的示意图，如图 1 所示：

![图1：勾股定理示意图](./img/Pythagorean_Theorem.png)

### 绘制表格

除了插图元素之外，表格也是学术文档中经常会出现的元素。我们经常使用它来罗列一些统计性的、汇总性的数据，以便对要说明的学术理论进行进一步的论证。在 $\LaTeX$ 中，表格元素可以通过定义一个名为`table`的环境来实现。例如在之前的《$\LaTeX$ 排版示例》文稿中，如果我们想在“表格元素”这个二级标题下面以表格的形式列出勾股定理的所有公式，就可以像下面这样写：

```tex
% 省略之前的文档结构定义部分
\usepackage{amsmath} % 用于插入数学公式
% 开始组织文档内容
\begin{document}
    % 省略之前的章节
    \section{图表元素示例}
        % 省略之前的插图元素
        \subsection{表格元素}
            勾股定理的公式有多种不同的表达形式，下面的表格\ref{tab:pythagorean_formulas}总结了一些常见的勾股定理公式。
            \begin{table}[htbp]
                \centering  % 表格居中
                \caption{勾股定理公式汇总} % 表格标题
                \label{tab:pythagorean_formulas} % 表格标签
                \resizebox{0.7\textwidth}{!}{ % 调整表格大小以适应页面宽度
                    % 设置表格的每列都采用左对齐
                    \begin{tabular}{|l|l|}
                        \hline   % 表格行间线
                        \textbf{公式名称} & \textbf{数学表达式} \\
                        \hline   % 表格行间线
                        标准形式 & \( a^2 + b^2 = c^2 \) \\
                        \hline   % 表格行间线
                        求斜边 \(c\) & \( c = \sqrt{a^2 + b^2} \) \\
                        \hline  % 表格行间线
                        求直角边 \(a\) & \( a = \sqrt{c^2 - b^2} \) \\
                        \hline  % 表格行间线
                        求直角边 \(b\) & \( b = \sqrt{c^2 - a^2} \) \\
                        \hline  % 表格行间线
                        三角函数形式（正弦与余弦） & \( \sin^2(\theta) + \cos^2(\theta) = 1 \) \\
                        \hline  % 表格行间线
                        向量形式（二维空间） & \( \|\mathbf{v}\|^2 = v_x^2 + v_y^2 \) \\
                        \hline  % 表格行间线   
                    \end{tabular}
                }
            \end{table}
    % 省略之后的章节
\end{document}
```


注意：

- 列对齐符号（如 `l`、`c`、`r`）应根据内容选择；
- 表格中避免竖线（`|`）分隔，视觉更干净；
- 给 \caption 与 \label 排序如上，确保标签引用正确。

图与表都属于“浮动体”（float），建议将 `\begin{figure}` / `\begin{table}` 放在能表达相关语义的合适位置，并在文本中引用（如“见图 \ref{fig:architecture}”）。加载 `\usepackage{caption}` 或 `\usepackage{subcaption}` 可进一步增强图注或子图处理能力。

## 专用环境元素

### 定理证明

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

### 数学公式

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

### 算法描述

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

### 代码高亮

## 参考文献管理

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

## 使用排版模板

若你经常撰写论文或报告，建议构建一个个人 LaTeX 模板，包含常用宏包、页眉页脚、定理环境、算法环境、图表样式、参考文献设定等。每次写作时只需复制模板，替换标题、作者、内容即可，使撰写流程更高效。

## 笔记小节
