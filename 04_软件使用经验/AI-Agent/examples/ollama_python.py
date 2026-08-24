"""通过 HTTP API 调用 Ollama 模型的最小示例。

演示同时访问本机（localhost）与局域网（my-openclaw）上的 Ollama 服务，
脚本会依次向两个端点发送同一个 prompt 并打印模型的回答。

对应笔记：《LLM 的部署与测试》一文中"使用 Python 调用本地 Ollama 模型"一节。
"""

import requests


# 两个 Ollama /api/generate 端点
LOCAL_URL = "http://localhost:11434/api/generate"
LAN_URL = "http://my-openclaw:11434/api/generate"

# 演示用的模型与提示词
MODEL = "qwen3:4b-8k"  # 或 "llama3.2:3b"
PROMPT = "请用一句话解释什么是操作系统。"

REQUEST_TIMEOUT = 120.0  # 秒，避免网络异常时无限阻塞

# (label, url, model) 三元组列表，便于循环调用
ENDPOINTS = [
    ("local", LOCAL_URL, MODEL),
    ("LAN", LAN_URL, MODEL),
]


def query_ollama(url: str, model: str, prompt: str) -> str:
    """向 Ollama /api/generate 端点发送 prompt 并返回模型的回答。"""
    response = requests.post(
        url,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
        },
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()["response"]


def main() -> None:
    for label, url, model in ENDPOINTS:
        try:
            answer = query_ollama(url, model, PROMPT)
        except requests.RequestException as exc:
            print(f"[{label}] 请求失败：{exc}")
            continue
        print(f"[{label}] {answer}")


if __name__ == "__main__":
    main()
