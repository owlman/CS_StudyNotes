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

### 指向其他端点（局域网机器 / 其他模型）

端点、模型名与超时都可用环境变量覆盖，无需改源码：

```powershell
$env:OLLAMA_URL = "http://my-openclaw:11434/api/generate"
$env:OLLAMA_MODEL = "qwen3:4b-8k"
$env:OLLAMA_TIMEOUT = "500"   # 秒；qwen3 这类思考型模型很慢
uv run pytest -v
```

```bash
# bash 写法
OLLAMA_URL=http://my-openclaw:11434/api/generate \
OLLAMA_MODEL=qwen3:4b-8k \
OLLAMA_TIMEOUT=500 \
uv run pytest -v
```

> ⚠️ **代理陷阱**：`conftest.py` 里共享的 `SESSION.trust_env = False` 是**必需的**。
> 本机装了 HTTP 代理时，`requests` 的代理绕过规则只按主机名字符串匹配 `NO_PROXY`，
> 既不解析主机名对应的 IP 去套 `192.168.0.0/16` 这类 CIDR，也不读 Windows 注册表的
> `ProxyOverride`。于是 `my-openclaw` 这种局域网主机名会被代理接管，代理机解析不到，
> 报 `502 Server Error: Bad Gateway`。新增任何直接发请求的测试，请一律用 `http_session`
> fixture，不要直接调 `requests.post`。

> ⏱️ **耗时提醒**：`test_streaming.py` 在 `qwen3:4b-8k` 上实测约 322 秒（非流式 + 流式各一次，
> 且思考型模型默认先输出推理过程）。本地 `llama3.2:3b` 则快得多。

## 测试设计原则

这些测试不是用来评估模型的"聪明程度"，而是观察 LLM 作为系统组件时的响应方式、失败模式以及可控性边界。每个测试文件都对应主文章中某个特定阶段所暴露的能力边界。
