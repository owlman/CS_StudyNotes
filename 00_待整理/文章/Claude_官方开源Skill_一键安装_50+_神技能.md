# Claude 官方开源Skill：一键安装 50+ 神技能，再也不用手写 Prompt！

> 来源：知乎
> 链接：https://zhuanlan.zhihu.com/p/1998758838342547118

上一篇文章《继续堆 Prompt，真的不如早点学 Skill》我们聊了 AI 工作流革命：Prompt → MCP → Skill，为什么 Skill 才是当前最实用的降本增效方案（节省 60-80% Token、一致性拉满、可复用沉淀）。很多人留言问："Skill 听起来牛，但到底从哪入手？不会写代码的程序员也能玩吗？"

今天就直接上手最权威的起点：**Anthropic 官方的 Skills 仓库** → [anthropics/skills](https://github.com/anthropics/skills)

这个库是 Claude Skills 的「官方示范包」，里面放了 50+ 个高质量、可直接用的技能示例。安装后，Claude 瞬间变身你的专属「文档专家」「代码测试员」「创意设计师」……再也不用每次狂塞长 prompt 了。

读完这篇，你就能在 15 分钟内把官方 Skills 装进 Claude Code / Claude.ai，立马感受到「AI 记住你工作方式」的高效体验。

---

## 一、为什么先装官方 anthropics/skills？（新手必备理由）

上一篇文章对比表里提到，Skill 的核心是「渐进式加载 + 可组合知识包」。官方这个库完美诠释：

- **权威标准**：Anthropic 自己维护，格式最规范，Claude 加载最稳。
- **覆盖广**：创意（艺术/音乐/设计）、开发（web 测试/服务器生成）、企业（品牌/沟通）、文档（docx/pdf/pptx/xlsx 创建&编辑）全都有。
- **开源友好**：大部分 Apache 2.0 许可，可 fork 修改；文档技能 source-available，供参考。
- **演示价值高**：每个技能都是文件夹 + SKILL.md（含 YAML 元数据 + 详细指令 + 示例），一看就懂怎么自己写。
- **社区反馈**：GitHub 上很多人 clone 后直接当「打底包」，再叠社区的 superpowers 等。

一句话：新手先 clone 官方仓库，熟悉格式 + 快速上手；进阶用户拿它当模板，自定义专属技能。

> Claude Skills 执行流程图（渐进式加载）

这张图展示了 Skills 如何动态加载：Claude 先读简短描述，需要时再拉完整内容，Token 省到飞起。

---

## 二、官方 Skills 库里有哪些好用的技能？（亮点速览）

仓库结构简单：`./skills` 下按类别分文件夹，每个文件夹就是一个独立技能。

核心亮点技能分类（基于 README 和社区实测）：

### 文档技能（Document Skills） → 最实用，企业/程序员必装
- pdf / docx / pptx / xlsx：一键创建、编辑、提取表格/表单/图表。
- 示例：上传 PDF 说"用 PDF skill 提取所有表单字段并转成 Excel"，Claude 自动处理。

### 开发 & 技术技能（Development & Technical）
- **web-app-testing**：自动化测试 web 应用。
- **server-generation**：生成服务器配置/部署脚本。
- 适合后端/DevOps 同学，帮你标准化重复任务。

### 创意 & 设计技能（Creative & Design）
- **algorithmic-art** / music / design：生成算法艺术、音乐提示、UI 设计规范。
- 前端/产品同学可以用它快速 brainstorm 视觉方案。

### 企业 & 沟通技能（Enterprise & Communication）
- **branding** / communications：按品牌指南写邮件/报告/提案。
- 职场人士的福音：风格一致性直接拉满。

### 元技能（Meta Skills）
- **skill-creator**：让 Claude 帮你一步步创建新技能！零基础神器。

仓库还有 `./template`（新建技能模板）和 `./spec`（Skills 标准规范），想深入的同学可以直接参考。

实际就长这样：一个文件夹 + SKILL.md，超级简单、可版本控制。

---

## 三、怎么安装 & 使用？（Claude Code / Claude.ai 实操步骤）

前提：确保你的 Claude 账号已开启 Skills（Settings > Capabilities > Skills 打开；Code execution 和 file creation 也启用）。

### 方法1：Claude Code（推荐，程序员最爽）

1. 打开 Claude Code 终端/界面。
2. 添加仓库为插件市场（或直接 clone）：

```bash
git clone https://github.com/anthropics/skills.git
```

3. 把 skills 文件夹 copy 到 `~/.claude/skills/` 或项目 `.claude/skills/`
4. Claude Code 会自动扫描并加载。
5. 使用：在对话里直接提技能名或描述，例如：
   - "Use the PDF skill to summarize this report.pdf"
   - 或如果有 slash：`/pdf extract-tables file.pdf`

> Claude Code 集成 Skills 示例界面

安装完成后，Claude 会自动发现并在需要时加载，非常方便。

### 方法2：Claude.ai（网页版，付费计划）

1. 去 Settings > Capabilities > Skills。
2. 点击 "Upload Skill" 或拖拽整个技能文件夹（zip 打包）。
3. 上传后，在对话中提到技能名或描述，Claude 就会用。

小 Tips：先装 skill-creator，用它对话让 Claude 帮你改/建新技能，超级 meta。

---

## 四、结语：官方 Skills 是你的生产力"作弊码"

上一篇文章我们说 Skill 是「教 AI 成为专家」，今天 anthropics/skills 就是最好的教材和起点。

花 15 分钟安装它，你会发现：Claude 不再是「聪明但健忘」的聊天机器人，而是真正记住你风格、流程的数字搭档。

行动起来吧！先 clone 仓库，装 document-skills，试试让 Claude 帮你处理个 PDF/Excel，看看省了多少时间。

你装了哪些技能？最爽的是哪个？评论区交流，我们下篇继续聊怎么自己写 Skill～

---

个人博客：[小贺的博客](https://xiaohev.com/)（更多技术干货）

### 历史文章
- 知乎：相关文章链接
