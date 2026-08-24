"""通过 HTTP API 验证本地与局域网 Ollama 服务的连通性。

依次访问本机（localhost）与局域网（my-openclaw）上的 Ollama 服务，
向两个端点发送同一个 prompt 并打印模型的回答。

对应笔记：《LLM 的部署与测试》一文中"使用 Python 调用本地 Ollama 模型"一节。
"""

from typing import TypedDict
import requests


class OllamaEndpoint(TypedDict):
    """Ollama /api/generate 端点的最小配置。"""

    url: str
    model: str


LOCAL_ENDPOINT: OllamaEndpoint = {
    "url": "http://localhost:11434/api/generate",
    "model": "llama3.2:3b",
}
LAN_ENDPOINT: OllamaEndpoint = {
    "url": "http://my-openclaw:11434/api/generate",
    "model": "qwen3:4b-8k",
}

PROMPT = "请用一句话解释什么是操作系统。"
REQUEST_TIMEOUT = 120.0  # 秒，避免网络异常时无限阻塞

# label -> endpoint 配置，便于按名称迭代调用
ENDPOINTS: dict[str, OllamaEndpoint] = {
    "local": LOCAL_ENDPOINT,
    "LAN": LAN_ENDPOINT,
}

# 共享 HTTP Session：复用 TCP 连接，避免同一进程内多次请求反复握手。
SESSION = requests.Session()


def query_ollama(endpoint: OllamaEndpoint, prompt: str) -> dict:
    """向 Ollama /api/generate 端点发送 prompt，返回 Ollama 的完整 JSON 响应。

    完整响应除 `response` 字段外，还包含 `done`、`total_duration`、`eval_count` 等
    元数据，调用方可按需取用。
    """
    response = SESSION.post(
        endpoint["url"],
        json={
            "model": endpoint["model"],
            "prompt": prompt,
            "stream": False,
        },
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def main() -> None:
    for label, endpoint in ENDPOINTS.items():
        try:
            result = query_ollama(endpoint, PROMPT)
        except requests.exceptions.RequestException as exc:
            # 跳过 urllib3 的 MaxRetryError 包装层——它的 __str__ 总会带
            # "Max retries exceeded with url: ..." 冗余前缀，直接取底层 socket 错误
            # （exc.__context__.__context__，对应 NewConnectionError 等）。
            cause = exc.__context__.__context__ if exc.__context__ else exc
            print(f"[{label}] 请求失败：{cause}")
            continue
        print(f"[{label}] {result['response']}")


if __name__ == "__main__":
    main()
