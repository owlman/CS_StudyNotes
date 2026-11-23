"""与《Transformer 架构详解》正文逐行对应的最小实现（PyTorch）。

本文件把笔记中的公式翻译为可运行的代码，并在教学版的基础上补齐了三类
工程必备项：

1. **Padding Mask**：区分有效 token 与填充位；
2. **Attention Dropout**：注意力权重的随机丢弃；
3. **KV Cache**：自回归推理时复用历史键值，把每步复杂度从 O(t^2 d) 降到 O(t d)。

另外还实现了正文中出现过的 RoPE（旋转位置编码）与 GQA（分组查询注意力），
它们都是可选开关，默认关闭以保持与正文公式一一对应。

形状约定（与笔记表 2、表 3 一致）：

* 输入隐藏状态 ``X``：``(batch, seq_len, d_model)``；
* 注意力内部：``(batch, n_head, seq_len, d_k)``，其中 ``d_k = d_model // n_head``；
* 输出：``(batch, seq_len, d_model)``。

作者：本文配套示例，随笔记同步维护。
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F

__all__ = [
    "MultiHeadSelfAttention",
    "FeedForward",
    "DecoderBlock",
    "MiniGPT",
    "KVCache",
]


# --------------------------------------------------------------------------- #
# 位置编码：RoPE（旋转位置编码）
# --------------------------------------------------------------------------- #
def build_rope_cache(
    seq_len: int,
    d_k: int,
    device: torch.device | str = "cpu",
    base: float = 10000.0,
) -> tuple[torch.Tensor, torch.Tensor]:
    """构造 RoPE 的 cos / sin 缓存表。

    对应笔记中「RoPE 把位置信息以二维旋转的形式注入 Q 与 K」的描述：
    位置 ``m`` 对应第 ``i`` 对维度的旋转角为 ``m * base^(-2i/d_k)``，
    于是两个 token 之间的注意力分数只依赖它们的**相对位置差**。

    返回形状均为 ``(seq_len, d_k // 2)``，其中奇数维度先取偶数位、再取奇数位
    配对成 ``(d_k // 2)`` 个旋转对。
    """
    if d_k % 2 != 0:
        raise ValueError("RoPE 要求 d_k 为偶数")
    half = d_k // 2
    inv_freq = torch.exp(
        torch.arange(0, half, dtype=torch.float32, device=device)
        * (-math.log(base) / half)
    )
    pos = torch.arange(seq_len, dtype=torch.float32, device=device)
    freqs = torch.outer(pos, inv_freq)  # (seq_len, d_k // 2)
    return freqs.cos(), freqs.sin()


def apply_rope(
    x: torch.Tensor,
    cos: torch.Tensor,
    sin: torch.Tensor,
    positions: torch.Tensor | None = None,
) -> torch.Tensor:
    """对 ``x``（``(batch, n_head, seq_len, d_k)``）就地施加旋转位置编码。

    ``positions`` 给出每个位置在序列中的绝对下标；自回归增量解码时，
    新 token 的下标大于 0，因此这里按 ``positions`` 取行，而不是默认取前 ``n`` 行。
    """
    seq_len = x.shape[-2]
    if positions is None:
        cos = cos[:seq_len]
        sin = sin[:seq_len]
    else:
        cos = cos[positions]  # (batch, seq_len, d_k // 2)
        sin = sin[positions]
        cos = cos.unsqueeze(1)  # (batch, 1, seq_len, d_k // 2)
        sin = sin.unsqueeze(1)

    x1 = x[..., 0::2]
    x2 = x[..., 1::2]
    rotated = torch.stack((x1 * cos - x2 * sin, x1 * sin + x2 * cos), dim=-1)
    return rotated.flatten(-2)  # (batch, n_head, seq_len, d_k)


# --------------------------------------------------------------------------- #
# KV Cache
# --------------------------------------------------------------------------- #
@dataclass
class KVCache:
    """自回归推理时保存的历史键值。

    每个元素形状为 ``(batch, n_kv_head, seq_len_so_far, d_k)``。
    """

    k: torch.Tensor | None = None
    v: torch.Tensor | None = None

    def update(self, k: torch.Tensor, v: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """把本步的 K/V 追加到缓存，返回拼接后的完整 K/V。"""
        if self.k is None:
            self.k, self.v = k, v
        else:
            self.k = torch.cat([self.k, k], dim=-2)
            self.v = torch.cat([self.v, v], dim=-2)
        return self.k, self.v


# --------------------------------------------------------------------------- #
# 多头自注意力
# --------------------------------------------------------------------------- #
class MultiHeadSelfAttention(nn.Module):
    """因果掩码的多头自注意力（Decoder-only LLM 的第一个子层）。

    对应笔记公式：

    * ``Q = X W^Q``、``K = X W^K``、``V = X W^V``；
    * ``scores = Q K^T / sqrt(d_k)``；
    * ``scores = scores + M``（``M`` 为掩码，屏蔽未来位置与填充位）；
    * ``attn = softmax(scores)``；
    * ``out = attn V``，再经 ``W^O`` 投影回 ``d_model``。

    相比正文教学版，本类额外支持：

    * ``padding_mask``：``(batch, seq_len)``，``True`` 表示该位置是填充位；
    * ``attn_dropout``：注意力权重上的 dropout；
    * ``use_kv_cache`` + ``cache``：自回归推理时复用历史 K/V；
    * ``use_rope``：对 Q、K 施加旋转位置编码；
    * ``n_kv_head``：GQA 场景下小于 ``n_head``，此时启用 KV Cache。
    """

    def __init__(
        self,
        d_model: int,
        n_head: int,
        *,
        n_kv_head: int | None = None,
        attn_dropout: float = 0.0,
        use_kv_cache: bool = False,
        use_rope: bool = False,
        rope_base: float = 10000.0,
        dropout: float = 0.0,
    ) -> None:
        super().__init__()
        if d_model % n_head != 0:
            raise ValueError("d_model 必须能被 n_head 整除")
        self.n_head = n_head
        self.n_kv_head = n_kv_head if n_kv_head is not None else n_head
        if self.n_head % self.n_kv_head != 0:
            raise ValueError("GQA 要求 n_head 能被 n_kv_head 整除")
        self.d_k = d_model // n_head
        self.d_v = self.d_k
        self.use_kv_cache = use_kv_cache
        self.use_rope = use_rope
        self.rope_base = rope_base

        # GQA 下 K/V 的输出维度是 n_kv_head * d_k。
        self.d_kv = self.n_kv_head * self.d_k

        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, self.d_kv)
        self.W_v = nn.Linear(d_model, self.d_kv)
        self.W_o = nn.Linear(d_model, d_model)
        self.attn_dropout = nn.Dropout(attn_dropout)
        self.resid_dropout = nn.Dropout(dropout)

        self._rope_cache: tuple[torch.Tensor, torch.Tensor] | None = None

    # -- RoPE 缓存 ---------------------------------------------------------- #
    def _get_rope_cache(self, seq_len: int, device: torch.device) -> tuple[torch.Tensor, torch.Tensor]:
        if self._rope_cache is None or self._rope_cache[0].shape[0] < seq_len:
            self._rope_cache = build_rope_cache(
                max(seq_len, 16), self.d_k, device=device, base=self.rope_base
            )
        return self._rope_cache

    def _rope_positions(self, positions: torch.Tensor | None, n: int, device: torch.device) -> int:
        """RoPE 缓存需要覆盖到的最大绝对位置。"""
        if positions is None:
            return n
        return int(positions.max().item()) + 1

    # -- 前向 --------------------------------------------------------------- #
    def forward(
        self,
        X: torch.Tensor,
        *,
        padding_mask: torch.Tensor | None = None,
        cache: KVCache | None = None,
        positions: torch.Tensor | None = None,
    ) -> torch.Tensor:
        """``X``：``(batch, seq_len, d_model)``。

        ``padding_mask``：``(batch, seq_len)``，``True`` 表示填充位。
        ``cache``：非空时启用 KV Cache（并自动启用自回归因果掩码）。
        ``positions``：``(batch, seq_len)`` 的绝对位置下标，配合 RoPE 与 KV Cache 使用。
        """
        B, n, d = X.shape
        if d != self.W_q.in_features:
            raise ValueError(f"输入维度应为 {self.W_q.in_features}，收到 {d}")

        q = self.W_q(X).view(B, n, self.n_head, self.d_k).transpose(1, 2)
        k = self.W_k(X).view(B, n, self.n_kv_head, self.d_k).transpose(1, 2)
        v = self.W_v(X).view(B, n, self.n_kv_head, self.d_k).transpose(1, 2)

        if self.use_rope:
            need = self._rope_positions(positions, n, X.device)
            cos, sin = self._get_rope_cache(need, X.device)
            if positions is None:
                q = apply_rope(q, cos, sin)
                k = apply_rope(k, cos, sin)
            else:
                q = apply_rope(q, cos, sin, positions)
                k = apply_rope(k, cos, sin, positions)

        if self.use_kv_cache and cache is not None:
            k, v = cache.update(k, v)

        # GQA：把 KV 头沿组复制到查询头（查询头 i 使用 KV 头 i // repeat）。
        if self.n_kv_head != self.n_head:
            repeat = self.n_head // self.n_kv_head
            k_exp = k.repeat_interleave(repeat, dim=1)
            v_exp = v.repeat_interleave(repeat, dim=1)
        else:
            k_exp, v_exp = k, v

        # (B, h, n_q, n_kv_total)
        scores = q @ k_exp.transpose(-2, -1) / math.sqrt(self.d_k)

        # 因果掩码：屏蔽未来位置（查询位置小于键位置即为未来）。
        total_kv = k.shape[-2]
        q_positions = (
            torch.arange(total_kv - n, total_kv, device=X.device)
            if positions is None
            else positions[0]
        )
        future = q_positions[:, None] < torch.arange(total_kv, device=X.device)[None, :]
        scores = scores.masked_fill(future[None, None], float("-inf"))

        # Padding 掩码：屏蔽填充位。
        if padding_mask is not None:
            key_pad = padding_mask[:, None, None, :]  # (B, 1, 1, total_kv)
            scores = scores.masked_fill(key_pad, float("-inf"))

        attn = scores.softmax(dim=-1)
        # 整行被屏蔽时 softmax 会得到 NaN，这里用 0 兜底。
        attn = torch.nan_to_num(attn, nan=0.0)
        attn = self.attn_dropout(attn)

        out = attn @ v_exp  # (B, h, n, d_v)
        out = out.transpose(1, 2).contiguous().view(B, n, self.n_head * self.d_v)
        return self.resid_dropout(self.W_o(out))


# --------------------------------------------------------------------------- #
# 前馈网络
# --------------------------------------------------------------------------- #
class FeedForward(nn.Module):
    """两个线性层夹一个激活函数，隐藏维度通常为 ``4 * d_model``。

    可切换为 SwiGLU 写法（Llama 系列采用），此时隐藏维度由 ``hidden_dim`` 显式给出。
    """

    def __init__(self, d_model: int, hidden_dim: int | None = None, *, swiglu: bool = False) -> None:
        super().__init__()
        if swiglu:
            if hidden_dim is None:
                hidden_dim = int(8 * d_model / 3)
            hidden_dim = (hidden_dim + 7) // 8 * 8  # 对齐到 8 的倍数
            self.w1 = nn.Linear(d_model, hidden_dim)
            self.w3 = nn.Linear(d_model, hidden_dim)
            self.w2 = nn.Linear(hidden_dim, d_model)
            self.swiglu = True
        else:
            hidden_dim = hidden_dim or 4 * d_model
            self.fc1 = nn.Linear(d_model, hidden_dim)
            self.fc2 = nn.Linear(hidden_dim, d_model)
            self.swiglu = False

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if self.swiglu:
            return self.w2(F.silu(self.w1(x)) * self.w3(x))
        return self.fc2(F.relu(self.fc1(x)))


class RMSNorm(nn.Module):
    """RMSNorm：只按均方根做缩放，不减均值，因而比 LayerNorm 更省计算。

    对应笔记中「RMSNorm 计算更省」的讨论：它省掉了均值与方差的求解。
    """

    def __init__(self, d_model: int, eps: float = 1e-6) -> None:
        super().__init__()
        self.weight = nn.Parameter(torch.ones(d_model))
        self.eps = eps

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        dtype = x.dtype
        x32 = x.float()
        rms = torch.rsqrt(x32.pow(2).mean(-1, keepdim=True) + self.eps)
        return (x32 * rms).to(dtype) * self.weight


# --------------------------------------------------------------------------- #
# Decoder Block 与最小语言模型
# --------------------------------------------------------------------------- #
class DecoderBlock(nn.Module):
    """Pre-LN 结构的 Decoder-only 块：自注意力 → 前馈网络，各带残差连接。"""

    def __init__(
        self,
        d_model: int,
        n_head: int,
        *,
        n_kv_head: int | None = None,
        dropout: float = 0.0,
        attn_dropout: float = 0.0,
        use_kv_cache: bool = False,
        use_rope: bool = False,
        norm: str = "rms",
        swiglu: bool = False,
    ) -> None:
        super().__init__()
        self.use_kv_cache = use_kv_cache
        make_norm = (lambda: RMSNorm(d_model)) if norm == "rms" else (lambda: nn.LayerNorm(d_model))
        self.norm1 = make_norm()
        self.norm2 = make_norm()
        self.attn = MultiHeadSelfAttention(
            d_model,
            n_head,
            n_kv_head=n_kv_head,
            attn_dropout=attn_dropout,
            use_kv_cache=use_kv_cache,
            use_rope=use_rope,
            dropout=dropout,
        )
        self.ffn = FeedForward(d_model, swiglu=swiglu)
        self.dropout = nn.Dropout(dropout)

    def forward(
        self,
        x: torch.Tensor,
        *,
        padding_mask: torch.Tensor | None = None,
        cache: KVCache | None = None,
        positions: torch.Tensor | None = None,
    ) -> torch.Tensor:
        x = x + self.dropout(
            self.attn(self.norm1(x), padding_mask=padding_mask, cache=cache, positions=positions)
        )
        x = x + self.dropout(self.ffn(self.norm2(x)))
        return x


class MiniGPT(nn.Module):
    """一个可训练、可自回归生成的最小 Decoder-only 语言模型。

    结构：token embedding + 位置编码（可选 RoPE / 正弦）→ N 层 Decoder Block → 输出投影。
    """

    def __init__(
        self,
        vocab_size: int,
        d_model: int = 128,
        n_head: int = 4,
        n_layer: int = 2,
        *,
        max_seq_len: int = 128,
        n_kv_head: int | None = None,
        dropout: float = 0.0,
        use_kv_cache: bool = False,
        use_rope: bool = False,
        norm: str = "rms",
        swiglu: bool = False,
    ) -> None:
        super().__init__()
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.max_seq_len = max_seq_len
        self.use_kv_cache = use_kv_cache
        self.use_rope = use_rope

        self.tok_emb = nn.Embedding(vocab_size, d_model)
        self.blocks = nn.ModuleList(
            [
                DecoderBlock(
                    d_model,
                    n_head,
                    n_kv_head=n_kv_head,
                    dropout=dropout,
                    use_kv_cache=use_kv_cache,
                    use_rope=use_rope,
                    norm=norm,
                    swiglu=swiglu,
                )
                for _ in range(n_layer)
            ]
        )
        self.norm_f = RMSNorm(d_model) if norm == "rms" else nn.LayerNorm(d_model)
        self.lm_head = nn.Linear(d_model, vocab_size, bias=False)
        self.lm_head.weight = self.tok_emb.weight  # 权重共享

        # 正弦位置编码（非 RoPE 时的默认选择），按需增长以支持超长生成
        if not use_rope:
            self._pos_emb: torch.Tensor | None = None

        self.apply(self._init_weights)

    @staticmethod
    def _init_weights(module: nn.Module) -> None:
        if isinstance(module, nn.Linear):
            nn.init.normal_(module.weight, std=0.02)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            nn.init.normal_(module.weight, std=0.02)

    def _sinusoidal_pe(self, seq_len: int, device: torch.device) -> torch.Tensor:
        """按需构造（或扩展）正弦位置编码表。

        表格随长度增长，因此即使生成步数超过初始的 ``max_seq_len`` 也不会越界。
        """
        if self._pos_emb is None or self._pos_emb.shape[0] < seq_len:
            length = max(seq_len, 16)
            pe = torch.zeros(length, self.d_model, device=device)
            pos = torch.arange(length, dtype=torch.float32, device=device)[:, None]
            div = torch.exp(
                torch.arange(0, self.d_model, 2, dtype=torch.float32, device=device)
                * (-math.log(10000.0) / self.d_model)
            )
            pe[:, 0::2] = torch.sin(pos * div)
            pe[:, 1::2] = torch.cos(pos * div)
            self._pos_emb = pe
        return self._pos_emb[:seq_len]

    def forward(
        self,
        input_ids: torch.Tensor,
        *,
        padding_mask: torch.Tensor | None = None,
        caches: list[KVCache] | None = None,
        positions: torch.Tensor | None = None,
    ) -> torch.Tensor:
        """返回 ``(batch, seq_len, vocab_size)`` 的 logits。

        ``caches`` 非空时启用 KV Cache 增量解码。
        """
        B, n = input_ids.shape
        h = self.tok_emb(input_ids)
        if not self.use_rope:
            h = h + self._sinusoidal_pe(n, input_ids.device).unsqueeze(0)

        for i, block in enumerate(self.blocks):
            cache = None if caches is None else caches[i]
            h = block(h, padding_mask=padding_mask, cache=cache, positions=positions)

        h = self.norm_f(h)
        return self.lm_head(h)

    # -- 生成 --------------------------------------------------------------- #
    @torch.no_grad()
    def generate(
        self,
        input_ids: torch.Tensor,
        max_new_tokens: int = 20,
        temperature: float = 1.0,
        top_k: int | None = None,
        eos_id: int | None = None,
    ) -> torch.Tensor:
        """贪心 / 采样生成，用于直观检查模型是否学到东西。"""
        self.eval()
        device = input_ids.device
        caches = [KVCache() for _ in self.blocks] if self.use_kv_cache else None
        ids = input_ids
        past_len = 0
        for step in range(max_new_tokens):
            if self.use_kv_cache:
                step_ids = ids[:, past_len:] if past_len else ids
                positions = torch.arange(past_len, past_len + step_ids.shape[1], device=device)[None].expand(
                    step_ids.shape[0], -1
                )
                logits = self(step_ids, caches=caches, positions=positions)
                past_len += step_ids.shape[1]
            else:
                logits = self(ids)
            logits = logits[:, -1, :] / max(temperature, 1e-6)
            if top_k:
                v, _ = torch.topk(logits, min(top_k, logits.size(-1)))
                logits = logits.masked_fill(logits < v[:, [-1]], float("-inf"))
            probs = logits.softmax(dim=-1)
            next_id = torch.multinomial(probs, num_samples=1)
            ids = torch.cat([ids, next_id], dim=1)
            if eos_id is not None and int(next_id.item()) == eos_id:
                break
        return ids
