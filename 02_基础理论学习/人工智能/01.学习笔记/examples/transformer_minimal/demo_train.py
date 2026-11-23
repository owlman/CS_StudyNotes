"""端到端演示：在一个极小的字符级任务上训练 MiniGPT，观察 loss 下降与生成结果。

任务设定（刻意选得足够简单，便于在 CPU 上几十秒跑完）：

* 语料是一段循环出现的固定字符串，模型只需学会「记住这个模式」；
* 训练若干步后打印平均 loss；
* 最后用贪心解码生成续写，检查模型是否真的学到了结构。

运行：

    python demo_train.py            # 默认配置
    python demo_train.py --steps 300 --d-model 64 --n-head 4
"""

from __future__ import annotations

import argparse
import os
import sys
import time

import torch
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from transformer_minimal.model import MiniGPT  # noqa: E402

CORPUS = "Transformer 的核心是自注意力机制，自注意力机制的核心是查询、键与值的点积。\n"


def build_dataset(corpus: str, seq_len: int) -> tuple[torch.Tensor, list[str]]:
    """把字符串映射为 token id，并切分成训练样本。"""
    chars = sorted(set(corpus))
    stoi = {c: i for i, c in enumerate(chars)}
    ids = torch.tensor([stoi[c] for c in corpus], dtype=torch.long)
    # 用同一段文本反复采样，保证模型有足够多的重复模式可学
    reps = max(1, (seq_len * 32) // len(ids))
    data = ids.repeat(reps)
    n_sample = (len(data) - seq_len - 1) // seq_len
    x = torch.stack([data[i * seq_len : i * seq_len + seq_len] for i in range(n_sample)])
    y = torch.stack([data[i * seq_len + 1 : i * seq_len + 1 + seq_len] for i in range(n_sample)])
    return x, y, chars


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=300)
    ap.add_argument("--seq-len", type=int, default=32)
    ap.add_argument("--d-model", type=int, default=64)
    ap.add_argument("--n-head", type=int, default=4)
    ap.add_argument("--n-layer", type=int, default=2)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--use-rope", action="store_true", help="启用 RoPE 位置编码")
    ap.add_argument("--use-kv-cache", action="store_true", help="启用 KV Cache（推理时）")
    ap.add_argument("--n-kv-head", type=int, default=None, help="GQA 的 KV 头数，默认等于查询头数")
    args = ap.parse_args()

    torch.manual_seed(args.seed)
    x, y, chars = build_dataset(CORPUS, args.seq_len)
    print(f"词表大小={len(chars)}  样本数={x.shape[0]}  序列长度={args.seq_len}")

    model = MiniGPT(
        vocab_size=len(chars),
        d_model=args.d_model,
        n_head=args.n_head,
        n_layer=args.n_layer,
        max_seq_len=args.seq_len,
        n_kv_head=args.n_kv_head,
        use_rope=args.use_rope,
        use_kv_cache=args.use_kv_cache,
    )
    n_params = sum(p.numel() for p in model.parameters())
    print(f"参数量={n_params:,}")

    opt = torch.optim.AdamW(model.parameters(), lr=args.lr)
    model.train()
    t0 = time.time()
    losses: list[float] = []
    for step in range(1, args.steps + 1):
        idx = torch.randint(0, x.shape[0], (8,))
        logits = model(x[idx])
        loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), y[idx].reshape(-1))
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        losses.append(loss.item())
        if step % max(1, args.steps // 6) == 0 or step == 1:
            recent = sum(losses[-20:]) / len(losses[-20:])
            print(f"step {step:4d}  loss {recent:.4f}")

    print(f"训练耗时 {time.time() - t0:.1f}s")

    # 生成：给一个前缀，让模型续写
    prefix = "Transformer 的核心是"
    ids = torch.tensor([[chars.index(c) for c in prefix]], dtype=torch.long)
    model.eval()
    out = model.generate(ids, max_new_tokens=40, temperature=0.8, top_k=5)
    text = "".join(chars[i] for i in out[0].tolist())
    print("\n生成结果：")
    print(text)


if __name__ == "__main__":
    main()
