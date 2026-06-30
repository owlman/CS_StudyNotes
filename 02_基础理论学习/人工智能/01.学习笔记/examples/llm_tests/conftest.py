# llm_tests/conftest.py
'''
PyTest 公共配置，提供调用 LLM 的基础 fixture。
本文件对应主文章中"概率方法 → 数据驱动"这一范式转变中的测试基础设施层：
测试的可靠性与可复现性，从根本上取决于底层调用的可控程度。
'''
import json
import pytest
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"


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
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120,
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
        response = requests.post(url, json=payload, stream=True, timeout=180)
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
