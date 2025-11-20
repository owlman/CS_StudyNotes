# LaTex学习笔记：专业内容排版

## 图表元素应用

### 插图元素

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

### 表格元素

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

## 引用规范建议

- 文中引用应简洁明了，如 “Smith 等人在 \cite{smith2022deep} 中提出…”；
- 避免 “作者在其论文中” 而不注明文献编号；
- 多篇引用可用 `\cite{ref1,ref2,ref3}`；
- 保持与正文、表格、图中的引用一致；即使文献量大，也应通过自动化工具统一管理。


### 标题页与目录
 
```tex
\tableofcontents
```

生成目录并自动建立书签。若希望目录自动更新页码，建议在文档编译过程中多运行两次。

## 排版优化与版式细节

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
