# OpenClaw 常用命令

尽管，OpenClaw 是一款可部署在服务器上的 AI Agent，它拥有强大的自动化操作能力，支持通过接入 Telegram、Whatsapp、飞书等即时通讯软件来进行远程操控计算机，颇受业界人士喜欢。但是，由于该项目目前版本更新频繁，一些操作命令经常会发生细微的变化，而官方文档更新又不够不及时，导致我们在使用过程中经常会遇到各种问题。因此，本文将整理它一些常用的命令，并将其维护在 GitHub 上，以便日常参考。

## 安装命令

```bash
# 使用 Bash 安装（MacOS/Linux/WSL）
curl -fsSL https://openclaw.ai/install.sh | bash

# 使用 PowerShell 安装（Windows）
iwr -useb https://openclaw.ai/install.ps1 | iex

# 使用 NPM 安装
npm i -g @openclaw/cli
```

### 安装后台服务

```bash
openclaw gateway install
```

他会生成 /home/appinn/.config/systemd/user/openclaw-gateway.service 自启动配置文件

### 后台启动(兼基础向导)

```bash
openclaw onboard --install-daemon
```

### 配置向导

```bash
openclaw configure
```

虽然可以直接修改配置文件,但使用向导配置是最稳的。

### 配对控制台

```bash
openclaw devices list
openclaw devices approve <requestId>
openclaw devices reject <requestId>
```

list 之后可以看到 id,然后在运行第二行就行了。

## 使用浏览器链接

这个时候,就可以使用 http://127.0.0.1:18789 打开你的 OpenClaw 了。

## 维护

### 重启

```bash
#重启
systemctl --user restart openclaw-gateway
#查看日志
journalctl --user -u openclaw-gateway.service -f
```

或者

```bash
openclaw gateway restart
```

### 升级

```bash
openclaw update
```

### 修复

如果出了小问题,但还没彻底坏,可以让他自己修复:

```bash
openclaw doctor --fix
```

之后它会帮你修改配置文件

* Updated ~/.openclaw/openclaw.json
* Backup: ~/.openclaw/openclaw.json.bak

## Telegram 频道配置

在 ~/.openclaw/openclaw.json 文件中,编辑 channels 的部分,加入 proxy 即可:

```json
"channels": {
  "telegram": {
    "enabled": true,
    "dmPolicy": "pairing",
    "botToken": ":",
    "groupPolicy": "allowlist",
    "streamMode": "partial",
    "proxy": "http://127.0.0.1:7890"
  }
},
```

## 日常使用

### 切换模型

我觉得那个 Web 配置页面里添加模型十分难用,可以直接让机器人帮你添加模型,然后再使用命令行切换(或者跟 bot 说切换)

```bash
# 列出所有模型
openclaw models
# 设置模型 <模型名称>
openclaw models set <openrouter/auto>
```

### 启动 TUI 模式(在终端对话)

有时候在升级维护时,或者 bot 坏了的时候,可以直接在终端对话

```bash
openclaw tui
```

## 升级

OpenClaw 基本上保持着日更的节奏,想要跟上最新功能,最好的办法是直接升级。

放心升级不会破坏你此前的设置,只需要:

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

运行重新安装即可。

## 错误检查

一旦遇到问题,不要慌,只需要运行:

```bash
openclaw doctor --fix
```

它就会帮你自动检测、自动修复,多数情况下就好了。少部分情况会搞砸,不过跟着页面的错误提示,也能修好😂

## 查看当前状态

```bash
openclaw status
```

