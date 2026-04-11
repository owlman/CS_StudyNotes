---
title: Agent 的记忆机制
author: 凌杰
date: 2026-03-11
tags: RAG 长上下文窗口
categories: 软件配置与使用
---

> [!NOTE] 笔记说明
>
> 这篇笔记是《[[Agent 的能力体系]]》一文的后续。其中记录了我学习如何为 Agent 应用构建记忆机制（包括 RAG 架构、长上下文窗口），并将其运用于实际工作场景的实践经验与心得体会。同样的，这些内容也将作为我 AI 系列笔记的一部分，被存储在本人 Github 上的[计算机学习笔记库](https://github.com/owlman/CS_StudyNotes)中，并予以长期维护。

## Agent 应用的记忆机制

由于，人工智能这项技术归根结底是机器对于人类智能的一种模拟，而人类智能大致上可以分为处理问题的“技能”和储存信息的“记忆”两部分，之前在[[Agent 的能力体系]]一文中所讨论的基本上是 Agent 应用对于人类技能的模拟。所以接下来，让我们继续来看看 Agent 应用对于人类记忆的模拟。

### 基于 RAG 架构的记忆机制

和能力体系一样，Agent 的记忆机制也是一个基于分层结构来实现的**工程系统**，其目前最典型的实现方式是一个被称为 RAG 架构的三层结构设计，具体如图 1 所示。

![基于 RAG 架构的 Agent 记忆机制](./img/rag_architecture.png)

**图 1** 基于 RAG 架构的 Agent 记忆机制

下面，让我们从系统概念的层面来为读者具体介绍一下这三层结构中所涉及的技术。

- **上下文窗口（Context Window）**：这是 Agent 应用的记忆机制中最基础的一层，负责的是 Agent 应用的短期记忆。它的作用是保存 Agent 应用在当前窗口中的对话记录，确保该应用能够“记得”用户刚刚说了什么（因而在专业术语中，它被称为“上下文窗口”）。很显然，该窗口的容量是相当有限的，当其中的对话记录过长时，它可能就会被 Agent 应用截断或遗忘，这就会在某种程度上严重影响应用的用户体验，从而使其无法真正参与到实际生产环境中去。

- **检索增强生成（Retrieval-Augmented Generation，以下简称 RAG）**：为了解决上下文窗口容量有限、LLM 的知识过时以及它无法访问用户的私有数据等问题，AI 的研究者们引入了 RAG 技术。它的工作机制是：先将用户的查询语句转化为用向量表示的文本切片，然后在向量数据库中检索与之最相关的若干文本切片，并将这些检索结果与用户输入拼接为上下文一并输入到 LLM 中，以此来生成最终响应。在这里需要提醒读者的是，RAG 的本质是一种信息查询技术，它不是一个会主动记住信息的记忆系统，而只是一套记忆访问机制。
  
  换言之，RAG 技术使得 Agent 应用可以在处理用户查询时，动态地引入来自外部的知识，这些知识既可以来自存储在本地的向量数据库，也可以是通过搜索引擎获得的信息。这也很好地解释了一个问题：为什么尽管 LLM 的预训练知识库在时间上普遍存在滞后，但 Agent 应用仍可用它们来处理当前的最新信息。

- **持久化存储（Persistent Storage）**：这是 Agent 应用中真正用于实现长期记忆的核心层，负责的是持久化地存储与历史对话、用户偏好以及任务经验，属于真正的“记忆”。它的具体实现方式有很多种，例如向量数据库（如 LanceDB / FAISS / Milvus）、键值存储（Key-Value Store）以及日志系统（Logging System）等。

从上述每一层结构所展现的技术特性，读者应该可以大致判断出，基于 RAG 架构的 Agent 记忆机制通常会具备以下四大特征：

1. **并行检索**：用户的提问会同时激活这三层记忆结构，它并非串行流程；
2. **独立存储**：每层记忆结构是独立维护和优化的，它们互不影响；
3. **智能融合**：Context Fusion 层动态调配权重（如客服场景中期记忆权重高）；
4. **统一输出**：融合后的上下文一次性输入 LLM，保证回答一致性；

需要特别指出的是，RAG 架构并非是由单一技术或组件构成的，其中的向量数据库与 RAG 技术之间存在着配套关系。尤其对于中长期记忆的实现来说，没有向量数据库提供可持久化的存储，RAG 就无法工作；而没有 RAG 技术的支持，向量数据库中存储的信息也没有什么价值。理解这一点是非常关键的，不然在后续的学习中很容易出现理解的碎片化，这不利于我们在生产环境对 Agent 应用的实际操作。

### 基于长上下文窗口的混合记忆

尽管目前主要的 Agent 应用还都是基于 RAG 架构来构建记忆机制的，但考虑到这种架构的实现严重依赖于向量数据库和嵌入式模型，并且它的每次检索通常都是基于预先构建的向量索引进行相似度匹配，这本质上是一种“局部语义检索”，并不利于进行一些跨文档的全局关联分析。为了缓解这个问题，越来越多的 LLM 提供商都在尝试扩大自己的上下文窗口（在 2025 到 2026 年间，市面上主要 LLM 的上下文窗口大小如表 1 所示），以便 Agent 应用在部分场景下可以通过长上下文直接处理大规模输入，同时结合 RAG 机制对关键信息进行筛选与补充。

**表 1** 2025–2026 年主要 LLM 的上下文窗口大小

| 模型                 | 最大容量（tokens） | 备注说明                           |
| -------------------- | ------------------ | ---------------------------------- |
| GPT-4o / GPT-4.1     | 128K – 1M          | 不同版本差异较大（API 可扩展）     |
| Claude 3 / 3.5 / 3.7 | 200K               | 长上下文能力稳定，擅长文档处理     |
| Gemini 1.5 / 2.0     | 1M – 2M            | 当前上下文窗口最大的商业模型       |
| Kimi（Moonshot）     | 200K – 2M          | 主打超长上下文                     |
| MiniMax（abab系列）  | 128K – 1M          | 支持长上下文，多模态能力逐步增强   |
| Qwen（通义千问）     | 32K – 1M           | 新版本支持超长上下文               |
| LLaMA 3（开源）      | 8K – 128K          | 依赖具体部署与扩展方案             |
| Mistral / Mixtral    | 32K – 128K         | 轻量模型，适合本地或成本敏感场景   |

当然，长上下文窗口也存在着不可忽视的问题，例如它对计算资源的需求会显著增加，并且它对 LLM 的注意力分配能力提出了更高的要求。所以在具体实践中，我们还需要通过合理的上下文组织方式（如分段结构、显式提示、层级摘要等）来提升 LLM 在长上下文中的信息利用效率。

目前在关于长上下文窗口方面的实践，最为典型的就是由 Andrej Karpathy 于 2026 年 4 月 3 日在 X 平台分享的 LLM 知识库方法论了，这套方法论主张先让 LLM 将我们日常所收集到的博客、论文、代码、图片等资料“预编译”成结构化的 Wiki，让其成为可被 LLM 的长上下文窗口直接处理的语料，以便减少实时检索带来的不确定性（其工作流程如图 2 所示，更详细的介绍可阅读这篇笔记的“参考资料”部分列出的博客文章）。换言之，我们现在可以将某一特定领域的知识进行持续的增量编译并将结果保存在本地，然后让 Agent 应用在需要时加载这个预编译的结果，并利用长上下文窗口的特性来提升 LLM 的推理效果。

![Andrej Karpathy的LLM知识库工作流](./img/karpathy-workflow-diagram.png)

**图 2**：Andrej Karpathy 的 LLM 知识库工作流

需要再次强调的是，从工程角度来看，长上下文窗口与 RAG 并不是相互替代的关系，它们是两种相辅相成的不同“记忆访问策略”：前者通过扩大上下文窗口的容量来提升信息整合能力，后者通过检索机制来降低信息获取成本。在实际系统设计中，如何在这两种策略之间进行权衡，才是 Agent 记忆机制设计的核心问题。正如 Karpathy 所说的，低于 40 万字的知识库，通常是不需要用到 RAG 这套复杂架构的。

## Agent 记忆机制的应用

在从系统概念的层面对 Agent 应用的记忆机制有了一个初步的了解之后，我们接下来将分别以可部署在服务端的 OpenClaw 和仅在本地运行的 OpenCode 这两种典型的 Agent 应用为例，从工程实践的角度来探讨如何为 Agent 应用构建相应的记忆机制。

### 实践1：赋予服务型 Agent 长期记忆

对于 OpenClaw、Hermes Agent 这类需要以系统服务形式长期运行的 Agent 应用来说，增强跨会话的长期记忆能力可能比保证它在单一长会话的短期记忆更重要一些，因为这直接关系到它作为一款服务端应用，能否长期与用户保持协作关系的能力，这需要它能记住用户之前执行过操作，制定的解决方案，甚至在某程度上了解用户的使用习惯与偏好，形成某种意义上的任务协同经验，我会推荐读者直接借助 GitHub 上一款名为`memory-lancedb-pro`的开源项目来为其增强长期记忆能力，以便在实践中去体验 RAG 架构的实际效果，其具体步骤如下。

1. 在 Github 上搜索`memory-lancedb-pro-skill`，找到该项目的作者为方便用户安装这个插件提供的 Skill，如图 3 所示。

    ![memory-lancedb-pro-skill](./img/memory_lancedb_pro_skill.png)

    **图 3**：memory-lancedb-pro-skill

2. 使用`git clone`命令将这个 Skill 下载到本地，并复制到 OpenClaw 的用户自定义 Skills 目录中（`~/.openclaw/workspace/skills`），然后在飞书客户端中确认该 Skill 是否已经成功加载，如图 4 所示。

    ![memory-lancedb-pro-skill](./img/memory_lancedb_pro_skill_load.png)

    **图 4**：确认`memory-lancedb-pro-skill`加载成功

3. 继续在飞书客户端中输入内容为“请通过这个 skill，替我自动从零安装 memory-lancedb-pro 插件”的提示词，让 OpenClaw 自动安装`memory-lancedb-pro`插件，如图 5 所示。

    ![memory-lancedb-pro-skill](./img/memory_lancedb_pro_install.png)

    **图 5**：自动安装`memory-lancedb-pro`插件

4. 接着输入内容为“请按照你的理解自动帮我配置”的提示词，让 OpenClaw 自动选择配置`memory-lancedb-pro`插件的最佳方案，如图 6 所示。

    ![memory-lancedb-pro-skill](./img/memory_lancedb_pro_config.png)

    **图 6**：自动配置`memory-lancedb-pro`插件

5. 待配置完成之后，我们就可以继续在飞书客户端中输入内容为“请为我测试写入与检索记忆”的提示词，让OpenClaw自动测试`memory-lancedb-pro`插件的效果。如果一切顺利，读者应该会看到类似于图 7 的回复效果。

    ![memory-lancedb-pro-skill](./img/memory_lancedb_pro_test.png)

    **图 7**：测试`memory-lancedb-pro`插件的效果

至此，我们就赋予了 OpenClaw 长期记忆能力。这意味着，OpenClaw 在执行任务时，可以借助记忆能力来增强其生成效果，从而解决幻觉现象、知识滞后、数据孤岛等问题。与此同时，读者也应该从上述过程中看到 Agent Skills 在工程化应用中的实际价值：通过封装 Skills，我们可以将复杂行为模块化，降低系统复杂度，提高复用效率。

### 实践2：赋予本地型 Agent 专业知识

对于 Claude Code、OpenCode 这类仅在本地运行的 Agent 应用来说，它所执行的任务通常都是以会话为单位来进行的，因此它们自带的记忆系统都是关于会话管理的，其中包括了历史会话列表、启动新会话时要载入的系统提示词、当前会话要跟踪的任务列表等，它们通常都是一些 Markdown 格式的线性记忆文件，在大多数情况下更侧重于上下文窗口的优化应用，很少需要用到基于 RAG 架构的长期记忆、相反，由于这类 Agent 应用更关注的是单一的特定任务，而不是与用户维持长期稳定的协作服务，任务所需的专业知识通常比了解用户的使用偏好更为重要一些。在这种情况下，Karpathy 的 LLM 知识库所具备的实用性就体现出来了。下面，我就以 Github 上一款名为`graphify`的开源项目为例，来演示一下如何为 OpenCode 增强编程领域的专业知识并将其运用到具体编程工作中，其具体步骤如下。

1. 在 Github 上搜索`graphify`，找到该项目的说明文档（即`README.md`或`README_zh-CN.md`），如图 8 所示。

    ![graphify项目的说明文档](./img/graphify_readme.png)

    **图 8**：graphify 项目的说明文档

2. 现在，我们既可以按照说明文档进行手动安装和配置，也可以打开 OpenCode 并输入内容为“请为我安装这个项目并完成相应的配置，<这个项目的 URL>”的提示词，让 OpenCode 自动安装和配置`graphify`知识库，如图 9 所示。

    ![graphify的安装与配置](./img/opencode_graphify_install.png)

    **图 9**：安装与配置`graphify`知识库

3. 待安装与配置完成之后，我们就可以继续在 OpenCode 中打开我的一个现有项目（在这里，我以`pythonShell`这个项目为例），然后输入`/graphify .`命令，让 OpenCode 自动生成编程知识图谱，如图 10 所示。

    ![为指定项目生成知识库及图谱](./img/opencode_graphify_generate.png)

    **图 10**：为指定项目生成知识库及图谱

4. 待上述操作完成之后，OpenCode 就会在当前项目的根目录下生成一个名为`graphify-out`的子目录，其中就包含了我们刚刚生成的知识库与图谱。如果我们用网页浏览器打开这个子目录中的`graph.html`文件，就可以看到可交互的编程知识图谱，如图 11 所示。

    ```bash
    graphify-out/
    ├── graph.html       # 可交互图谱：可点节点、搜索、按社区过滤
    ├── GRAPH_REPORT.md  # God nodes、意外连接、建议提问
    ├── graph.json       # 持久化图谱：数周后仍可查询，无需重新读原始文件
    └── cache/           # SHA256 缓存：重复运行时只处理变更过的文件
    ```

    ![查看graphify生成的知识图谱](./img/opencode_graphify_graph.png)

    **图 11**：查看 graphify 生成的知识图谱

现在，基于这个个知识库，我们可以在 OpenCode 中对项目进行详细分析。例如，通过输入`/graphify explain git_push_remote`命令来让 OpenCode 为我们解释`git-push-remote`这个工具，如图 12 所示。

![让OpenCode解释项目中的工具](./img/opencode_graphify_explain.png)

**图 12**：让 OpenCode 解释项目中的工具

除此之外，根据 graphify 的说明文档，我们还可以通过如下一系列命令来对这个项目进行分析、维护与优化。

```bash
/graphify                          # 对当前目录运行
/graphify ./raw                    # 对指定目录运行
/graphify ./raw --mode deep        # 更激进地抽取 INFERRED 边
/graphify ./raw --update           # 只重新提取变更文件，并合并到已有图谱
/graphify ./raw --cluster-only     # 只重新聚类已有图谱，不重新提取
/graphify ./raw --no-viz           # 跳过 HTML，只生成 report + JSON
/graphify ./raw --obsidian         # 额外生成 Obsidian vault（可选）

/graphify add https://arxiv.org/abs/1706.03762        # 拉取论文、保存并更新图谱
/graphify add https://x.com/karpathy/status/...       # 拉取推文
/graphify add https://... --author "Name"             # 标记原作者
/graphify add https://... --contributor "Name"        # 标记是谁把它加入语料库的

/graphify query "what connects attention to the optimizer?"
/graphify query "what connects attention to the optimizer?" --dfs   # 追踪一条具体路径
/graphify query "what connects attention to the optimizer?" --budget 1500  
                                                            # 把预算限制在 N tokens
/graphify path "DigestAuth" "Response"
/graphify explain "SwinTransformer"

/graphify ./raw --watch      # 文件变更时自动同步图谱（代码：立即更新；文档：提醒你）
/graphify ./raw --wiki       
                    # 构建可供 agent 抓取的 wiki（index.md + 每个 community 一篇文章）
/graphify ./raw --svg              # 导出 graph.svg
/graphify ./raw --graphml          # 导出 graph.graphml（Gephi、yEd）
/graphify ./raw --neo4j            # 生成给 Neo4j 用的 cypher.txt
/graphify ./raw --neo4j-push bolt://localhost:7687    # 直接推送到运行中的 Neo4j
/graphify ./raw --mcp              # 启动 MCP stdio server

# git hooks - 跨平台，在 commit 和切分支后重建图谱
graphify hook install
graphify hook uninstall
graphify hook status

# 常驻助手规则 - 按平台区分
graphify claude install            # CLAUDE.md + PreToolUse hook（Claude Code）
graphify claude uninstall
graphify codex install             # AGENTS.md（Codex）
graphify opencode install          # AGENTS.md（OpenCode）
graphify claw install              # AGENTS.md（OpenClaw）
graphify droid install             # AGENTS.md（Factory Droid）
graphify trae install              # AGENTS.md（Trae）
graphify trae uninstall
graphify trae-cn install           # AGENTS.md（Trae CN）
graphify trae-cn uninstall
```

## 参考资料

- 博客文章
  - [[Andrej Karpathy的LLM知识库方法论]]：[这篇博客来自名为“时光的沙盒”的知乎专栏](https://zhuanlan.zhihu.com/p/2023803203725135995)

- 开源项目
  - [memory-lancedb-pro-skill](https://github.com/win4r/memory-lancedb-pro-skill)
  - [memory-lancedb-pro](https://github.com/win4r/memory-lancedb-pro)
  - [graphify](https://github.com/safishamsi/graphify)

- 视频资料
  - memory-lancedb-pro 插件的安装与使用演示：[Youtube 链接](https://www.youtube.com/watch?v=bhuGrjuCM_g) / [Bilibili 链接](https://www.bilibili.com/video/BV1iWwtztEQf)
  - graphify 编程知识库的使用演示：[Youtube 链接](https://www.youtube.com/watch?v=m_5OLW52JwI) / [Bilibili 链接](https://www.bilibili.com/video/BV1G9DiBSEmj)
