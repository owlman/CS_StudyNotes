---
title: Transformer 架构详解
author: 凌杰
date: 2026-09-28
tags:
  - 人工智能
  - 深度神经网络
  - Transformer
categories: 基础技术研究
---

> [!NOTE] 笔记说明
>
> 这篇笔记对应的是《[[关于 AI 的学习路线图]]》一文中所规划的第二个学习阶段。与上一篇《[[深度学习的训练与评估]]》的视角不同，那一篇讨论的是训练侧——损失函数、优化器、训练动力学；这一篇要讨论的是架构侧——以 Transformer 为代表，深度神经网络到底是用什么样的结构来处理序列数据的。同样的，这些内容也将成为我 AI 系列笔记的一部分，被存储在本人 Github 上的[计算机学习笔记库](https://github.com/owlman/CS_StudyNotes)中，并予以长期维护。

在《[[深度学习的训练与评估]]》那篇笔记中，我们已经了解到：神经网络的训练本质上是在参数空间 $\Theta$ 中寻找一组参数 $\theta^*$，使得 $f_{\theta^*}$ 能够在给定数据分布上足够接近目标函数 $f^*$。但这里有一个我们刻意回避的问题——**架构**。一个神经网络究竟应该长成什么样子，才能高效地完成它需要完成的映射任务？这一篇笔记就要来回答这个问题。

准确地说，我们要回答的核心问题是：**现代主流大语言模型（LLM）背后的那套基础架构到底是什么、它为什么有效、各组件又分别承担了什么责任**。该架构就是 2017 年由 Vaswani 等人在论文《[Attention Is All You Need](https://arxiv.org/abs/1706.03762)》中提出的 **Transformer**。理解 Transformer，是理解现代 LLM 一切行为的前提——无论是 GPT、LLaMA、Claude 还是 Gemini，其底层都是 Transformer（或其变体）。换言之，**如果说《深度学习》是 AI 时代的"花书"，那 Transformer 就是 LLM 时代同样不可绕开的那一章**——不读它就读不懂之后任何关于现代 LLM 的演进。

下面我以表 1 给出本笔记要讨论的主题。

| 主题 | 要讨论的内容 |
|------|--------------|
| 序列建模的历史困境 | RNN/LSTM 在处理长序列时遇到了什么问题。 |
| 自注意力的直觉 | 从循环聚合到全连接加权聚合的思路转变。 |
| Scaled Dot-Product Attention | 注意力机制的数学形式化定义。 |
| Multi-Head Attention | 多头注意力如何让模型在不同子空间并行观察。 |
| 位置编码 | 没有位置编码就没有顺序感。 |
| 整体架构 | Encoder、Decoder、残差连接与层归一化的协作。 |
| 典型变体 | BERT、GPT、T5 等变体是如何从同一架构分化出来的。 |
| 与现代 LLM 的关系 | Decoder-only Transformer 为何成为 LLM 的事实标准。 |

**表 1** 本笔记要讨论的主题及其内容

需要首先说明的是，本笔记**不打算**详细讨论 Transformer 的数学训练细节（这部分由《[[深度学习的训练与评估]]》承担），也**不打算**逐个比较不同的注意力变体（Flash Attention、Linear Attention、MoE 等会在后续笔记中介绍）。这篇笔记只解决一个问题：**把原始 Transformer 的工作原理讲清楚**。换言之，我们关心的是"为什么是这个结构"，而不是"如何训练它"或"如何高效实现它"。

## 序列建模的历史困境

在 Transformer 出现之前，主流的序列建模工具是**循环神经网络（RNN）**及其改进版**长短时记忆网络（LSTM）**。它们的核心思路非常直觉：**让信息沿时间步依次传递，每一步都对历史做一次总结**。这种"循环"结构天然契合"序列"的定义——第 $t$ 个时间步的输出依赖于前 $t-1$ 步的信息。但正是这种看似自然的结构，带来了三个根本性的工程瓶颈。

### 长距离依赖丢失

RNN 在第 $t$ 步计算隐藏状态 $h_t$ 时，会基于上一步的 $h_{t-1}$ 进行递归更新：

$$
h_t = f(W_h \cdot h_{t-1} + W_x \cdot x_t + b)
$$

这意味着第 1 个时间步的信息需要经过 $t-1$ 次矩阵乘法与激活函数的"挤压"才能传递到第 $t$ 步。当序列长度较大时，**早期信息会在反复的乘法与激活中被反复衰减或放大**——梯度消失与梯度爆炸正是这一过程的两个极端表现。LSTM 通过引入"门控机制"（输入门、遗忘门、输出门）部分缓解了这一问题，但仍未能从根本上解决"信息必须沿路径传播"的本质约束。

### 串行计算无法并行

RNN 的循环结构要求**第 $t$ 步必须等第 $t-1$ 步计算完成**。这意味着无论 GPU 多么强大，单个序列内的时间步无法被并行处理。当训练数据从几百个词扩展到几万个词时，训练时间会随序列长度线性增长。这一约束使得 RNN/LSTM 在大规模预训练场景下很快失去竞争力。

### 注意力机制的早期尝试

在 Transformer 之前，已经有工作尝试将"注意力"引入 RNN。例如 Bahdanau Attention（2014）允许解码器在生成每个词时回看编码器的所有隐藏状态，从而**绕过固定长度向量**的瓶颈。但这种"注意力 + RNN"的混合结构仍然受制于 RNN 本身，无法彻底摆脱串行约束。

Transformer 的革命性在于：**它把循环结构彻底删掉了**，转而用一种名为"自注意力（Self-Attention）"的机制直接建立序列中任意两个位置之间的连接。下面，我们就要来理解这一替换的数学直觉。

## 自注意力的直觉

自注意力的核心思想可以一句话概括：**序列中的每个位置，都应该能够直接访问序列中所有其他位置的信息，而不需要通过中间状态"接力"传递**。

为了直观地理解这一点，我们可以做一个思想实验。假设我们有一个长度为 $n$ 的序列 $[x_1, x_2, \dots, x_n]$，我们希望为其中任意一个位置 $x_i$ 生成一个"上下文表示" $z_i$。在 RNN 中，$z_i$ 是通过逐步累积 $h_1 \to h_2 \to \dots \to h_i$ 得到的"压缩摘要"。这种压缩是有损的——早期信息越传越模糊。

而自注意力允许我们跳过这种"接力"，直接计算 $z_i$：

$$
z_i = \sum_{j=1}^{n} \alpha_{ij} \cdot x_j
$$

其中 $\alpha_{ij}$ 是一个**权重系数**，表示位置 $j$ 对位置 $i$ 的重要性。这里的关键设计是：**所有位置都共享同一组 $x_j$**，但每个位置 $i$ 都根据自己的上下文独立地决定如何加权聚合它们。换言之，自注意力把"信息聚合"的方式从"沿时间步递归"换成了"按权重一次性加权"。

这种替换带来了三个直接好处：

1. **长距离依赖不再衰减**：因为第 1 个位置可以直接"看到"第 $n$ 个位置，中间没有任何乘法挤压。
2. **位置间计算可并行**：所有 $z_i$ 可以同时计算，不存在串行依赖。
3. **可解释性更强**：权重 $\alpha_{ij}$ 本身就是"位置 $j$ 对位置 $i$ 有多重要"的量化指标，可以可视化分析。

当然，自注意力也带来一个问题：**序列的顺序信息消失了**。因为上面的公式对所有 $j$ 是一视同仁的，$x_1$ 和 $x_n$ 在公式里没有区别。我们稍后会用"位置编码"解决这一问题。

## Scaled Dot-Product Attention

在理解了自注意力的直觉之后，我们来看它在 Transformer 中的精确数学形式。这就是论文《Attention Is All You Need》中提出的 **Scaled Dot-Product Attention**：

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right) V
$$

这里的 $Q$、$K$、$V$ 三个矩阵分别是**查询（Query）**、**键（Key）**和**值（Value）**。它们都是从同一组输入 $X$ 经过三个不同的可学习线性变换得到的：

$$
Q = X W^Q,\quad K = X W^K,\quad V = X W^V
$$

其中 $W^Q$、$W^K$、$W^V$ 是模型需要学习的参数矩阵，$d_k$ 是 $Q$、$K$ 矩阵的列维度（即"键向量"的维度）。

下面我们逐步拆解这个公式的语义。

### 第一步：相似度计算 $QK^\top$

$QK^\top$ 的第 $i$ 行第 $j$ 列元素 $\langle q_i, k_j \rangle$ 表示"位置 $i$ 的查询向量"与"位置 $j$ 的键向量"之间的点积相似度。这一步相当于**让每个位置向所有位置发出查询，并接收所有位置返回的相关性分数**。

直觉上可以理解为：在图书馆找书时，你写下你的需求（$q_i$），然后和图书馆所有书的索引标签（$k_j$）一一比对，看哪本书最相关。

### 第二步：缩放 $\frac{1}{\sqrt{d_k}}$

直接用 $QK^\top$ 作为 softmax 的输入会出现一个问题：当 $d_k$ 较大时，点积的方差会随 $d_k$ 线性增长，导致 softmax 的输入值进入极端区间，**梯度变得极小**。除以 $\sqrt{d_k}$ 这一缩放操作正是为了控制点积的方差，使其无论 $d_k$ 多大都保持稳定的分布。这是 Transformer 训练稳定性的关键工程细节之一，**并非可省略的修饰**。

### 第三步：归一化 $\text{softmax}$

对每一行（即每个查询位置）做 softmax，将相似度分数转换为**权重分布** $\alpha_{ij}$，满足 $\sum_j \alpha_{ij} = 1$。这一步等价于"把相似度分数解释为概率：位置 $i$ 应该把多大比例的注意力分配给位置 $j$"。

### 第四步：加权求和 $V$

最后用得到的权重对值矩阵 $V$ 做加权求和，得到每个位置的输出表示。整个过程可以理解为：**根据相关性分布，把所有位置的信息重新组织一次**。

至此，我们就完成了自注意力的完整计算。值得强调的是，自注意力的所有计算步骤都是**对序列内所有位置同时进行的**——这就是它能够高效利用 GPU 并行性的原因。

## Multi-Head Attention

单个 Scaled Dot-Product Attention 输出的表示空间是单一的——所有位置都共享同一组 $W^Q$、$W^K$、$W^V$。这会带来一个限制：模型被迫在同一个表示空间里表达所有类型的"相关性"。

为了突破这一限制，Transformer 引入了**多头注意力（Multi-Head Attention）**：

$$
\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \dots, \text{head}_h) W^O
$$

$$
\text{head}_i = \text{Attention}(Q W_i^Q, K W_i^K, V W_i^V)
$$

其中 $h$ 是头数（原始论文中 $h = 8$），$W_i^Q$、$W_i^K$、$W_i^V$ 是每个头**独立**的参数矩阵，$W^O$ 是最终的输出投影矩阵。

### 多头的语义

直觉上，多头机制允许模型在**多个不同的表示子空间**中并行地观察序列中的相关性。例如：

- 某个头可能专门关注"句法依赖"（主谓关系、修饰关系）；
- 某个头可能专门关注"共指关系"（代词指向哪个名词）；
- 某个头可能专门关注"局部上下文"（相邻词之间的搭配）。

这种分工并不需要人为指定，而是通过训练自然涌现的。这也是为什么后续的 interpretability 研究（如 BERTology）能够从训练好的 Transformer 中识别出"功能专一化"的头。

### 计算代价的不变性

值得注意的是，多头机制**没有增加总计算量**。单个头的注意力计算复杂度为 $O(n^2 d_k)$（其中 $n$ 为序列长度，$d_k = d/h$ 为单头的键向量维度，$d$ 为模型维度），而 $h$ 个头的计算复杂度总和为 $O(h \cdot n^2 d_k) = O(n^2 d)$——每个头的维度被相应缩小为 $d/h$，总计算量守恒。这是一种"以结构换表达力"的设计选择。

## 位置编码

我们前面提到，自注意力机制有一个先天缺陷：**它对序列中的所有位置一视同仁**。具体来说，无论输入是 $[x_1, x_2, x_3]$ 还是 $[x_3, x_1, x_2]$，自注意力输出的都是同一个集合，只是顺序会随输入的置换而置换（即所谓**置换等变性，permutation equivariance**）——这意味着模型本身不携带任何顺序信息。这显然不符合我们对"语言"的直觉——"猫吃鱼"和"鱼吃猫"的语义截然不同。

为了给模型注入**顺序信息**，Transformer 引入了**位置编码（Positional Encoding）**。其核心思想是：**在输入嵌入中加上一个与位置相关的向量**，使每个位置在进入注意力层之前就携带"我是第几位"的信号。

### 固定位置编码（原始 Transformer）

原始论文采用的是基于正弦和余弦函数的固定位置编码：

$$
PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d}}\right)
$$

$$
PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d}}\right)
$$

其中 $pos$ 是位置索引，$i$ 是维度索引，$d$ 是嵌入维度。这种设计的两个核心优势是：

1. **从原理上可外推到训练时未见过更长的序列**（论文原文表述为 *we hypothesized that this would allow the model to extrapolate*）：因为正弦函数是连续的，模型在理论上可以平滑地处理比训练序列更长的位置；但学界普遍观察到，这种外推能力在实际训练中相当有限。
2. **不同位置之间有可学习的相对关系**：通过三角恒等式，$PE_{pos+k}$ 可以表示为 $PE_{pos}$ 的线性函数。

### 可学习位置编码

另一种主流方案是直接把位置编码视为可学习的参数矩阵，每个位置对应一个可训练的向量（如 BERT 至今仍在使用的可学习绝对位置编码）。这种方案简单直接，但**无法外推到训练时未见过更长的序列**。后来的 RoPE、ALiBi 等旋转式 / 线性偏置位置编码则尝试兼顾两种方案的优点——它们已经成为现代 LLM（LLaMA、Qwen 等）的事实标准。这一演进留待后续笔记讨论。

## 整体架构

把前面讨论的所有组件拼起来，我们就得到了原始 Transformer 的完整架构。它由 **Encoder** 和 **Decoder** 两部分组成，每部分各包含若干个相同的"块（Block）"。

### Encoder Block

每个 Encoder Block 由两个子层组成：

1. **Multi-Head Self-Attention 子层**：输入是上一层输出 $X$，经过多头自注意力后再经过残差连接与层归一化，得到 $X' = \text{LayerNorm}(X + \text{MultiHead}(X))$。
2. **Feed-Forward Network（FFN）子层**：对每个位置独立地施加一个两层的全连接网络，再经过残差连接与层归一化，得到 $X'' = \text{LayerNorm}(X' + \text{FFN}(X'))$。

其中 FFN 通常实现为：

$$
\text{FFN}(x) = \max(0, x W_1 + b_1) W_2 + b_2
$$

即一个"扩展-压缩"的两层感知机，隐藏维度通常是模型维度的 4 倍。

### Decoder Block

每个 Decoder Block 由三个子层组成，比 Encoder 多一个：

1. **Masked Multi-Head Self-Attention**：在自注意力的相似度矩阵上施加一个**下三角掩码**，使位置 $i$ 只能看到 $\leq i$ 的位置。这是为了让 Decoder 在生成任务中保持"自回归"特性——生成第 $t$ 个词时不能偷看第 $t+1$ 个之后的词。
2. **Cross-Attention（Encoder-Decoder Attention）**：Query 来自 Decoder 上一层的输出，而 Key 和 Value 来自 Encoder 的最终输出。这一步让 Decoder 在生成每个词时能够"参考"输入序列的完整表示。
3. **Feed-Forward Network**：与 Encoder Block 中的 FFN 结构相同。

### 残差连接与层归一化的意义

残差连接（$X + \text{Sublayer}(X)$）与层归一化（LayerNorm）的组合并非 Transformer 的发明，但 Transformer 是第一个把它们作为"标配"应用到如此深网络结构上的架构之一。它们的作用是：

- **缓解深层网络的梯度消失**：残差连接提供了从输入到输出的"直连通路"，使梯度可以无损地反向传播。
- **稳定训练过程**：层归一化对每个样本的特征维度做归一化，使各层的输入分布保持稳定，从而允许更大的学习率。

没有这两个机制，今天动辄几十层、上百层的 Transformer 根本无法稳定训练。

## 典型变体

原始 Transformer 是一个 Encoder-Decoder 的对称结构，主要面向机器翻译这类"输入-输出"任务。但实际工程中，更常见的做法是根据任务需求**只取 Encoder 或 Decoder 的一部分**。这种分化催生了现代 NLP 的三大主流架构。

### BERT：Encoder-only

2018 年 Google 提出的 BERT 只使用了 Transformer 的 Encoder 部分，并在预训练阶段引入了两个自监督任务——**掩码语言模型（Masked Language Modeling, MLM）**和**下一句预测（Next Sentence Prediction, NSP）**。MLM 让模型学会"双向"理解上下文（既能看上文也能看下文），但代价是无法直接用于文本生成。BERT 架构特别适合需要"理解"的场景——文本分类、问答、命名实体识别、检索排序等。

### GPT：Decoder-only

2018 年 OpenAI 提出的 GPT 只使用了 Transformer 的 Decoder 部分，并通过**自回归语言模型**作为预训练目标——即给定前文预测下一个词。这种架构天然适合文本生成，且通过规模化（参数量、数据量、计算量）展现了强大的"涌现能力"。从 GPT-2 到 GPT-3 再到 GPT-4，从 LLaMA 到 Claude 再到 Gemini，几乎所有现代 LLM 都基于 Decoder-only 架构。

### T5：Encoder-Decoder

2019 年 Google 提出的 T5 保留了完整的 Encoder-Decoder 结构，并把所有 NLP 任务统一为"文本到文本"的转换问题（即使分类任务也输出"类别名"作为文本）。这种架构在翻译、摘要等"输入-输出"对齐任务上仍有竞争力，但在通用对话场景下不如 Decoder-only 流行。

### 选型直觉

可以粗略地总结：

- **需要理解语义、不需要生成文本** → Encoder-only（如 BERT）；
- **需要生成文本** → Decoder-only（如 GPT、LLaMA）；
- **需要严格的对齐与改写** → Encoder-Decoder（如 T5、原始翻译系统）。

## 与现代 LLM 的关系

理解了原始 Transformer 之后，我们就可以看清现代 LLM 的本质：**它们基本上都是 Decoder-only Transformer 的规模化与工程优化版本**。规模化体现在参数量从亿级跃升到千亿乃至万亿级，训练数据从 GB 级跃升到 TB 级。工程优化体现在引入了 RoPE、SwiGLU、GQA、Flash Attention 等一系列改进，使得大模型在长上下文推理、低显存训练、高吞吐推理等场景下变得可行。

但**所有这些演进都没有改变 Decoder-only Transformer 的核心骨架**——自注意力 + 前馈网络 + 残差归一化 + 自回归语言模型。这意味着，掌握了原始 Transformer 的工作原理，就具备了阅读后续所有 LLM 相关文献的"地基"。

## 结束语

回到学习路线图的坐标系中，这篇笔记承担的是**架构视角**的入门任务。在《[[深度学习的训练与评估]]》中，我们了解了"训练侧"——如何把数据转换为参数；而本篇则补充了"架构侧"——Transformer 这个特定架构是如何组织参数、又是如何处理序列数据的。两篇合在一起，就构成了理解现代 LLM 的最小知识单元。

接下来，按照路线图的规划，第三阶段的笔记（如《[[LLM 的部署与测试]]》《[[LLM 的微调实验]]》）会把视角从"架构 + 训练"切换到"系统 + 角色"——观察 LLM 在 AI 系统中是如何被集成的、在不同约束下又会表现出什么样的边界。这是更偏向工程实践的内容，需要建立在架构理解之上——这正是我们花两篇笔记打地基的原因。

## 参考资料

- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). *Attention Is All You Need*. NeurIPS 2017 / arXiv:1706.03762. <https://arxiv.org/abs/1706.03762>
- Bahdanau, D., Cho, K., & Bengio, Y. (2015). *Neural Machine Translation by Jointly Learning to Align and Translate*. ICLR 2015 / arXiv:1409.0473. <https://arxiv.org/abs/1409.0473>
- Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2019). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. NAACL 2019 / arXiv:1810.04805. <https://arxiv.org/abs/1810.04805>
- Radford, A., Narasimhan, K., Salimans, T., & Sutskever, I. (2018). *Improving Language Understanding by Generative Pre-Training*. OpenAI Technical Report. <https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf>
- Raffel, C., Shazeer, N., Roberts, A., Lee, K., Narang, S., Matena, M., Zhou, Y., Li, W., & Liu, P. J. (2020). *Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer*. JMLR 21(140). <https://jmlr.org/papers/v21/20-074.html>
