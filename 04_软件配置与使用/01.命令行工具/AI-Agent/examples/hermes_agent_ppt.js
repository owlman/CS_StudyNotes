const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.author = '凌杰';
pres.title = '关于 Hermes Agent';

// Color palette - Midnight Executive
const COLORS = {
  primary: "1E2761",      // Navy
  secondary: "CADCFC",    // Ice blue
  accent: "0891B2",       // Teal accent
  white: "FFFFFF",
  dark: "0F172A",         // Dark slate
  text: "1E293B",          // Body text
  muted: "64748B",         // Muted text
  lightBg: "F8FAFC"        // Light background
};

// Helper for shadows
const makeShadow = () => ({ type: "outer", blur: 6, offset: 2, angle: 135, color: "000000", opacity: 0.12 });

// ============ SLIDE 1: Title Slide ============
let slide1 = pres.addSlide();
slide1.background = { color: COLORS.primary };

// Decorative accent bar at top
slide1.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.08, fill: { color: COLORS.accent }
});

// Title
slide1.addText("关于 Hermes Agent", {
  x: 0.5, y: 1.8, w: 9, h: 1.2,
  fontSize: 48, fontFace: "Arial Black", color: COLORS.white,
  align: "center", valign: "middle"
});

// Subtitle
slide1.addText("新一代智能代理框架", {
  x: 0.5, y: 3.1, w: 9, h: 0.6,
  fontSize: 24, fontFace: "Calibri", color: COLORS.secondary,
  align: "center", valign: "middle"
});

// Author info
slide1.addText("凌杰 | 2026-05-05", {
  x: 0.5, y: 4.8, w: 9, h: 0.4,
  fontSize: 14, fontFace: "Calibri", color: COLORS.muted,
  align: "center", valign: "middle"
});

// Bottom accent line
slide1.addShape(pres.shapes.RECTANGLE, {
  x: 3.5, y: 4.5, w: 3, h: 0.04, fill: { color: COLORS.accent }
});

// ============ SLIDE 2: Overview ============
let slide2 = pres.addSlide();
slide2.background = { color: COLORS.lightBg };

// Header bar
slide2.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.9, fill: { color: COLORS.primary }
});
slide2.addText("概述", {
  x: 0.5, y: 0.2, w: 9, h: 0.5,
  fontSize: 28, fontFace: "Arial Black", color: COLORS.white, margin: 0
});

// Key stats in cards
const stats = [
  { value: "2.2万+", label: "首月 Stars" },
  { value: "9500", label: "周均新增 Stars" },
  { value: "3x", label: "增速领先同类" }
];

stats.forEach((stat, i) => {
  const x = 0.7 + i * 3.1;
  slide2.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 1.2, w: 2.8, h: 1.4,
    fill: { color: COLORS.white }, shadow: makeShadow()
  });
  slide2.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 1.2, w: 0.08, h: 1.4, fill: { color: COLORS.accent }
  });
  slide2.addText(stat.value, {
    x: x + 0.2, y: 1.3, w: 2.4, h: 0.7,
    fontSize: 32, fontFace: "Arial Black", color: COLORS.primary, margin: 0
  });
  slide2.addText(stat.label, {
    x: x + 0.2, y: 2.0, w: 2.4, h: 0.4,
    fontSize: 12, fontFace: "Calibri", color: COLORS.muted, margin: 0
  });
});

// Description
slide2.addText("Hermes Agent 于 2026 年 2 月由 Nous Research 公司发布，\n构建了「记忆-技能-训练数据」的三层闭环体系。", {
  x: 0.5, y: 2.9, w: 9, h: 0.8,
  fontSize: 16, fontFace: "Calibri", color: COLORS.text, align: "center"
});

// Core features preview
slide2.addText("核心特性预览", {
  x: 0.5, y: 3.8, w: 9, h: 0.4,
  fontSize: 14, fontFace: "Arial Black", color: COLORS.primary, margin: 0
});

const features = ["分层记忆系统", "可扩展 Skills", "多平台接入", "自我迭代"];
features.forEach((f, i) => {
  const x = 0.7 + i * 2.3;
  slide2.addShape(pres.shapes.OVAL, {
    x: x, y: 4.3, w: 0.25, h: 0.25, fill: { color: COLORS.accent }
  });
  slide2.addText(f, {
    x: x + 0.35, y: 4.28, w: 2, h: 0.3,
    fontSize: 13, fontFace: "Calibri", color: COLORS.text, margin: 0
  });
});

// ============ SLIDE 3: Memory System L1 & L2 ============
let slide3 = pres.addSlide();
slide3.background = { color: COLORS.lightBg };

slide3.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.9, fill: { color: COLORS.primary }
});
slide3.addText("分层设计的记忆系统", {
  x: 0.5, y: 0.2, w: 9, h: 0.5,
  fontSize: 28, fontFace: "Arial Black", color: COLORS.white, margin: 0
});

// L1 Card
slide3.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.2, w: 4.3, h: 2.0,
  fill: { color: COLORS.white }, shadow: makeShadow()
});
slide3.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.2, w: 4.3, h: 0.5, fill: { color: COLORS.primary }
});
slide3.addText("L1 核心记忆", {
  x: 0.7, y: 1.25, w: 4, h: 0.4,
  fontSize: 16, fontFace: "Arial Black", color: COLORS.white, margin: 0
});
slide3.addText([
  { text: "存储于 MEMORY.md 文件", options: { breakLine: true } },
  { text: "容量限制：800 tokens", options: { breakLine: true } },
  { text: "会话启动时冻结为快照", options: { breakLine: true } },
  { text: "精准保留核心上下文", options: {} }
], {
  x: 0.7, y: 1.85, w: 3.9, h: 1.2,
  fontSize: 12, fontFace: "Calibri", color: COLORS.text, margin: 0
});

// L2 Card
slide3.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.2, w: 4.3, h: 2.0,
  fill: { color: COLORS.white }, shadow: makeShadow()
});
slide3.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.2, w: 4.3, h: 0.5, fill: { color: "0891B2" }
});
slide3.addText("L2 用户画像", {
  x: 5.4, y: 1.25, w: 4, h: 0.4,
  fontSize: 16, fontFace: "Arial Black", color: COLORS.white, margin: 0
});
slide3.addText([
  { text: "存储于 USER.md 文件", options: { breakLine: true } },
  { text: "容量约 500 tokens", options: { breakLine: true } },
  { text: "记录技术栈偏好", options: { breakLine: true } },
  { text: "分析沟通风格偏好", options: {} }
], {
  x: 5.4, y: 1.85, w: 3.9, h: 1.2,
  fontSize: 12, fontFace: "Calibri", color: COLORS.text, margin: 0
});

// L3 & L4 Cards
// L3 Card
slide3.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.4, w: 4.3, h: 2.0,
  fill: { color: COLORS.white }, shadow: makeShadow()
});
slide3.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.4, w: 4.3, h: 0.5, fill: { color: "10B981" }
});
slide3.addText("L3 会话记忆", {
  x: 0.7, y: 3.45, w: 4, h: 0.4,
  fontSize: 16, fontFace: "Arial Black", color: COLORS.white, margin: 0
});
slide3.addText([
  { text: "全量存储于 SQLite 数据库", options: { breakLine: true } },
  { text: "FTS5 全文索引支持", options: { breakLine: true } },
  { text: "毫秒级检索", options: { breakLine: true } },
  { text: "按需查询，不主动加载", options: {} }
], {
  x: 0.7, y: 4.05, w: 3.9, h: 1.2,
  fontSize: 12, fontFace: "Calibri", color: COLORS.text, margin: 0
});

// L4 Card
slide3.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 3.4, w: 4.3, h: 2.0,
  fill: { color: COLORS.white }, shadow: makeShadow()
});
slide3.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 3.4, w: 4.3, h: 0.5, fill: { color: "8B5CF6" }
});
slide3.addText("L4 技能系统", {
  x: 5.4, y: 3.45, w: 4, h: 0.4,
  fontSize: 16, fontFace: "Arial Black", color: COLORS.white, margin: 0
});
slide3.addText([
  { text: "存储于 ~/.hermes/skills/", options: { breakLine: true } },
  { text: "自动提炼可复用 SKILL.md", options: { breakLine: true } },
  { text: "持续迭代优化", options: { breakLine: true } },
  { text: "跨会话能力沉淀", options: {} }
], {
  x: 5.4, y: 4.05, w: 3.9, h: 1.2,
  fontSize: 12, fontFace: "Calibri", color: COLORS.text, margin: 0
});

// ============ SLIDE 4: Skills Framework ============
let slide4 = pres.addSlide();
slide4.background = { color: COLORS.lightBg };

slide4.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.9, fill: { color: COLORS.primary }
});
slide4.addText("可扩展的 Skills 框架", {
  x: 0.5, y: 0.2, w: 9, h: 0.5,
  fontSize: 28, fontFace: "Arial Black", color: COLORS.white, margin: 0
});

// Core features
const skillsFeatures = [
  { title: "持续优化机制", desc: "基于 DSPy 和 GEPA 算法，自动优化 Skills 库" },
  { title: "标准化格式", desc: "遵循 agentskills.io 规范，SKILL.md 定义" },
  { title: "70+ 内置 Skills", desc: "覆盖 15+ 类别，支持第三方扩展" },
  { title: "安全审批机制", desc: "支持 /approve session 安全隔离" }
];

skillsFeatures.forEach((item, i) => {
  const y = 1.2 + i * 1.05;
  slide4.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: y, w: 9, h: 0.9,
    fill: { color: COLORS.white }, shadow: makeShadow()
  });
  slide4.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: y, w: 0.08, h: 0.9, fill: { color: COLORS.accent }
  });
  slide4.addText(item.title, {
    x: 0.8, y: y + 0.1, w: 3, h: 0.35,
    fontSize: 15, fontFace: "Arial Black", color: COLORS.primary, margin: 0
  });
  slide4.addText(item.desc, {
    x: 0.8, y: y + 0.45, w: 8.5, h: 0.35,
    fontSize: 12, fontFace: "Calibri", color: COLORS.muted, margin: 0
  });
});

// ============ SLIDE 5: Core Capabilities ============
let slide5 = pres.addSlide();
slide5.background = { color: COLORS.lightBg };

slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.9, fill: { color: COLORS.primary }
});
slide5.addText("核心能力", {
  x: 0.5, y: 0.2, w: 9, h: 0.5,
  fontSize: 28, fontFace: "Arial Black", color: COLORS.white, margin: 0
});

const capabilities = [
  { title: "持久化记忆", desc: "跨会话持久存储用户偏好和高频操作" },
  { title: "反馈式学习", desc: "实时根据用户的评价调整策略" },
  { title: "智能化执行", desc: "执行复杂任务，如写 Proposal、调用外部接口" },
  { title: "自动化沉淀", desc: "将临时任务转化为可复用的标准化技能" },
  { title: "定时/触发任务", desc: "支持 Cron 表达式或事件的自动化工作流" }
];

capabilities.forEach((item, i) => {
  const row = Math.floor(i / 2);
  const col = i % 2;
  const x = 0.5 + col * 4.7;
  const y = 1.15 + row * 1.4;

  slide5.addShape(pres.shapes.RECTANGLE, {
    x: x, y: y, w: 4.4, h: 1.2,
    fill: { color: COLORS.white }, shadow: makeShadow()
  });

  // Number circle
  slide5.addShape(pres.shapes.OVAL, {
    x: x + 0.2, y: y + 0.35, w: 0.5, h: 0.5, fill: { color: COLORS.accent }
  });
  slide5.addText(String(i + 1), {
    x: x + 0.2, y: y + 0.35, w: 0.5, h: 0.5,
    fontSize: 16, fontFace: "Arial Black", color: COLORS.white,
    align: "center", valign: "middle", margin: 0
  });

  slide5.addText(item.title, {
    x: x + 0.9, y: y + 0.2, w: 3.3, h: 0.4,
    fontSize: 14, fontFace: "Arial Black", color: COLORS.primary, margin: 0
  });
  slide5.addText(item.desc, {
    x: x + 0.9, y: y + 0.6, w: 3.3, h: 0.5,
    fontSize: 11, fontFace: "Calibri", color: COLORS.muted, margin: 0
  });
});

// ============ SLIDE 6: Comparison ============
let slide6 = pres.addSlide();
slide6.background = { color: COLORS.lightBg };

slide6.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.9, fill: { color: COLORS.primary }
});
slide6.addText("Hermes Agent vs OpenClaw", {
  x: 0.5, y: 0.2, w: 9, h: 0.5,
  fontSize: 28, fontFace: "Arial Black", color: COLORS.white, margin: 0
});

// Comparison table
const tableData = [
  [
    { text: "维度", options: { fill: { color: COLORS.primary }, color: COLORS.white, bold: true, align: "center" } },
    { text: "Hermes Agent", options: { fill: { color: COLORS.primary }, color: COLORS.white, bold: true, align: "center" } },
    { text: "OpenClaw", options: { fill: { color: COLORS.primary }, color: COLORS.white, bold: true, align: "center" } }
  ],
  [
    { text: "技能定义", options: { fill: { color: COLORS.secondary }, color: COLORS.text, bold: true } },
    { text: "Agent 自动生成并优化", options: { fill: { color: COLORS.white } } },
    { text: "需人工编写指令规则", options: { fill: { color: COLORS.white } } }
  ],
  [
    { text: "记忆机制", options: { fill: { color: COLORS.secondary }, color: COLORS.text, bold: true } },
    { text: "持久化分层存储", options: { fill: { color: COLORS.white } } },
    { text: "需借助外部扩展", options: { fill: { color: COLORS.white } } }
  ],
  [
    { text: "安全机制", options: { fill: { color: COLORS.secondary }, color: COLORS.text, bold: true } },
    { text: "内置安全审批与隔离", options: { fill: { color: COLORS.white } } },
    { text: "需后期人工维护", options: { fill: { color: COLORS.white } } }
  ],
  [
    { text: "角色定位", options: { fill: { color: COLORS.secondary }, color: COLORS.text, bold: true } },
    { text: "面向长期能力沉淀", options: { fill: { color: COLORS.white } } },
    { text: "偏向工具编排框架", options: { fill: { color: COLORS.white } } }
  ]
];

slide6.addTable(tableData, {
  x: 0.5, y: 1.2, w: 9, h: 4.2,
  colW: [2, 3.5, 3.5],
  fontFace: "Calibri",
  fontSize: 13,
  color: COLORS.text,
  border: { pt: 0.5, color: COLORS.secondary },
  valign: "middle"
});

// ============ SLIDE 7: Deployment ============
let slide7 = pres.addSlide();
slide7.background = { color: COLORS.lightBg };

slide7.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.9, fill: { color: COLORS.primary }
});
slide7.addText("简单易用的部署方案", {
  x: 0.5, y: 0.2, w: 9, h: 0.5,
  fontSize: 28, fontFace: "Arial Black", color: COLORS.white, margin: 0
});

// Supported platforms
slide7.addText("支持平台", {
  x: 0.5, y: 1.1, w: 2, h: 0.4,
  fontSize: 14, fontFace: "Arial Black", color: COLORS.primary, margin: 0
});

const platforms = ["Linux", "macOS", "Windows", "Android Termux"];
platforms.forEach((p, i) => {
  slide7.addShape(pres.shapes.RECTANGLE, {
    x: 0.5 + i * 2.3, y: 1.5, w: 2.1, h: 0.5,
    fill: { color: COLORS.accent }
  });
  slide7.addText(p, {
    x: 0.5 + i * 2.3, y: 1.5, w: 2.1, h: 0.5,
    fontSize: 13, fontFace: "Calibri", color: COLORS.white,
    align: "center", valign: "middle", margin: 0
  });
});

// Installation commands
slide7.addText("安装命令", {
  x: 0.5, y: 2.3, w: 2, h: 0.4,
  fontSize: 14, fontFace: "Arial Black", color: COLORS.primary, margin: 0
});

// Command card 1
slide7.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 2.8, w: 9, h: 1.1,
  fill: { color: COLORS.dark }
});
slide7.addText("Linux / MacOS / WSL", {
  x: 0.7, y: 2.9, w: 8.6, h: 0.35,
  fontSize: 11, fontFace: "Calibri", color: COLORS.muted, margin: 0
});
slide7.addText("curl -fsSL https://raw.githubusercontent.com/.../install.sh | bash", {
  x: 0.7, y: 3.25, w: 8.6, h: 0.5,
  fontSize: 12, fontFace: "Consolas", color: COLORS.secondary, margin: 0
});

// Command card 2
slide7.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.1, w: 9, h: 1.1,
  fill: { color: COLORS.dark }
});
slide7.addText("Windows", {
  x: 0.7, y: 4.2, w: 8.6, h: 0.35,
  fontSize: 11, fontFace: "Calibri", color: COLORS.muted, margin: 0
});
slide7.addText("irm https://raw.githubusercontent.com/.../install.ps1 | iex", {
  x: 0.7, y: 4.55, w: 8.6, h: 0.5,
  fontSize: 12, fontFace: "Consolas", color: COLORS.secondary, margin: 0
});

// ============ SLIDE 8: Messaging Platforms ============
let slide8 = pres.addSlide();
slide8.background = { color: COLORS.lightBg };

slide8.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.9, fill: { color: COLORS.primary }
});
slide8.addText("标准化的通信平台接入", {
  x: 0.5, y: 0.2, w: 9, h: 0.5,
  fontSize: 28, fontFace: "Arial Black", color: COLORS.white, margin: 0
});

// Key point
slide8.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.15, w: 9, h: 0.7,
  fill: { color: COLORS.white }, shadow: makeShadow()
});
slide8.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.15, w: 0.08, h: 0.7, fill: { color: COLORS.accent }
});
slide8.addText("内置统一消息网关，通过适配器模式支持 15+ 个主流通讯平台，记忆与技能数据完全互通", {
  x: 0.8, y: 1.25, w: 8.5, h: 0.5,
  fontSize: 13, fontFace: "Calibri", color: COLORS.text, margin: 0
});

// Platforms grid
const msgPlatforms = [
  ["飞书", "钉钉", "企业微信"],
  ["微信", "Slack", "Discord"],
  ["Telegram", "WhatsApp", "iMessage"]
];

msgPlatforms.forEach((row, ri) => {
  row.forEach((p, ci) => {
    const x = 0.7 + ci * 3.0;
    const y = 2.1 + ri * 0.85;
    slide8.addShape(pres.shapes.RECTANGLE, {
      x: x, y: y, w: 2.7, h: 0.65,
      fill: { color: COLORS.white }, shadow: makeShadow()
    });
    slide8.addShape(pres.shapes.OVAL, {
      x: x + 0.15, y: y + 0.17, w: 0.3, h: 0.3, fill: { color: COLORS.accent }
    });
    slide8.addText(p, {
      x: x + 0.55, y: y + 0.15, w: 2, h: 0.35,
      fontSize: 13, fontFace: "Calibri", color: COLORS.text, margin: 0
    });
  });
});

// Setup command
slide8.addText("配置命令：hermes gateway setup", {
  x: 0.5, y: 4.8, w: 9, h: 0.4,
  fontSize: 14, fontFace: "Consolas", color: COLORS.accent, margin: 0
});

// ============ SLIDE 9: Commands ============
let slide9 = pres.addSlide();
slide9.background = { color: COLORS.lightBg };

slide9.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.9, fill: { color: COLORS.primary }
});
slide9.addText("精简实用的常用命令集", {
  x: 0.5, y: 0.2, w: 9, h: 0.5,
  fontSize: 28, fontFace: "Arial Black", color: COLORS.white, margin: 0
});

const commands = [
  { cmd: "hermes", desc: "启动 TUI 对话窗口" },
  { cmd: "hermes model", desc: "配置 LLM 提供商和模型" },
  { cmd: "hermes tools", desc: "配置可使用的工具集" },
  { cmd: "hermes setup", desc: "执行完整配置向导" },
  { cmd: "hermes doctor", desc: "诊断并修复配置问题" },
  { cmd: "hermes gateway", desc: "管理消息网关服务" },
  { cmd: "hermes --continue", desc: "回到上次会话" }
];

commands.forEach((item, i) => {
  const y = 1.1 + i * 0.62;
  slide9.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: y, w: 9, h: 0.55,
    fill: { color: COLORS.white }, shadow: makeShadow()
  });
  slide9.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: y, w: 0.08, h: 0.55, fill: { color: COLORS.accent }
  });
  slide9.addText(item.cmd, {
    x: 0.8, y: y + 0.1, w: 3, h: 0.35,
    fontSize: 13, fontFace: "Consolas", color: COLORS.primary, margin: 0
  });
  slide9.addText(item.desc, {
    x: 3.8, y: y + 0.1, w: 5.5, h: 0.35,
    fontSize: 12, fontFace: "Calibri", color: COLORS.muted, margin: 0
  });
});

// ============ SLIDE 10: Conclusion ============
let slide10 = pres.addSlide();
slide10.background = { color: COLORS.primary };

// Decorative accent bar
slide10.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.08, fill: { color: COLORS.accent }
});

slide10.addText("总结与展望", {
  x: 0.5, y: 0.8, w: 9, h: 0.8,
  fontSize: 36, fontFace: "Arial Black", color: COLORS.white,
  align: "center", valign: "middle"
});

// Key takeaways
const takeaways = [
  "配置使用逻辑与 OpenClaw 一致，易于迁移",
  "以牺牲自由度换取版本更新的稳定性与扩展应用的安全性",
  "多平台接入能力相对 OpenClaw 更简单且规范化",
  "保持对前沿技术的敏感度，是非常必要的投资"
];

takeaways.forEach((t, i) => {
  slide10.addShape(pres.shapes.OVAL, {
    x: 1.2, y: 1.9 + i * 0.75, w: 0.2, h: 0.2, fill: { color: COLORS.accent }
  });
  slide10.addText(t, {
    x: 1.6, y: 1.85 + i * 0.75, w: 7.5, h: 0.4,
    fontSize: 15, fontFace: "Calibri", color: COLORS.secondary, margin: 0
  });
});

// Reference info
slide10.addText("参考资料", {
  x: 0.5, y: 4.6, w: 9, h: 0.4,
  fontSize: 12, fontFace: "Arial Black", color: COLORS.muted, margin: 0
});
slide10.addText("Hermes Agent 官方文档 | Hermes Agent 中文文档 | Bilibili 安装演示", {
  x: 0.5, y: 4.95, w: 9, h: 0.3,
  fontSize: 11, fontFace: "Calibri", color: COLORS.muted, margin: 0
});

// Save
pres.writeFile({ fileName: "D:\\user\\Documents\\working\\notes\\CS_Studynotes\\04_软件配置与使用\\01.命令行工具\\AI-Agent\\examples\\关于 Hermes Agent.pptx" })
  .then(() => console.log("PPT created successfully!"))
  .catch(err => console.error("Error:", err));
