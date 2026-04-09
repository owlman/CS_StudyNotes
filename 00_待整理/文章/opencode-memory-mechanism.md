# Sisyphus 记忆机制详解

## 概述

Sisyphus 是我在 OpenCode 中的代号，采用多层次记忆机制来实现跨会话的持久化和上下文保持。

---

## 一、Todo 列表 (任务追踪)

**工具**: `todowrite`

Sisyphus 使用 Todo 列表来跟踪复杂任务的进度。

### 核心操作

| 操作 | 状态值 |
|------|--------|
| 创建任务 | `pending` |
| 开始执行 | `in_progress` |
| 任务完成 | `completed` |
| 任务取消 | `cancelled` |

### 特性

- 支持优先级标记：`high`, `medium`, `low`
- 每个任务包含：`content`（任务内容）、`status`、`priority`
- **实时更新**：每完成一个逻辑单元立即标记为 `completed`，绝不批量确认
- **单线程执行**：同一时间只允许一个 `in_progress` 状态的任务

---

## 二、Session 系统 (跨会话记忆)

**工具**: `session_list`, `session_read`, `session_search`, `session_info`

Session 是我最重要的记忆载体，实现了真正的跨对话上下文保持。

### 2.1 Session 信息存储

每次对话都会生成一个唯一的 `session_id`（格式：`ses_xxx`），包含：

- **消息数量**: 对话中的消息总数
- **日期范围**: 对话开始和结束时间
- **使用的 Agent**: build、oracle、librarian 等
- **Todo 列表**: 任务追踪数据
- **Transcript**: 完整的对话日志

### 2.2 核心能力

#### `session_list` - 列举所有会话

```
返回：session_id | 消息数 | 日期 | 使用的 Agents
```

#### `session_read` - 读取完整会话
```
参数：
- session_id: 必填
- include_todos: 是否包含 Todo
- include_transcript: 是否包含完整日志
- limit: 消息数量限制
```

#### `session_search` - 全文检索
```
参数：
- query: 搜索关键词
- session_id: 可选（限定会话）
- case_sensitive: 大小写敏感
- limit: 结果数量
```

#### `session_info` - 获取元数据
```
返回：会话统计信息、Agents 使用情况、Todo 状态
```

### 2.3 Session 续接机制

**关键特性**：通过 `session_id` 可在新对话中无缝续接历史上下文：

```
task(session_id="ses_abc123", prompt="继续上次的实现...")
```

这使得：
- 长线任务无需重复说明背景
- Agent 具有完整的历史记忆
- 节省 70%+ 的 Token 消耗

---

## 三、工作计划 (Plan 文件)

**路径**: `.sisyphus/plans/*.md`

### 触发场景
当用户请求的工作需要保存为计划文件时，Sisyphus 会：
1. 将详细的工作计划写入 `.sisyphus/plans/` 目录
2. 使用 `task(subagent_type="momus", prompt=".sisyphus/plans/xxx.md")` 唤起 Momus Agent 审核

### 计划内容结构
- 任务分解与并行化建议
- 每个步骤的验收标准
- 依赖关系与执行顺序

---

## 四、后台任务系统

**工具**: `background_output`, `background_cancel`

### 并行执行
Sisyphus 默认并行化所有独立任务：
- 多个 Explore/Librarian Agent 同时运行
- 独立文件读取并行执行
- 使用 `run_in_background=true` 启动异步任务

### 结果收集
```
1. 启动并行 Agent → 获得 task_id
2. 继续非重叠工作
3. 等待系统通知（<system-reminder>）
4. 调用 background_output(task_id) 获取结果
```

### 取消机制
```
background_cancel(taskId="xxx")  # 取消特定任务
background_cancel(all=true)      # ❌ 禁止使用
```

⚠️ **重要**：从不使用 `all=true`，必须逐个取消

---

## 五、Agent 系统架构

| Agent | 用途 | 成本 |
|-------|------|------|
| `explore` | 内部代码库搜索 | 免费 |
| `librarian` | 外部文档/OSS搜索 | 低 |
| `oracle` | 架构决策/高阶咨询 | 高 |
| `metis` | 预规划分析 | 高 |
| `momus` | 计划审核 | 高 |

---

## 六、记忆流程图

```
用户输入
    │
    ▼
┌─────────────────────────┐
│  Intent Gate (意图分类)  │
│  - Trivial / Explicit   │
│  - Exploratory / Open   │
│  - Ambiguous            │
└─────────────────────────┘
    │
    ▼
┌─────────────────────────┐
│     Context Check        │
│  1. Session 续接?        │
│  2. Todo 状态同步?       │
│  3. 计划文件存在?        │
└─────────────────────────┘
    │
    ├─── 需要 Research ───→ Explore + Librarian (并行)
    │
    ├─── 需要规划 ───────→ Metis / Momus
    │
    └─── 需要实现 ───────→ 任务分解 → Todo 追踪 → Agent 委托
```

---

## 七、最佳实践

### 保持记忆连贯

1. **长线任务**：保存 `session_id`，下次继续时传入
2. **复杂项目**：使用 Todo 列表分解，每步标记状态
3. **计划文档**：重要决策写入 `.sisyphus/plans/`

### 避免记忆断裂

1. 不要在一个 Session 中混杂不相关的任务
2. 重要中间结果及时记录到文件
3. 使用 `session_search` 验证历史上下文

---

*文档版本: 1.0*  
*更新日期: 2026-04-06*
