#!/usr/bin/env python3
"""Ollama 本地推理基准 —— 对比「纯 CPU」与「iGPU(Vulkan) 加速」两种后端。

为什么必须自己起 serve:
    Ollama 选择设备只能靠启动时的环境变量控制（运行期无法切换）：
        OLLAMA_IGPU_ENABLE=1     # 启用集显 Vulkan 后端，默认会打印
                                 # "dropping integrated GPU; to enable, set OLLAMA_IGPU_ENABLE=1"
    所以本脚本为每种模式启动一个独立端口的 `ollama serve` 子进程，
    测完统一回收，全程不影响你日常在 11434 上跑的 Ollama。

补充事实: Ollama **没有 NPU 后端**（后端只有 ggml-cpu-* / cuda / rocm / vulkan），
    Intel NPU 请改用 ov_bench.py（OpenVINO GenAI）。

用法示例:
    python ollama_bench.py                       # CPU vs iGPU，自动起 serve
    python ollama_bench.py --model qwen3:8b --runs 3 --max-tokens 128
    python ollama_bench.py --mode igpu --no-spawn # 直接测现有 11434
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import statistics
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS_DIR = HERE / "results"

DEFAULT_MODEL = "qwen3:8b"
DEFAULT_PROMPT = "用一句话解释什么是 NPU（神经网络处理单元）。"


# ---------------------------------------------------------------- venv 自举
# 本目录若存在 .venv，自动把自己重新执行到该解释器里（与 ov_bench.py 一致）。
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

OLLAMA_CANDIDATES = [
    Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Ollama" / "ollama.exe",
    Path(r"C:\Program Files\Ollama\ollama.exe"),
]

MODES = {
    "cpu":  {"OLLAMA_IGPU_ENABLE": "0", "label": "CPU（纯 CPU 后端）"},
    "igpu": {"OLLAMA_IGPU_ENABLE": "1", "label": "iGPU（Vulkan 后端）"},
}

# 模型仓库候选：不同安装方式/版本落点不同，新起的 serve 若指错目录就会
# 出现 /api/tags 为空、POST 返回 {"error":"model 'xxx' not found"} 的假 404。
MODELS_DIR_CANDIDATES = [
    Path(r"E:\ollama"),                    # 本机实测：桌面版实际仓库
    Path.home() / ".ollama" / "models",    # 老结构：<dir>/blobs + <dir>/manifests
    Path.home() / ".ollama",               # 0.31+ 新结构：blobs 直接在根下
    Path(os.environ.get("LOCALAPPDATA", "")) / "Ollama" / "models",
]


def _has_models(path: Path) -> bool:
    """判断某目录是不是有效的模型仓库（blobs/manifests 任一非空）。"""
    if not path or not path.is_dir():
        return False
    for sub in ("blobs", "manifests", "manifests-v2"):
        d = path / sub
        if d.is_dir() and any(d.iterdir()):
            return True
    return False


def find_models_dir(explicit: str | None = None) -> Path | None:
    """定位 OLLAMA_MODELS。优先级：命令行 > 环境变量 > 候选目录探测。"""
    if explicit:
        p = Path(explicit)
        if not p.is_dir():
            raise FileNotFoundError(f"--models-dir 指定的目录不存在: {p}")
        return p
    env_val = os.environ.get("OLLAMA_MODELS")
    if env_val and Path(env_val).is_dir():
        return Path(env_val)
    for cand in MODELS_DIR_CANDIDATES:
        if _has_models(cand):
            return cand
    return None


# ---------------------------------------------------------------- 基础工具
def find_ollama() -> Path:
    for p in OLLAMA_CANDIDATES:
        if p.is_file():
            return p
    found = shutil.which("ollama")
    if found:
        return Path(found)
    raise FileNotFoundError("找不到 ollama.exe，请用 --ollama 指定路径")


def http_json(url: str, payload: dict | None = None, timeout: int = 600) -> dict:
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers,
                                method="POST" if data else "GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def wait_ready(port: int, timeout: float = 60.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            http_json(f"http://127.0.0.1:{port}/api/version", timeout=3)
            return True
        except Exception:
            time.sleep(0.5)
    return False


# ---------------------------------------------------------------- serve 生命周期
class OllamaServer:
    """在指定端口拉起一个隔离的 ollama serve，退出时确保回收。"""

    def __init__(self, exe: Path, port: int, igpu: bool, debug: bool = False,
                 models_dir: Path | None = None):
        self.exe = exe
        self.port = port
        self.igpu = igpu
        self.debug = debug
        self.models_dir = models_dir
        self.proc: subprocess.Popen | None = None
        self.log_path = HERE / "logs" / f"serve-{port}-{'igpu' if igpu else 'cpu'}.log"

    def __enter__(self) -> "OllamaServer":
        env = os.environ.copy()
        env["OLLAMA_HOST"] = f"127.0.0.1:{self.port}"
        env["OLLAMA_IGPU_ENABLE"] = "1" if self.igpu else "0"
        env.pop("ALL_PROXY", None)
        env.pop("all_proxy", None)
        if self.models_dir:
            env["OLLAMA_MODELS"] = str(self.models_dir)
        if self.debug:
            env["OLLAMA_DEBUG"] = "1"

        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._log = self.log_path.open("w", encoding="utf-8", errors="replace")
        self.proc = subprocess.Popen(
            [str(self.exe), "serve"],
            stdout=self._log, stderr=subprocess.STDOUT,
            env=env, creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
        )
        if not wait_ready(self.port):
            log = self._tail_log()
            self.__exit__(None, None, None)
            hint = ""
            if "Only one usage of each socket address" in log:
                hint = f"\n端口 {self.port} 已被占用（可能有残留的 ollama serve），换个 --port 或在任务管理器结束它。"
            raise RuntimeError(
                f"ollama serve 未在 60s 内就绪（端口 {self.port}），见 {self.log_path}{hint}"
                f"\n--- 日志尾部 ---\n{log}"
            )
        return self

    def _tail_log(self, lines: int = 8) -> str:
        try:
            self._log.flush()
            with self.log_path.open("r", encoding="utf-8", errors="replace") as fh:
                return "".join(fh.readlines()[-lines:])
        except Exception:
            return ""

    def ensure_model(self, model: str) -> None:
        """就绪后确认模型可见，避免后续 /api/generate 返回令人误解的 404。"""
        try:
            tags = http_json(f"http://127.0.0.1:{self.port}/api/tags", timeout=15)
            names = {m.get("name") or m.get("model") for m in tags.get("models", [])}
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(f"查询 /api/tags 失败: {exc}") from exc
        if model in names:
            return
        shown = ", ".join(sorted(n for n in names if n)) or "（空）"
        raise RuntimeError(
            f"新起的 serve 看不到模型 '{model}'。可用: {shown}\n"
            f"多半是 OLLAMA_MODELS 指错了目录（当前={self.models_dir}）。\n"
            f"用 --models-dir 指定真实仓库，或先跑: ollama list 找到模型所在盘。"
        )

    def __exit__(self, *exc) -> None:
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=15)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait(timeout=10)
        try:
            self._log.close()
        except Exception:
            pass


# ---------------------------------------------------------------- 单模式测试
def ps_info(port: int) -> dict:
    try:
        for m in http_json(f"http://127.0.0.1:{port}/api/ps", timeout=10).get("models", []):
            if m.get("size_vram", 0) or True:
                return {
                    "size_bytes": m.get("size", 0),
                    "size_vram": m.get("size_vram", 0),
                    "on_gpu": m.get("size_vram", 0) > 0,
                }
    except Exception:
        pass
    return {"size_bytes": 0, "size_vram": 0, "on_gpu": False}


def generate_once(port: int, model: str, prompt: str, num_predict: int) -> dict:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": num_predict, "temperature": 0.3},
    }
    return http_json(f"http://127.0.0.1:{port}/api/generate", payload)


def unload(port: int, model: str) -> None:
    try:
        http_json(f"http://127.0.0.1:{port}/api/generate",
                  {"model": model, "keep_alive": 0}, timeout=60)
    except Exception:
        pass


def bench_mode(port: int, mode: str, model: str, runs: int, warmups: int,
               num_predict: int, prompt: str) -> dict:
    label = MODES[mode]["label"]
    print(f"\n{'=' * 68}\n[mode] {mode} —— {label}（端口 {port}）\n{'=' * 68}")

    unload(port, model)

    for i in range(warmups):
        t0 = time.perf_counter()
        r = generate_once(port, model, prompt, num_predict)
        print(f"[{mode}] warmup {i + 1}/{warmups} 墙钟 {time.perf_counter() - t0:.2f}s"
              f"（load {r.get('load_duration', 0) / 1e9:.2f}s）")

    mem = ps_info(port)
    print(f"[{mode}] size={mem['size_bytes'] / 2**30:.2f} GiB  "
          f"size_vram={mem['size_vram'] / 2**30:.2f} GiB  on_gpu={mem['on_gpu']}")

    rows, sample = [], ""
    for i in range(runs):
        t0 = time.perf_counter()
        r = generate_once(port, model, prompt, num_predict)
        wall = time.perf_counter() - t0

        eval_count = r.get("eval_count", 0) or 0
        eval_ns = r.get("eval_duration", 0) or 0
        prompt_count = r.get("prompt_eval_count", 0) or 0
        prompt_ns = r.get("prompt_eval_duration", 0) or 0
        load_ns = r.get("load_duration", 0) or 0

        gen_tps = eval_count / (eval_ns / 1e9) if eval_ns else 0.0
        prefill_tps = prompt_count / (prompt_ns / 1e9) if prompt_ns else 0.0
        ttft_s = (load_ns + prompt_ns) / 1e9
        sample = r.get("response", "")

        rows.append({
            "run": i + 1,
            "wall_seconds": round(wall, 3),
            "load_seconds": round(load_ns / 1e9, 3),
            "ttft_seconds": round(ttft_s, 3),
            "prompt_tokens": prompt_count,
            "prefill_tok_per_s": round(prefill_tps, 2),
            "output_tokens": eval_count,
            "gen_tok_per_s": round(gen_tps, 2),
        })
        print(f"[{mode}] run{i + 1}: 生成 {eval_count:4d} tok / {eval_ns / 1e9:6.2f}s "
              f"-> {gen_tps:6.2f} tok/s | prefill {prefill_tps:7.2f} tok/s | TTFT {ttft_s:5.2f}s")

    rates = [r["gen_tok_per_s"] for r in rows] or [0.0]
    return {
        "mode": mode,
        "label": label,
        "on_gpu": mem["on_gpu"],
        "size_gib": round(mem["size_bytes"] / 2**30, 2),
        "size_vram_gib": round(mem["size_vram"] / 2**30, 2),
        "runs": rows,
        "avg_gen_tok_per_s": round(statistics.fmean(rates), 2),
        "best_gen_tok_per_s": round(max(rates), 2),
        "worst_gen_tok_per_s": round(min(rates), 2),
        "stddev_gen_tok_per_s": round(statistics.pstdev(rates), 2) if len(rates) > 1 else 0.0,
        "sample_output": sample.replace("\n", " ")[:200],
    }


# ---------------------------------------------------------------- 结果落盘
def save_results(payload: dict) -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out = RESULTS_DIR / f"ollama-{stamp}.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    with (RESULTS_DIR / "history.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({
            "ts": payload["timestamp"],
            "engine": "ollama",
            "model": payload["model"],
            "results": [{"mode": r["mode"],
                         "avg_tok_per_s": r["avg_gen_tok_per_s"],
                         "on_gpu": r["on_gpu"]}
                        for r in payload["results"]],
        }, ensure_ascii=False) + "\n")
    return out


def print_summary(payload: dict) -> None:
    print(f"\n{'-' * 74}")
    print(f"模型: {payload['model']}   输出上限: {payload['max_tokens']} tokens")
    print(f"{'-' * 74}")
    print(f"{'模式':<12}{'平均 tok/s':>14}{'最好':>10}{'最差':>10}{'在显存':>10}{'VRAM(GiB)':>12}")
    for r in payload["results"]:
        print(f"{r['mode']:<12}{r['avg_gen_tok_per_s']:>14.2f}{r['best_gen_tok_per_s']:>10.2f}"
              f"{r['worst_gen_tok_per_s']:>10.2f}{str(r['on_gpu']):>10}{r['size_vram_gib']:>12.2f}")
    if len(payload["results"]) == 2:
        a, b = payload["results"]
        if a["avg_gen_tok_per_s"] and b["avg_gen_tok_per_s"]:
            hi = max(a["avg_gen_tok_per_s"], b["avg_gen_tok_per_s"])
            lo = min(a["avg_gen_tok_per_s"], b["avg_gen_tok_per_s"])
            print(f"{'-' * 74}")
            print(f"加速比: {hi / lo:.2f}x")
    print(f"{'-' * 74}")


# ---------------------------------------------------------------- 入口
def main() -> int:
    ap = argparse.ArgumentParser(description="Ollama CPU vs iGPU 基准")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--mode", default="both", choices=["cpu", "igpu", "both"])
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--warmups", type=int, default=1)
    ap.add_argument("--max-tokens", type=int, default=128)
    ap.add_argument("--prompt", default=DEFAULT_PROMPT)
    ap.add_argument("--port", type=int, default=11500, help="自起 serve 的起始端口")
    ap.add_argument("--models-dir", default=None,
                    help="OLLAMA_MODELS 模型仓库（默认自动探测 E:\\ollama / ~/.ollama 等）")
    ap.add_argument("--host", default="127.0.0.1:11434",
                    help="配合 --no-spawn 使用的现有服务地址")
    ap.add_argument("--no-spawn", action="store_true",
                    help="不启动新 serve，直接测 --host 指向的实例")
    ap.add_argument("--ollama", default=None, help="ollama.exe 路径")
    ap.add_argument("--debug", action="store_true", help="开启 OLLAMA_DEBUG 日志")
    ap.add_argument("--no-save", action="store_true")
    args = ap.parse_args()

    modes = ["cpu", "igpu"] if args.mode == "both" else [args.mode]
    payload = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "engine": "ollama",
        "model": args.model,
        "max_tokens": args.max_tokens,
        "prompt": args.prompt,
        "env": {
            "hostname": platform.node(),
            "os": f"{platform.system()} {platform.release()}",
            "cpu": platform.processor(),
        },
        "results": [],
        "failures": [],
    }

    if args.no_spawn:
        port = int(args.host.rsplit(":", 1)[-1])
        if not wait_ready(port, 20):
            print(f"[error] {args.host} 不可达")
            return 2
        try:
            payload["results"].append(
                bench_mode(port, modes[0], args.model, args.runs,
                           args.warmups, args.max_tokens, args.prompt))
        except Exception as exc:
            payload["failures"].append({"mode": modes[0], "error": f"{type(exc).__name__}: {exc}"})
    else:
        exe = Path(args.ollama) if args.ollama else find_ollama()
        print(f"[ollama] {exe}")
        models_dir = find_models_dir(args.models_dir)
        if models_dir:
            print(f"[models] OLLAMA_MODELS = {models_dir}")
            payload["env"]["models_dir"] = str(models_dir)
        else:
            print("[models] 未找到模型仓库，将用 ollama 默认路径（如失败请加 --models-dir）")
        for idx, mode in enumerate(modes):
            port = args.port + idx
            try:
                with OllamaServer(exe, port, igpu=(mode == "igpu"), debug=args.debug,
                                  models_dir=models_dir) as srv:
                    srv.ensure_model(args.model)
                    payload["results"].append(
                        bench_mode(port, mode, args.model, args.runs,
                                   args.warmups, args.max_tokens, args.prompt))
            except Exception as exc:
                msg = f"{type(exc).__name__}: {exc}"
                payload["failures"].append({"mode": mode, "error": msg})
                print(f"[error] {mode} 失败: {msg}")

    if not payload["results"]:
        print("[error] 没有任何模式测试成功")
        return 1

    print_summary(payload)
    if not args.no_save:
        print(f"[save] {save_results(payload)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
