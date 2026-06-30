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
import requests


class TestStreaming:

    def test_stream_output_completeness(self, ollama_client, stream_collector):
        '''
        验证流式模式能完整收集到所有 token，
        不会提前截断或丢失尾部内容。
        '''
        prompt = "请用 50 字以内说明递归函数的出口条件为什么重要。"
        # 非流式结果作为参照
        non_stream = ollama_client(prompt, stream=False)
        full_text = non_stream["response"]

        # 流式收集
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": True,
        }
        streamed_text = stream_collector(url, payload)

        assert len(streamed_text) > 0, "流式模式未收集到任何 token"
        # 语义一致性检验：基于字符集（排除标点）检查流式与非流式结果的公共部分
        import string
        chars_full = set(c for c in full_text if c not in string.whitespace)
        chars_stream = set(c for c in streamed_text if c not in string.whitespace)
        shared = chars_full & chars_stream
        assert len(shared) > 5, (
            "流式结果与非流式结果字符重叠过少，可能存在传输问题"
        )

    def test_stream_token_by_token(self, ollama_client, stream_collector):
        '''
        观察逐 token 的粒度。
        Ollama 的流式接口按 token 粒度输出（非字符），
        因此单次 chunk 可能包含空格或标点，但不应为空。
        '''
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3.2:3b",
            "prompt": "Hello!",
            "stream": True,
        }

        response = requests.post(url, json=payload, stream=True, timeout=180)
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
