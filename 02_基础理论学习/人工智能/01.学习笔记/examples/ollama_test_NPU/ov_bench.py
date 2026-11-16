#!/usr/bin/env python3
"""OpenVINO GenAI 本地推理基准 —— Intel Lunar Lake (Core Ultra 200V) 的 NPU / iGPU / CPU 对比。

用法示例:
    python ov_bench.py --device all
    python ov_bench.py --device NPU --runs 5 --max-tokens 128
    python ov_bench.py --device GPU --model OpenVINO/Qwen3-1.7B-int4-ov

设计要点（踩过的坑都固化在这里）:
1. 必须先 pop 掉 ALL_PROXY —— 本机 ALL_PROXY=socks5h://... 会让 httpx 抛
   "Using SOCKS proxy, but the 'socksio' package is not installed"，
   表现为 huggingface_hub 下载静默失败。
2. NPU 首次 compile 极慢（分钟级），必须与 warmup、正式计时分离统计。
3. NPU 只吃静态 shape 的 OpenVINO IR（int4 量化），不能直接读 GGUF。
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import statistics
import sys
import time
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------- 环境修复
# 必须在 import huggingface_hub / httpx 之前执行
for _var in ("ALL_PROXY", "all_proxy"):
    os.environ.pop(_var, None)

# Windows 控制台默认 GBK，中文会变乱码；写文件始终是 UTF-8，这里只修显示
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HERE = Path(__file__).resolve().parent
DEFAULT_MODEL_DIR = HERE / "models"
RESULTS_DIR = HERE / "results"

DEFAULT_REPO = "OpenVINO/Qwen2.5-1.5B-instruct-int4-ov"
DEFAULT_PROMPT = "用一句话解释什么是 NPU（神经网络处理单元）。"


# ---------------------------------------------------------------- venv 自举
# 本目录若存在 .venv，自动把自己重新执行到该解释器里。
# 目的：本机主版本已切到 3.15（openvino 无 cp315 wheel），而本项目锁 3.14；
#      只要在本目录下运行，不管外面 `python` 指向哪个版本，用的都是 .venv 的依赖。
def _ensure_venv() -> None:
    if os.environ.get("BENCH_IN_VENV") == "1":
        return
    venv_py = HERE / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not venv_py.exists():
        return
    try:
        if Path(sys.executable).resolve() == venv_py.resolve():
            return
    except OSError:
        return
    os.environ["BENCH_IN_VENV"] = "1"
    sys.stderr.write(f"[venv] 已切换到项目虚拟环境: {venv_py}\n")
    sys.stderr.flush()
    sys.stdout.flush()
    os.execv(str(venv_py), [str(venv_py), str(Path(__file__).resolve()), *sys.argv[1:]])


if os.environ.get("BENCH_IN_VENV") != "1":
    _ensure_venv()


# ---------------------------------------------------------------- 工具函数
def ensure_model(repo: str, model_dir: Path) -> Path:
    """把 HF 上的 OpenVINO IR 模型拉到本地缓存目录，返回本地路径。"""
    local = model_dir / repo.split("/")[-1]
    marker = local / "openvino_model.xml"
    if marker.exists():
        print(f"[model] 命中本地缓存: {local}")
        return local

    from huggingface_hub import snapshot_download

    local.mkdir(parents=True, exist_ok=True)
    print(f"[model] 下载 {repo} -> {local}")
    t0 = time.perf_counter()
    snapshot_download(repo, local_dir=str(local))
    print(f"[model] 下载完成，耗时 {time.perf_counter() - t0:.1f}s")
    return local


def collect_env() -> dict:
    import openvino as ov

    core = ov.Core()
    devices = {}
    for dev in core.available_devices:
        try:
            devices[dev] = core.get_property(dev, "FULL_DEVICE_NAME")
        except Exception:
            devices[dev] = "?"
    return {
        "hostname": platform.node(),
        "os": f"{platform.system()} {platform.release()} ({platform.version()})",
        "cpu": platform.processor(),
        "python": sys.version.split()[0],
        "openvino": ov.__version__,
        "devices": devices,
    }


def count_tokens(pipe, text: str) -> int:
    """统计文本的 token 数。

    坑: `Tokenizer.encode()` 返回 `TokenizedInputs`，其 `.input_ids` 是
    `openvino.Tensor`（shape `[1, N]`）。对 Tensor 用 len() 或 np.array()
    都会得到 1（0 维），必须走 `get_size()` / `get_shape()` 乘积。
    """
    try:
        ids = pipe.get_tokenizer().encode(text).input_ids
        try:
            return int(ids.get_size())
        except Exception:
            n = 1
            for d in ids.get_shape():
                n *= int(d)
            return int(n)
    except Exception:
        return max(1, len(text.split()))


def timed_generate(pipe, prompt: str, cfg) -> tuple[float, str, int]:
    """跑一次生成，返回 (耗时秒, 文本, 输出 token 数)。

    顺带说明: `pipe.generate(prompt, cfg)` 返回纯 str（2026.4 的行为）；
    传自定义 StreamerBase 才能拿 DecodedResults/perf_metrics，但该路径在
    2026.4.1 上会直接崩溃无输出，所以这里不依赖它，改用 tokenizer 计数。
    """
    t0 = time.perf_counter()
    text = pipe.generate(prompt, cfg)
    dt = time.perf_counter() - t0
    return dt, text, count_tokens(pipe, text)


# ---------------------------------------------------------------- 单设备测试
def bench_device(device: str, model_path: Path, runs: int, max_tokens: int,
                 prompt: str, warmups: int, think: bool = False,
                 max_prompt_len: int | None = None,
                 min_response_len: int | None = None) -> dict:
    import openvino_genai as ov_genai

    print(f"\n{'=' * 68}\n[device] {device}\n{'=' * 68}", flush=True)

    # NPU/GPU 上 LLM 的大坑：不约束 shape 时，pipeline 会为每种 prompt/response
    # 长度组合各编译一份 blob，NPU 上首次编译能拖到 10 分钟以上且看起来像死掉。
    # 固定 MAX_PROMPT_LEN / MIN_RESPONSE_LEN 后编译时间降到分钟级以内。
    props: dict[str, int] = {}
    if max_prompt_len:
        props["MAX_PROMPT_LEN"] = max_prompt_len
    if min_response_len:
        props["MIN_RESPONSE_LEN"] = min_response_len
    if props:
        print(f"[{device}] 固定 shape: {props}", flush=True)

    t0 = time.perf_counter()
    pipe = ov_genai.LLMPipeline(str(model_path), device, **props)
    compile_s = time.perf_counter() - t0
    print(f"[{device}] 加载+编译耗时 {compile_s:.2f}s", flush=True)

    cfg = ov_genai.GenerationConfig()
    cfg.max_new_tokens = max_tokens
    cfg.temperature = 0.3
    cfg.do_sample = True

    # Qwen3 默认走 thinking，会把 max_new_tokens 全烧在 <think> 里。
    # 关思考的方式是给 prompt 追加 /no_think（Qwen3 官方约定）。
    if not think and "qwen3" in str(model_path).lower().replace("_", "").replace("-", ""):
        prompt = prompt.rstrip() + " /no_think"
        print(f"[{device}] Qwen3 检测到 -> 追加 /no_think 关闭思考", flush=True)

    for i in range(warmups):
        t0 = time.perf_counter()
        pipe.generate(prompt, cfg)
        print(f"[{device}] warmup {i + 1}/{warmups} 耗时 {time.perf_counter() - t0:.2f}s", flush=True)

    rows = []
    sample = ""
    for i in range(runs):
        dt, text, n_tokens = timed_generate(pipe, prompt, cfg)
        tps = n_tokens / dt if dt > 0 else 0.0
        rows.append({
            "run": i + 1,
            "seconds": round(dt, 3),
            "tokens": n_tokens,
            "tok_per_s": round(tps, 2),
            "ms_per_tok": round(dt / n_tokens * 1000, 1) if n_tokens else 0.0,
        })
        sample = text
        print(f"[{device}] run{i + 1}: {dt:6.2f}s  {n_tokens:4d} tok  -> {tps:6.2f} tok/s", flush=True)

    rates = [r["tok_per_s"] for r in rows]
    return {
        "device": device,
        "compile_seconds": round(compile_s, 3),
        "runs": rows,
        "avg_tok_per_s": round(statistics.fmean(rates), 3),
        "stddev_tok_per_s": round(statistics.pstdev(rates), 3) if len(rates) > 1 else 0.0,
        "best_tok_per_s": round(max(rates), 3),
        "worst_tok_per_s": round(min(rates), 3),
        "sample_output": sample.replace("\n", " ")[:200],
    }


# ---------------------------------------------------------------- 结果落盘
def save_results(payload: dict) -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    out = RESULTS_DIR / f"ov-{stamp}.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    with (RESULTS_DIR / "history.jsonl").open("a", encoding="utf-8") as fh:
        flat = {
            "ts": payload["timestamp"],
            "engine": "openvino-genai",
            "model": payload["model"],
            "results": [
                {k: r[k] for k in ("device", "avg_tok_per_s", "compile_seconds")}
                for r in payload["results"]
            ],
        }
        fh.write(json.dumps(flat, ensure_ascii=False) + "\n")
    return out


def print_summary(payload: dict) -> None:
    print(f"\n{'-' * 68}")
    print(f"模型: {payload['model']}   输出上限: {payload['max_tokens']} tokens")
    print(f"{'-' * 68}")
    print(f"{'设备':<10}{'平均 tok/s':>14}{'最好':>10}{'最差':>10}{'编译(s)':>12}")
    for r in payload["results"]:
        print(f"{r['device']:<10}{r['avg_tok_per_s']:>14.2f}"
              f"{r['best_tok_per_s']:>10.2f}{r['worst_tok_per_s']:>10.2f}"
              f"{r['compile_seconds']:>12.2f}")
    print(f"{'-' * 68}")


# ---------------------------------------------------------------- 入口
def main() -> int:
    ap = argparse.ArgumentParser(description="OpenVINO GenAI NPU/GPU/CPU 基准")
    ap.add_argument("--device", default="all",
                    help="NPU / GPU / CPU / all（可逗号分隔）")
    ap.add_argument("--model", default=DEFAULT_REPO, help="HF 上的 OpenVINO IR 模型 ID")
    ap.add_argument("--model-dir", default=str(DEFAULT_MODEL_DIR), help="本地模型缓存目录")
    ap.add_argument("--runs", type=int, default=3, help="正式计时轮数（默认 3）")
    ap.add_argument("--warmups", type=int, default=1, help="预热轮数（默认 1）")
    ap.add_argument("--max-tokens", type=int, default=128, help="每轮生成 token 上限")
    ap.add_argument("--think", action="store_true",
                    help="保留 Qwen3 的 thinking（默认追加 /no_think 关闭，否则 token 全烧在思考里）")
    ap.add_argument("--max-prompt-len", type=int, default=None,
                    help="固定 MAX_PROMPT_LEN（NPU 默认 1024，可大幅缩短首次编译时间）")
    ap.add_argument("--min-response-len", type=int, default=None,
                    help="固定 MIN_RESPONSE_LEN（NPU 默认取 max(max_tokens,128)）")
    ap.add_argument("--prompt", default=DEFAULT_PROMPT)
    ap.add_argument("--no-save", action="store_true", help="不写 results/")
    args = ap.parse_args()

    env = collect_env()
    print("[env] " + json.dumps(env, ensure_ascii=False))

    if args.device.lower() == "all":
        wanted = [d for d in ("NPU", "GPU", "CPU") if d in env["devices"]]
    else:
        wanted = [d.strip().upper() for d in args.device.split(",") if d.strip()]
        missing = [d for d in wanted if d not in env["devices"]]
        if missing:
            print(f"[error] 设备不存在: {missing}（可用: {list(env['devices'])}）")
            return 2

    model_path = ensure_model(args.model, Path(args.model_dir))

    results, failures = [], []
    for dev in wanted:
        try:
            mpl = args.max_prompt_len
            mrl = args.min_response_len
            if dev == "NPU":
                mpl = mpl or 1024
                mrl = mrl or max(args.max_tokens, 128)
            results.append(bench_device(dev, model_path, args.runs,
                                        args.max_tokens, args.prompt, args.warmups,
                                        think=args.think,
                                        max_prompt_len=mpl, min_response_len=mrl))
        except Exception as exc:  # 单设备失败不影响其它设备
            failures.append({"device": dev, "error": f"{type(exc).__name__}: {exc}"})
            print(f"[error] {dev} 测试失败: {type(exc).__name__}: {exc}")

    if not results:
        print("[error] 没有任何设备测试成功")
        return 1

    payload = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "engine": "openvino-genai",
        "model": args.model,
        "max_tokens": args.max_tokens,
        "prompt": args.prompt,
        "think": args.think,
        "env": env,
        "results": results,
        "failures": failures,
    }
    print_summary(payload)

    if not args.no_save:
        path = save_results(payload)
        print(f"[save] {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
