"""最小实现的单元测试：逐条验证笔记中的关键性质。

运行：

    python -m pytest tests/test_transformer_minimal.py -v
    # 或不装 pytest：
    python tests/test_transformer_minimal.py

覆盖的性质：

1. 形状守恒：多头拆分后总维度仍为 ``d_model``；
2. 因果性：未来 token 的改动不影响前面位置的输出；
3. Padding Mask：填充位不影响有效位的输出；
4. KV Cache：增量解码与一次性前向的 logits 一致；
5. GQA：查询头与 KV 头的分组映射正确；
6. RoPE：注意力分数只依赖相对位置；
7. Dropout：训练态与推理态行为不同，推理态确定性。
"""

from __future__ import annotations

import os
import sys

import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from transformer_minimal.model import (  # noqa: E402
    KVCache,
    MiniGPT,
    MultiHeadSelfAttention,
    build_rope_cache,
)

torch.manual_seed(0)


def test_shape_preservation() -> None:
    """多头拆分与拼接后，模型维度保持 d_model 不变。"""
    d_model, n_head = 32, 4
    attn = MultiHeadSelfAttention(d_model, n_head)
    x = torch.randn(2, 5, d_model)
    out = attn(x)
    assert out.shape == (2, 5, d_model)
    assert attn.d_k == d_model // n_head


def test_causality() -> None:
    """改动最后一个 token，前面的输出必须保持不变。"""
    d_model, n_head = 32, 4
    attn = MultiHeadSelfAttention(d_model, n_head).eval()
    x = torch.randn(1, 6, d_model)
    x2 = x.clone()
    x2[:, -1] += 10.0
    with torch.no_grad():
        out1 = attn(x)
        out2 = attn(x2)
    assert torch.allclose(out1[:, :-1], out2[:, :-1], atol=1e-5)
    assert not torch.allclose(out1[:, -1], out2[:, -1], atol=1e-5)


def test_padding_mask() -> None:
    """被标记为填充位的位置不应影响有效位的输出。"""
    d_model, n_head = 32, 4
    attn = MultiHeadSelfAttention(d_model, n_head).eval()
    x = torch.randn(1, 6, d_model)
    pad = torch.zeros(1, 6, dtype=torch.bool)
    pad[:, -2:] = True
    x_masked = x.clone()
    x_masked[:, -2:] = torch.randn(1, 2, d_model)
    with torch.no_grad():
        out1 = attn(x, padding_mask=pad)
        out2 = attn(x_masked, padding_mask=pad)
    assert torch.allclose(out1[:, :-2], out2[:, :-2], atol=1e-5)


def test_kv_cache_consistency() -> None:
    """KV Cache 增量解码应与一次性前向得到相同 logits。"""
    d_model, n_head = 32, 4
    attn = MultiHeadSelfAttention(d_model, n_head, use_kv_cache=True).eval()
    x = torch.randn(1, 5, d_model)
    cache = KVCache()
    with torch.no_grad():
        full = attn(x)
        # 前 4 个 token 一次性喂入
        attn(x[:, :4], cache=cache, positions=torch.arange(4)[None])
        # 第 5 个 token 单独喂入
        step = attn(x[:, 4:], cache=cache, positions=torch.tensor([[4]]))
    assert torch.allclose(full[:, -1], step[:, -1], atol=1e-5)


def test_gqa_group_mapping() -> None:
    """GQA 下，同组查询头共享同一份 K/V。"""
    d_model, n_head, n_kv = 32, 4, 2
    attn = MultiHeadSelfAttention(d_model, n_head, n_kv_head=n_kv).eval()
    x = torch.randn(1, 4, d_model)
    with torch.no_grad():
        q = attn.W_q(x).view(1, 4, n_head, attn.d_k).transpose(1, 2)
        k = attn.W_k(x).view(1, 4, n_kv, attn.d_k).transpose(1, 2)
        v = attn.W_v(x).view(1, 4, n_kv, attn.d_k).transpose(1, 2)
        scores = q @ k.repeat_interleave(n_head // n_kv, dim=1).transpose(-2, -1) / attn.d_k**0.5
        causal = torch.triu(torch.ones(4, 4, dtype=torch.bool), diagonal=1)
        attn_w = scores.masked_fill(causal, float("-inf")).softmax(-1)
        expect = attn_w @ v.repeat_interleave(n_head // n_kv, dim=1)
        got = attn(x)
    expect = expect.transpose(1, 2).contiguous().view(1, 4, d_model)
    assert torch.allclose(got, expect @ attn.W_o.weight.T + attn.W_o.bias, atol=1e-5)


def test_rope_relative_property() -> None:
    """RoPE 下注意力分数只依赖相对位置差：整体平移后分数不变。"""
    d_model, n_head = 32, 2
    attn = MultiHeadSelfAttention(d_model, n_head, use_rope=True).eval()
    x = torch.randn(1, 6, d_model)
    with torch.no_grad():
        cos, sin = build_rope_cache(16, attn.d_k)
        q = attn.W_q(x).view(1, 6, n_head, attn.d_k).transpose(1, 2)
        k = attn.W_k(x).view(1, 6, n_head, attn.d_k).transpose(1, 2)
        from transformer_minimal.model import apply_rope

        q = apply_rope(q, cos, sin)
        k = apply_rope(k, cos, sin)
        s1 = q @ k.transpose(-2, -1)
        # 位置整体 +2（对原始 q/k 重新施加旋转，而不是对已旋转结果再旋转）
        q2 = apply_rope(
            attn.W_q(x).view(1, 6, n_head, attn.d_k).transpose(1, 2), cos, sin, torch.arange(2, 8)[None]
        )
        k2 = apply_rope(
            attn.W_k(x).view(1, 6, n_head, attn.d_k).transpose(1, 2), cos, sin, torch.arange(2, 8)[None]
        )
        s2 = q2 @ k2.transpose(-2, -1)
    assert torch.allclose(s1, s2, atol=1e-4)


def test_dropout_and_determinism() -> None:
    """推理态输出确定；训练态受 dropout 影响。"""
    d_model, n_head = 32, 4
    attn = MultiHeadSelfAttention(d_model, n_head, attn_dropout=0.5)
    x = torch.randn(2, 5, d_model)
    attn.eval()
    with torch.no_grad():
        assert torch.allclose(attn(x), attn(x), atol=1e-6)
    attn.train()
    out1, out2 = attn(x), attn(x)
    assert not torch.allclose(out1, out2, atol=1e-6)


def test_mini_gpt_forward_and_generate() -> None:
    """最小语言模型能前向、能在 KV Cache 下自洽生成。"""
    model = MiniGPT(
        vocab_size=32,
        d_model=32,
        n_head=4,
        n_layer=2,
        max_seq_len=32,
        use_kv_cache=True,
        use_rope=True,
    ).eval()
    ids = torch.randint(0, 32, (2, 6))
    with torch.no_grad():
        logits = model(ids)
    assert logits.shape == (2, 6, 32)
    with torch.no_grad():
        out = model.generate(ids, max_new_tokens=5, temperature=1.0)
    assert out.shape == (2, 11)


def test_mini_gpt_kv_cache_matches_full_forward() -> None:
    """整模型层面：KV Cache 增量解码的 logits 与一次性前向一致。"""
    torch.manual_seed(1)
    model = MiniGPT(
        vocab_size=32,
        d_model=32,
        n_head=4,
        n_layer=2,
        max_seq_len=32,
        use_kv_cache=True,
        use_rope=True,
    ).eval()
    ids = torch.randint(0, 32, (1, 7))
    caches = [KVCache() for _ in model.blocks]
    with torch.no_grad():
        full = model(ids)
        model(ids[:, :4], caches=caches, positions=torch.arange(4)[None])
        step = model(ids[:, 4:7], caches=caches, positions=torch.arange(4, 7)[None])
    assert torch.allclose(full[:, 4:7], step, atol=1e-4)


def test_gqa_kv_cache_shares_kv() -> None:
    """GQA + KV Cache：缓存里的 K/V 头数少于查询头数。"""
    model = MiniGPT(
        vocab_size=32,
        d_model=32,
        n_head=4,
        n_layer=1,
        n_kv_head=2,
        max_seq_len=32,
        use_kv_cache=True,
    ).eval()
    ids = torch.randint(0, 32, (1, 5))
    caches = [KVCache() for _ in model.blocks]
    with torch.no_grad():
        model(ids, caches=caches, positions=torch.arange(5)[None])
    assert caches[0].k is not None
    assert caches[0].k.shape[1] == 2  # n_kv_head
    assert caches[0].k.shape[-1] == model.d_model // model.blocks[0].attn.n_head


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(list(globals().items())):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS  {name}")
            except Exception as exc:  # noqa: BLE001
                failures += 1
                print(f"FAIL  {name}: {exc}")
    print("全部通过" if failures == 0 else f"{failures} 个用例失败")
    sys.exit(1 if failures else 0)
