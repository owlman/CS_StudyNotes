---
title: 补充 OpenClaw
author: 凌杰
date: 2026-04-01
tags: OpenClaw
categories: 软件使用经验
---

> [!NOTE] 笔记说明
>
> 尽管，我已经在之前的 Agent 系列笔记中介绍过了 OpenClaw 中的一些通用于所有 Agent 的使用方法，但为了让[这个笔记库](https://github.com/owlman/CS_StudyNotes)中记录的知识更为系统，我决定再写一篇补充性的笔记，用于记录那些独属于 OpenClaw 的使用经验，并予以长期维护。

正如我在《[[Agent 的基础应用]]》一文中所介绍的，OpenClaw 是一款可部署在服务器上的 AI Agent，它拥有强大的自动化操作能力，支持通过接入 Telegram、Whatsapp、飞书等即时通讯软件来进行远程操控计算机，颇受业界人士喜欢。但是，由于该项目目前版本更新频繁，一些操作命令经常会发生细微的变化，而官方文档更新又不够不及时，导致我们在使用过程中经常会遇到各种问题。因此，本文将整理它的一些常用配置与应用场景，以作为 Agent 系列笔记的补充。

## 接入 IM

### 接入 Whatsapp

### 接入飞书

### 接入微信

## 服务端维护

### 网关重启

```bash
# 重启
systemctl --user restart openclaw-gateway
# 查看日志
journalctl --user -u openclaw-gateway.service -f
```

或者

```bash
openclaw gateway restart
```

### 版本升级

```bash
openclaw update
```

### 修复

如果出了小问题，只要程序本身还没彻底坏，可以执行如下命令让他自己修复:

```bash
openclaw doctor --fix
```

之后它会帮你修改配置文件

* Updated ~/.openclaw/openclaw.json
* Backup: ~/.openclaw/openclaw.json.bak

### 自我学习


<!-- 以下待整理 -->

### 启动新手安装向导

```bash
openclaw onboard --install-daemon
```

### 安装后台服务

```bash
openclaw gateway install
```

该命令会生成`~/appinn/.config/systemd/user/openclaw-gateway.service`自启动配置文件。

### 启动配置向导

```bash
openclaw configure
```

虽然我们也可以直接修改配置文件，但使用向导配置是最稳的。

### 配对控制台

```bash
openclaw devices list
openclaw devices approve <requestId>
openclaw devices reject <requestId>
```

list 之后可以看到 id，然后在运行第二行就行了。



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
