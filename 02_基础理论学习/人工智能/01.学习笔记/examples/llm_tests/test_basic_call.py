# llm_tests/test_basic_call.py
'''
基础连通性与响应结构测试。

测试目标：
- LLM API 是否可被稳定调用（对应主文章中"概率转向"的基础假设：系统应可被可靠地查询）；
- 响应数据结构是否符合预期；
- 模型对不同类型指令是否都能产出非空且有意义的回复。

这些测试是后续所有观察的基線——如果基础调用就不可靠，
那么对"非确定性""模糊推断"等高级行为的分析就失去了立足点。
'''
import pytest


class TestBasicCall:

    @pytest.mark.parametrize("prompt", [
        "请用一句话解释什么是操作系统。",
        "Python 中的列表和元组有什么区别？",
        "1+1 等于几？",
    ])
    def test_llm_responds_to_various_prompts(self, ollama_client, prompt):
        '''对不同类型的指令，模型都应返回非空字符串响应。'''
        result = ollama_client(prompt)

        assert "response" in result, "响应中缺少 'response' 字段"
        assert isinstance(result["response"], str), "'response' 字段应为字符串"
        assert len(result["response"].strip()) > 0, "响应内容不应为空"

    @pytest.mark.parametrize("prompt", [
        "",
        " ",
        "\n",
    ])
    def test_llm_behavior_on_empty_or_whitespace_prompt(
            self, ollama_client, prompt):
        '''
        边界情况：空或纯空白指令。
        这类输入在传统 API 中应返回 4xx 错误，
        但 LLM API 的行为值得观察——它会如何"应对"无意义的输入？
        '''
        result = ollama_client(prompt)
        response_text = result["response"].strip()

        # 模型不会因为空输入而崩溃（服务可用），
        # 但输出内容可能是不确定的默认回复
        assert isinstance(response_text, str)

    def test_llm_response_contains_expected_fields(self, ollama_client):
        '''验证 Ollama API 返回的完整字段集合。'''
        result = ollama_client("Hello。")

        # 核心字段存在性检查
        assert "model" in result
        assert "response" in result
        assert "done" in result
        assert "eval_count" in result
        assert "eval_duration" in result
        assert result["done"] is True
