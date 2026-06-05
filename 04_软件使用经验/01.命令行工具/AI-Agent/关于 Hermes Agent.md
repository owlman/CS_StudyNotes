---
title: 关于 Hermes Agent
author: 凌杰
date: 2026-05-05
tags: [Hermes-Agent, OpenClaw]
categories: 软件配置与使用
---

> [!NOTE] 笔记说明
>
> 这篇文章是 Agent 系列笔记的后续补充，主要用于补充介绍 Hermes Agent 的使用方法以及相关的个人体验。同样的，这些内容也将被存储在本人 Github 上的[计算机学习笔记库](https://github.com/owlman/CS_StudyNotes)中，并予以长期维护。

Hermes Agent 于 2026 年 2 月由一家名为 Nous Research 公司发布在 Github 上，首月即斩获 2.2 万个 stars，截至 2026 年 4 月中旬，其周均新增 stars 数达 9500 个，增速达同期主流智能代理产品的三倍以上，连续两周登顶 GitHub 全球趋势榜首位。Hermes Agent 的核心竞争力源于其独特的技术架构设计，构建了”记忆-技能-训练数据”的三层闭环体系，这让它具备了如下主要特性：

## 分层设计的记忆系统

Hermes Agent 打破了传统的全量存储模式，它借鉴 CPU 缓存的设计思想打造出了一个分层记忆系统，这一解决方案在一定程度上缓解了由 OpenClaw 在跨会话记忆方面的缺陷所带来的一系列问题，为 Agent 应用的持久记忆机制提供了一种更稳定的工程实现。具体来说，这个记忆机制主要有如图 1 所示的四个分层结构组成。

<!-- ![Hermes Agent 的记忆系统](./img/Hermes_agent_memory_system.png) -->
![img](https://img2024.cnblogs.com/blog/691082/202605/691082-20260513152546804-1547140810.png)

**图 1**：Hermes Agent 的记忆系统

- L1 核心记忆：相关记忆数据存储于`MEMORY.md`文件，该文件可以被视为 Agent 的记事本，它的容量被严格限制在 800 tokens 以内。Hermes Agent 会在每次启动一个会话时将其冻结为快照，并注入系统提示词，确保关键上下文不丢失。例如在代码调试场景中，这样做能精准保留错误堆栈、变量状态等核心信息。

- L2 用户画像：相关记忆数据存储于`USER.md`文件，容量约 500 tokens，主要用于通过分析历史对话自动记录用户的技术栈偏好（如 Python/JavaScript/C++ 倾向）、喜欢的沟通风格（简洁/详细）等维度标签，以便实现与用户的个性化交互。

- L3 会话记忆：相关记忆数据会被全量存储在 SQLite 数据库中，并利用 FTS5 全文索引支持毫秒级检索。对于这部分记忆数据，Hermes Agent 并不会主动加载，而是会在需要时通过 session_search 工具进行针对性的查询。

- L4 技能系统：相关记忆数据存储于`~/.hermes/skills`目录下，Hermes Agent 能将复杂任务的解决路径自动提炼为各种可复用的`SKILL.md`文件，并能根据后续相似任务的执行情况对这些 Skills 进行持续迭代。

总而言之，与 OpenClaw 相比，Hermes Agent 拥有更接近人类对信息进行分层管理的方式，这使它能根据信息的价值和新鲜度进行分层、压缩与主动遗忘，实现跨会话的可复用技能。而 OpenClaw 的持久记忆功能则相对更基础一些，如果我们想要让它具备这种内化的、分层管理的能力，就得借助 [memory-lancedb-pro](https://github.com/CortexReach/memory-lancedb-pro) 或 [memory-powermem](https://github.com/ob-labs/memory-powermem) 这样的第三方插件来实现，但这些第三方插件又正是 OpenClaw 每次版本更新会引发兼容性问题的根源。有时候，计算机世界就是这样，牺牲自由度就会换来便利性，反之亦然。

## 可扩展的 Skills 框架

Hermes Agent 提供了标准化的、可自我迭代的 Skills 框架，这一框架具有如下几个核心特性：

1. 持续优化机制：不同于传统的硬编码工具，Hermes Agent 会将任务的执行经验自动提取为可复用的 Skills，并能根据后续相似任务的执行情况保持自我更新。这是因为，它可以利用 DSPy 和 GEPA（遗传帕累托提示进化）算法，基于用户反馈自动优化自身的 Skills 库。

2. 标准化格式：Hermes Agent 中的所有 Skill 都遵循 [agentskills.io](https://agentskills.io/home) 定义的规范，被存放在`~/.hermes/skills/`目录下。具体来说就是：
   - 每个 Skill 都需由一个名为`SKILL.md`的 Markdown 文件来定义；
   - 定义的内容通常包含：元数据、名称、版本、作者、功能描述、输入/输出规范、任务执行策略（Thought Process）、以及要执行的动作（Actions）等。

3. 内置的 Skills 库及其扩展生态：Hermes Agent 框架自带了 70+ 个，覆盖 15+ 类别的内置 Skills。应用场景包括 Apple Notes/Reminders、iMessage、Claude Code、OpenCode 等。除此之外，用户还可以通过 Skills Hub 安装其他第三方 Skills，或在`~/.hermes/skills/`目录下创建自定的 Skills。

4. 安全性机制：在 1Panel 等环境中提供技能管理界面，支持安全审批 /approve session。

正是以上特性赋予了 Hermes Agent 强大的、可自我提升的能力，其中的核心能力包括：

- 持久化记忆：跨会话持久存储用户偏好和高频操作。
- 反馈式学习：实时根据用户的“好/坏”评价调整策略。
- 智能化执行：能够执行复杂任务，如写 Proposal、调用外部接口。
- 自动化沉淀： 将临时任务转化为可复用的标准化技能。
- 定时/触发任务：支持基于 Cron 表达式或事件的自动化工作流。

这让同为可部署为系统服务的 Agent，Hermes Agent 相对于 OpenClaw，具备了如表 1 所示的明显优势。

| 维度     | Hermes Agent            | OpenClaw                         |
| -------- | ----------------------- | -------------------------------- |
| 技能定义 | 由 Agent 自动生成并优化 | 需人工编写指令规则与相关脚本     |
| 记忆机制 | 持久化分层存储          | 原生记忆能力较弱，需借助外部扩展 |
| 安全机制 | 内置安全审批与隔离机制  | 需在后期进行人工维护             |
| 角色定位 | 面向长期能力沉淀的系统  | 偏向用于工具编排的框架           |

**表 1**：Hermes Agent 相对于 OpenClaw 的优势

## 简单易用的部署方案

Hermes Agent 支持 Linux/macOS/Windows/Android Termux 环境，用户通常只需根据自己所在的操作系统平台执行一条命令即可完成服务的部署（包括安装相关的依赖）。

```bash
# 在 Linux / MacOS / WSL 环境下执行如下命令
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# 在 Windows 原生环境下执行如下命令
irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1 | iex
```

在上述命令启动之后，我们会先下载到 Hermes Agent 的安装脚本，然后该脚本会自动检测其所在的计算机系统环境，并安装部署环境所依赖的 Node.js、Python、Git 等基础设施，如图 2 所示。

<!-- ![Hermes Agent 的安装过程](./img/Hermes_agent_install.png) -->
![img](https://img2024.cnblogs.com/blog/691082/202605/691082-20260513152656290-1194796035.png)

**图 2**：Hermes Agent 的安装过程

接下来，安装脚本就会启动 Hermes Agent 核心组件的安装与配置向导。和 OpenClaw 一样，Hermes Agent 在网关服务启动前，也会要求用户指定要连接的 LLM 提供商（包括 API Key），由于操作方式大同小异，这里就不再赘述了，如果读者真有需要，可参考我在“参考资料”一节中提供的视频资料：《Hermes Agent 安装与配置演示》。

如果安装过程一切顺利，用户就只需要继续在命令行终端中执行`hermes`命令，Hermes Agent 就会启动一个如图 3 所示的 TUI 对话窗口，它的作用和我们之前在[[Agent 的基础应用]]这篇笔记中介绍过的 OpenClaw TUI 是一样的，只不过它的界面更美观一些。

<!-- ![Hermes Agent TUI](./img/Hermes_agent_tui.png) -->
![img](https://img2024.cnblogs.com/blog/691082/202605/691082-20260513152737056-1982214737.png)

**图 3**：Hermes Agent TUI 的对话窗口

## 标准化的通信平台接入

内置统一消息网关，通过适配器模式支持包括微信、飞书在内的 15+ 个主流通讯平台。记忆与技能数据在各平台间完全互通，解决传统智能代理”平台孤岛”问题。用户通过执行`hermes gateway setup`命令即可完成通信平台的接入配置，如图 4 所示：

<!-- ![Hermes Agent 的通讯平台接入配置](./img/Hermes_agent_messaging.png) -->
![img](https://img2024.cnblogs.com/blog/691082/202605/691082-20260513152815929-1024475850.png)

**图 4**：Hermes 的通讯平台接入配置

例如，如果我们在上述界面中选择飞书（Feishu / lark），就会看到如图 5 所示的接入方式界面。然后，我们在这里既可以选择第一项，然后用手机端的飞书通过扫二维码方式自动在飞书开放平台中创建机器人（它会按照指定的智能体模版配置好机器人被赋予的执行权限）；也可以和之前在 OpenClaw 种所做的一样，先去飞书开放平台手动创建机器人，并为它配置好你想赋予的权限，然后再回到这里选择第二项，将该机器人的 App ID 和 App Secret 填入。前者比较方便，后者则比较自由，我们可以根据自己的需求来做出选择。

<!-- ![hermes 的飞书接入方式](./img/Hermes_feishu_config.png) -->
![img](https://img2024.cnblogs.com/blog/691082/202605/691082-20260513152859368-422665907.png)

**图 5**：Hermes Agent 的飞书接入方式

如果一切顺利，我们就可以利用配置的飞书机器人与 Hermes Agent 进行对话了，如图 6 所示：

<!-- ![hermes 的对话窗口](./img/Hermes_feishu.png) -->
![img](https://img2024.cnblogs.com/blog/691082/202605/691082-20260513152931782-948451245.png)

**图 6**：Hermes Agent 与飞书的对话窗口

除了飞书之外，我们从图 4 中还可以看到，Hermes Agent 还支持微信、钉钉、企业微信、Slack、Discord、Telegram、WhatsApp、iMessage 等主流通讯平台，而且这些平台都可以通过类似的方式接入，因此，Hermes Agent 的多平台接入能力相对于 OpenClaw 来说，无疑要简单且规范化得多，而这通常也意味着更稳定。

## 精简实用的常用命令集

由于 Hermes Agent 归根结底还是和 OpenClaw 一样，同属于运行在服务器环境中的 Agent，主要使用方式依然是基于命令行界面的，毕竟目前还没有什么图形化界面的程序在远程登录到服务器上并执行运维相关工作时，能获得好于命令行界面程序的用户体验。但相对于 OpenClaw 来说，Hermes Agent 的常用命令集要精简许多，而且这些命令的命名也相对规范，用户可以很容易地通过`hermes --help`命令查看到所有可用的命令，如图 7 所示。

<!-- ![Hermes Agent 的常用命令](./img/Hermes_agent_help.png) -->
![img](https://img2024.cnblogs.com/blog/691082/202605/691082-20260513153016365-937022105.png)

**图 7**：Hermes Agent 的可用命令

其中较为常用的命令包括：

- `hermes`命令：用于启动 TUI 对话窗口。
- `hermes model`命令：用于配置要使用的 LLM 提供商和具体要接入的模型。
- `hermes tools`命令：用于配置 Hermes Agent 可使用的工具集。
- `hermes setup`命令：用于执行完整的配置向导，包括 LLM 配置、工具配置、消息网关配置等。
- `hermes doctor`命令：用于诊断并修复 Hermes Agent 中的各种配置问题。
- `hermes update`命令：用于更新至最新版本。
- `hermes gateway`命令：用于启动、停止或重启消息网关服务。
- `hermes --continue`命令：用于回到上次会话，其中`--continue`也可以简写为`-c`。

例如，如果我们想要看看当前运行的 Hermes Agent 服务是否正常，就可以执行`hermes doctor`命令，如图 8 所示：

<!-- ![Hermes Agent 的诊断结果](./img/Hermes_agent_doctor.png) -->
![img](https://img2024.cnblogs.com/blog/691082/202605/691082-20260513153028648-1474467614.png)

**图 8**：Hermes Agent 的诊断结果

如果在上述命令中检测出了什么错误，Hermes Agent 就会在输出中给出相应的修复建议，并提示用户执行`hermes doctor --fix`命令来修复这些错误。

## 结束语：一些个人观点

总而言之，Hermes Agent 的配置和使用逻辑与 OpenClaw 几乎是完全一致的。这意味着，人们只要学会了如何使用 OpenClaw。基本上就可以举一反三了。只不过，Hermes Agent 的配置方式相对来说会比 OpenClaw 黑盒化一点，说白了就是用牺牲自由度来换取版本更新的稳定性与扩展应用的安全性。

在目前这个阶段，我对这类部署在服务端 Agent 的基本观点是：如果最近这段时间真有老板听信了资本炒作或自媒体唬烂，认为 OpenClaw 或 Hermes Agent 能代替人类工作，而做大量裁员或者搞一人公司，十八个月之后，他们有非常高的概率会惨不忍睹。当然了，学会使用 Agent 和清醒地认识它之间并不存在矛盾，事实上恰恰相反，越懂它，我们恐怕就越不信这种炒作。因为这会让人面对一个主要的哲学问题：**我们要如何只用概率解释世界，这是唯心论还是唯物论？** 建议读者可以想想，想得越清楚，就越不容易被忽悠。

当然了，虽然我本人对当前这波 AI 热潮有诸多基于神经网络这项技术本源的质疑，但我还是建议，只要条件允许，我们还是应该要多花点时间折腾 OpenClaw、Hermes Agent 这类工具，毕竟它们依然能有很大的概率会是未来 Agent 应用的发展方向，保持对这种前沿技术的敏感度，是非常必要的投资。

## 参考资料

- 文档资料
  - [Hermes Agent 官方文档](https://hermes-agent.nousresearch.com/docs/)
  - [Hermes Agent 中文文档](https://hermesagent.org.cn/docs/getting-started/quickstart)

- 视频资料：
  - [Hermes Agent 安装与配置演示](https://www.bilibili.com/video/BV1PMRTBYEdV)
