# llm_tests/conftest.py
'''
PyTest 公共配置，提供调用 LLM 的基础 fixture。
本文件对应主文章中"概率方法 → 数据驱动"这一范式转变中的测试基础设施层：
测试的可靠性与可复现性，从根本上取决于底层调用的可控程度。
'''
import json
import os
import pytest
import requests

# 端点与模型可通过环境变量覆盖，方便在局域网机器上跑同一套测试：
#   set OLLAMA_URL=http://my-openclaw:11434/api/generate
#   set OLLAMA_MODEL=qwen3:4b-8k
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")
# 局域网上的较大模型（如 qwen3:4b-8k）首次加载 + 推理可能超过 120s，
# 超时可用 OLLAMA_TIMEOUT 覆盖。
REQUEST_TIMEOUT = float(os.environ.get("OLLAMA_TIMEOUT", "120"))

# 共享 Session，且强制忽略环境里的代理变量。
# 本机装有 HTTP 代理（HTTP_PROXY/ALL_PROXY），而 requests 的代理绕过规则
# 只按"主机名"字符串匹配 NO_PROXY，既不解析主机名对应的 IP 去套 CIDR 网段
# （如 NO_PROXY 里的 192.168.0.0/16），也不读 Windows 注册表的 ProxyOverride。
# 一旦把 URL 改成局域网主机名（如 my-openclaw），请求就会被代理接管，
# 代理机解析不到该名字，返回 502 Bad Gateway。
SESSION = requests.Session()
SESSION.trust_env = False


@pytest.fixture
def ollama_url():
    '''
    实际使用的 Ollama 端点（可由环境变量 OLLAMA_URL 覆盖）。
    '''
    return OLLAMA_URL


@pytest.fixture
def model_name():
    '''
    实际使用的模型名（可由环境变量 OLLAMA_MODEL 覆盖）。
    '''
    return MODEL_NAME


@pytest.fixture
def request_timeout():
    '''
    单次请求的超时秒数（可由环境变量 OLLAMA_TIMEOUT 覆盖）。
    '''
    return REQUEST_TIMEOUT


@pytest.fixture
def http_session():
    '''
    共享的直连 HTTP Session。
    测试中所有对 Ollama 的请求都应经由它发起，避免走系统代理。
    '''
    return SESSION


@pytest.fixture
def ollama_client():
    '''
    基础调用 fixture，封装 Ollama 的 generate API。
    返回一个可接受 prompt 和可选参数字典的闭包。
    '''
    def call_llm(prompt, stream=False, options=None):
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": stream,
        }
        if options:
            payload["options"] = options
        response = SESSION.post(
            OLLAMA_URL,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()
    return call_llm


@pytest.fixture
def deterministic_client(ollama_client):
    '''
    确定性调用 fixture：固定 temperature=0, seed=42。
    对应主文章中"非确定性输出"的对照实验——在参数固定时，
    模型输出是否仍存在不可控的波动？
    '''
    def call_deterministic(prompt, stream=False):
        return ollama_client(
            prompt,
            stream=stream,
            options={"temperature": 0, "seed": 42}
        )
    return call_deterministic


@pytest.fixture
def stream_collector():
    '''
    流式响应收集器，用于测试 stream=True 时的逐 token 行为。
    Ollama 流式 API 每行返回一个 JSON 对象，最后一行 {"done": true}。
    '''
    def collect(url, payload):
        response = SESSION.post(url, json=payload, stream=True, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        tokens = []
        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue
            chunk = json.loads(line)
            if chunk.get("done"):
                break
            tokens.append(chunk.get("response", ""))
        return "".join(tokens)
    return collect
