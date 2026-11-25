# transformer_minimal —— 《Transformer 架构详解》配套最小实现

本目录把笔记正文《最小实现（PyTorch）》一节的代码固化为可运行、可测试的工程，
并在其之上补齐了正文明确列出但未实现的三项工程必备项。

## 目录结构

```text
transformer_minimal/
├── model.py                      # 核心实现（注意力、FFN、Norm、Decoder 块、最小 LM）
├── demo_train.py                 # 端到端演示：字符级小语料上训练并生成
├── tests/
│   └── test_transformer_minimal.py   # 10 个用例，逐条验证关键性质
├── requirements.txt              # 依赖（CPU 版 PyTorch）
└── README.md
```

## 与正文的关系

正文的教学版只有 `MultiHeadSelfAttention` 一个类，约 30 行（含注释共 35 行），公式与代码逐行可查。
本实现保留了这一对应关系，并做了如下扩展：

| 能力 | 正文教学版 | 本实现 | 说明 |
|---|---|---|---|
| 因果掩码多头自注意力 | ✅ | ✅ | 与正文完全一致 |
| Padding Mask | ❌ | ✅ | `padding_mask` 参数，`True` 表示填充位 |
| Attention Dropout | ❌ | ✅ | `attn_dropout`，作用于 softmax 之后的权重 |
| KV Cache | ❌ | ✅ | `use_kv_cache` + `KVCache`，自回归推理复用历史 K/V |
| RoPE 位置编码 | 正文另章 | ✅ | `use_rope`，注意力分数只依赖相对位置 |
| GQA | 正文另章 | ✅ | `n_kv_head < n_head`，组内共享 K/V，KV Cache 份数按组缩小 |
| RMSNorm / SwiGLU | 正文另章 | ✅ | `norm="rms"`、`swiglu=True` |
| 最小语言模型 + 训练 | ❌ | ✅ | `MiniGPT`，可训练、可自回归生成 |

## 快速开始

```bash
# 1) 建虚拟环境并安装依赖（CPU 版 PyTorch）
uv venv .venv --python 3.12
uv pip install --python .venv/Scripts/python.exe torch numpy --index-url https://download.pytorch.org/whl/cpu

# 2) 跑测试（10 个用例，全部通过）
.venv/Scripts/python.exe tests/test_transformer_minimal.py

# 3) 跑端到端演示
.venv/Scripts/python.exe demo_train.py --steps 300
```

预期输出（实测，CPU、约 2 秒）：

```text
词表大小=31  样本数=30  序列长度=32
参数量=101,760
step    1  loss 3.4623
step   50  loss 2.9644
step  100  loss 0.1424
step  150  loss 0.0094
step  300  loss 0.0022
训练耗时 2.3s
```

常用开关：

```bash
--use-rope              # 启用 RoPE
--use-kv-cache          # 启用 KV Cache（推理路径）
--n-kv-head 2           # GQA：4 个查询头共享 2 组 KV
--d-model 128 --n-layer 4   # 放大模型
```

## 测试覆盖的性质

1. **形状守恒**：多头拆分与拼接后维度仍为 `d_model`；
2. **因果性**：改动最后一个 token 不影响前面位置的输出；
3. **Padding Mask**：填充位的内容不影响有效位输出；
4. **KV Cache 一致性**：增量解码与一次性前向的 logits 相同（注意力层与整模型各一例）；
5. **GQA 分组映射**：同组查询头共享同一份 K/V，且缓存中 KV 头数确实更少；
6. **RoPE 相对性质**：注意力分数只依赖相对位置差，整体平移后不变；
7. **Dropout**：推理态确定性，训练态受随机丢弃影响。

## 实现要点（踩坑记录）

* **因果掩码的方向**：掩码矩阵必须满足 `query_pos < key_pos` 才是 “未来位置”。
  写反成 `>=` 会让模型看到未来，训练 loss 依然会下降，但生成结果完全错乱。
* **KV Cache 下的位置偏移**：启用缓存后，查询位置不再是 `0..n-1`，而是
  `total_kv - n .. total_kv - 1`；因果掩码与 RoPE 的位置下标都必须用这个偏移量。
* **GQA 的广播方向**：应把 KV 头 `repeat_interleave` 到查询头（查询头 `i` 使用
  KV 头 `i // (h/h_kv)`），而不是把查询头求和——后者等价于 MQA，语义不同。
* **RoPE 的旋转配对**：必须对 `(2i, 2i+1)` 成对旋转；若对已旋转的张量再次施加
  旋转，得到的不是位置平移后的结果，相对性质测试会失败。
* **正弦位置编码要能增长**：固定长度的 `pos_emb` 缓冲在生成长度超出时会越界，
  这里改为按需扩展。

## 参考

配套笔记：`../../Transformer 架构详解.md`（《Transformer 架构详解》，
`CS_StudyNotes/02_基础理论学习/人工智能/01.学习笔记/`）。
