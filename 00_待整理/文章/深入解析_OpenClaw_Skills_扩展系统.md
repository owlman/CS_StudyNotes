# 深入解析 OpenClaw 的 Skills 扩展系统：AI Agent 如何学会"自我进化"

> 作者：陶刚  
> 来源：https://zhuanlan.zhihu.com/p/2006196534333694047

---

[OpenClaw](https://link.zhihu.com/?target=https%3A//github.com/openclaw/openclaw) 是当下最火的开源 AI Agent 框架，GitHub star 数已突破 19 万。我们之前对他的系统架构，提示词系统和记忆管理都做了介绍。今天我们来看看系统的另一个关键功能，Skills扩展。

- [谈谈最近爆火的Agent项目Moltbot（原 Clawdbot）](https://zhuanlan.zhihu.com/p/2000362996422181628)
- [OpenClaw 记忆系统架构深度解析：从 Markdown 到混合检索](https://zhuanlan.zhihu.com/p/2005943466006438841)
- [深入研究OpenClaw - 系统提示词解析](https://zhuanlan.zhihu.com/p/2005106362745652018)

OpenClaw最吸引人的设计之一，就是它的 Skills（技能）扩展系统——一种让 AI 助手可以不断学习新本领、甚至能"自己给自己写技能"的插件架构。本文将从原理到实践，全面拆解这套系统的运作方式。

---

## 一、为什么 AI Agent 需要 Skills？

想象你雇了一个非常聪明的助理。他什么都懂一点，但你让他做 PPT、处理 Excel、操作智能家居、帮你发 WhatsApp 消息……他可能一脸茫然——不是因为不够聪明，而是因为不知道具体怎么操作。

这就是大语言模型（LLM）面临的核心困境：通用知识很强，专项操作能力很弱。

LLM 天生擅长理解语言、推理分析，但它不知道你的 PDF 工具怎么调用，不了解你的智能音箱的 API 是什么，也不清楚生成 Word 文档的最佳实践。传统的做法是把所有工具的调用方式硬编码到系统里，但这样做有三个致命问题：

- **扩展性差**：每加一个新能力，就要改代码、重新部署
- **Token 浪费**：把所有工具的说明都塞进上下文窗口，大量 token 被浪费在当前用不上的工具描述上
- **无法个性化**：每个用户的需求不同，一刀切的能力集合无法满足所有人

OpenClaw 的 Skills 系统正是为了解决这些问题而生。简单来说：**Skills 就是给 AI 助手的"操作手册"**，让它在需要的时候翻阅对应的说明书，而不是把所有说明书都背下来。

---

## 二、OpenClaw 的 Skills 是如何定义的？

### 核心理念：用 Markdown 教 AI 做事

与 LangChain 用 Python 函数定义工具、OpenAI 用 JSON Schema 描述函数调用不同，OpenClaw 的 Skill 本质上就是一个 Markdown 文档——准确地说，是一个名为 `SKILL.md` 的文件，外加 YAML 格式的元数据头。

这个设计理念非常精妙：既然 LLM 最擅长阅读和理解自然语言，那为什么不直接用自然语言来教它怎么做事呢？

### 一个 Skill 的目录结构

```
skills/
└── my-awesome-skill/
    ├── SKILL.md          # 必需：YAML 元数据 + Markdown 操作指南
    ├── bins/             # 可选：可执行文件（自动加入 PATH）
    ├── references/       # 可选：参考文档
    ├── scripts/          # 可选：辅助脚本（Python、Bash、JS 等）
    └── skill.json        # 可选：旧版元数据格式
```

整个 Skill 里，只有 `SKILL.md` 是必须的，其它都是锦上添花的可选项。

### SKILL.md 长什么样？

以一个图片生成 Skill 为例：

```yaml
---
name: nano-banana-pro
description: 使用 Gemini 3 Pro 生成或编辑图片
metadata: {
  "openclaw": {
    "emoji": "🎨",
    "os": ["darwin", "linux"],
    "primaryEnv": "GEMINI_API_KEY",
    "requires": {
      "bins": ["uv"],
      "env": ["GEMINI_API_KEY"]
    },
    "install": [{
      "id": "brew",
      "kind": "brew",
      "formula": "gemini-cli",
      "label": "安装 Gemini CLI (brew)",
      "os": ["darwin"]
    }]
  }
}
---

# Nano Banana Pro - 图片生成技能

## 使用方法

1. 首先确认用户的需求：是生成新图片还是编辑已有图片
2. 使用 {baseDir}/scripts/generate.py 调用 Gemini API
3. 生成结果保存到工作目录
4. 向用户展示结果并询问是否需要调整

## 注意事项

- 始终使用中性、安全的提示词
- 图片尺寸默认 1024x1024
- 如果 API 返回错误，提示用户检查 API Key
```

让我们拆解这个文件的关键部分：

**必填字段：**

- `name`：技能名称，最长 64 个字符，必须和目录名一致
- `description`：技能描述，这是最关键的字段——AI 就是根据这段描述来判断什么时候该用这个技能

**可选但实用的字段：**

- `requires.bins`：运行这个技能需要哪些命令行工具
- `requires.env`：需要哪些环境变量（比如 API Key）
- `install`：如何一键安装所需依赖
- `os`：支持的操作系统

**Markdown 正文：** 就是用自然语言写的操作指南，告诉 AI "第一步做什么、第二步做什么、遇到什么情况怎么处理"。

---

## 三、Skills 的完整生命周期：从发现到执行

### 第一步：发现——去哪里找 Skills？

OpenClaw 启动时会从四个位置扫描 Skills，按优先级从高到低排列：

| 优先级 | 位置 | 作用范围 |
|--------|------|----------|
| 最高 | `<工作区>/skills` | 仅当前 Agent |
| 中 | `~/.openclaw/skills` | 本机所有 Agent 共享 |
| 低 | 内置（随安装包附带） | 默认可用 |
| 低 | `skills.load.extraDirs` 配置 | 自定义共享目录 |

当出现同名 Skill 时，高优先级的会覆盖低优先级的。这意味着你可以在工作区目录放一个同名 Skill 来覆盖内置版本，实现"定制化"。

### 第二步：资格检查——这个 Skill 能用吗？

扫描到一个 SKILL.md 后，OpenClaw 会根据 `requires` 字段做一系列检查：

- `bins`：指定的命令行工具是否都装了？（比如 `ffmpeg`、`uv`）
- `env`：必需的环境变量是否已设置？（比如 `GEMINI_API_KEY`）
- `config`：OpenClaw 配置中是否满足条件？（比如 `browser.enabled`）
- `os`：当前操作系统是否在支持列表中？

只有所有条件都满足的 Skill 才会被标记为"可用"。这避免了 Agent 试图使用一个根本跑不起来的技能。

### 第三步：加载——三级渐进式披露

这是 OpenClaw Skill 系统最精妙的设计之一。它不会一股脑把所有 Skill 的完整内容塞进 AI 的上下文窗口，而是采用**三级渐进式披露**：

**第一级——名片（约 24 个 token/Skill）：** 只把 Skill 的名称、描述和文件位置以 XML 标签的形式注入系统提示词。50 个 Skill 加在一起也才约 1,200 个 token——非常经济。

```xml
<available_skills>
  <skill>
    <name>docx</name>
    <description>创建、编辑 Word 文档</description>
    <location>/mnt/skills/public/docx/SKILL.md</location>
  </skill>
  <!-- 更多 skills... -->
</available_skills>
```

**第二级——完整说明书（按需加载）：** 当 AI 判断某个 Skill 跟当前任务相关时，它会主动调用 `read` 工具读取完整的 SKILL.md 内容。

**第三级——深度资源（需要时才加载）：** 参考文档、辅助脚本等只在执行具体子任务时才会被读取。

系统提示词里会明确告诉 AI 这样的策略指引："先扫描可用技能列表。如果恰好有一个技能明显适用，读取它的 SKILL.md。如果有多个可能适用，选最具体的那个。如果都不适用，不要读取任何 SKILL.md。"

这种设计相比 MCP 等方案动辄把所有工具 Schema 全量注入的做法，token 效率高出一个数量级。

### 第四步：调用——AI 自主决策

当 AI 读取了 SKILL.md 的完整内容后，它就像一个学会了新技能的人，按照说明书上的步骤一步步执行：调用相应的命令行工具、运行脚本、处理结果、回复用户。整个过程通过 OpenClaw 的 Agentic Loop（代理循环）驱动：模型提出工具调用 → 执行 → 结果回填 → 继续推理 → 直到任务完成。

### 第五步：更新——热重载

OpenClaw 默认开启了文件监听器（debounce 250ms），实时监控 Skill 目录的变化。你修改了一个 SKILL.md，不需要重启 Agent——下一轮对话就会自动使用新版本。

配置示例（`openclaw.json`）：

```json
{
  "skills": {
    "load": {
      "watch": true,
      "watchDebounceMs": 250,
      "extraDirs": ["~/shared-skills"]
    },
    "entries": {
      "nano-banana-pro": {
        "enabled": true,
        "env": { "GEMINI_API_KEY": "你的密钥" }
      },
      "some-other-skill": { "enabled": false }
    }
  }
}
```

注意这里的密钥注入机制：通过 `entries.<name>.env` 设置的环境变量只在该 Skill 执行期间生效，执行完毕后自动恢复——不会污染全局环境。

---

## 四、与 AgentSkills.io 的兼容性

### AgentSkills 是什么？

AgentSkills（[agentskills.io](https://link.zhihu.com/?target=https%3A//agentskills.io/home)）是 Anthropic 发起的一个开放标准，最初于 2025 年 10 月作为 Claude 的专属功能推出，随后在 2025 年 12 月作为行业通用标准开放发布。它定义了一套极简的 Agent 技能描述规范：一个包含 `SKILL.md` 文件的文件夹，YAML 头部包含 `name`、`description` 等字段，正文是 Markdown 格式的操作说明。

### OpenClaw 完全兼容 AgentSkills 标准

OpenClaw 官方文档明确表示："我们遵循 AgentSkills 规范的布局和设计意图。" OpenClaw 在 AgentSkills 基本规范之上，通过 `metadata.openclaw` 扩展块添加了平台特定的功能（如依赖检查、安装器、密钥管理），但核心格式完全兼容。

这意味着什么？**一次编写，到处运行。** 一个符合 AgentSkills 规范的 Skill 可以跨平台使用：

- **Claude Code**（`~/.claude/skills/`）
- Claude.ai 和 Claude API
- **OpenAI Codex CLI**（`~/.codex/skills/`）
- ChatGPT（`/home/oai/skills`）
- **GitHub Copilot / VS Code**（`.agents/skills/`）
- **Cursor**（`.cursor/rules/`）
- Amp、Goose、Manus 等其他兼容平台

不过需要注意：[agentskills.io](https://link.zhihu.com/?target=http%3A//agentskills.io) 本身只是一个规范和文档网站，它不是一个技能市场或商店。各种第三方市场（如 [SkillHub.club](https://link.zhihu.com/?target=https%3A//skillhub.club/)、[ClawHub](https://link.zhihu.com/?target=https%3A//clawhub.ai/)，[The Agent Skills Directory](https://link.zhihu.com/?target=https%3A//skills.sh/) 等）是围绕这个标准建立的独立生态。

---

## 五、内置了哪些默认 Skills？

OpenClaw 开箱即附带 53 个官方内置 Skill，覆盖以下几大类别：

### 文档处理

- `docx` — 创建和编辑 Word 文档
- `pdf` — 读取、合并、拆分、填写 PDF 表单
- `pptx` — 制作和编辑演示文稿
- `xlsx` — 处理电子表格

### 生产力工具

- `gog` — Google Workspace 集成（Drive、Docs、Sheets）
- `obsidian` — Obsidian 笔记管理
- `notion` — Notion 集成
- `apple-notes` — macOS 备忘录
- `trello` — Trello 看板管理
- `things-mac` — Things 待办事项

### 消息通讯

- `wacli` — WhatsApp 消息
- `slack` — Slack 频道管理
- `discord` — Discord 服务器
- `imsg` — iMessage 短信

### 开发者工具

- `github` — GitHub 仓库操作
- `tmux` — 终端多路复用
- `coding-agent` — 编程辅助
- `frontend-design` — 前端设计最佳实践

### 智能家居与媒体

- `spotify-player` — Spotify 播放控制
- `sonoscli` — Sonos 音箱控制
- `sag` — ElevenLabs 语音合成
- `peekaboo` — macOS 截图

### 元技能（Meta Skills）

- `clawhub` — 技能注册中心管理
- `skill-creator` — 让 AI 自己创建新技能
- `summarize` — 内容摘要

这些内置 Skill 默认全部可用，你也可以通过配置文件中的 `skills.allowBundled` 字段来控制只加载特定的内置技能。

---

## 六、为什么这套 Skills 系统如此强大？

### 1. 自然语言定义，人人可写

不需要会编程，不需要理解 JSON Schema，不需要学习任何框架 API。你只需要用清晰的中文或英文写一份操作指南，就完成了一个 Skill 的创建。这把 AI Agent 的扩展能力从程序员群体解放出来，交给了所有用户。

### 2. 三级渐进式披露，极致的 Token 效率

对比其他方案：MCP 需要把所有工具的完整 Schema 一次性注入上下文；LangChain 需要加载所有工具定义。OpenClaw 的三级加载策略让 50 个 Skill 只占约 1,200 个 token 的"固定开销"，详细说明只在需要时才加载。在 Token 就是金钱的时代，这种设计极具经济性。

### 3. AI 可以自己写 Skills

这是最令人兴奋的能力。你可以对 OpenClaw 说："帮我创建一个 Skill，每天晚上自动把 Documents 文件夹备份到 Dropbox。" Agent 会自动生成 SKILL.md、编写辅助脚本、测试、迭代修复——最终产出的 Skill 立刻可用。内置的 [skill-creator](https://link.zhihu.com/?target=https%3A//github.com/openclaw/openclaw/blob/b1dd23f61d8ddf2c618728f285a5dc1104a3a22f/skills/skill-creator/SKILL.md%3Fplain%3D1%23L2) 技能就是为此而生的。

一个叫 [OpenClaw Foundry](https://link.zhihu.com/?target=https%3A//github.com/lekt9/openclaw-foundry) 的社区项目更进一步：它能观察你的工作流程，自动提炼出可复用的模式，将其封装为新的 Skill。这是真正的"自我进化"。

### 4. 热重载，即改即用

修改一个 SKILL.md 后不需要重启任何东西，文件监听器会自动检测变化，下一轮对话就生效。这种开发体验接近于前端的"热模块替换"（HMR），极大降低了调试和迭代的成本。

### 5. 跨平台可移植

遵循 AgentSkills 开放标准意味着你的 Skill 不被锁定在 OpenClaw 一个平台上。同一个 Skill 可以在 Claude Code、OpenAI Codex、GitHub Copilot、Cursor 等十多个平台上使用。

### 6. 安全隔离的密钥管理

每个 Skill 的 API Key 和环境变量通过配置注入，只在执行期间生效，不会泄漏到全局环境或其他 Skill 中。在沙箱容器中运行时，隔离性更强。

---

## 七、与其他 Agent 扩展机制的对比

| 维度 | OpenClaw Skills | LangChain Tools | OpenAI Function Calling | MCP | CrewAI/AutoGen |
|------|----------------|-----------------|------------------------|-----|----------------|
| 定义方式 | Markdown 自然语言 | Python/TS 函数 | JSON Schema | JSON-RPC 协议 | Python 类/函数 |
| 编写门槛 | 零代码 | 需要编程 | 需要编程 | 需要编程 | 需要编程 |
| Token 效率 | 三级渐进加载，极高 | 一次性全量加载 | 按需（但 Schema 较大） | 一次性全量加载 | 取决于实现 |
| 可移植性 | 跨平台（AgentSkills 标准） | 绑定 LangChain 生态 | 绑定 OpenAI API | 跨平台（开放协议） | 框架内部 |
| 自生成能力 | AI 可自己创建新 Skill | 不支持 | 不支持 | 不支持 | 不支持 |
| 热重载 | 支持 | 需重启 | 需重新部署 | 需重连 | 需重启 |
| 适用场景 | 个人 AI 助手 | 后端编排 | API 集成 | 企业标准化 | 多 Agent 协作 |
| 粒度 | 工作流级（多步骤） | 函数级（单步骤） | 函数级（单步骤） | 工具级 | 任务级 |

几个关键差异值得注意：

**Skills vs. Tools 不是同一层级。** OpenClaw 里，Tools（工具）是执行层，比如 `bash`、`read`、`write`；Skills（技能）是知识层，教 Agent "什么时候用哪个 Tool、怎么用"。一个 Skill 可能涉及多个 Tools 的组合使用。LangChain 的 Tools 和 OpenAI 的 Function Calling 都更接近 OpenClaw 的 "Tool" 层级。

**MCP 的哲学差异。** OpenClaw 创始人 Peter Steinberger 公开批评过 MCP，认为大多数 MCP 实现"没什么用"，容易产生大量"上下文垃圾"。OpenClaw 偏好 CLI 优先的设计——通过 `--help` 发现工具能力，而不是预加载庞大的 Schema。不过 MCP 在企业级审计和标准化方面有其优势。

**与 CrewAI/AutoGen 的本质区别。** CrewAI 和 AutoGen 面向多 Agent 后端编排，OpenClaw 是单 Agent 个人助手范式，通过独立工作区实现多 Agent 路由。前者适合复杂的后端自动化流水线，后者面向终端用户的日常助理场景。

---

## 八、有哪些流行且实用的社区 Skills？

OpenClaw 的官方技能注册中心 ClawHub（[clawhub.ai](https://link.zhihu.com/?target=https%3A//clawhub.ai/)）已积累超过 5,700 个社区贡献的 Skill，社区精选列表 [awesome-openclaw-skills](https://link.zhihu.com/?target=https%3A//github.com/VoltAgent/awesome-openclaw-skills) 收录了约 3,000 个经过审核的 Skill。以下是一些最受欢迎的：

### 下载量最高的 Skills

| Skill 名称 | 下载量 | 功能 |
|-----------|--------|------|
| soul-personality | 18,700+ | 赋予 Agent 独特个性和语气 |
| memory-system | 15,200+ | 跨会话记忆管理 |
| system-prompt-engine | 14,300+ | 动态系统提示词管理 |
| bootstrap-ritual | 12,900+ | Agent 启动时的初始化流程 |

### 按类别推荐

**AI 与创意：**

- `fal-ai-image` — 使用 fal.ai 生成高质量图片
- `video-generation` — AI 视频生成
- `nano-banana-pro` — Gemini 图片生成与编辑

**开发者效率：**

- `github` — GitHub 仓库管理、PR 审查
- `figma` — Figma 设计文件操作
- `azure-cli` — Azure 云服务管理
- `coding-agent` — 智能编程助手

**金融与数据：**

- `polymarket` — 预测市场数据查询
- `bankrbot` — DeFi 代币交易

**智能家居：**

- `home-assistant` — Home Assistant 设备控制
- `hue` — Philips Hue 灯光控制

**内容创作：**

- `obsidian` — 笔记知识库管理
- `notion` — Notion 内容管理
- `summarize` — 智能内容摘要

### 安装方式

通过 ClawHub CLI 一行命令搞定：

```bash
# 搜索技能
clawhub search "图片生成"

# 安装技能
clawhub install nano-banana-pro

# 批量更新
clawhub update --all
```

---

## 九、安全：不得不提的另一面

Skills 系统的开放性是一把双刃剑。近期多家安全公司的研究发现了不容忽视的风险：

- Cisco 扫描了 31,000 个 Agent Skills，发现 26% 存在至少一个安全漏洞
- Snyk 扫描 ClawHub 全部 3,984 个 Skill，发现 283 个（7.1%）存在明文凭据泄露
- Kaspersky 发现 512 个漏洞，包含 8 个严重级别

ClawHub 下载排名第一的 Skill 甚至被发现是恶意软件——它在提供正常功能的同时，偷偷把用户数据发送到攻击者控制的服务器。

OpenClaw 团队已经做出响应，集成了 VirusTotal 扫描：所有发布的 Skill 会被 SHA-256 哈希校验并与 VirusTotal 数据库交叉比对，每日重新扫描。但这场安全攻防战显然才刚刚开始。

**建议：** 优先使用内置 Skill 和经过审核的社区 Skill，对来源不明的第三方 Skill 保持警惕，定期检查工作区中的 Skill 内容。

---

## 总结

OpenClaw 的 Skills 系统代表了 AI Agent 可扩展性的一次范式转变——从僵硬的函数签名和 JSON Schema，转向自然语言操作手册。任何人都可以编写，AI 自身也能生成，多个平台通过 AgentSkills 开放标准共享使用。

三级渐进式披露解决了困扰 MCP 等方案的 Token 成本问题；热重载和文件监听让迭代体验丝滑无比；跨平台可移植性让技能真正成为可版本化、可共享的资产。

当然，"用 Markdown 当安装器"的极简设计也让生态面临前所未有的供应链安全挑战。但从技术架构的角度来看，OpenClaw 证明了一件事：**让 AI 用自然语言学习新能力，比让程序员写代码教 AI 做事，要高效得多。**

对于我们做流处理和实时分析的同行来说，这种"声明式扩展 + 按需加载 + 热重载"的架构思想，在设计可扩展系统时同样值得借鉴。

---

## 参考资料

- OpenClaw 官方文档（[docs.openclaw.ai](https://link.zhihu.com/?target=https%3A//docs.openclaw.ai/)）
- AgentSkills 规范（[agentskills.io](https://link.zhihu.com/?target=https%3A//agentskills.io/home)）
- [DeepWiki OpenClaw](https://link.zhihu.com/?target=https%3A//deepwiki.com/openclaw/openclaw) Skills System 分析
- [awesome-openclaw-skills](https://link.zhihu.com/?target=https%3A//github.com/VoltAgent/awesome-openclaw-skills) 社区精选列表
