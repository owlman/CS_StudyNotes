# llm_tests/test_basic_call.py

def test_llm_basic_response(ollama_client):
    result = ollama_client("请用一句话解释什么是操作系统。")

    assert "response" in result
    assert isinstance(result["response"], str)
    assert len(result["response"].strip()) > 0
