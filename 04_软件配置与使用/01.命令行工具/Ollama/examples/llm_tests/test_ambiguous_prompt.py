# llm_tests/test_ambiguous_prompt.py

def test_llm_over_inference_on_ambiguous_prompt(ollama_client):
    prompt = "请判断这个方案是否合理。"

    result = ollama_client(prompt)
    response_text = result["response"]

    # 不判断“对错”，只确认模型会生成完整叙述
    assert len(response_text) > 50
