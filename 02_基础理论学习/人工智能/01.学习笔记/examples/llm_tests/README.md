# llm_tests

LLM 行为模式自动化测试套件，配合《LLM 的部署与测试》笔记使用。

## 项目结构

```
llm_tests/
├── conftest.py                  # PyTest 公共配置与 fixtures
├── pyproject.toml               # 项目依赖配置
├── .python-version              # Python 版本锁定
├── test_basic_call.py           # 基础连通性与响应结构测试
├── test_latency.py              # 响应延迟与吞吐量观察测试
├── test_nondeterminism.py       # 非确定性输出测试
├── test_ambiguous_prompt.py     # 模糊指令下的模型行为测试
├── test_streaming.py            # 流式响应行为测试
└── test_knowledge_boundary.py   # 知识边界与幻觉行为测试
```

## 前置条件

- Ollama 已安装并运行
- 已拉取测试用模型：`ollama pull llama3.2:3b`

## 运行测试

```bash
cd llm_tests
uv run pytest -v
```

## 测试设计原则

这些测试不是用来评估模型的"聪明程度"，而是观察 LLM 作为系统组件时的响应方式、失败模式以及可控性边界。每个测试文件都对应主文章中某个特定阶段所暴露的能力边界。
