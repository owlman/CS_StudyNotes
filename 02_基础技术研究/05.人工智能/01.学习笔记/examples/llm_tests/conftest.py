# llm_tests/conftest.py
import pytest
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"


@pytest.fixture
def ollama_client():
    def call_llm(prompt, stream=False):
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": stream,
            },
            timeout=120,
        )
        response.raise_for_status()
        return response.json()
    return call_llm
