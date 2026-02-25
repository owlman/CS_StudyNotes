---
titile: Agent 的进阶应用
author: 凌杰
date: 2026-02-19
tags: Prompt MCP Skills
categories: 人工智能
---

> [!NOTE] 笔记说明
>
> 这篇笔记是《[[Agent 的基础应用]]》一文的后续内容。其中记录了我学习 AI Agent 的扩展机制，并将其应用于实际工作场景的全过程，以及在该过程中所获得的心得体会。同样的，这些内容也将成为我 AI 系列笔记的一部分，被存储在本人 Github 上的[计算机学习笔记库](https://github.com/owlman/CS_StudyNotes)中，并予以长期维护。

## AI Agent 的扩展机制

在《[[Agent 的基础应用]]》一文中，我对于 Agent 的应用演示都是基于简单的提示词（Prompt）来进行的。在实际生产环境中，我们要描述的问题会远比这些演示复杂得多，这不仅需要掌握更专业的提示词写法，而且还需要充分利用 Agent 提供的各种扩展机制来提高提示词的命中率。现在，让我们从提示词本身的工作原理及其能力边界来开始接下来的进阶之旅。

### 提示词及其能力边界

这部分介绍：

* Prompt 作为“软控制”的本质
* 为什么 Prompt 不等于能力扩展
* Prompt 的成本模型（token 成本）
* Prompt 规模化时的维护难题

结论应该是：

> Prompt 是最便宜的扩展方式，但也是最不稳定的。

由此引出：

Anthropic 提出的 MCP 与 Skills

并说明它们出现的背景。

重点回答：

* 这三层分别解决什么问题？
* 它们之间的关系是什么？
* 是否可以替代？

### MCP 服务

#### MCP 解决了什么问题？

* 工具接入标准化
* 跨平台复用
* 安全边界管理

#### MCP 与传统 function calling 的区别

可以对比：

OpenAI 的 function calling 机制

讨论：

* 协议 vs API 绑定
* 可移植性
* 开放性

#### MCP 的成本与风险

* 部署复杂度
* 安全问题
* 依赖管理

### Agent Skills

#### Skills 的核心思想

* 将“行为模式”固化
* 可版本化
* 可复用
* 可组合

#### Skills ≠ Prompt 模板

* 技术差异
* 工程差异
* 维护成本差异

#### Skills 的使用边界

* 何时适合封装？
* 何时不该封装？

### 扩展机制的三层决策结构

### 扩展风险与系统复杂度管理

* Skills 爆炸问题
* MCP 服务膨胀问题
* 过度工程化
* 依赖外部服务的风险

## 项目实践演示

### 项目1：个人网站的重构

### 项目2：文档的格式转换

### 项目3：笔记系统的建构

## 结束语

不要只总结“学到了什么”。

总结：

* 能力扩展的层级模型
* 架构决策原则
* 未来可能的演化方向

## 参考资料

- 官方文档：
  - [MCP 简介](https://www.anthropic.com/news/model-context-protocol)
  - [Agent skills 构建指南](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)

- 视频教程
  - 关于 Token 的科普：[YouTube 链接](https://www.youtube.com/watch?v=QNiaoD5RxPA) / [Bilibili 链接](https://www.bilibili.com/video/BV1S5miBvEsu)
  - MCP 教程（基础篇）： [YouTube 链接](https://www.youtube.com/watch?v=yjBUnbRgiNs) / [Bilibili 链接](https://www.bilibili.com/video/BV1uronYREWR/)
  - MCP 教程（进阶篇）：[YouTube 链接](https://www.youtube.com/watch?v=zrs_HWkZS5w) / [Bilibili 链接](https://www.bilibili.com/video/BV1Y854zmEg9)
  - Agent Skills 教程：[YouTube 链接](https://www.youtube.com/watch?v=yDc0_8emz7M) / [Bilibili 链接](https://www.bilibili.com/video/BV1cGigBQE6n)

[^1]:AI Agent Skills：2025年10月16日由Anthropic正式推出，同年12月18日将其发布为开放标准。
