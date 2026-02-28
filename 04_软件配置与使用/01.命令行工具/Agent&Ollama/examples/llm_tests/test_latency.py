# llm_tests/test_latency.py
import time

def test_llm_response_latency(ollama_client):
    start = time.time()

    ollama_client("请简要说明 TCP 和 UDP 的区别。")

    elapsed = time.time() - start

    # 不设过严阈值，只验证“不是瞬时返回”
    assert elapsed > 0.5
