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

## 问题背景：为什么 Prompt 不够用了？

* Agent 从“对话工具”走向“系统组件”
* Prompt 工程的边界在哪里？

  * 上下文长度限制
  * 稳定性问题
  * 复杂逻辑不可控
* 当任务变复杂时，会出现什么瓶颈？

> 目标：建立“必须扩展”的动机，而不是直接讲技术名词。

## Agent 能力扩展的三层模型

构建一个抽象框架：

1. Prompt 层 —— 语言控制
2. 协议层 —— 工具调用（MCP）
3. 能力封装层 —— Skills

可以在这里介绍：

Anthropic 提出的 MCP 与 Skills

并说明它们出现的背景。

重点回答：

* 这三层分别解决什么问题？
* 它们之间的关系是什么？
* 是否可以替代？

### Prompt 的工程边界

不要讲基础知识，而讲：

* Prompt 作为“软控制”的本质
* 为什么 Prompt 不等于能力扩展
* Prompt 的成本模型（token 成本）
* Prompt 规模化时的维护难题

结论应该是：

> Prompt 是最便宜的扩展方式，但也是最不稳定的。

---

### MCP：工具调用的协议化

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

### Agent Skills：能力的产品化封装

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

### MCP vs Skills：架构选择决策模型

建议用决策表：

| 场景     | Prompt | MCP | Skills |
| ------ | ------ | --- | ------ |
| 简单逻辑   | ✓      | ✗   | ✗      |
| 外部数据访问 | ✗      | ✓   | ✗      |
| 复杂流程固化 | ✗      | 部分  | ✓      |
| 多人协作维护 | ✗      | ✓   | ✓      |

这一节非常重要，它会体现你的工程判断力。

## 项目实践：从 0 到可维护 Agent 系统

这一部分必须具体化：

* 项目目标
* 架构设计
* 扩展方式选择理由
* 实际踩坑
* 性能与成本分析
* 重构前后对比

如果没有量化指标，至少给出：

* 复杂度变化
* 维护成本变化
* Prompt 长度变化

## 扩展风险与系统复杂度管理

* Skills 爆炸问题
* MCP 服务膨胀问题
* 过度工程化
* 依赖外部服务的风险

这一节能让文章成熟一个层级。

## 总结：Agent 扩展的工程思维

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
