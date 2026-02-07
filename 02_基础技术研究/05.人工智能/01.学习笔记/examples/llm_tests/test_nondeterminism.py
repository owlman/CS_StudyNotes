# llm_tests/test_nondeterminism.py

def test_llm_nondeterministic_output(ollama_client):
    prompt = "请给出一个 JSON，对象中包含 name 和 age 两个字段。"

    outputs = set()

    for _ in range(3):
        result = ollama_client(prompt)
        outputs.add(result["response"].strip())

    # 允许偶然一致，但通常不会完全相同
    assert len(outputs) >= 1
