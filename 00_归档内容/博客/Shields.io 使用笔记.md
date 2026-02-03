# Shields.io 使用参考

以下是 **Shields.io** 的详细使用参考，涵盖基础用法、动态数据集成、高级自定义及常见场景示例。通过 URL 参数和模板化配置，你可以生成高度定制化的状态徽章。

## 基础语法与参数说明

Shields.io 徽章通过 URL 参数动态生成，基本格式如下：  

```text
https://img.shields.io/badge/{LABEL}-{VALUE}-{COLOR}?{OPTIONS}
```

### 1. 核心参数

- **`{LABEL}`**：左侧标签文本（如 `version`、`build`）。  
- **`{VALUE}`**：右侧数值或状态文本（如 `1.0.0`、`passing`）。  
- **`{COLOR}`**：右侧背景颜色（支持颜色名称或十六进制代码）。  
  - 预设颜色：`brightgreen`, `green`, `yellowgreen`, `yellow`, `orange`, `red`, `blue`, `lightgrey`, `success`, `important`, `critical`, `informational`, `inactive`  
  - 自定义颜色：使用 `%23` 替代 `#`（如 `%23ff0000` 表示红色）。

### 2. 常用可选参数

| 参数          | 说明                                                                 | 示例                          |
|---------------|----------------------------------------------------------------------|-------------------------------|
| `logo`        | 左侧标签前的图标（支持 [Simple Icons](https://simpleicons.org/) 名称） | `logo=github`                 |
| `logoColor`   | 图标颜色（十六进制或颜色名称）                                       | `logoColor=white`             |
| `style`       | 徽章样式（`flat`、`plastic`、`flat-square`、`for-the-badge`）         | `style=for-the-badge`         |
| `link`        | 徽章点击跳转链接                                                     | `link=https://example.com`    |
| `labelColor`  | 左侧标签背景颜色                                                     | `labelColor=%23234`           |
| `color`       | 右侧值背景颜色（等同于 `{COLOR}`，优先级更高）                        | `color=blue`                  |

---

## 基础示例

### 1. 静态徽章

```markdown
![版本](https://img.shields.io/badge/version-1.0.0-blue?logo=git&style=flat-square)
```

效果：  

![版本](https://img.shields.io/badge/version-1.0.0-blue?logo=git&style=flat-square)

### **2. 动态数据徽章**

使用预设服务获取实时数据（如 GitHub stars、npm 下载量）：

```markdown
![GitHub Stars](https://img.shields.io/github/stars/vuejs/vue?label=Stars&logo=github)
```

效果：  
![GitHub Stars](https://img.shields.io/github/stars/vuejs/vue?label=Stars&logo=github)

---

## **三、高级自定义**

### **1. 多颜色与图标组合**

```markdown
![React](https://img.shields.io/badge/React-18.2.0-%2361DAFB?logo=react&logoColor=white&style=plastic)
```

效果：  

![React](https://img.shields.io/badge/React-18.2.0-%2361DAFB?logo=react&logoColor=white&style=plastic)

### **2. 左右部分独立颜色**

```markdown
![License](https://img.shields.io/badge/License-MIT-yellowgreen?labelColor=lightgrey&logo=apache)
```

效果：  

![License](https://img.shields.io/badge/License-MIT-yellowgreen?labelColor=lightgrey&logo=apache)

### **3. 特殊字符转义**

使用 `%20` 替代空格，`%E2%98%85` 替代 Unicode 符号：

```markdown
![Rating](https://img.shields.io/badge/Rating-%E2%98%85%E2%98%85%E2%98%85%E2%98%85%E2%98%85-gold)
```

效果：  

![Rating](https://img.shields.io/badge/Rating-%E2%98%85%E2%98%85%E2%98%85%E2%98%85%E2%98%85-gold)

---

## **四、集成动态服务**

Shields.io 支持与多种开发工具和平台集成，自动生成实时数据徽章。

### **1. GitHub 相关**

| 示例                                                                 | 说明                     |
|----------------------------------------------------------------------|--------------------------|
| `https://img.shields.io/github/issues/{user}/{repo}`                 | 仓库 Issue 数量          |
| `https://img.shields.io/github/last-commit/{user}/{repo}`            | 最后提交时间             |
| `https://img.shields.io/github/license/{user}/{repo}`                | 许可证类型               |

### **2. npm 包管理**

| 示例                                                                 | 说明                     |
|----------------------------------------------------------------------|--------------------------|
| `https://img.shields.io/npm/v/{package}`                             | 包版本号                 |
| `https://img.shields.io/npm/dm/{package}`                            | 月度下载量               |
| `https://img.shields.io/npm/dt/{package}`                            | 总下载量                 |

### **3. CI/CD 构建状态**

| 示例                                                                 | 说明                     |
|----------------------------------------------------------------------|--------------------------|
| `https://img.shields.io/github/actions/workflow/status/{user}/{repo}/{workflow}.yml` | GitHub Actions 状态      |
| `https://img.shields.io/travis/{user}/{repo}`                        | Travis CI 构建状态       |

---

## **五、常用场景模板**

### **1. GitHub README 展示**

```markdown
[![GitHub License](https://img.shields.io/github/license/vuejs/vue)](https://github.com/vuejs/vue)
[![npm version](https://img.shields.io/npm/v/vue)](https://www.npmjs.com/package/vue)
[![Build Status](https://img.shields.io/github/actions/workflow/status/vuejs/vue/ci.yml)](https://github.com/vuejs/vue/actions)
```

效果：  

[![GitHub License](https://img.shields.io/github/license/vuejs/vue)](https://github.com/vuejs/vue)  
[![npm version](https://img.shields.io/npm/v/vue)](https://www.npmjs.com/package/vue)  
[![Build Status](https://img.shields.io/github/actions/workflow/status/vuejs/vue/ci.yml)](https://github.com/vuejs/vue/actions)

### **2. 文档网站头部**

```markdown
![Documentation](https://img.shields.io/badge/docs-latest-brightgreen?logo=gitbook&style=for-the-badge)
```

效果：  

![Documentation](https://img.shields.io/badge/docs-latest-brightgreen?logo=gitbook&style=for-the-badge)

---

## **六、工具与扩展**

1. **在线生成器**  

   - [Shields.io 官网](https://shields.io/)：可视化配置徽章参数并生成 URL。
   - [Badgen](https://badgen.net/)：更快的徽章生成服务，语法类似。

2. **本地开发工具**  
   - **VSCode 插件**：`Badge Tools` 可直接在编辑器内生成徽章。
   - **Python 库**：`anybadge` 支持以编程方式生成徽章。

---

## **七、注意事项**

- **缓存机制**：Shields.io 默认缓存徽章 5 分钟，可通过 `?cacheSeconds=3600` 调整。
- **速率限制**：频繁请求可能导致 IP 被暂时限制，建议本地缓存徽章图片。
- **版本兼容性**：动态服务徽章依赖平台 API，需定期检查接口变动。

---

## **总结**

Shields.io 是一个功能强大且灵活的工具，通过简单的 URL 参数即可生成专业级状态徽章。无论是展示项目健康度、集成实时数据，还是增强文档可读性，合理使用 Shields.io 都能显着提升项目的可视化效果与用户体验。