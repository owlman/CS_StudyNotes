# 微信(WeChat)

约 2203 字大约 7 分钟

2026-03-02

## 概述

微信是国内最主流的即时通讯工具。OpenClaw 支持多种方式接入微信生态。

由于微信个人号没有开放的 Bot API(不像 Telegram/Discord),无法直接原生集成。目前常用的方案有:

* 企业微信:官方支持,稳定可靠(推荐)
* 微信服务号:适合企业和组织
* 微信个人号:通过第三方桥接(实验性,有封号风险)

## 接入方式对比

| 接入方式 | 难度 | 稳定性 | 成本 | 适用场景 |
| --- | --- | --- | --- | --- |
| 企业微信 | ⭐⭐ 中等 | ✅ 高 | 免费 | 企业团队,工作协作 |
| 微信服务号 | ⭐⭐⭐ 复杂 | ✅ 高 | 需认证费 | 企业对外服务 |
| 微信个人号 | ⭐⭐ 较复杂 | ⚠️ 风险高 | 免费 | 个人使用、测试 |

> **推荐**
>
> 对于 AI 聊天机器人场景,Telegram 是目前最佳选择。微信个人号接入存在封号风险,建议优先考虑 Telegram 或企业微信。
>
> 参考:Telegram 对接指南

## 方式一:企业微信接入(推荐)

### 前置准备

* 企业微信账号(可免费注册)
* 管理员权限

### 1. 创建企业微信应用

1. 登录企业微信管理后台
2. 进入「应用管理」→「应用」→「创建应用」
3. 填写应用信息:
   * 应用名称:OpenClaw
   * 应用介绍:AI 智能助手
   * 上传应用 Logo
4. 选择可见范围(哪些成员可以使用)
5. 点击「创建应用」

### 2. 获取应用凭证

在应用详情页面获取:

* AgentId:应用 ID
* Secret:应用密钥
* CorpId:企业 ID(在「我的企业」页面)

### 3. 配置接收消息

1. 在应用详情页,找到「接收消息」配置
2. 设置接收消息服务器配置:
   * URL:https://your-domain.com/wechat/callback
   * Token:自定义令牌(用于验证)
   * EncodingAESKey:点击「随机生成」

> **提示**
>
> 如果使用本地部署,需要配置内网穿透工具(如 ngrok)获取公网地址。

### 4. 配置 OpenClaw

```
openclaw channels add
```

选择「企业微信」,输入配置信息:

```json
{
  "channels": {
    "wechat-work": {
      "enabled": true,
      "corpId": "YOUR_CORP_ID",
      "agentId": "YOUR_AGENT_ID",
      "secret": "YOUR_SECRET",
      "token": "YOUR_TOKEN",
      "encodingAESKey": "YOUR_AES_KEY"
    }
  }
}
```

### 5. 验证配置

1. 在企业微信中找到应用
2. 发送测试消息
3. 查看是否收到回复

## 方式二:微信服务号接入

### 前置准备

* 已认证的微信服务号
* 开发者权限

### 1. 配置服务器

1. 登录微信公众平台
2. 进入「开发」→「基本配置」
3. 配置服务器地址:
   * URL:https://your-domain.com/wechat/callback
   * Token:自定义令牌
   * EncodingAESKey:随机生成
   * 消息加解密方式:明文模式或安全模式

### 2. 获取凭证

在「开发」→「基本配置」中获取:

* AppID:应用 ID
* AppSecret:应用密钥

### 3. 配置 OpenClaw

```json
{
  "channels": {
    "wechat-mp": {
      "enabled": true,
      "appId": "YOUR_APP_ID",
      "appSecret": "YOUR_APP_SECRET",
      "token": "YOUR_TOKEN",
      "encodingAESKey": "YOUR_AES_KEY"
    }
  }
}
```

### 4. 配置菜单和自动回复

在公众平台后台配置:

* 自定义菜单
* 关键词自动回复
* 关注自动回复

## 方式三:微信个人号接入(社区方案)

> **重要风险提示**
>
> 微信个人号接入方案基于第三方桥接工具,存在封号风险。请严格遵守以下原则:
> 1. 建议使用小号测试,不要使用主号
> 2. 杜绝营销轰炸:严禁短时间内批量发送广告、拼团链接
> 3. 内容合规:AI 输出必须经过过滤
> 4. 定位清晰:将 AI 定义为「私人助理」而非「群发机器」
>
> **以下场景是安全的**:日程提醒、文档整理、知识问答
>
> **以下场景会导致封号**:无差别骚扰用户、频繁发送营销内容

### 方案一:通过腾讯云轻量应用服务器部署

这是目前最稳定的个人微信接入方案。

#### 1. 创建服务器实例

登录腾讯云轻量应用服务器控制台:

* 镜像:Ubuntu 22.04 LTS(推荐)或 Docker CE 镜像
* 规格:2核 2GB(建议月流量 ≥ 200GB)
* 地域:优先选择华南(广州)或华东(上海)

#### 2. 环境初始化

通过 SSH 连接服务器,安装 Docker 环境:

```bash
curl -fsSL https://get.docker.com | bash -s docker
sudo systemctl enable docker && sudo systemctl start docker
```

#### 3. 部署 OpenClaw 容器

拉取镜像并启动服务:

```bash
docker run -d \
  --name openclaw-wechat \
  -p 8080:8080 \
  -e WECHAT_API_KEY="your_api_key_here" \
  -e AI_MODEL="gpt-4o-mini" \
  openclaw/wechat-ai:latest
```

* WECHAT_API_KEY:在 OpenClaw 官网获取
* AI_MODEL:支持 GPT-4o-mini、Claude-3.5 等主流模型

#### 4. 配置 Webhook

进入 OpenClaw 管理后台,在回调地址栏填写:

```
http://你的服务器公网IP:8080/webhook
```

#### 5. 扫码绑定

浏览器访问 http://你的服务器IP:8080/qrcode,页面将显示登录二维码。

使用个人微信扫码,点击"登录网页版微信"。

控制台输出 [INFO] WeChat login success 即表示 AI 助理已上线。

#### 6. 功能验证

绑定成功后,尝试以下操作:

```
今天深圳天气怎么样?
```

或拉入群聊 @它:

```
总结以上 10 条消息
```

正常情况下,AI 会在 3 秒内生成结构化回复。

### 方案二:通过 Wechaty 接入

Wechaty 是一个开源的微信个人号接口框架。

#### 1. 安装 Wechaty

```bash
npm install wechaty wechaty-puppet-wechat
```

#### 2. 配置桥接服务

```javascript
const { WechatyBuilder } = require('wechaty')

const bot = WechatyBuilder.build({
  puppet: 'wechaty-puppet-wechat',
})

bot
  .on('scan', (qrcode) => {
    console.log('扫码登录:' + qrcode)
  })
  .on('message', async (msg) => {
    // 忽略自己发的消息
    if (msg.self()) return
    
    const text = msg.text()
    // 调用 OpenClaw 处理
    const reply = await processWithOpenClaw(text)
    await msg.say(reply)
  })

bot.start()
```

#### 3. 启动服务

```bash
node wechaty-bot.js
```

扫码登录后即可使用。

### 方案三:通过 openclaw-wechat 插件接入(社区方案)

这是社区开发者(freestylefly)开发的微信插件,提供了更稳定的微信个人号接入方案。

项目地址:https://github.com/freestylefly/openclaw-wechat

功能特点:

* 支持私聊与群聊
* 支持文字与图片收发
* 二维码扫码登录流程
* SDK 级上下文记忆
* 语音转文字(FunASR/微信)
* 多账号支持

#### 1. 安装插件

```bash
openclaw plugins install @canghe/openclaw-wechat
```

#### 2. 配置插件

```bash
# 设置 API Key(必填)
openclaw config set channels.wechat.apiKey "wc_live_xxxxxxxxxxxxxxxx"

# 设置代理服务地址(必填)
openclaw config set channels.wechat.proxyUrl "http://你的代理服务器:3000"

# 设置 webhook 公网地址(云服务器部署必填)
openclaw config set channels.wechat.webhookHost "你的服务器IP"

# 启用通道
openclaw config set channels.wechat.enabled true
```

#### 3. 配置选项说明

完整的配置文件 ~/.openclaw/openclaw.json:

```yaml
channels:
  wechat:
    enabled: true
    apiKey: "wc_live_xxxxxxxxxxxxxxxx"        # 必填
    proxyUrl: "http://你的代理:3000"           # 必填 - 代理服务地址
    
    # Webhook 配置(云服务器部署必填)
    webhookHost: "1.2.3.4"                    # 服务器公网 IP 或域名
    webhookPort: 18790                        # 默认: 18790
    webhookPath: "/webhook/wechat"            # 默认: /webhook/wechat
    
    # 可选配置
    deviceType: "mac"                         # "ipad" 或 "mac",默认: "ipad"
```

| 选项 | 必填 | 说明 |
| --- | --- | --- |
| apiKey | ✅ | 微信 API Key |
| proxyUrl | ✅ | 代理服务地址 |
| webhookHost | ✅ | 服务器公网 IP 或域名 |
| webhookPort | - | 默认:18790 |
| webhookPath | - | 默认:/webhook/wechat |
| deviceType | - | 设备类型:ipad 或 mac,默认 ipad |

#### 4. 升级插件

```bash
openclaw plugins update wechat
```

#### 5. 首次登录

首次启动 gateway 时会显示二维码,用微信扫码登录:

```bash
openclaw gateway start
```

#### 6. 多账号支持

```yaml
channels:
  wechat:
    accounts:
      work:
        apiKey: "wc_live_work_xxx"
        webhookHost: "1.2.3.4"
      personal:
        apiKey: "wc_live_personal_xxx"
        webhookHost: "1.2.3.4"
```

#### 7. 常见问题

**机器人收不到消息?**

1. 确保 webhookHost 配置了服务器的公网 IP
2. 确保 webhookPort 端口可从外网访问
3. 检查 gateway 是否运行:openclaw gateway status

**获取 API Key**

项目优化中,需要体验的可以先进群等待。详情请访问:openclaw-wechat GitHub

## 常见问题

### Q: 企业微信和个人微信有什么区别?

* 企业微信:官方支持,稳定可靠,适合企业使用
* 个人微信:通过第三方桥接,可能存在封号风险

### Q: 如何获取用户 ID?

企业微信:在管理后台「通讯录」中查看成员 ID

### Q: 消息发送失败怎么办?

1. 检查应用凭证是否正确
2. 确认服务器 URL 可访问
3. 查看 OpenClaw 日志
4. 检查用户是否在可见范围内

### Q: 如何处理图片和文件?

OpenClaw 会自动下载并处理:

```
// 图片识别
@OpenClaw 这张图片是什么?

// 文件分析
@OpenClaw 帮我分析这个文档
```

### Q: 支持语音消息吗?

支持,OpenClaw 会自动将语音转为文字处理。

### Q: 登录失败怎么办?

* 等待 24 小时后重试
* 换一个微信号测试

## 限制说明

### 企业微信限制

* 消息发送频率:每分钟最多 200 条
* 文件大小:最大 20MB
* 群成员数量:最多 500 人

### 服务号限制

* 主动消息:需要用户 48 小时内互动
* 模板消息:需要用户授权
* 接口调用:有频率限制

## 相关资源

* 企业微信开发文档
* 微信公众平台文档
* Wechaty 文档
* 腾讯云轻量应用服务器
* Telegram 对接指南
* 飞书对接指南

---

原文链接: https://openclawgithub.cc/guide/channels/wechat