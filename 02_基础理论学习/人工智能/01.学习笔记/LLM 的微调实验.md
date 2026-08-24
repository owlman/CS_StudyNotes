---
title: LLM 的微调实验
author: 凌杰
date: 2026-08-21
tags: LoRA, LLaMA-Factory
categories: 人工智能
---

> [!NOTE] 笔记说明
>
> 这篇笔记对应的是《[[关于 AI 的学习路线图]]》一文中所规划的第三个学习阶段。其中记录了我尝试在个人开发环境中对一款轻量型的 LLM 进行微调的实验过程，以及个人在该过程中所获得的心得体会。同样的，这些内容也将成为我 AI 系列笔记的一部分，被存储在本人 Github 上的[计算机学习笔记库](https://github.com/owlman/CS_StudyNotes)中，并予以长期维护。

操作步骤：

- 用 uv 创建使用 Python 3.12 的虚拟环境
- 安装 LLaMA-Factory 及其 CPU 版的依赖
- 去 ModelScope 获取 Qwen 2.5-0.5b 模型
- 准备一个极小规模的微调数据集（基于《论语》）
- 配置并运行 CPU 版的 LoRA 微调
- 验证微调结果并生成报告

（待完成）

## 参考资料

- 文档资料

- 视频资料
  什么是 LoRA？大模型微调是怎么回事：[YouTube 链接](https://www.youtube.com/watch?v=hZ6fSjPGQWM&t=2s) / [Bilibili 链接](https://www.bilibili.com/video/BV1PvwYzxE9D)

- 博客文章
  - 