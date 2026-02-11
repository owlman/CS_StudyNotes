---
title:Agent 的使用与实践
author: 凌杰
date: 2026-02-10
tags: agent claude opencode
categories: 人工智能
---

> [!NOTE] 笔记说明
>
> 这篇笔记对应的是《[[关于 AI 的学习路线图]]》一文中所规划的第四个学习阶段。其中记录了我学习 AI Agent 并将其应用于实际工作场景的全过程，以及在该过程中所获得的心得体会。同样的，这些内容也将成为我 AI 系列笔记的一部分，被存储在本人 Github 上的[计算机学习笔记库](https://github.com/owlman/CS_StudyNotes)中，并予以长期维护。

## AI Agent 简介

在理解了 LLM 在生产环境中所扮演的角色之后，我们接下来要解决的问题是：如何让它参与到实际工作流程中？到目前为止（截至 2026 年 2 月），我们所能提出的、最具可行性的解决方案是构建并使用 AI Agent。

### 为什么需要 AI Agent

在早期，大多数用户是通过 Web 应用或移动端应用，以文本对话的方式来使用 LLM。例如 ChatGPT 就是这类应用的典型代表。这类应用本质上是基于 HTTP API 构建的人机交互界面，其主要交互模式是“输入文本—生成文本”的往返过程（我们之前在《[[LLM 的部署与测试]]》一文中基于 PyTest 框架编写的测试用例，本质上就是模拟了这种交互模式）。

很显然，这类应用尽管极大地降低了 LLM 的使用门槛，也使其成为了一种能惠及普通用户的智能问答工具，但它的能力也在很大程度上被局限在了这种聊天式的交互模式中。换言之，LLM 在这种交互模式下只能根据当前输入生成文本结果，无法主动访问本地环境、调用系统资源或执行实际任务。更重要的是，在这种模式下，LLM 并不处于一个持续运行的控制结构之中，它只在收到请求时做出一次性响应，而不负责流程的推进与状态管理。

正是在这种背景下，我们要解决的真正问题就逐渐显现出来了。试想一下，如果 LLM 已经具备理解和规划复杂任务的能力，那么仅仅把它限制在对话窗口中，是否是一种能力上的浪费？为了让模型不仅“给出建议”，而是能够在特定环境中“执行操作”，AI Agent 的概念逐渐发展起来。Agent 的核心目标，并不是提升模型本身的智能水平，而是赋予 LLM 与外部系统交互的能力，使其能够参与到真实的工作流程之中。在这一转变中，LLM 的角色也发生了变化，它不再只是一个回答问题的工具，而成为了一个可以参与任务执行的系统组件。

### AI Agent 的工作原理

### AI Agent 的应用场景

## 安装与基本配置

### 命令行工具型 Agent

### 编辑器插件型 Agent

### 可部署服务型 Agent

## Agent 的扩展机制

### MCP 服务

### Agent Skills

## 实际应用演示

### 文档处理

### 程序开发

### 自动化任务

## 结束语

在完成了对 AI Agent 的学习与实践之后，一个明显的感受是：
Agent 并没有让系统变得更简单，反而让系统的边界变得更加清晰。

与传统的自动化脚本或工具不同，Agent 并不是一组固定规则的集合，而是一个基于语言模型进行任务理解、规划与执行的系统组件。这意味着，在很多场景下，它所做的并不是“按预期运行”，而是“尽力完成任务”。

正因如此，Agent 的引入并没有削弱人类在系统中的作用，反而对人的判断能力提出了更高要求：
我们需要能够理解 Agent 在做什么、为什么这么做，以及在什么情况下应该介入、修正甚至中止它的行为。

从这个角度来看，学习和使用 AI Agent，并不意味着把控制权完全交给 AI，而是学会如何在一个由 AI 参与执行的系统中，重新定位人的职责与边界。这也正是本学习阶段的核心目标。

## 参考资料

- 视频教程：
  - [Claude Code 教程](https://www.youtube.com/watch?v=AT4b9kLtQCQ) [B站链接](https://www.bilibili.com/video/BV14rzQB9EJj)
  - [agent skills 教程](https://www.youtube.com/watch?v=yDc0_8emz7M) [B站链接](https://www.bilibili.com/video/BV1cGigBQE6n)
- 官方文档：
  - [基于 Agent skills 和 MCP 服务的协同工作流](https://claude.com/blog/extending-claude-capabilities-with-skills-mcp-servers)
  - [Agent skills 构建指南](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)
  -  


AI Agent Skills：2025年10月16日由Anthropic正式推出，同年12月18日将其发布为开放标准。
