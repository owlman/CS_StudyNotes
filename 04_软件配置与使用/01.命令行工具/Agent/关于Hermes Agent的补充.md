---
title: 关于 Hermes Agent 的补充
author: 凌杰
date: 2026-05-05
tags: Hermes-Agent
categories: 软件配置与使用
---

> [!NOTE] 笔记说明
>
> 本节为 2026 年 5 月新增内容

随着 OpenClaw 近几个月以来的大量应用，越来越多的用户开始抱怨它的安装与配置方法过于繁琐，并且每次版本更新都会给之前安装的第三方插件带来各种各样的兼容性问题。为了获得更好的用户体验，人们开始寻找安装与配置更为方便，维护也更为安全的可部署型 Agent，于是，一款名为 Hermes 的 Agent 出现在了大众的视野中。

Hermes Agent 于 2026 年 2 月由一家名为 Nous Research 公司发布在 Github 上，首月即斩获 2.2 万个 stars，截至 2026 年 4 月中旬，其周均新增 stars 数达 9500 个，增速达同期主流智能代理产品的三倍以上，连续两周登顶 GitHub 全球趋势榜首位。Hermes Agent的核心竞争力源于其独特的技术架构设计，构建了”记忆-技能-训练数据”的三层闭环体系，这让它具备了如下主要特性：

1. 拥有四级分层的记忆架构：Hermes 突破了传统的全量存储模式，借鉴 CPU 缓存分级思想打造如下记忆系统：
   - L1 核心记忆：存储于`MEMORY.md`文件，严格限制在 800 tokens 以内。每次会话启动时冻结为快照注入系统提示词，确保关键上下文不丢失。例如在代码调试场景中，能精准保留错误堆栈、变量状态等核心信息。
   - L2 用户画像：存储于`USER.md`文件，约 500 tokens 的容量。通过分析历史对话自动生成用户技术栈偏好（如Python/Java倾向）、沟通风格（简洁/详细）等维度标签，实现个性化交互。
   - L3 长时记忆：采用 SQLite FTS5 全文检索技术，存储所有跨会话历史。通过 LLM 摘要技术实现万级条目 10ms 级检索，支持按时间范围、关键词组合等条件筛选。在客户支持场景中，可快速调取用户历史问题及解决方案。
   - L4 冷数据存档：对接对象存储服务，自动归档超过 90 天的低频访问数据。通过异步压缩算法将存储成本降低 80%，同时保持秒级检索能力。

2. 拥有完整的技能扩展框架，Hermes 提供了标准化技能开发接口，支持通过YAML配置快速集成新功能。例如添加数据库查询技能仅需定义：

    ```yaml
    skills:
    - name: database_query
        type: sql
        connection:
        driver: postgresql
        endpoint: ${DB_ENDPOINT}
        templates:
        - "查询{{table}}表中{{condition}}的记录"
    ```

    技能市场已收录 200+ 预训练技能，覆盖数据分析、运维监控、创意生成等八大场景。开发者可基于模板库在 10 分钟内完成新技能开发。

3. 提供有简单易用的部署方案：支持 Linux/macOS/Windows/Android Termux 环境，用户通过执行一条安装命令即可完成部署，如图 1 所示：

    ```bash
    # Linux / macOS / Android Termux / Windows（WSL）
    curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
    ```

    ![hermes 的安装过程](./img/Hermes_agent_install.png)

    **图 1**：Hermes 的安装过程

4. 提供有多平台互通能力：内置统一消息网关，通过适配器模式支持包括微信、飞书在内的 15+ 个主流通讯平台。记忆与技能数据在各平台间完全互通，解决传统智能代理”平台孤岛”问题。用户通过执行`hermes gateway setup`命令即可完成通信平台的接入配置，如图 2 所示：

   ![hermes 的通讯平台接入配置](./img/Hermes_agent_messaging.png)

   **图 2**：Hermes 的通讯平台接入配置

连接好之后，我们同样也可以在配置好的通信平台上与 Hermes Agent 进行对话，例如图 3 中所示的就是在飞书上的对话窗口：

![hermes 的对话窗口](./img/Hermes_feishu.png)
【
**图 3**：Hermes 的对话窗口

同样的，我们也可以在命令行环境中通过执行`hermes`命令来打开 Hermes Agent 的 TUI 对话界面与它进行对话，如图 4 所示：

![hermes 的命令行对话界面](./img/Hermes_agent_tui.png)

**图 4**：Hermes 的命令行对话界面

#未完成