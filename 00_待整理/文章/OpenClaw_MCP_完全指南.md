# OpenClaw 使用和管理 MCP 完全指南

原文链接: https://blog.csdn.net/coolyoung520/article/details/120611835

---

## 概述

OpenClaw(原名 Clawdbot)是一款开源的本地 AI 智能体框架,在 GitHub 上拥有超过 180K 星标。MCP(Model Context Protocol)是由 Anthropic 推出的一种开放标准协议,旨在让 AI 模型通过统一接口连接各种外部工具和数据源。通过配置 MCP,OpenClaw 可以直接访问本地文件系统、数据库、GitHub 仓库,甚至 Google Drive 和 Slack 等服务。

MCP 在 OpenClaw 中扮演"万能插槽"的角色:以往每个工具都要编写单独的插件(Skill),现在只要工具支持 MCP,OpenClaw 就能直接调用,实现即插即用。

## 环境准备

在开始配置 MCP 之前,需要确保本地环境满足以下条件:

- **Node.js**:建议 v22 或更高版本(`node -v` 查看)
- **npm**:随 Node.js 自带(`npm -v` 查看)
- **OpenClaw**:已安装并可运行(`openclaw --version` 确认)
- **mcporter**(可选):OpenClaw 用来连接和管理 MCP 服务器的工具

安装 OpenClaw 后,可以运行 `openclaw doctor` 检查系统健康状态,确认运行时环境正常。

## 连接 MCP 的三种方式

OpenClaw 提供了多种将 MCP 服务器接入系统的途径,适配不同技术水平和使用场景。

### 方式一:CLI 命令行添加(推荐)

这是官方推荐的最简便方式。打开终端执行以下格式的命令:

```bash
# 格式
openclaw mcp add --transport <传输协议> <服务器名称> <启动命令>

# 示例:添加本地文件系统访问
openclaw mcp add --transport stdio local-files npx -y @modelcontextprotocol/server-filesystem /Users/yourname/Documents
```

上述命令会添加一个本地文件读取工具，`/Users/yourname/Documents` 是授权 AI 访问的目录。MCP 支持两种传输协议:

- **stdio**(本地进程通信,低延迟)
- **http/SSE**(远程服务器连接,支持多客户端)

### 方式二:通过 mcporter 工具管理

mcporter 是 OpenClaw 生态中专门用于连接和管理 MCP 服务器的工具。安装方式:

```bash
npm install -g mcporter
mcporter --version
```

#### 创建 mcporter 配置文件

mcporter 通过 `mcporter.json` 文件知道有哪些 MCP 服务器。配置文件路径如下:

| 系统 | 配置文件路径 |
|------|------------|
| Windows | `C:\Users\你的用户名\.mcporter\mcporter.json` |
| macOS / Linux | `~/.mcporter/mcporter.json` |

配置文件示例:

```json
{
  "mcpServers": {
    "my-tool": {
      "command": "npx",
      "args": ["-y", "@some-mcp-package"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```

#### 在 openclaw.json 中启用 mcporter

编辑 `~/.openclaw/openclaw.json`,在 skills 部分添加 mcporter 配置:

```json
{
  "skills": {
    "entries": {
      "mcporter": {
        "enabled": true,
        "env": {
          "MCPORTER_CONFIG": "/Users/你的用户名/.mcporter/mcporter.json"
        }
      }
    }
  }
}
```

> **注意**: `MCPORTER_CONFIG` 必须写成绝对路径。Windows 路径中的反斜杠在 JSON 里需要写成 `\\`。

### 方式三:通过 openclaw-mcp-adapter 插件

openclaw-mcp-adapter 是一个将 MCP 服务器工具转换为 OpenClaw 原生工具的插件。安装方式:

```bash
openclaw plugins install mcp-adapter

# 或从源码安装
git clone https://github.com/androidStern/openclaw-mcp-adapter.git
openclaw plugins install ./openclaw-mcp-adapter
```

在 `~/.openclaw/openclaw.json` 中配置:

```json
{
  "plugins": {
    "entries": {
      "openclaw-mcp-adapter": {
        "enabled": true,
        "config": {
          "servers": [
            {
              "name": "my-mcp-server",
              "transport": "stdio",
              "command": "npx",
              "args": ["-y", "@some-mcp-package"]
            },
            {
              "name": "remote-server",
              "transport": "http",
              "url": "http://localhost:3000/mcp"
            }
          ],
          "toolPrefix": true
        }
      }
    }
  }
}
```

该插件的工作原理是:

1. 网关启动时,插件连接到每个已配置的 MCP 服务器
2. 调用 `listTools()` 发现所有可用工具
3. 将每个工具注册为 OpenClaw 的原生工具
4. 当 AI 调用工具时,插件将调用代理到 MCP 服务器
5. 连接断开后,下次工具调用时自动重连

## 将 MCP 服务器转换为 OpenClaw Skill

社区还提供了一个便捷工具,可以一行命令将任何 HTTP MCP 服务器转换为完整的 OpenClaw Skill:

```bash
npx @filiksyos/mcptoskill@latest https://mcp.example.com/mcp
```

这个命令会自动完成以下操作:

- 连接到 MCP 服务器并发现所有工具
- 生成带有描述和触发短语的 `SKILL.md`
- 创建通过 curl 调用 MCP 服务器的 Shell 脚本
- 支持 JSON 和 SSE 两种响应格式
- 自动安装到 `~/.openclaw/skills/` 并在配置中启用

## OpenClaw 作为 MCP 服务器

OpenClaw 不仅可以连接 MCP 服务器(作为客户端),它本身也可以作为 MCP 服务器,让其他 AI 系统调用。

### 连接到 Claude Desktop

通过 Docker 部署 openclaw-mcp 桥接服务器:

```yaml
services:
  mcp-bridge:
    image: ghcr.io/freema/openclaw-mcp:latest
    container_name: openclaw-mcp
    ports:
      - "3000:3000"
    environment:
      - OPENCLAW_URL=http://host.docker.internal:18789
      - OPENCLAW_GATEWAY_TOKEN=${OPENCLAW_GATEWAY_TOKEN}
      - AUTH_ENABLED=true
      - MCP_CLIENT_ID=openclaw
      - MCP_CLIENT_SECRET=${MCP_CLIENT_SECRET}
      - CORS_ORIGINS=https://claude.ai
```

在 Claude Desktop 配置中添加:

```json
{
  "mcpServers": {
    "openclaw": {
      "command": "npx",
      "args": ["openclaw-mcp"]
    }
  }
}
```

### 连接到 Cursor / Windsurf 等 IDE

在 IDE 配置文件中添加类似配置:

```json
{
  "mcp.servers": {
    "openclaw": {
      "command": "node",
      "args": ["/absolute/path/to/openclaw-mcp-server/dist/index.js"],
      "env": {
        "OPENCLAW_GATEWAY_TOKEN": "your-token-here"
      }
    }
  }
}
```

## 配置文件路径汇总

| 文件 | 路径(macOS/Linux) | 路径(Windows) | 说明 |
|------|------------------|---------------|------|
| OpenClaw 主配置 | `~/.openclaw/openclaw.json` | `C:\Users\用户名\.openclaw\openclaw.json` | 核心配置文件 |
| mcporter 配置 | `~/.mcporter/mcporter.json` | `C:\Users\用户名\.mcporter\mcporter.json` | MCP 服务器列表 |
| Skills 目录 | `~/.clawdbot/skills/` | `~/.clawdbot/skills/` | Skill 文件存放位置 |
| MCP 日志 | `~/openclaw/logs/mcp.log` | — | MCP 运行日志 |

## 网关管理

OpenClaw 的 MCP 工具需要网关(Gateway)进程正常运行才能工作。

```bash
# 启动网关
openclaw gateway

# 查看网关状态
openclaw gateway status

# 重启网关(重新加载所有 Skill 和配置)
openclaw gateway restart

# 检查系统健康状态
openclaw doctor

# 查看网关日志
openclaw gateway logs
```

修改了 `openclaw.json` 或 `mcporter.json` 后,必须重启 OpenClaw 才能使新配置生效。

## 验证与调试

### 验证 MCP 连接

配置完成后,通过以下步骤确认 MCP 已正确生效:

1. **状态查询**:运行 `openclaw status` 查看 MCP 服务器是否处于 running 状态
2. **工具列表**:运行 `mcporter list` 查看所有已连接的 MCP 服务器及工具
3. **交互验证**:在 OpenClaw 对话框中尝试发送相关指令(如"列出我授权目录下的前 5 个文件名")
4. **Skill 列表**:运行 `clawdbot skills list` 查看所有已加载的 Skill 及其状态

### 常见问题排查

| 问题 | 可能原因 | 解决方法 |
|------|---------|---------|
| `mcporter list` 提示无配置 | 配置文件路径错误或未创建 | 核对 `mcporter.json` 路径及 JSON 格式 |
| AI 说"没有配置 MCP" | 未设置 `MCPORTER_CONFIG` 或未重启 | 检查绝对路径并重启 OpenClaw |
| Tool X not found | Skill 目录错误或会话膨胀 | 确认 Skill 在 `~/.clawdbot/skills/`,使用 `/molt` 清除会话状态 |
| HTTP 400 `tool_call_id` 错误 | 网关状态损坏 | 运行 `clawdbot gateway restart` |
| `npx` 报错或超时 | npm 缓存或网络问题 | 运行 `npm cache clean --force` 或检查网络 |
| undici 错误 | Node 版本管理器(nvm/fnm)冲突 | 使用系统 Node(`nvm use system`)或官方安装脚本 |
| OAuth Token 过期 | Google OAuth 令牌约 1 小时过期 | 运行 `gog auth add email --force-consent` 强制刷新 |
| 工具初期正常后失效 | 会话膨胀导致工具 Schema 被淹没 | 保持会话短小,使用 `/molt` 或 `clawdbot molt` 清理 |

## 连接第三方 MCP 平台

### MCP360

MCP360 提供 100+ 生产级工具的统一访问端点。集成步骤:

1. 在 mcp360.ai 创建账号并生成 API Token
2. 安装 MCPorter: `npm install -g mcporter`
3. 注册 MCP360 为 MCP 服务器:提供端点 URL 和 Token
4. 运行 `mcporter config list` 确认注册
5. 运行 `mcporter list` 验证工具访问

### Latenode

Latenode 提供可视化工作流引擎,支持 1000+ 应用集成。集成方式:

1. 在 Latenode 中创建 Scenario 并添加 MCP Trigger 节点
2. 配置 Tool Name、Tool Description 和输入参数
3. 复制 Latenode 的 Server URL
4. 在 OpenClaw 中添加新的 MCP 服务器,粘贴该 URL
5. 如启用了认证,需提供 API Key

### ClawPad 桌面应用

ClawPad 是内嵌 OpenClaw 运行时的桌面应用,提供了一键安装 MCP 扩展的图形界面。通过 Extension Store 可以搜索、安装和启动 MCP 服务器(如 Filesystem MCP、Git MCP、Gmail MCP 等),无需手动编辑配置文件。

## MCP 传输协议对比

| 特性 | stdio | HTTP/SSE |
|------|-------|----------|
| 通信方式 | 本地子进程 stdin/stdout | HTTP 网络连接 |
| 延迟 | 极低(无网络栈) | 较高(网络开销) |
| 适用场景 | 本地工具集成 | 远程/分布式服务 |
| 客户端关系 | 一对一 | 支持多客户端 |
| 安全性 | 较高(无网络暴露) | 需额外配置认证 |
| 配置复杂度 | 较低 | 较高 |

选择 stdio 适合本地开发和安全敏感场景;选择 HTTP/SSE 适合需要跨设备共享或团队协作的生产环境。
