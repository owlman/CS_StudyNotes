# llm_tests/test_streaming.py
'''
流式（Streaming）响应行为测试。

测试目标：
- 流式模式下，内容是否能逐 token 完整返回；
- 流式结果与非流式结果在语义上是否一致；
- 流式传输是否存在丢 token 或乱序问题。

对应主文章中"工程与社会软约束"一节：在面向用户的实时场景中，
流式接口的可靠性直接影响产品体验。流式本身是 LLM 时代
区别于传统 API 的标志性交互范式。
'''
import json
import re
# 按标点切分文本，用于提取"关键短语"
CLAUSE_SPLIT = re.compile(r"[，。！？；、\n\r,.;!?]+")
def extract_clauses(text, min_len=4):
    """
    把一段文本按标点切成短语片段，并过滤掉过短的片段。
    比"字符集重叠"更贴近"是否丢了内容"这一本意。
    """
    parts = [p.strip() for p in CLAUSE_SPLIT.split(text)]
    return [p for p in parts if len(p) >= min_len]
class TestStreaming:

    def test_stream_output_completeness(self, ollama_client, stream_collector, ollama_url, model_name):
        '''
        验证流式模式能完整收集到所有 token，
        不会提前截断或丢失尾部内容。
        '''
        prompt = "请用 50 字以内说明递归函数的出口条件为什么重要。"
        # 非流式结果作为参照；固定 temperature=0 以尽量消除采样随机性，
        # 否则两次调用的措辞差异会被误判成"传输丢内容"
        non_stream = ollama_client(
            prompt,
            stream=False,
            options={"temperature": 0}
        )
        full_text = non_stream["response"]
        # 流式收集
        url = ollama_url
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": True,
            "options": {"temperature": 0},
        }
        streamed_text = stream_collector(url, payload)
        assert len(streamed_text) > 0, "流式模式未收集到任何 token"
        # 语义一致性检验：提取关键短语并统计命中率
        clauses = extract_clauses(full_text)
        assert clauses, "非流式结果未解析出任何关键短语"
        matched = [c for c in clauses if c in streamed_text]
        hit_rate = len(matched) / len(clauses)
        assert hit_rate >= 0.5, (
            f"流式结果的关键短语命中率仅 {hit_rate:.0%}"
            f"（{len(matched)}/{len(clauses)}），可能存在丢 token 或截断"
        )

    def test_stream_token_by_token(
        self, ollama_client, stream_collector, http_session, ollama_url, model_name, request_timeout
    ):
        '''
        观察逐 token 的粒度。
        Ollama 的流式接口按 token 粒度输出（非字符），
        因此单次 chunk 可能包含空格或标点，但不应为空。
        '''
        url = ollama_url
        payload = {
            "model": model_name,
            "prompt": "Hello!",
            "stream": True,
        }

        response = http_session.post(url, json=payload, stream=True, timeout=request_timeout)
        response.raise_for_status()

        token_count = 0
        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue
            chunk = json.loads(line)
            if chunk.get("done"):
                break
            token_text = chunk.get("response", "")
            # 检查每个 chunk 格式是否正确
            assert isinstance(token_text, str), f"chunk 中的 response 不是字符串：{chunk}"
            token_count += 1

        # 至少产生了多个 token
        assert token_count > 5, (
            f"仅产生了 {token_count} 个 token，流式粒度异常"
        )
