# ollama_test_NPU

Intel Lunar Lake（Core Ultra 7 258V）本地大模型推理基准 —— **NPU / iGPU / CPU 三方对比**。

在 ASUS 笔记本（Core Ultra 7 258V + Intel Arc 140V iGPU + Intel AI Boost NPU）上实测固化，
目的是**一条命令跑出一张可比的速度表**，而不是每次现写探针脚本。

> 项目位置：`CS_StudyNotes/02_基础理论学习/人工智能/01.学习笔记/examples/ollama_test_NPU/`
> 配套笔记：《[[LLM 的部署与测试]]》的 “延伸实验：在 NPU / iGPU / CPU 之间做一次推理后端选型” 一节。

---

## 能测什么 / 不能测什么

| 脚本 | 后端 | 覆盖设备 | 备注 |
| --- | --- | --- | --- |
| `ov_bench.py` | OpenVINO GenAI | **NPU / GPU / CPU** | 唯一能跑 Intel NPU 的路径 |
| `ollama_bench.py` | Ollama（llama.cpp） | **CPU / iGPU(Vulkan)** | Ollama **没有 NPU 后端** |

实测依据：`ollama 0.40.16` 的 `lib\ollama\` 下只有 `ggml-cpu-*.dll`（14 种微架构）、
`cuda_v12\`、`cuda_v13\`、`rocm_v7_1\`、`vulkan\ggml-vulkan.dll` —— 无 NPU / OpenVINO / SYCL。
**想测 NPU 只能用 OpenVINO。**

---

## 一、环境准备（只需一次）

### 1.1 Python 版本与虚拟环境

本项目**锁 3.14**，两个硬约束：

- `openvino 2026.4.1` 的 Windows wheel 只到 **cp314**，没有 cp315
  （实测 3.15 下 `pip install openvino==2026.4.1` → `from versions: none`）
- 本机主版本已切到 **3.15**（`python` / `python3` / `pip` 全指向 3.15），
  所以项目内必须靠 venv 隔离

```powershell
cd "D:\Working\writing\CS_StudyNotes\02_基础理论学习\人工智能\01.学习笔记\examples\ollama_test_NPU"
uv venv --python 3.14 .venv          # 已建好，重建时才需要
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

**切换是自动的**：`.venv` 存在时，`ov_bench.py` / `ollama_bench.py` 启动即把自己
重新执行到 `.venv\Scripts\python.exe`（`_ensure_venv()`，靠 `BENCH_IN_VENV=1` 防循环）。
所以哪怕外面是 3.15，直接跑就行：

```powershell
python ov_bench.py --device all      # stderr 会先打一行 [venv] 已切换到项目虚拟环境: ...
```

`run_all.ps1` 同理：`-Python` 未指定时自动用 `.venv\Scripts\python.exe`，找不到就报错并给出建立命令。

> 主版本切换方式（一次性，已完成）：把 `%LOCALAPPDATA%\Python\bin`（uv 的 shim 目录）
> 提到用户 PATH 最前。原 Python 3.12 仍在 PATH 中，`py -3.12` 随时可调。

### 1.2 安装依赖

```powershell
uv pip install --python .venv\Scripts\python.exe -r requirements.txt

# 确认三个设备都被识别
.venv\Scripts\python.exe -c "import openvino as ov; c=ov.Core(); print({d: c.get_property(d,'FULL_DEVICE_NAME') for d in c.available_devices})"
# 期望: {'CPU': 'Intel(R) Core(TM) Ultra 7 258V', 'GPU': 'Intel(R) Arc(TM) 140V GPU (16GB) (iGPU)', 'NPU': 'Intel(R) AI Boost'}
```

`requirements.txt`：

```
openvino>=2026.4.1
openvino-genai>=2026.4.1
openvino-tokenizers>=2026.4.1
huggingface_hub>=0.24
numpy
```

> 模型会自动从 HuggingFace 下载到 `models/`，首次运行需要联网（约 900 MB ~ 1.2 GB）。
> `models/`、`.venv/`、`*.log` 均在仓库根 `.gitignore` 里，不会被提交到公开仓库。

---

## 二、快速开始（三条命令）

```powershell
cd examples\ollama_test_NPU

# 1) OpenVINO：NPU + GPU + CPU 一次跑完（默认 Qwen2.5-1.5B int4，三设备都支持）
python ov_bench.py --device all

# 2) Ollama：CPU vs iGPU（自动起隔离实例，不干扰你日常的 11434）
python ollama_bench.py --model qwen3:8b --runs 3

# 3) 一键全跑 + 打印历史汇总
powershell -NoProfile -ExecutionPolicy Bypass -File run_all.ps1
```

结果统一落在 `results/`，控制台同时打印一张表。

---

## 三、按目的找配方

| 我想…… | 用这条命令 |
| --- | --- |
| 三设备横向对比 | `python ov_bench.py --device all` |
| 只想知道 NPU 多快 | `python ov_bench.py --device NPU` |
| 看看 8B 模型在集显上有没有用 | `python ollama_bench.py --model qwen3:8b` |
| 测我新下的 Ollama 模型 | `python ollama_bench.py --model <name>` |
| 测 HF 上新的 OpenVINO IR | `python ov_bench.py --model OpenVINO/xxx-int4-ov` |
| 长输出下的真实吞吐 | `--runs 3 --max-tokens 512` |
| 只看首次加载/编译有多慢 | `--runs 1 --warmups 0`（看 `compile_seconds`） |
| 复现历史数据看趋势 | `Get-Content results\history.jsonl` |
| 不写文件、只打印 | 加 `--no-save` |

---

## 四、`ov_bench.py` —— OpenVINO 三设备

### 参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `--device` | `all` | `NPU` / `GPU` / `CPU` / `all`，也可逗号组合：`GPU,CPU` |
| `--model` | `OpenVINO/Qwen2.5-1.5B-instruct-int4-ov` | HF 上的 OpenVINO IR 仓库 ID |
| `--model-dir` | `./models` | 本地缓存根目录（每个模型一个子目录） |
| `--runs` | `3` | 正式计时轮数 |
| `--warmups` | `1` | 预热轮数（不计入统计，用来排除首次 alloc 抖动） |
| `--max-tokens` | `128` | 每轮生成上限（模型自己 EOS 会提前停） |
| `--max-prompt-len` | NPU 下 `1024` | **NPU 专用**：固定 `MAX_PROMPT_LEN`，越小编译越快 |
| `--min-response-len` | NPU 下 `max(max_tokens,128)` | **NPU 专用**：固定 `MIN_RESPONSE_LEN` |
| `--think` | 关 | Qwen3 默认追加 `/no_think`，加此参数保留思考过程 |
| `--prompt` | 内置中文提示 | 自定义提问 |
| `--no-save` | — | 不写 `results/` |

> ⚠️ **`--max-tokens` 不要低于 64**。输出太短时首 token / prefill 的固定开销占比过大，
> 测出来严重失真：实测 16 token 时 CPU 只剩 6.66 tok/s，128 token 时是 36.10。
> 短输出只能用于「三设备连通性自检」，不能拿去选型对比。

### 输出怎么读

```
[NPU] 加载+编译耗时 25.56s        ← 一次性成本，别和 tok/s 混在一起看
[NPU] warmup 1/1 耗时 1.87s
[NPU] run1:   1.50s    35 tok  ->  23.39 tok/s
------------------------------------------------------------
设备              平均 tok/s        最好        最差       编译(s)
NPU                22.80     23.39     22.42       25.56
```

- **平均 tok/s**：`生成 token 数 / 纯解码耗时`，不含编译、不含 prefill 之外的开销
- **编译(s)**：`LLMPipeline` 构造耗时。NPU 远高于 CPU/GPU，这是 NPU 的固有代价
- 输出 token 数少于 `--max-tokens` 是正常的（模型自己 EOS）

### 实测基线

**A. `OpenVINO/Qwen2.5-1.5B-instruct-int4-ov`**，`--runs 3 --warmups 1 --max-tokens 128`：

当前环境（Python 3.14 venv，2026-11-16，两次独立复测）：

| 设备 | 平均 tok/s | 最好 | 最差 | 编译 | 结论 |
| --- | --- | --- | --- | --- | --- |
| **GPU** (Arc 140V) | **57.61 / 59.73** | 62.93 | 52.40 | 2.6 s | 首选 |
| CPU (Ultra 7 258V) | **46.45 / 47.31** | 47.79 | 43.90 | 1.2 s | 次选 |
| **NPU** (AI Boost) | **24.52 / 24.83** | 24.86 | 24.44 | 1.9 s（首次 29.0 s） | 能用但最慢 |

> 旧环境（Python 3.12，2026-11-15）为 GPU 41.43 / CPU 36.10 / NPU 22.80，编译 5.6 / 2.0 / 25.6 s。
> 换解释器后 GPU +39%~+44%、CPU +29%~+31%、NPU +8%~+9%，编译时间同步减半 ——
> openvino 版本号相同，差异只能来自 Python 与依赖环境本身，
> 归因（CPython 3.14 自身 / numpy 2.5.5 / wheel build 差异）未拆开验证。
> NPU 两次运行的编译耗时是 28.99 s → 1.89 s：编译产物被缓存到了磁盘，
> 所以 “第一次跑特别慢” 往往只是冷编译，不要当成 NPU 本身慢。

NPU 换 `--max-tokens 32 --max-prompt-len 256` 时是 19.05 tok/s、编译降到 14.9 s ——
shape 越小编译越快，但单 token 吞吐基本封顶在 20–25 tok/s。

**B. `OpenVINO/Qwen3-1.7B-int4-ov`**：

| 设备 | 平均 tok/s | 编译 |
| --- | --- | --- |
| CPU | 38.95 | 1.5 s |
| GPU (Arc 140V) | **54.83** | 6.8 s |
| NPU | **跑不出来** | 超 20 分钟未完成，见「故障排查」 |

**结论**：1.7B 这一档 GPU 比 CPU 快 40%；NPU 慢但省电、且不占 GPU。

---

## 五、`ollama_bench.py` —— CPU vs iGPU

### 参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `--model` | `qwen3:8b` | ollama 里的模型名（`ollama list` 可查） |
| `--mode` | `both` | `cpu` / `igpu` / `both`（both = 各起一个实例依次测） |
| `--runs` | `3` | 每模式计时轮数 |
| `--warmups` | `1` | 预热轮数 |
| `--max-tokens` | `128` | 每轮生成上限 |
| `--prompt` | 内置中文提示 | 自定义提问 |
| `--port` | `11500` | 自起 serve 的起始端口（both 模式会用到 11500/11501） |
| `--models-dir` | 自动探测 | `OLLAMA_MODELS` 模型仓库；探测顺序见下 |
| `--host` | `127.0.0.1:11434` | 配合 `--no-spawn` 用 |
| `--no-spawn` | — | 不起新实例，直接测 `--host` 指向的现有服务 |
| `--ollama` | 自动查找 | `ollama.exe` 路径 |
| `--debug` | — | 开 `OLLAMA_DEBUG`，日志更啰嗦 |
| `--no-save` | — | 不写 `results/` |

### 模型仓库自动探测顺序

1. `--models-dir` 显式指定
2. 环境变量 `OLLAMA_MODELS`
3. `E:\ollama`（本机桌面版实际仓库）
4. `~/.ollama/models`（老结构）
5. `~/.ollama`（0.31+ 新结构，blobs 直接在根下）
6. `%LOCALAPPDATA%\Ollama\models`

找不到、或 `/api/tags` 里没有目标模型时，脚本会**直接报错并列出可用模型名**，
而不是让你对着一个 `404 {"error":"model 'xxx' not found"}` 猜。

### 输出怎么读

```
[mode] igpu —— iGPU（Vulkan 后端）（端口 11801）
[igpu] warmup 1/1 耗时 41.70s，load 35.85s
[igpu] size=5.19 GiB  size_vram=5.19 GiB  on_gpu=True     ← 确认真的进了显存
[igpu] run1:   4.64s    64 tok  ->  13.81 tok/s | prefill 297.75 tok/s | TTFT 0.28s
```

- **`on_gpu` / `size_vram`**：判断 iGPU 是否真生效的硬证据，不是看命令行有没有设环境变量
- **TTFT**：首个 token 延迟
- **prefill tok/s**：提示词处理速度

### 实测基线（`qwen3:8b` Q4_K_M 5.2 GB）

64 token × 2 轮（2026-11-15）：

| 模式 | 平均 tok/s | 进显存 | 加载耗时 |
| --- | --- | --- | --- |
| CPU | 9.66 | 否（`size_vram=0`） | 15.5 s |
| iGPU (Vulkan) | **13.91** | 是（5.19 GiB） | 35.9 s |

128 token × 3 轮（2026-11-16，两次独立复测）：

| 模式 | 平均 tok/s | 最好 | 最差 | 进显存 |
| --- | --- | --- | --- | --- |
| CPU | 9.74 / 10.30 | 10.33 | 9.11 | 否（`size_vram=0`） |
| iGPU (Vulkan) | **18.61 / 18.71** | 18.84 | 18.46 | 是（7.81 GiB） |

输出越长，iGPU 优势越明显（大模型 decode 是显存带宽瓶颈，不是算力）。

---

## 六、`run_all.ps1` —— 一键全跑

```powershell
# 默认：OpenVINO 三设备 + Ollama 两模式
powershell -NoProfile -ExecutionPolicy Bypass -File run_all.ps1

# 常用组合
... -File run_all.ps1 -SkipNpu                  # 跳过 NPU（不想等编译）
... -File run_all.ps1 -SkipOllama               # 只测 OpenVINO
... -File run_all.ps1 -Runs 5 -MaxTokens 512    # 更严谨的长输出测试
... -File run_all.ps1 -OvModel OpenVINO/Qwen3-1.7B-int4-ov -SkipNpu
... -File run_all.ps1 -OllamaModel qwen2.5:14b
```

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `-Python` | `.venv\Scripts\python.exe`（自动探测） | 指定解释器；不传就用项目虚拟环境 |
| `-OvModel` | `OpenVINO/Qwen2.5-1.5B-instruct-int4-ov` | OpenVINO 模型 |
| `-OllamaModel` | `qwen3:8b` | Ollama 模型 |
| `-Runs` | `3` | 轮数 |
| `-MaxTokens` | `128` | 每轮生成上限 |
| `-SkipOllama` | — | 跳过 Ollama 部分 |
| `-SkipNpu` | — | OpenVINO 只用 `GPU,CPU` |

跑完会打印累计历史：

```
历史记录（results\history.jsonl）：
2026-11-15T14:24:28  openvino-genai OpenVINO/Qwen2.5-1.5B-instruct-int4-ov NPU=22.797
2026-11-15T14:25:30  openvino-genai OpenVINO/Qwen2.5-1.5B-instruct-int4-ov GPU=38.22  CPU=37.96
```

---

## 七、结果文件

```
results/
├── ov-20261115-142428.json       # 单次完整结果（含 env、每轮耗时、样例输出）
├── ollama-20261115-140953.json
└── history.jsonl                 # 追加式摘要，一行一次运行
```

`history.jsonl` 每行长这样，字段已统一（便于自己写脚本画趋势）：

```json
{"ts":"2026-11-15T14:24:28","engine":"openvino-genai","model":"OpenVINO/Qwen2.5-1.5B-instruct-int4-ov",
 "results":[{"device":"NPU","avg_tok_per_s":22.797,"compile_seconds":25.56}]}
{"ts":"2026-11-15T14:08:23","engine":"ollama","model":"qwen3:8b",
 "results":[{"mode":"cpu","avg_tok_per_s":9.66,"on_gpu":false},
            {"mode":"igpu","avg_tok_per_s":13.91,"on_gpu":true}]}
```

---

## 八、怎么加自己的模型

**OpenVINO（NPU 可用）**：必须是 int4/int8 量化的 OpenVINO IR，不能是 GGUF。

```powershell
# 直接用 HF 上现成的（OpenVINO 官方仓库通常叫 OpenVINO/<model>-int4-ov）
python ov_bench.py --model OpenVINO/Qwen2.5-3B-instruct-int4-ov

# 自己转（需要 optimum-intel）
optimum-cli export openvino --model Qwen/Qwen2.5-3B-Instruct --weight-format int4 --task text-generation-with-past models/Qwen2.5-3B-int4-ov
python ov_bench.py --device all --model-dir models --model Qwen2.5-3B-int4-ov
```

**Ollama**：先 `ollama pull`，再传 `--model`。

```powershell
ollama pull qwen2.5:14b
python ollama_bench.py --model qwen2.5:14b --runs 3
```

> NPU 选型提示：优先 **Qwen2.5 系列或 Intel 官方 NPU 示例用的模型**。
> Qwen3 系列的 IR 在 NPU 上编译不动（见下）。

---

## 九、故障排查

| 症状 | 原因 | 解法 |
| --- | --- | --- |
| `ImportError: Using SOCKS proxy, but the 'socksio' package is not installed` | 本机 `ALL_PROXY=socks5h://...`，httpx 优先它 | 两个脚本已在 import 前 pop 掉；自己写脚本也要 pop，或 `pip install "httpx[socks]"` |
| `404 {"error":"model 'xxx' not found"}` 但 `ollama list` 有这个模型 | 新起的 serve 指错模型仓库（`total blobs: 0`） | `--models-dir E:\ollama`；或看脚本打印的 `[models]` 行 |
| `bind: Only one usage of each socket address` | 端口被残留的 `ollama serve` 占用 | 换 `--port 12000`，或任务管理器结束残留 ollama 进程 |
| NPU 卡住十几分钟无输出 | ① shape 未固定 ② 模型不适配 NPU | 加 `--max-prompt-len 256 --min-response-len 64`；换 Qwen2.5 系列模型 |
| `to_shape was called on a dynamic shape` | 绕开 genai 直接 `core.compile_model(model,"NPU")` | 不能用这条路，必须走 `LLMPipeline`（genai 会 reshape） |
| 输出全是 `<think>...</think>`，正文被截断 | Qwen3 默认开思考 | 脚本已自动加 `/no_think`；想保留思考加 `--think` 并把 `--max-tokens` 调大 |
| tok/s 低得离谱（<2） | tokenizer 计数写错 | `encode(...).input_ids` 是 Tensor，必须用 `.get_size()`，不是 `len()` |
| PowerShell 脚本报 `The string is missing the terminator` 之类怪错 | `.ps1` 存成了 UTF-8 **无 BOM**，中文被按 ANSI 解码 | 存成 **UTF-8 with BOM** |
| 长任务日志只留一个 `^C` | 父进程被终止，CTRL_C_EVENT 打到了子进程 | 用 `Start-Process cmd.exe -WindowStyle Hidden`（独立 console） |

---

## 十、目录结构

```
ollama_test_NPU/
├── ov_bench.py           # OpenVINO：NPU / GPU / CPU
├── ollama_bench.py       # Ollama：CPU / iGPU(Vulkan)
├── run_all.ps1           # 一键全跑（UTF-8 with BOM）
├── requirements.txt
├── README.md
├── models/               # HF 模型缓存
│   ├── Qwen2.5-1.5B-instruct-int4-ov/   # 三设备通用（推荐主力）
│   └── Qwen3-1.7B-int4-ov/              # GPU 对照用，NPU 不支持
├── results/              # 结果 JSON + history.jsonl（入库）
├── logs/                 # ollama serve 日志（含 Vulkan 识别证据；*.log 不入库）
└── .venv/                # Python 3.14 虚拟环境（不入库）
```
