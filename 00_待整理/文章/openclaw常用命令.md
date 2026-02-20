# OpenClaw 常用命令[持续更新]

OpenClaw 好用也不好用,开始配置时,遇到了一堆不会的东西,慢慢熟悉。

青小蛙折腾了三天了,基本上跑起来了,也碰到不少坑。

核心就一点:在安装完成之后,首选 Qwen 登录,先让他跑起来,后面遇到问题了,只要服务不挂,就可以让它自己修复 😂

以下是青小蛙这两天使用时,记录下来的一些,持续更新

## 安装

是的,一行就行了。但是因为 OpenClaw 拥有管理员权限,建议不要使用人类电脑,而是给他一个隔离的、虚拟的电脑,比如 VPS、虚拟机等等。

```bash
# macOS / Linux
curl -fsSL https://openclaw.ai/install.sh | bash

# Windows(不建议,推荐在 wsl 中使用)
iwr -useb https://openclaw.ai/install.ps1 | iex
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

## 当前的 OpenClaw 操作建议

虽然 OpenClaw 带着自动化操作的名头,但它目前已久是一款强命令行工具,很多操作避免不了在终端中操作,所以还是要对此有耐心。
